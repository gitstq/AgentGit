"""Local web dashboard server for AgentGit.

Serves a zero-dependency, single-page dashboard plus a small JSON API.
Uses only the Python standard library (http.server).
"""

from __future__ import annotations

import json
import mimetypes
import os
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import parse_qs, urlparse

from .detect import detect_all
from .storage import AgentGitRepo

WEB_DIR = Path(__file__).parent / "web"


class AgentGitHandler(BaseHTTPRequestHandler):
    repo: AgentGitRepo = None  # type: ignore[assignment]
    quiet: bool = False

    # ------------------------------------------------------------------ #
    # helpers
    # ------------------------------------------------------------------ #
    def _send_json(self, data: Any, status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path) -> None:
        if not path.exists() or not path.is_file():
            self._send_json({"error": "not found"}, 404)
            return
        ctype, _ = mimetypes.guess_type(str(path))
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype or "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}

    def log_message(self, fmt: str, *args: Any) -> None:  # silence default logging
        if not self.quiet:
            super().log_message(fmt, *args)

    # ------------------------------------------------------------------ #
    # routing
    # ------------------------------------------------------------------ #
    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path in ("/", "/index.html"):
            self._send_file(WEB_DIR / "index.html")
            return
        if path.startswith("/static/"):
            rel = path[len("/static/") :]
            self._send_file((WEB_DIR / rel).resolve())
            return

        if path == "/api/status":
            try:
                self._send_json(self.repo.status())
            except Exception as exc:  # pragma: no cover
                self._send_json({"error": str(exc)}, 500)
            return

        if path == "/api/snapshots":
            self._send_json({"snapshots": self.repo.list_snapshots()})
            return

        if path == "/api/agents":
            self._send_json({"agents": detect_all()})
            return

        if path == "/api/diff":
            snap_id = query.get("id", [""])[0]
            target = query.get("target", [None])[0]
            try:
                self._send_json(self.repo.diff(snap_id, target))
            except Exception as exc:
                self._send_json({"error": str(exc)}, 404)
            return

        if path == "/api/file":
            snap_id = query.get("id", [""])[0]
            rel = query.get("path", [""])[0]
            content = self.repo.file_content(snap_id, rel)
            self._send_json({"path": rel, "content": content or ""})
            return

        if path == "/api/current":
            rel = query.get("path", [""])[0]
            f = self.repo.path / rel
            content = f.read_text(encoding="utf-8", errors="replace") if f.exists() else None
            self._send_json({"path": rel, "content": content})
            return

        self._send_json({"error": "not found"}, 404)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/snapshot":
            body = self._read_body()
            try:
                manifest = self.repo.create_snapshot(
                    agent=body.get("agent") or None,
                    message=body.get("message") or None,
                )
                self._send_json(manifest, 201)
            except Exception as exc:
                self._send_json({"error": str(exc)}, 500)
            return

        if path == "/api/revert":
            body = self._read_body()
            snap_id = body.get("id", "")
            dry_run = bool(body.get("dry_run", False))
            try:
                result = self.repo.revert(snap_id, dry_run=dry_run)
                self._send_json(result)
            except Exception as exc:
                self._send_json({"error": str(exc)}, 404)
            return

        self._send_json({"error": "not found"}, 404)


def serve(
    repo: AgentGitRepo,
    host: str = "127.0.0.1",
    port: int = 8765,
    open_browser: bool = False,
    quiet: bool = False,
) -> ThreadingHTTPServer:
    """Start the dashboard server (blocking)."""
    AgentGitHandler.repo = repo
    AgentGitHandler.quiet = quiet
    server = ThreadingHTTPServer((host, port), AgentGitHandler)
    url = f"http://{host}:{port}/"
    if not quiet:
        print(f"[agentgit] Dashboard running at {url}")
        print("[agentgit] Press Ctrl+C to stop")
    if open_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return server
