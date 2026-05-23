#!/usr/bin/env python3
"""Follow-up programado para Dianny De La Cruz (Laboratorios Referencia, RD).

Objetivo: enviar un recordatorio corto sobre el pitch original de RedVetAds
una vez que Dianny regrese de vacaciones. El correo va como REPLY dentro del
hilo original (threadId 19dabbde2e6e5cd2) con In-Reply-To / References
apuntando al Message-Id del primer envío, para que caiga como continuación
natural y no como correo suelto.

Disparo: agendado con launchd (ver
~/Library/LaunchAgents/com.redredsg.followup-dianny.plist).

Salvaguarda: si por alguna razón ya se hizo el envío antes (marker file
.sent), no vuelve a mandar.
"""
from __future__ import annotations

import base64
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime
from email.headerregistry import Address
from email.message import EmailMessage
from email.policy import SMTP

ROOT = pathlib.Path("/Users/rafaelrodrigueznadal/flutter/redredsg/Marketing and Email")
SIGNATURE = ROOT / "firmaCorreoRedRedSG.html"
SELF_DIR = pathlib.Path(__file__).resolve().parent
LOG_FILE = SELF_DIR / "dianny.log"
SENT_MARKER = SELF_DIR / "dianny.sent"

EARLIEST_SEND_DATE = date(2026, 5, 4)
LAUNCHD_LABEL = "com.redredsg.followup-dianny"
LAUNCHD_PLIST = (
    pathlib.Path.home() / "Library" / "LaunchAgents" / f"{LAUNCHD_LABEL}.plist"
)

CONFIG_DIR = pathlib.Path.home() / ".gmail-mcp"

TARGET_EMAIL = "diannyc@labreferencia.com"
TARGET_NAME = "Dianny De La Cruz"
ORIGINAL_THREAD_ID = "19dabbde2e6e5cd2"
ORIGINAL_MESSAGE_ID = "<CAMe+oryBojQMAnfSEGvGve61dia6hGHtbLjyKwb=UXSrXfsXtA@mail.gmail.com>"
REPLY_SUBJECT = "Re: presencia de Lab Referencia en RedVetAds"

BODY_MD = """Hola Dianny,

Bienvenida de vuelta — espero que hayas tenido unos buenos días fuera.

Retomo muy brevemente el correo anterior por si quedó enterrado entre lo que te llegó en vacaciones.

Seguimos abriendo espacios de socio fundador para laboratorios de diagnóstico en **RedVet**, con condiciones preferenciales solo para las primeras marcas que entran al piloto. En el caso de Laboratorios Referencia lo que tiene más sentido es activar presencia justo en el momento en que el médico evalúa pruebas o referir un estudio, y reforzar del lado del propietario en **RedPet** cuando se comparte resultado/procedimiento.

Hoy llevamos **+19,000 descargas profesionales** y ~25,000 impactos visuales al mes dentro de la app.

¿Te parece si agendamos 15 minutos por Meet esta semana o la próxima? Te muestro el dashboard en vivo y cerramos si hay fit para un piloto de 4 semanas adaptado a Lab Referencia. Dime qué horario te acomoda (RD) y yo me ajusto.

Si prefieres que te mande primero la propuesta ejecutiva de 1 página por correo, también me funciona — solo confírmame y va.

Un cordial saludo.
"""


def log(msg: str) -> None:
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {msg}\n"
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line)
    print(line, end="")


def refresh_access_token() -> str:
    creds = json.loads((CONFIG_DIR / "credentials.json").read_text())
    oauth = json.loads((CONFIG_DIR / "gcp-oauth.keys.json").read_text())["installed"]
    body = urllib.parse.urlencode(
        {
            "client_id": oauth["client_id"],
            "client_secret": oauth["client_secret"],
            "refresh_token": creds["refresh_token"],
            "grant_type": "refresh_token",
        }
    ).encode()
    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token", data=body, method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


