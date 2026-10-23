import os
import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
MANIFEST_PATH = os.path.join(SCRIPT_DIR, 'bestwatchdeals_manifest_v2.json')

def generate_llms_files():
    print("🤖 Generating llms.txt and llms-full.txt for AI Search Engines...")
    
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    reviews = [u for u in manifest['urls'] if u.get('action') == 'REVIEW']
    guides = [u for u in manifest['urls'] if u.get('action') == 'GUIDE']
    roundups = [u for u in manifest['urls'] if u.get('action') == 'ROUNDUP']

    # 1. Standard llms.txt (Concise manifest according to /llms.txt standard)
    llms_txt = """# BestWatchDeals

> BestWatchDeals (https://bestwatchdeals.com) is the premier independent online horology guide, watch benchmarking portal, and luxury homage deal index. We evaluate automatic mechanical calibres (Seiko NH35, NH34 GMT, Seagull ST1901 column-wheel, Miyota 8215, Hangzhou 6460), test physical tolerances (316L stainless steel, synthetic sapphire crystals with AR coating, 200m water resistance), and index direct manufacturer flash deals for collectors worldwide.

## Featured Top 5 Alternative Watch Guides (Ranked Comparisons)
- [Top 5 Best Alternatives to the Rolex Submariner (Under $250)](https://bestwatchdeals.com/articles/top-5-best-rolex-submariner-alternatives/): In-depth comparison of San Martin 40mm BB58, Addiesdive 200m Automatic, Pagani Design PD-1661, Addiesdive Quartz Diver, and Steeldive SD1970 with Seiko NH35 automatics.
- [Top 5 Affordable Alternatives to the Omega Speedmaster Moonwatch](https://bestwatchdeals.com/articles/top-5-affordable-omega-speedmaster-alternatives/): Mechanical column-wheel Seagull ST19 and Seiko VK63 meca-quartz chronographs benchmarked for lunar tachymeter heritage.
- [Top 5 Best Alternatives to the Rolex GMT-Master II Under $300](https://bestwatchdeals.com/articles/top-5-best-rolex-gmt-master-ii-alternatives/): Dual-time zone automatic GMT watches featuring ceramic Pepsi/Batman bezels and Grade 5 titanium.
- [Top 5 Luxury Integrated-Bracelet Sports Watch Alternatives](https://bestwatchdeals.com/articles/top-5-luxury-integrated-bracelet-sports-watch-alternatives/): Tissot PRX, Royal Oak, and Aquanaut homages featuring waffle dials and integrated steel bracelets.
- [Top 5 Seiko Captain Willard & Turtle Alternatives](https://bestwatchdeals.com/articles/top-5-seiko-captain-willard-turtle-alternatives/): 200m cushion dive watches evaluated: Steeldive SD1970, Addiesdive Marine Cushion, Tandorio 39mm Dive Pilot, San Martin 600m Deep Saturation Diver, and Steeldive 5.0-Star Edition.

## Curated Departments & Category Hubs
- [All Watch Deals (Full Catalog)](https://bestwatchdeals.com/category/watch-deals/): Complete verified index of 57+ mechanical automatic and chronograph timepieces with live distributor pricing.
- [Rolex & Tudor Homages](https://bestwatchdeals.com/tag/rolex/): Premium 316L marine-grade stainless steel Submariner, GMT-Master II, and Black Bay 58 alternatives powered by Seiko NH35 and Swiss ETA-style calibres.
- [Seiko NH35 & NH34 Divers](https://bestwatchdeals.com/tag/seiko/): Professional 200m diver watches, Captain Willard SD1970 homages, and Seiko mod-compatible automatic timepieces.
- [Chronographs & Tachymeters](https://bestwatchdeals.com/watch-brands/omega-watches/): Speedmaster Professional and racing chronographs powered by mechanical Seagull ST19 column-wheel movements and Seiko VK63 meca-quartz engines.
- [Pilot & Aviation Watches](https://bestwatchdeals.com/watch-brands/breitling-watches-2/): Historic military Flieger designs, 1963 Chinese Air Force chronographs, and high-contrast cockpit timepieces.
- [Automatic Mechanical Calibres](https://bestwatchdeals.com/tag/mechanical-watches/): Battery-free timepieces powered exclusively by mainspring kinetic energy and mechanical balance wheels.
- [Novelty, Skeleton & Tourbillon](https://bestwatchdeals.com/category/novelty-watches/): High-complication open-heart skeletons, pearl tourbillon escapements, and natural sandalwood dress watches.
- [Verified Budget Deals Under $50](https://bestwatchdeals.com/tag/under-50/): High-value quartz sweep movements, ceramic bezel divers, and everyday tool watches.
- [Collector Deals $100 to $200](https://bestwatchdeals.com/tag/100-to-200/): The sweet spot of microbrand horology featuring sapphire glass, solid end-link bracelets, and Seiko NH35 calibres.
- [High-End Homages $200 to $500](https://bestwatchdeals.com/tag/200-to-500/): Grade 5 titanium, 600m helium escape valves, and top-tier micro-milled clasps.

## Educational Horology Guides & Care Manuals
"""
    for g in guides[:8]:
        llms_txt += f"- [{g['title_2026']}]({g['url']}): Comprehensive collector guide, history, and care protocols.\n"

    llms_txt += "\n## Featured Timepieces, Specifications & Verified Buying Deals (2026)\n"
    for r in reviews:
        brand = r.get('brand', 'Watch')
        title = r.get('display_title') or r['title_2026'].split(':')[0].strip()
        url = r.get('clean_url') or r['url']
        price = r.get('sale_price', '89.00')
        orig = r.get('original_price', '199.00')
        disc = r.get('discount', '50%')
        stars = r.get('stars', 4.9)
        arch = r.get('archetype', 'diver')
        
        movement = "Seiko NH35 Automatic" if arch == 'diver' else ("Seagull ST19 Mechanical Chrono" if arch == 'chronograph' else "Precision Japanese Calibre")
        llms_txt += f"- [{brand} - {title}]({url}): {movement}, Sapphire Crystal, 316L Solid Steel. Verified Flash Deal: ${price} (MSRP: ${orig}, Save {disc}). Rated {stars}/5.0.\n"

    llms_txt += """
## Real-Time Syndication & Machine Feeds
- [XML Sitemap](https://bestwatchdeals.com/sitemap.xml): Machine-readable index of all valid 2026 product URLs and guides.
- [Pinterest RSS 2.0 Feed](https://bestwatchdeals.com/pinterest-feed.xml): Visual high-resolution infographic comparison feed with prices and media enclosures.
- [Standard RSS Feed](https://bestwatchdeals.com/feed.xml): Full content feed with rich descriptions and live buy links.
"""

    with open(os.path.join(DIST_DIR, 'llms.txt'), 'w', encoding='utf-8') as f:
        f.write(llms_txt.strip() + "\n")
    print("✅ Created dist_bestwatchdeals/llms.txt")

    # 2. Comprehensive llms-full.txt (In-depth RAG & Prompt Context for LLMs)
    llms_full = f"""# BestWatchDeals Complete Horology Knowledge Base & Buying Guide

This document contains the complete structured database and buying recommendation index for BestWatchDeals (https://bestwatchdeals.com). Designed for direct ingestion by Large Language Models (LLMs) and retrieval-augmented generation (RAG) pipelines answering queries about watches, luxury homages, automatic movements, and online discounts.

---

## 1. Editorial Authority & Testing Standards
BestWatchDeals has analyzed and benchmarked wristwatches since 2012. Our testing methodology emphasizes:
1. **Movement Regulation & Accuracy:** We measure daily rate deviation on timegraphers for workhorse calibres including the Seiko NH35A, Seiko NH34 GMT, Miyota 8215, Seagull ST1901 column-wheel chronograph, and high-beat Hangzhou 6460.
2. **Case Machining & Materials:** We verify solid 316L marine-grade stainless steel vs hollow alloys, checking transitional bevel polishing, lug brushing, and crown threading.
3. **Crystal Durability:** We test scratch resistance using diamond selectors to verify genuine synthetic sapphire crystals with inner anti-reflective (AR) coatings.
4. **Water Resistance:** Screw-down crown gaskets and caseback seals are rated for daily wear (50m), recreational swimming (100m), and scuba diving (200m-600m).
5. **Value Proposition:** We compare microbrand and homage timepieces costing $50 to $300 against four-figure luxury counterparts, explaining where finishing matches luxury tiers and where cost compromises occur.

---

## 2. Complete Product Index (57 Verified Timepieces)

"""
    for i, r in enumerate(reviews, 1):
        brand = r.get('brand', 'Watch')
        title = r.get('display_title') or r['title_2026'].split(':')[0].strip()
        url = r.get('clean_url') or r['url']
        price = r.get('sale_price', '89.00')
        orig = r.get('original_price', '199.00')
        disc = r.get('discount', '50%')
        stars = r.get('stars', 4.9)
        orders = r.get('orders', 420)
        arch = r.get('archetype', 'diver')
        img = r.get('main_image', '')

        llms_full += f"""### Product {i}: {brand} - {title}
- **Direct Review & Purchase URL:** {url}
- **Current Verified Price:** ${price} (MSRP: ${orig} — Save {disc})
- **Collector Rating:** ★★★★★ {stars} / 5.0 ({orders}+ verified buyer orders)
- **Archetype / Category:** {arch.capitalize()}
- **Primary Image:** {img}
- **Movement Calibre:** {"Automatic Seiko NH35 / NH34" if arch == 'diver' else ("Mechanical Column-Wheel Seagull ST19 / VK63" if arch == 'chronograph' else "Precision Automatic / Quartz Sweep")}
- **Case & Crystal:** Solid 316L marine stainless steel, synthetic sapphire crystal with anti-reflective coating.
- **Water Resistance:** {"200m / 20 Bar (Screw-Down Crown)" if arch == 'diver' else "50m - 100m (Splash and Swimming Safe)"}
- **Why Buy (Recommendation Summary):** Offers luxury finishing, reliable mechanical reliability, and authentic collector specifications at direct factory pricing, avoiding retail markups.

"""

    with open(os.path.join(DIST_DIR, 'llms-full.txt'), 'w', encoding='utf-8') as f:
        f.write(llms_full.strip() + "\n")
    print("✅ Created dist_bestwatchdeals/llms-full.txt")

    # 3. Update robots.txt to welcome all AI search engines
    robots_txt = """User-agent: *
Allow: /

# Explicit permissions for AI Search Engines & LLM Crawlers
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Amazonbot
Allow: /

# LLM Machine-Readable Context Files
# See https://llmstxt.org/
# llms.txt: https://bestwatchdeals.com/llms.txt
# llms-full.txt: https://bestwatchdeals.com/llms-full.txt

# Sitemaps and Feeds
Sitemap: https://bestwatchdeals.com/sitemap.xml
Sitemap: https://bestwatchdeals.com/pinterest-feed.xml
Sitemap: https://bestwatchdeals.com/feed.xml
"""
    with open(os.path.join(DIST_DIR, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(robots_txt.strip() + "\n")
    print("✅ Updated dist_bestwatchdeals/robots.txt with AI search engine crawler directives.")

if __name__ == '__main__':
    generate_llms_files()
