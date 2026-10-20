import os
import json
import re
import html
import sys
from urllib.parse import quote_plus

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
MANIFEST_PATH = os.path.join(SCRIPT_DIR, 'bestwatchdeals_manifest_v2.json')
MINED_WATCHES_PATH = os.path.join(SCRIPT_DIR, 'aliexpress_mined_watches.json')

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Brand names mapping
KNOWN_BRANDS = [
    ('San Martin', 'san-martin'),
    ('PAGANI DESIGN', 'pagani-design'),
    ('STEELDIVE', 'steeldive'),
    ('Addiesdive', 'addiesdive'),
    ('Sugess', 'sugess'),
    ('Baltany', 'baltany'),
    ('Lobinni', 'lobinni'),
    ('Escapement Time', 'escapement-time'),
    ('Tandorio', 'tandorio'),
    ('Specht&Sohne', 'specht-sohne'),
    ('Specht & Sohne', 'specht-sohne'),
    ('OBLVLO', 'oblvlo'),
    ('BOBO BIRD', 'bobo-bird'),
    ('Seagull', 'seagull')
]

def detect_brand(text, fallback='Watch'):
    for b_name, b_slug in KNOWN_BRANDS:
        if b_name.lower() in text.lower():
            return b_name, b_slug
    return fallback, re.sub(r'[^a-z0-9]+', '-', fallback.lower()).strip('-')

def generate_clean_slug(raw_title, brand, index):
    real_brand, brand_slug = detect_brand(raw_title, brand)
    
    # Strip unnecessary keywords
    t = raw_title.lower()
    t = re.sub(r'^(202[0-9]\s+)?', '', t)
    t = re.sub(r'^(pagani\s+design|san\s+martin|steeldive|addiesdive|sugess|baltany|lobinni|specht\s*&?\s*sohne|tandorio|bobo\s+bird)\s*', '', t)
    t = re.sub(r':\s*202[0-9].*', '', t)
    t = re.sub(r'watch(es)?', '', t)
    t = re.sub(r'for men', '', t)
    t = re.sub(r'mechanical', '', t)
    t = re.sub(r'automatic', 'auto', t)
    t = re.sub(r'waterproof', '', t)
    t = re.sub(r'brand', '', t)
    t = re.sub(r'rel[oó]j', '', t)
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')
    
    words = [w for w in t.split('-') if w and w != brand_slug]
    base_slug = f"{brand_slug}-" + "-".join(words[:5])
    base_slug = re.sub(r'-+', '-', base_slug).strip('-')
    return base_slug, real_brand

def run_upgrade():
    print("🚀 Upgrading BestWatchDeals Product URLs & Navigation Engine...")
    
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    reviews = [u for u in manifest['urls'] if u.get('action') == 'REVIEW']
    print(f"Loaded {len(reviews)} reviews from manifest.")
    
    used_slugs = {}
    updated_reviews = []
    old_to_new_redirects = []
    
    for i, r in enumerate(reviews):
        raw_name = r.get('product_name') or r.get('clean_title') or r['title_2026']
        brand = r.get('brand', 'Watch')
        
        slug, real_brand = generate_clean_slug(raw_name, brand, i)
        if slug in used_slugs:
            slug = f"{slug}-{i+1}"
        used_slugs[slug] = i
        
        new_path = f"/watches/{slug}/"
        new_url = f"https://bestwatchdeals.com{new_path}"
        old_path = r['path']
        
        # Save redirect mapping
        old_to_new_redirects.append((old_path, new_path))
        
        # Update review object
        r['brand'] = real_brand
        r['slug'] = slug
        r['clean_path'] = new_path
        r['clean_url'] = new_url
        r['old_path'] = old_path
        
        # Simplify display title for cards and PDP
        clean_title_only = r.get('clean_title') or r.get('product_name') or r['title_2026'].split(':')[0]
        r['display_title'] = clean_title_only
        
        updated_reviews.append(r)
        
    print(f"Generated {len(used_slugs)} unique modern product URLs under /watches/<slug>/")
    
    # Save back to manifest with clean_path
    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print("✅ Saved updated manifest with clean_path and clean_url.")
    
    return updated_reviews, old_to_new_redirects

if __name__ == '__main__':
    run_upgrade()
