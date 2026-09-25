#!/usr/bin/env python3
"""Dependency-free fixture server. Bound to loopback, fixed files only."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, parse_qs, unquote, quote
import argparse, json, time, re

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / 'web'
DOCS = ROOT / 'docs'
MANIFEST = {f['name']: f for f in json.loads((WEB/'manifest.json').read_text())}
STATIC = {'/mark.svg':('mark.svg','image/svg+xml'), '/':('index.html','text/html; charset=utf-8'), '/index.html':('index.html','text/html; charset=utf-8'), '/style.css':('style.css','text/css; charset=utf-8'), '/site.js':('site.js','text/javascript; charset=utf-8'), '/manifest.json':('manifest.json','application/json; charset=utf-8'), '/README.md':('README.md','text/plain; charset=utf-8'), '/MANUAL.md':('MANUAL.md','text/plain; charset=utf-8')}

class Handler(BaseHTTPRequestHandler):
    server_version = 'CosmicWebTest/1.0'
    def do_HEAD(self): self.respond(False)
    def do_GET(self): self.respond(True)
    def respond(self, body):
        try: self._respond(body)
        except (BrokenPipeError, ConnectionResetError): pass
    def _respond(self, body):
        # Do not expose source/build files or a filesystem directory listing.
        host = self.headers.get('Host', '').split(':')[0].lower()
        if host not in ('127.0.0.1','localhost'):
            self.send_error(403);return
        target=urlsplit(self.path); path=unquote(target.path)
        mode='files'; name=''; download_name=''
        if path in STATIC:
            filename,mime=STATIC[path]
            source = ROOT / filename if filename == 'README.md' else DOCS / filename if filename == 'MANUAL.md' else WEB / filename
            data=source.read_bytes()
            if filename == 'index.html':
                data = data.replace(b'<html lang="zh-CN"', b'<html lang="zh-CN" data-server-fixtures', 1)
        else:
            if path == '/download':
                ext=parse_qs(target.query).get('id',[''])[0];name='sample.'+ext
                mode='attachment';download_name='文档 预览测试.'+ext
            else:
                parts=path.strip('/').split('/')
                if len(parts)!=2 or parts[0] not in ('files','attachment','slow','unknown-size','redirect'):
                    self.send_error(404);return
                mode,name=parts
            if name not in MANIFEST:
                self.send_error(404,'No such test fixture');return
            if mode=='redirect':
                self.send_response(302);self.send_header('Location','/attachment/'+quote(name));self.send_header('Content-Length','0');self.end_headers();return
            meta=MANIFEST[name];mime=meta['mime'];data=(WEB/'files'/name).read_bytes()
        start,end,status=0,len(data)-1,200
        requested=self.headers.get('Range')
        if requested and mode!='unknown-size':
            match=re.fullmatch(r'bytes=(\d*)-(\d*)',requested)
            if match and any(match.groups()):
                left,right=match.groups()
                if left:start=int(left);end=min(int(right),end) if right else end
                else:start=max(0,len(data)-int(right))
                if start>end or start>=len(data):
                    self.send_response(416);self.send_header('Content-Range',f'bytes */{len(data)}');self.end_headers();return
                status=206
        self.send_response(status)
        self.send_header('Content-Type',mime)
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','no-referrer')
        if mode!='unknown-size':self.send_header('Content-Length',str(end-start+1));self.send_header('Accept-Ranges','bytes')
        if status==206:self.send_header('Content-Range',f'bytes {start}-{end}/{len(data)}')
        if name:
            disposition='attachment' if mode in ('attachment','unknown-size','slow') else 'inline'
            self.send_header('Content-Disposition',f'{disposition}; filename="{name}"; filename*=UTF-8\'\'{quote(download_name or name)}')
        self.end_headers()
        if not body:return
        payload=data[start:end+1]
        if mode=='slow':
            chunk=max(1,(len(payload)+15)//16)
            for i in range(0,len(payload),chunk):
                time.sleep(.25);self.wfile.write(payload[i:i+chunk]);self.wfile.flush()
        else:self.wfile.write(payload)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--port',type=int,default=8765);args=parser.parse_args()
    try: server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    except OSError as error:raise SystemExit(f'Cannot start server: {error}\nTry: python3 tools/server.py --port 8766')
    print(f'Cosmic WebTest: http://127.0.0.1:{args.port}/\nPress Control+C to stop. Serving only this test website.',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
