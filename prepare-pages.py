#!/usr/bin/env python3
"""Stage only public site assets for GitHub Pages; no document regeneration."""
from pathlib import Path
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent
OUT = ROOT / '.pages'
if OUT.is_symlink():
    raise SystemExit('Refusing a symlink as the staging directory.')
if OUT.exists():
    shutil.rmtree(OUT)
(OUT / 'files').mkdir(parents=True)
for name in ('style.css', 'site.js', 'mark.svg', 'manifest.json', 'README.md', '.nojekyll'):
    shutil.copyfile(ROOT / name, OUT / name)
page = (ROOT / 'index.html').read_text()
# Pages cannot serve custom HTTP response fixtures. Do not publish dead entries.
page = re.sub(r'\s*<!-- server-fixtures:start -->.*?<!-- server-fixtures:end -->', '', page, flags=re.S)
(OUT / 'index.html').write_text(page)
files = json.loads((ROOT / 'manifest.json').read_text())
for file in files:
    name = file['name']
    if Path(name).name != name or name.startswith('.'):
        raise SystemExit(f'Invalid fixture filename: {name!r}')
    source = ROOT / 'files' / name
    if source.is_symlink() or not source.is_file():
        raise SystemExit(f'Invalid fixture: {name}')
    shutil.copyfile(source, OUT / 'files' / name)
print(f'GitHub Pages files ready: {OUT}')
