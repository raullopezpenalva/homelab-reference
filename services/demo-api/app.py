"""Small read-only PostgreSQL example; no deployment or real data is bundled."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def read_message():
    import psycopg
    with psycopg.connect(host=os.environ["DB_HOST"], dbname=os.environ["DB_NAME"],
                         user=os.environ["DB_USER"],
                         password=Path(os.environ["DB_PASSWORD_FILE"]).read_text().strip(),
                         connect_timeout=3, options="-c default_transaction_read_only=on") as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT message FROM public.greeting WHERE id = 1")
            row = cursor.fetchone()
            if row is None:
                raise ValueError("Missing reference data")
            return row[0]


def response(path, reader=read_message):
    if path == "/health/live":
        return 200, {"status": "alive"}
    if path not in {"/health/ready", "/api/message"}:
        return 404, {"error": "not found"}
    try:
        message = reader()
        return 200, ({"status": "ready"} if path == "/health/ready" else {"message": message})
    except Exception:
        # Database errors can embed connection details. Never send their text.
        return 503, {"error": "database unavailable"}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, payload = response(self.path)
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # Avoid persisting request paths, headers or client identifiers.
        pass


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
