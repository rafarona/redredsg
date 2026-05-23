#!/usr/bin/env python3
import argparse
import base64
import json
import pathlib
import sys
import urllib.parse
import urllib.request
from email.headerregistry import Address
from email.message import EmailMessage
from email.policy import SMTP


DEFAULT_CONFIG_DIR = pathlib.Path.home() / ".gmail-mcp"
DEFAULT_SIGNATURE_FILE = pathlib.Path(__file__).with_name("firmaCorreoRedRedSG.html")


def load_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def refresh_access_token(config_dir: pathlib.Path) -> str:
    credentials = load_json(config_dir / "credentials.json")
    oauth_keys = load_json(config_dir / "gcp-oauth.keys.json")["installed"]
    payload = urllib.parse.urlencode(
        {
            "client_id": oauth_keys["client_id"],
            "client_secret": oauth_keys["client_secret"],
            "refresh_token": credentials["refresh_token"],
            "grant_type": "refresh_token",
        }
    ).encode()
    request = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=payload,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())["access_token"]


def parse_recipients(raw_value: str) -> list[str]:
    recipients = [item.strip() for item in raw_value.split(",")]
    recipients = [item for item in recipients if item]
    if not recipients:
        raise ValueError("Debes indicar al menos un destinatario en --to")
    return recipients


def build_message(args: argparse.Namespace) -> EmailMessage:
    html_body = pathlib.Path(args.html_file).read_text(encoding="utf-8").strip()
    signature_html = pathlib.Path(args.signature_file).read_text(encoding="utf-8").strip()
    full_html = f"{html_body}\n{signature_html}"

    text_body = args.text.strip() if args.text else "Este correo requiere visualizacion HTML."

    message = EmailMessage(policy=SMTP)
    message["From"] = str(
        Address(
            display_name="Ing. Rafael Rodriguez Nadal",
            username="info",
            domain="redredsg.com",
        )
    )
    message["To"] = ", ".join(parse_recipients(args.to))
    message["Subject"] = args.subject
    message["Content-Language"] = args.lang
    message.set_content(text_body)
    message.add_alternative(full_html, subtype="html")
    return message


def send_message(access_token: str, message: EmailMessage) -> dict:
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("ascii").rstrip("=")
    payload = json.dumps({"raw": raw}).encode("utf-8")
    request = urllib.request.Request(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        data=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Enviar correo raw por Gmail API con firma HTML fija."
    )
    parser.add_argument("--to", required=True, help="Destinatarios separados por coma")
    parser.add_argument("--subject", required=True, help="Asunto del correo")
    parser.add_argument("--html-file", required=True, help="Archivo HTML del cuerpo")
    parser.add_argument("--text", default="", help="Version texto plano opcional")
    parser.add_argument("--lang", default="es", help="Idioma del correo")
    parser.add_argument(
        "--config-dir",
        default=str(DEFAULT_CONFIG_DIR),
        help="Directorio de credenciales Gmail MCP",
    )
    parser.add_argument(
        "--signature-file",
        default=str(DEFAULT_SIGNATURE_FILE),
        help="Archivo HTML de firma",
    )
    args = parser.parse_args()

    config_dir = pathlib.Path(args.config_dir)
    if not config_dir.exists():
        print(f"No existe el directorio de configuracion: {config_dir}", file=sys.stderr)
        return 1

    try:
        access_token = refresh_access_token(config_dir)
        message = build_message(args)
        result = send_message(access_token, message)
    except Exception as error:  # noqa: BLE001
        print(f"Error enviando correo: {error}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
