#!/usr/bin/env python3
"""Envio masivo de correos personalizados a las entradas de la seccion VII
(31-157, incl. cluster ERMA 78-95) y de la seccion VIII (158-266) del master
'Busqueda de Contactos Empresas Veterinarias Mexico.md'.

- Reutiliza la autenticacion OAuth del MCP de Gmail (~/.gmail-mcp).
- Convierte el cuerpo en Markdown a HTML (parrafos, <b> para negritas, enlaces).
- Adjunta la firma visual real desde firmaCorreoRedRedSG.html.
- Hace throttle entre envios para no saturar.
- Genera un log en bulkSendLog.md con el resultado de cada envio.

Modo dry-run: pasar --dry-run para listar sin enviar.
"""
from __future__ import annotations

import argparse
import base64
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from email.headerregistry import Address
from email.message import EmailMessage
from email.policy import SMTP

ROOT = pathlib.Path("/Users/rafaelrodrigueznadal/flutter/redredsg/Marketing and Email")
MASTER = ROOT / "Búsqueda de Contactos Empresas Veterinarias México.md"
SIGNATURE = ROOT / "firmaCorreoRedRedSG.html"
CONFIG_DIR = pathlib.Path.home() / ".gmail-mcp"
LOG_PATH = ROOT / "bulkSendLog.md"

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")

PRIORIDAD_ALTA = {163, 194, 202, 207, 211, 220, 229, 255}


def refresh_access_token() -> str:
    creds = json.loads((CONFIG_DIR / "credentials.json").read_text())
    oauth = json.loads((CONFIG_DIR / "gcp-oauth.keys.json").read_text())["installed"]
    payload = urllib.parse.urlencode(
        {
            "client_id": oauth["client_id"],
            "client_secret": oauth["client_secret"],
            "refresh_token": creds["refresh_token"],
            "grant_type": "refresh_token",
        }
    ).encode()
    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token", data=payload, method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


