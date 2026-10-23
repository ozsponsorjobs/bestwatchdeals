import json

with open('tools/bestwatchdeals_manifest_v2.json', 'r', encoding='utf-8') as f:
    manifest = json.load(f)

reviews = [u for u in manifest['urls'] if u.get('action') == 'REVIEW']
print(f"Total reviews: {len(reviews)}")

for i, r in enumerate(reviews):
    title = r.get('display_title') or r.get('title_2026', '')[:40]
    path = r.get('clean_path') or r.get('path')
    brand = r.get('brand')
    price = r.get('sale_price')
    stars = r.get('stars')
    orders = r.get('orders')
    print(f"{i:2d} | {brand:15s} | ${price:>6} | {stars}* | {orders:>5} orders | {path} | {title}")
