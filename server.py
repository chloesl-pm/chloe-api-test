#!/usr/bin/env python3
"""
Swagger API Tester - 로컬 프록시 서버
- 정적 파일 서빙 (index.html, swagger/*.json 등)
- /proxy 엔드포인트: 브라우저 CORS 우회하여 실제 API 요청 중계
"""

import json
import os
import ssl
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn

PROXY_TIMEOUT = 30  # 초 — 이 시간 안에 응답 없으면 에러 반환

PORT = int(os.environ.get('PORT', 8765))


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    """요청마다 별도 스레드 — 느린 외부 API가 다른 요청을 블로킹하지 않음"""
    daemon_threads = True

class ProxyHandler(SimpleHTTPRequestHandler):

    # ── CORS preflight ─────────────────────────────────────────────
    def do_OPTIONS(self):
        self._cors_headers(200)

    # ── Proxy endpoint ─────────────────────────────────────────────
    def do_POST(self):
        if self.path != '/proxy':
            self.send_error(404)
            return

        length = int(self.headers.get('Content-Length', 0))
        try:
            payload = json.loads(self.rfile.read(length))
        except Exception:
            self._json_response({'error': '잘못된 요청 형식'}, 400)
            return

        url     = payload.get('url', '')
        method  = payload.get('method', 'GET').upper()
        headers = payload.get('headers', {})
        body    = payload.get('body')

        if not url:
            self._json_response({'error': 'url 필드가 필요합니다'}, 400)
            return

        # Content-Type 은 서버에서 그대로 전달; Transfer-Encoding 등 hop-by-hop 제거
        skip = {'transfer-encoding', 'connection', 'host'}
        safe_headers = {k: v for k, v in headers.items() if k.lower() not in skip}

        body_bytes = None
        if body:
            body_bytes = body.encode('utf-8') if isinstance(body, str) else body

        req = urllib.request.Request(url, data=body_bytes, headers=safe_headers, method=method)

        # 로컬 테스트 도구이므로 SSL 검증 비활성화
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            with urllib.request.urlopen(req, context=ctx, timeout=PROXY_TIMEOUT) as resp:
                resp_body = resp.read().decode('utf-8', errors='replace')
                # 헤더를 소문자 키로 정규화 + 원본 케이스도 함께 보존
                resp_hdrs = {}
                for k, v in resp.getheaders():
                    resp_hdrs[k] = v               # 원본 케이스
                    resp_hdrs[k.lower()] = v        # 소문자 케이스
                self._json_response({'status': resp.status, 'body': resp_body, 'headers': resp_hdrs})
        except urllib.error.HTTPError as e:
            resp_body = e.read().decode('utf-8', errors='replace')
            # HTTPError도 헤더 반환 (IAM 토큰은 헤더에 있음)
            resp_hdrs = {}
            for k, v in e.headers.items():
                resp_hdrs[k] = v
                resp_hdrs[k.lower()] = v
            self._json_response({'status': e.code, 'body': resp_body, 'headers': resp_hdrs})
        except Exception as e:
            self._json_response({'error': str(e)}, 502)

    # ── Helpers ────────────────────────────────────────────────────
    def _cors_headers(self, code=200):
        self.send_response(code)
        self.send_header('Access-Control-Allow-Origin',  '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    def _json_response(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type',                'application/json; charset=utf-8')
        self.send_header('Content-Length',              str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        method = args[0].split()[0] if args else ''
        if '/proxy' in (args[0] if args else ''):
            print(f'[proxy] {args[0]}  →  {args[1]}')
        else:
            super().log_message(fmt, *args)


if __name__ == '__main__':
    server = ThreadingHTTPServer(('', PORT), ProxyHandler)
    print(f'✅  서버 시작: http://localhost:{PORT}')
    print(f'   정적 파일 서빙 + CORS 프록시 활성화')
    print(f'   종료: Ctrl+C\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n서버 종료')