def markdown_to_html(md: str) -> str:
    """Very small markdown->HTML converter (bold, links, paragraphs)."""
    paragraphs: list[str] = []
    current: list[str] = []
    for raw_line in md.strip().split("\n"):
        line = raw_line.rstrip()
        if not line:
            if current:
                paragraphs.append(current)
                current = []
            continue
        # Escape HTML-sensitive chars first (before inserting our own tags).
        line = (
            line.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        # **bold**
        line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
        # [text](url)
        line = re.sub(
            r"\[([^\]]+)\]\(([^)]+)\)",
            r'<a href="\2" target="_blank">\1</a>',
            line,
        )
        current.append(line)
    if current:
        paragraphs.append(current)

    html_parts = []
    for para in paragraphs:
        html_parts.append("<p>" + "<br>\n".join(para) + "</p>")
    return '<div dir="ltr">\n' + "\n".join(html_parts) + "\n</div>"


def parse_master_entries() -> list[dict]:
    """Parse numbered entries (#### **N\\. ...**) from master and return a
    list of dicts with num, display, emails, subject, body_md."""
    text = MASTER.read_text(encoding="utf-8")
    header_re = re.compile(r"^#### \*\*(\d+)\\\. (.+?)\*\*\s*$", re.M)
    headers = list(header_re.finditer(text))

    entries: list[dict] = []
    for i, m in enumerate(headers):
        num = int(m.group(1))
        display = m.group(2).strip()
        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        block = text[start:end]

        send_match = re.search(r"\*\*Enviar a:\*\*\s*([^\n]+)", block)
        subj_match = re.search(r"\*\*Asunto:\*\*\s*([^\n]+)", block)
        if not send_match or not subj_match:
            continue

        emails = EMAIL_RE.findall(send_match.group(1))
        if not emails:
            # placeholder (e.g. "[Sin correo publico verificado...]")
            continue
        subject = subj_match.group(1).strip()

        # Body: after nota paragraph, until "Ing. Rafael Rodriguez Nadal."
        nota_end = re.search(r"\*\*Nota de origen:\*\*[^\n]*(?:\n[^\n]+)*", block)
        if not nota_end:
            continue
        rest = block[nota_end.end():].lstrip("\n")
        sig_match = re.search(r"Ing\. Rafael Rodriguez Nadal\.\s*", rest)
        if not sig_match:
            continue
        body_md = rest[: sig_match.end()].rstrip()
        entries.append(
            {
                "num": num,
                "display": display,
                "emails": emails,
                "subject": subject,
                "body_md": body_md,
            }
        )
    return entries


def parse_erma_entries() -> list[dict]:
    """Parse the ERMA cluster (78-95). Uses the recommended template and the
    table rows to generate per-zone personalized entries."""
    text = MASTER.read_text(encoding="utf-8")
    erma_match = re.search(
        r"#### \*\*78–95\.[\s\S]+?(?=\n### ARGENTINA)", text
    )
    if not erma_match:
        return []
    block = erma_match.group(0)

    # Extract the recommended template (quoted block starting with "> Hola [Nombre],").
    tpl_match = re.search(
        r"\*\*Cuerpo recomendado[^*]*\*\*\s*\n\s*\n((?:>[^\n]*\n?)+)", block
    )
    if not tpl_match:
        return []
    template_lines = []
    for line in tpl_match.group(1).splitlines():
        if line.startswith(">"):
            line = line[1:]
            if line.startswith(" "):
                line = line[1:]
        template_lines.append(line)
    template = "\n".join(template_lines).strip()

    row_re = re.compile(
        r"\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|\s]+@[^|\s]+)\s*\|\s*([^|]+?)\s*\|"
    )
    entries: list[dict] = []
    for m in row_re.finditer(block):
        num = int(m.group(1))
        zona = m.group(2).strip()
        nombre = m.group(3).strip()
        email = m.group(4).strip()
        tel = m.group(5).strip()

        generic = nombre.lower().startswith(("promotoría", "promotoria"))
        if generic:
            body_md = (
                template
                .replace("Hola [Nombre],", "Hola,")
                .replace("[Zona]", zona)
            )
        else:
            first_name = nombre.split()[0]
            body_md = (
                template
                .replace("[Nombre]", first_name)
                .replace("[Zona]", zona)
            )
        subject = "presencia de Laboratorios ERMA en RedVetAds"
        display = f"Laboratorios ERMA — {zona} ({nombre})"
        entries.append(
            {
                "num": num,
                "display": display,
                "emails": [email],
                "subject": subject,
                "body_md": body_md,
                "tel": tel,
            }
        )
    return entries


def build_message(to_emails: list[str], subject: str, body_md: str) -> EmailMessage:
    body_html = markdown_to_html(body_md)
    signature_html = SIGNATURE.read_text(encoding="utf-8").strip()
    full_html = body_html + "\n" + signature_html

    message = EmailMessage(policy=SMTP)
    message["From"] = str(
        Address(
            display_name="Ing. Rafael Rodriguez Nadal",
            username="info",
            domain="redredsg.com",
        )
    )
    message["To"] = ", ".join(to_emails)
    message["Subject"] = subject
    message["Content-Language"] = "es"
    message.set_content("Este correo requiere visualizacion HTML.")
    message.add_alternative(full_html, subtype="html")
    return message


def send_via_gmail(access_token: str, message: EmailMessage) -> dict:
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("ascii").rstrip("=")
    payload = json.dumps({"raw": raw}).encode("utf-8")
    req = urllib.request.Request(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        data=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Listar sin enviar")
    parser.add_argument("--throttle", type=float, default=2.5, help="segundos entre envios")
    parser.add_argument("--only", type=str, default="", help="lista de numeros separados por coma")
    parser.add_argument(
        "--skip-ranges", type=str, default="",
        help="lista de rangos A-B separados por coma que se omiten"
    )
    args = parser.parse_args()

    numeric = parse_master_entries()
    # Mantener solo los de secciones VII (31-157, excepto 78-95) y VIII (158-266).
    numeric = [e for e in numeric if 31 <= e["num"] <= 266 and not (78 <= e["num"] <= 95)]
    # Agregar ERMA 78-95 dinamicamente.
    erma = parse_erma_entries()

    all_entries = numeric + erma

    if args.only:
        wanted = {int(x.strip()) for x in args.only.split(",") if x.strip()}
        all_entries = [e for e in all_entries if e["num"] in wanted]
    if args.skip_ranges:
        skip = set()
        for part in args.skip_ranges.split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                a, b = part.split("-", 1)
                skip.update(range(int(a), int(b) + 1))
            else:
                skip.add(int(part))
        all_entries = [e for e in all_entries if e["num"] not in skip]

    all_entries.sort(key=lambda e: (0 if e["num"] in PRIORIDAD_ALTA else 1, e["num"]))

    print(f"Total a procesar: {len(all_entries)}")
    print(f"PRIORIDAD ALTA: {sum(1 for e in all_entries if e['num'] in PRIORIDAD_ALTA)}")
    print()
    for e in all_entries[:10]:
        tag = " [PA]" if e["num"] in PRIORIDAD_ALTA else ""
        print(f"  #{e['num']}{tag} {e['display']} -> {', '.join(e['emails'])}")
    if len(all_entries) > 10:
        print(f"  ... y {len(all_entries) - 10} mas")
    print()

    if args.dry_run:
        print("DRY-RUN: no se envia nada.")
        return 0

    access_token = refresh_access_token()
    log_lines: list[str] = [
        f"# Bulk send log - {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"Total a enviar: {len(all_entries)}",
        "",
    ]
    sent = 0
    errors = 0
    for i, e in enumerate(all_entries, 1):
        tag = "[PA] " if e["num"] in PRIORIDAD_ALTA else ""
        try:
            message = build_message(e["emails"], e["subject"], e["body_md"])
            result = send_via_gmail(access_token, message)
            status = f"SENT id={result.get('id', '?')}"
            sent += 1
        except urllib.error.HTTPError as err:  # noqa: PERF203
            body = err.read().decode(errors="replace")
            status = f"ERROR HTTP {err.code}: {body[:300]}"
            errors += 1
            # Refresh token on 401 and retry once.
            if err.code == 401:
                try:
                    access_token = refresh_access_token()
                    message = build_message(e["emails"], e["subject"], e["body_md"])
                    result = send_via_gmail(access_token, message)
                    status = f"SENT (retry) id={result.get('id', '?')}"
                    sent += 1
                    errors -= 1
                except Exception as err2:  # noqa: BLE001
                    status = f"ERROR retry: {err2}"
        except Exception as err:  # noqa: BLE001
            status = f"ERROR: {err}"
            errors += 1

        msg = (
            f"[{i}/{len(all_entries)}] {tag}#{e['num']} {e['display']} "
            f"-> {', '.join(e['emails'])} | {status}"
        )
        print(msg, flush=True)
        log_lines.append(f"- {msg}")

        if i < len(all_entries):
            time.sleep(args.throttle)

    log_lines.append("")
    log_lines.append(f"Resumen: ENVIADOS={sent}  ERRORES={errors}")
    LOG_PATH.write_text("\n".join(log_lines), encoding="utf-8")
    print()
    print(f"Log: {LOG_PATH}")
    print(f"ENVIADOS: {sent}  ERRORES: {errors}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