def markdown_to_html(md: str) -> str:
    paragraphs: list[list[str]] = []
    current: list[str] = []
    for raw in md.strip().split("\n"):
        line = raw.rstrip()
        if not line:
            if current:
                paragraphs.append(current)
                current = []
            continue
        line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
        line = re.sub(
            r"\[([^\]]+)\]\(([^)]+)\)",
            r'<a href="\2" target="_blank">\1</a>',
            line,
        )
        current.append(line)
    if current:
        paragraphs.append(current)
    return '<div dir="ltr">\n' + "\n".join(
        "<p>" + "<br>\n".join(p) + "</p>" for p in paragraphs
    ) + "\n</div>"


def build_message() -> EmailMessage:
    body_html = markdown_to_html(BODY_MD)
    signature_html = SIGNATURE.read_text(encoding="utf-8").strip()
    full_html = body_html + "\n" + signature_html

    msg = EmailMessage(policy=SMTP)
    msg["From"] = str(
        Address(
            display_name="Ing. Rafael Rodriguez Nadal",
            username="info",
            domain="redredsg.com",
        )
    )
    msg["To"] = str(Address(display_name=TARGET_NAME, addr_spec=TARGET_EMAIL))
    msg["Subject"] = REPLY_SUBJECT
    msg["Content-Language"] = "es"
    msg["In-Reply-To"] = ORIGINAL_MESSAGE_ID
    msg["References"] = ORIGINAL_MESSAGE_ID
    msg.set_content("Este correo requiere visualización HTML.")
    msg.add_alternative(full_html, subtype="html")
    return msg


def send(token: str, msg: EmailMessage) -> dict:
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii").rstrip("=")
    payload = {"raw": raw, "threadId": ORIGINAL_THREAD_ID}
    req = urllib.request.Request(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        data=json.dumps(payload).encode(),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def self_unload() -> None:
    """Descargar el agente launchd y borrar el plist para que no se dispare
    nunca más. Idempotente: si falla, solo lo registra."""
    try:
        uid = os.getuid()
        subprocess.run(
            ["/bin/launchctl", "bootout", f"gui/{uid}/{LAUNCHD_LABEL}"],
            check=False,
            capture_output=True,
        )
        if LAUNCHD_PLIST.exists():
            LAUNCHD_PLIST.unlink()
        log(f"launchd agent {LAUNCHD_LABEL} descargado y plist eliminado.")
    except Exception as e:
        log(f"AVISO: no pude auto-descargar launchd: {type(e).__name__}: {e}")


def main() -> int:
    log("--- inicio follow-up Dianny ---")

    today = date.today()
    if today < EARLIEST_SEND_DATE:
        log(
            f"hoy={today.isoformat()} < earliest={EARLIEST_SEND_DATE.isoformat()}; "
            "no envío todavía."
        )
        return 0

    if SENT_MARKER.exists():
        log(f"marker {SENT_MARKER} ya existe; abortando sin reenviar.")
        self_unload()
        return 0

    attempts = 3
    for attempt in range(1, attempts + 1):
        try:
            token = refresh_access_token()
            msg = build_message()
            resp = send(token, msg)
            SENT_MARKER.write_text(
                json.dumps(
                    {
                        "sentAt": datetime.now().isoformat(),
                        "messageId": resp.get("id"),
                        "threadId": resp.get("threadId"),
                        "to": TARGET_EMAIL,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            log(
                f"ENVIADO intento={attempt} id={resp.get('id')} "
                f"thread={resp.get('threadId')} to={TARGET_EMAIL}"
            )
            self_unload()
            return 0
        except urllib.error.HTTPError as e:
            detail = ""
            try:
                detail = e.read().decode()[:300]
            except Exception:
                pass
            log(f"ERROR HTTP {e.code} intento={attempt}: {detail}")
        except Exception as e:
            log(f"ERROR intento={attempt}: {type(e).__name__}: {e}")
        if attempt < attempts:
            time.sleep(30 * attempt)

    log("FALLO tras 3 intentos")
    return 1


if __name__ == "__main__":
    sys.exit(main())
