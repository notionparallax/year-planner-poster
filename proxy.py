#!/usr/bin/env python3
"""
Simple CORS proxy for fetching Google Calendar iCal feeds.
Usage:  python proxy.py
Then open poster.html at http://localhost:8080/poster.html
(serve the repo with: python -m http.server 8080)
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request

PORT = 8765


class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/fetch":
            qs = parse_qs(parsed.query)
            urls = qs.get("url", [])
            if not urls:
                self.send_error(400, "Missing url parameter")
                return
            target = urls[0]
            try:
                req = urllib.request.Request(target, headers={"User-Agent": "CalendarProxy/1.0"})
                with urllib.request.urlopen(req, timeout=15) as r:
                    data = r.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/calendar; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(data)
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(str(e).encode())
        elif parsed.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Calendar proxy is running.")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, fmt, *args):
        print(f"[proxy] {args[0]} -> {args[1]}")


if __name__ == "__main__":
    print(f"Calendar CORS proxy running at http://localhost:{PORT}")
    print(f"Fetch URL: http://localhost:{PORT}/fetch?url=<encoded-ical-url>")
    print("Press Ctrl+C to stop.")
    HTTPServer(("", PORT), ProxyHandler).serve_forever()
