from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "synthetic_records.json"
STATIC_PATH = ROOT / "static"


def load_records() -> list[dict]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))["records"]


def build_summary(records: list[dict]) -> dict:
    entities: dict[str, dict] = {}
    for record in records:
        entity = entities.setdefault(
            record["entity"],
            {"entity": record["entity"], "currency_totals": {}, "records": 0},
        )
        currency = record["currency"]
        totals = entity["currency_totals"].setdefault(
            currency, {"receivable": 0, "payable": 0, "missing_materials": 0}
        )
        entity["records"] += 1
        if record["kind"] == "receivable":
            totals["receivable"] += record["amount"]
        elif record["kind"] == "payable":
            totals["payable"] += record["amount"]
        elif record["kind"] == "missing_material":
            totals["missing_materials"] += 1

    return {
        "period_start": "2026-01",
        "synthetic": True,
        "entities": list(entities.values()),
        "records": records,
        "currency_note": "Totals stay separated by currency until an explicit FX rate and date are supplied.",
    }


class AccountingHandler(BaseHTTPRequestHandler):
    def do_HEAD(self) -> None:  # noqa: N802
        if urlparse(self.path).path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            return
        self.send_error(404)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/summary":
            self.send_json(build_summary(load_records()))
            return
        if path == "/" or path == "/index.html":
            self.send_file(STATIC_PATH / "index.html", "text/html; charset=utf-8")
            return
        if path.startswith("/static/"):
            asset = STATIC_PATH / path.removeprefix("/static/")
            if asset.is_file() and asset.parent == STATIC_PATH:
                content_type = "text/css; charset=utf-8" if asset.suffix == ".css" else "text/javascript; charset=utf-8"
                self.send_file(asset, content_type)
                return
        self.send_error(404)

    def send_json(self, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path: Path, content_type: str) -> None:
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), AccountingHandler)
    print(f"Feigin Accounting Control: http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    serve()