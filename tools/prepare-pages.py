#!/usr/bin/env python3
"""Stage only public site assets for GitHub Pages; no document regeneration."""
from pathlib import Path
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / 'web'
DOCS = ROOT / 'docs'
OUT = ROOT / '.pages'
if OUT.is_symlink():
    raise SystemExit('Refusing a symlink as the staging directory.')
if OUT.exists():
    shutil.rmtree(OUT)
(OUT / 'files').mkdir(parents=True)
for name in ('style.css', 'site.js', 'mark.svg', 'manifest.json', 'CNAME', '.nojekyll'):
    shutil.copyfile(WEB / name, OUT / name)
shutil.copyfile(ROOT / 'README.md', OUT / 'README.md')
shutil.copyfile(DOCS / 'MANUAL.md', OUT / 'MANUAL.md')
page = (WEB / 'index.html').read_text()
# Pages cannot serve custom HTTP response fixtures. Do not publish dead entries.
page = re.sub(r'\s*<!-- server-fixtures:start -->.*?<!-- server-fixtures:end -->', '', page, flags=re.S)
(OUT / 'index.html').write_text(page)
files = json.loads((WEB / 'manifest.json').read_text())
for file in files:
    name = file['name']
    if Path(name).name != name or name.startswith('.'):
        raise SystemExit(f'Invalid fixture filename: {name!r}')
    source = WEB / 'files' / name
    if source.is_symlink() or not source.is_file():
        raise SystemExit(f'Invalid fixture: {name}')
    shutil.copyfile(source, OUT / 'files' / name)
print(f'GitHub Pages files ready: {OUT}')
