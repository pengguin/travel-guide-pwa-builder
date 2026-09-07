#!/usr/bin/env python3
"""Check local documentation links, paired PNG dimensions and version labels."""
import re
import struct
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def main():
    errors=[]
    version=re.search(r'version:\s*"([0-9.]+)"',(ROOT/'SKILL.md').read_text()).group(1)
    for name in ['README.md','README.en.md','README.zh-CN.md']:
        if f'**{version}**' not in (ROOT/name).read_text():errors.append(f'Version mismatch: {name}')
    for p in ROOT.rglob('*.md'):
        if any(part in {'.git','node_modules'} for part in p.parts):continue
        for link in re.findall(r'\]\(([^)\s]+)(?:\s+"[^"]*")?\)',p.read_text()):
            link=link.split('#',1)[0]
            if not link or re.match(r'[a-z]+:',link):continue
            if not (p.parent/link).exists():errors.append(f'Broken local link: {p.relative_to(ROOT)} -> {link}')
    for shot,height in [('chat',1000),('home',1000),('map',900),('logistics',1000)]:
        for lang in ['zh','en']:
            p=ROOT/'docs'/'images'/f'{shot}-{lang}.png'
            if not p.is_file():errors.append(f'Missing PNG: {p.name}');continue
            data=p.read_bytes()
            if data[:8]!=b'\x89PNG\r\n\x1a\n' or len(data)<10000 or struct.unpack('>II',data[16:24])!=(1600,height):errors.append(f'Invalid PNG dimensions/content: {p.name}')
    for error in errors:print('ERROR:',error)
    if not errors:print(f'Documentation links, version {version} and 8 paired PNG captures passed.')
    return bool(errors)
if __name__=='__main__':raise SystemExit(main())
