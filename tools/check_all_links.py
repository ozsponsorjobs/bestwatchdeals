import os
import glob
from bs4 import BeautifulSoup
from urllib.parse import urlparse

DIST = r"c:\Users\er\seo backlink\dist_bestwatchdeals"

def test_all_links():
    html_files = glob.glob(os.path.join(DIST, "**", "index.html"), recursive=True)
    print(f"Total HTML files found: {len(html_files)}")
    
    total_links = 0
    broken_internal = []
    
    for fpath in html_files:
        rel_fpath = os.path.relpath(fpath, DIST)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
        except Exception as e:
            print(f"Error reading {rel_fpath}: {e}")
            continue
            
        links = soup.find_all('a')
        for a in links:
            total_links += 1
            href = a.get('href', '').strip()
            if not href or href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
                continue
            
            # If absolute URL to bestwatchdeals.com
            if href.startswith("https://bestwatchdeals.com") or href.startswith("http://bestwatchdeals.com"):
                parsed = urlparse(href)
                path = parsed.path
            elif href.startswith("http://") or href.startswith("https://"):
                # External link (affiliate or external)
                continue
            else:
                path = href
                
            clean_path = path.split('?')[0].split('#')[0].strip('/')
            
            # Check target
            if not clean_path:
                target = os.path.join(DIST, "index.html")
            else:
                target = os.path.join(DIST, clean_path, "index.html")
                if not os.path.exists(target):
                    target = os.path.join(DIST, clean_path)
            
            if not os.path.exists(target):
                broken_internal.append({
                    "source": rel_fpath,
                    "anchor_text": a.text.strip()[:40],
                    "href": href,
                    "attempted_path": clean_path
                })

    print(f"Total links checked: {total_links}")
    print(f"Total broken internal links: {len(broken_internal)}")
    
    # Print distinct broken hrefs
    distinct_broken = {}
    for item in broken_internal:
        h = item["href"]
        if h not in distinct_broken:
            distinct_broken[h] = item
            
    print(f"\nDistinct broken URLs ({len(distinct_broken)}):")
    for h, item in list(distinct_broken.items())[:25]:
        print(f"  Href: {h} | Text: '{item['anchor_text']}' | Found in: {item['source']}")

if __name__ == "__main__":
    test_all_links()
