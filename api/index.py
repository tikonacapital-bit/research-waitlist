import json
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler
from urllib import error, request

GOOGLE_SHEETS_WEBHOOK_URL = os.getenv("GOOGLE_SHEETS_WEBHOOK_URL", "").strip()


def append_signup_to_google_sheets(email, phone):
    if not GOOGLE_SHEETS_WEBHOOK_URL:
        raise ValueError("Google Sheets webhook is not configured.")

    payload = json.dumps(
        {
            "submittedAt": datetime.now(timezone.utc).isoformat(),
            "email": email,
            "phone": phone,
            "source": "website",
        }
    ).encode("utf-8")

    webhook_request = request.Request(
        GOOGLE_SHEETS_WEBHOOK_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(webhook_request, timeout=10) as response:
            if response.status >= 400:
                raise RuntimeError("Google Sheets rejected the signup.")
    except error.URLError as exc:
        raise RuntimeError("Unable to reach Google Sheets.") from exc


def is_valid_email(email):
    if "@" not in email or "." not in email.split("@")[-1]:
        return False
    return " " not in email and len(email) >= 5


def is_valid_phone(phone):
    allowed = set("0123456789+-() ")
    digits_only = "".join(char for char in phone if char.isdigit())
    return 7 <= len(digits_only) <= 12 and all(char in allowed for char in phone)


def send_json(handler, status_code, payload):
    encoded = json.dumps(payload).encode("utf-8")
    handler.send_response(status_code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.send_header("Content-Length", str(len(encoded)))
    handler.end_headers()
    handler.wfile.write(encoded)


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length).decode("utf-8")

        try:
            data = json.loads(body or "{}")
        except json.JSONDecodeError:
            send_json(self, 400, {"ok": False, "message": "Invalid request payload."})
            return

        email = str(data.get("email", "")).strip()
        phone = str(data.get("phone", "")).strip()

        if not is_valid_email(email):
            send_json(self, 400, {"ok": False, "message": "Please enter a valid email address."})
            return

        if phone and not is_valid_phone(phone):
            send_json(self, 400, {
                "ok": False,
                "message": "Phone number must be 7 to 12 digits and can include spaces, brackets, plus and hyphen.",
            })
            return

        try:
            append_signup_to_google_sheets(email, phone)
            send_json(self, 200, {"ok": True, "message": "You're on the list. We'll be in touch soon."})
        except ValueError as exc:
            send_json(self, 500, {"ok": False, "message": str(exc)})
        except RuntimeError as exc:
            send_json(self, 502, {"ok": False, "message": str(exc)})
