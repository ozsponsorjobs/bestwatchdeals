import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from build_roundup_articles import ROUNDUP_ARTICLES

MANIFEST_PATH = os.path.join(SCRIPT_DIR, 'bestwatchdeals_manifest_v2.json')

with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

existing_paths = {u.get('path') for u in manifest['urls']}
added = 0
for a in ROUNDUP_ARTICLES:
    p = a['path']
    if p not in existing_paths:
        manifest['urls'].append({
            'url': a['url'],
            'path': a['path'],
            'clean_url': a['url'],
            'clean_path': a['path'],
            'section': 'Alternative Watch Roundups',
            'archived_year': '2026',
            'action': 'ROUNDUP',
            'title_2026': a['title'],
            'topic': a['id'],
            'type': 'roundup'
        })
        added += 1

manifest['total_urls'] = len(manifest['urls'])

with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"Added {added} roundup articles to manifest. Total URLs: {manifest['total_urls']}")
