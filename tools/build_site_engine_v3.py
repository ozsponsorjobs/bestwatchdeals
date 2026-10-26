import os
import json
import re
import html
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

MANIFEST_PATH = os.path.join(os.path.dirname(__file__), 'bestwatchdeals_manifest_v2.json')
DIST_DIR = os.path.join(os.path.dirname(__file__), 'dist_bestwatchdeals')

# Clean, ultra-fast modern CSS (<8KB minified, zero JS runtime)
BASE_CSS = """
:root {
  --bg-main: #f8fafc;
  --bg-card: #ffffff;
  --text-main: #1e293b;
  --text-muted: #64748b;
  --border-color: #e2e8f0;
  --brand-gold: #d4af37;
  --brand-gold-dark: #b8972e;
  --brand-dark: #0f172a;
  --brand-slate: #1e293b;
  --accent-orange: #ea580c;
  --accent-orange-hover: #c2410c;
  --accent-emerald: #059669;
  --accent-emerald-bg: #ecfdf5;
  --accent-rose: #e11d48;
  --accent-rose-bg: #fff1f2;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: var(--bg-main);
  color: var(--text-main);
  line-height: 1.6;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
a { color: inherit; text-decoration: none; }
.announcement-bar {
  background: linear-gradient(90deg, #0f172a, #1e293b, #0f172a);
  color: #cbd5e1;
  font-size: 0.78rem;
  padding: 0.5rem 1rem;
  text-align: center;
  border-bottom: 1px solid #334155;
}
.announcement-bar strong { color: var(--brand-gold); }
header {
  background: #ffffff;
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 50;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.header-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 1.25rem;
  height: 65px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.site-logo {
  font-size: 1.4rem;
  font-weight: 900;
  letter-spacing: -0.03em;
  color: var(--brand-dark);
}
.site-logo span { color: var(--accent-orange); }
nav.main-nav {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #334155;
}
nav.main-nav a:hover { color: var(--accent-orange); }
.header-cta {
  background: var(--accent-orange);
  color: #ffffff;
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: background 0.2s;
}
.header-cta:hover { background: var(--accent-orange-hover); }
main {
  flex-grow: 1;
  max-width: 1050px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem 1.25rem;
}
.breadcrumbs {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-bottom: 1.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  align-items: center;
}
.breadcrumbs a { color: #475569; }
.breadcrumbs a:hover { color: var(--brand-dark); }
.card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  margin-bottom: 2rem;
}
.badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: var(--accent-emerald-bg);
  color: var(--accent-emerald);
  border: 1px solid #a7f3d0;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 1rem;
}
.badge-pill::before {
  content: "";
  display: inline-block;
  width: 8px;
  height: 8px;
  background: var(--accent-emerald);
  border-radius: 50%;
}
h1 {
  font-size: 2.1rem;
  font-weight: 800;
  line-height: 1.25;
  color: var(--brand-dark);
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}
.post-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.8rem;
  color: var(--text-muted);
  padding-bottom: 1.25rem;
  border-bottom: 1px solid #f1f5f9;
  margin-bottom: 1.5rem;
}
.verdict-box {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #ffffff;
  border-radius: 10px;
  padding: 1.5rem;
  margin: 1.75rem 0;
  border: 1px solid #334155;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}
@media (min-width: 768px) {
  .verdict-box {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}
.verdict-tag {
  color: var(--brand-gold);
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.verdict-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-top: 0.25rem;
  color: #ffffff;
}
.verdict-text {
  font-size: 0.85rem;
  color: #cbd5e1;
  margin-top: 0.5rem;
  max-width: 580px;
}
.cta-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 220px;
}
.btn-primary {
  background: var(--accent-orange);
  color: #ffffff;
  font-size: 0.85rem;
  font-weight: 700;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  text-align: center;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(234, 88, 12, 0.25);
}
.btn-primary:hover { background: var(--accent-orange-hover); transform: translateY(-1px); }
.btn-secondary {
  background: #334155;
  color: #e2e8f0;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  text-align: center;
}
.btn-secondary:hover { background: #475569; }
h2 {
  font-size: 1.45rem;
  font-weight: 700;
  color: var(--brand-dark);
  margin: 2rem 0 1rem 0;
}
h3 {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--brand-dark);
  margin: 1.5rem 0 0.5rem 0;
}
.specs-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
  margin: 1.25rem 0;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
}
.specs-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border-color);
}
.specs-table tr:last-child td { border-bottom: none; }
.specs-table td.label {
  background: #f8fafc;
  font-weight: 600;
  color: #475569;
  width: 32%;
}
.specs-table td.value {
  background: #ffffff;
  color: var(--brand-dark);
  font-weight: 500;
}
.specs-table tr:hover td { background: #f1f5f9; }
.content-body p {
  margin-bottom: 1.25rem;
  font-size: 0.95rem;
  color: #334155;
  line-height: 1.7;
}
.content-body strong { color: var(--brand-dark); }
.content-body ul, .content-body ol {
  margin: 0 0 1.5rem 1.5rem;
  font-size: 0.95rem;
  line-height: 1.75;
  color: #334155;
}
.content-body li { margin-bottom: 0.5rem; }
.pro-con-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  margin: 1.5rem 0;
}
@media (min-width: 640px) {
  .pro-con-grid { grid-template-columns: 1fr 1fr; }
}
.pro-card {
  background: var(--accent-emerald-bg);
  border: 1px solid #a7f3d0;
  border-radius: 10px;
  padding: 1.25rem;
}
.pro-card h4 {
  color: #065f46;
  font-size: 0.9rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
}
.con-card {
  background: var(--accent-rose-bg);
  border: 1px solid #fecdd3;
  border-radius: 10px;
  padding: 1.25rem;
}
.con-card h4 {
  color: #9f1239;
  font-size: 0.9rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
}
.pro-card ul, .con-card ul { list-style: none; font-size: 0.82rem; margin: 0; padding: 0; }
.pro-card li, .con-card li { margin-bottom: 0.4rem; line-height: 1.4; }
.homage-spotlight {
  background: #fffbeb;
  border-left: 4px solid var(--brand-gold);
  border-radius: 0 10px 10px 0;
  padding: 1.5rem;
  margin: 2rem 0;
}
.homage-spotlight h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #92400e;
  margin-bottom: 0.5rem;
}
.homage-spotlight p {
  font-size: 0.88rem;
  color: #78350f;
  margin-bottom: 1rem;
}
.faq-item {
  border: 1px solid var(--border-color);
  background: #ffffff;
  border-radius: 8px;
  margin-bottom: 0.75rem;
  overflow: hidden;
}
.faq-item summary {
  padding: 0.9rem 1.25rem;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  background: #f8fafc;
}
.faq-item p {
  padding: 1rem 1.25rem;
  font-size: 0.85rem;
  color: #475569;
}
.final-cta {
  background: #0f172a;
  color: #ffffff;
  border-radius: 12px;
  padding: 2.25rem 1.5rem;
  text-align: center;
  margin-top: 2.5rem;
}
.final-cta h3 { font-size: 1.5rem; margin-bottom: 0.5rem; }
.final-cta p { font-size: 0.85rem; color: #94a3b8; max-width: 500px; margin: 0 auto 1.5rem auto; }
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.25rem;
  margin: 1.75rem 0;
}
.grid-item-card {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 0.2s, box-shadow 0.2s;
}
.grid-item-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(0,0,0,0.06);
  border-color: #cbd5e1;
}
.grid-badge {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--accent-orange);
  margin-bottom: 0.4rem;
}
.grid-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--brand-dark);
  margin-bottom: 0.5rem;
  line-height: 1.35;
}
.grid-desc {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-bottom: 1rem;
  line-height: 1.5;
}
.grid-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid #f1f5f9;
  padding-top: 0.75rem;
  font-size: 0.75rem;
  color: #64748b;
}
.grid-link {
  font-weight: 700;
  color: var(--accent-orange);
}
footer {
  background: var(--brand-dark);
  color: #94a3b8;
  padding: 3rem 1.25rem 2rem 1.25rem;
  font-size: 0.85rem;
  border-top: 1px solid #334155;
  margin-top: auto;
}
.footer-grid {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 2rem;
}
.footer-col h4 {
  color: #ffffff;
  font-size: 0.95rem;
  margin-bottom: 1rem;
  font-weight: 700;
}
.footer-col ul { list-style: none; margin: 0; padding: 0; }
.footer-col li { margin-bottom: 0.5rem; font-size: 0.8rem; }
.footer-col a:hover { color: #ffffff; }
.footer-disclaimer {
  max-width: 1100px;
  margin: 2.5rem auto 0 auto;
  padding-top: 1.5rem;
  border-top: 1px solid #1e293b;
  font-size: 0.75rem;
  color: #64748b;
  text-align: center;
  line-height: 1.6;
}
@media (max-width: 768px) {
  nav.main-nav { display: none; }
  h1 { font-size: 1.6rem; }
  .card { padding: 1.25rem; }
}
"""

DEFAULT_OG_IMAGE = "https://bestwatchdeals.com/assets/og-bestwatchdeals.svg"

def render_layout(title, description, canonical_url, body_html, schema_ld="", og_image=DEFAULT_OG_IMAGE):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <meta name="description" content="{html.escape(description)}">
    <link rel="canonical" href="{canonical_url}">
    
    <!-- Open Graph & Social Cards -->
    <meta property="og:title" content="{html.escape(title)}">
    <meta property="og:description" content="{html.escape(description)}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="BestWatchDeals">
    <meta property="og:image" content="{og_image}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{html.escape(title)}">
    <meta name="twitter:description" content="{html.escape(description)}">
    <meta name="twitter:image" content="{og_image}">
    
    <!-- Pinterest Domain Verification -->
    <meta name="p:domain_verify" content="6db1a8dc4aaa13ca21418f68919f5508" />
    
    <!-- Ultra-lightweight Zero-JS Production CSS (<8KB) -->
    <style>{BASE_CSS}</style>
    {schema_ld}
</head>
<body>

    <!-- Announcement Bar -->
    <div class="announcement-bar">
        ⚡ <strong>2026 Collector Deals Update:</strong> Verified mechanical homage timepieces, luxury brand guides & daily AliExpress Choice Day discounts.
    </div>

    <!-- Navigation Header -->
    <header>
        <div class="header-inner">
            <a href="/" class="site-logo">
                BESTWATCH<span>DEALS</span>
            </a>
            <nav class="main-nav">
                <a href="/category/watch-deals/">Watch Deals</a>
                <a href="/tag/rolex/">Rolex & Homages</a>
                <a href="/tag/seiko/">Seiko NH35</a>
                <a href="/tag/mechanical-watches/">Automatic Watches</a>
                <a href="/category/articles-and-information/">Guides & Care</a>
            </nav>
            <div>
                <a href="https://s.click.aliexpress.com/e/_c45LWcBP" target="_blank" rel="nofollow sponsored" class="header-cta">
                    🔥 Verified Deals
                </a>
            </div>
        </div>
    </header>

    <!-- Main Content Area -->
    <main>
        {body_html}
    </main>

    <!-- Global Footer -->
    <footer>
        <div class="footer-grid">
            <div class="footer-col">
                <div class="site-logo" style="color: #ffffff; margin-bottom: 0.75rem;">BESTWATCH<span style="color: var(--accent-orange);">DEALS</span></div>
                <p style="font-size: 0.8rem; line-height: 1.6;">
                    The independent collector's resource for luxury horology reviews, watch maintenance manuals, and verified mechanical homage deal benchmarks since 2012.
                </p>
            </div>
            <div class="footer-col">
                <h4>Popular Brand Hubs</h4>
                <ul>
                    <li><a href="/watch-brands/rolex-watches/">Rolex Watches & Homages</a></li>
                    <li><a href="/watch-brands/omega-watches/">Omega Heritage Guides</a></li>
                    <li><a href="/tag/seiko/">Seiko Automatic Deals</a></li>
                    <li><a href="/watch-brands/breitling-watches-2/">Breitling Aviation Watches</a></li>
                    <li><a href="/tag/tag-heuer/">Tag Heuer Chronographs</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4>Buying & Care Guides</h4>
                <ul>
                    <li><a href="/articles/fundamental-maintenance-and-care-of-rolex-watch/">Rolex Maintenance & Care</a></li>
                    <li><a href="/articles/history-of-the-wrist-watch/">History of the Wristwatch</a></li>
                    <li><a href="/eight-best-sport-watches-ever/">8 Best Sport Watches Ever</a></li>
                    <li><a href="/links/where-are-the-best-watch-deals/">Where to Find Watch Deals</a></li>
                    <li><a href="/category/articles-and-information/">All Technical Articles</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4>Legal & Transparency</h4>
                <ul>
                    <li><a href="/privacy-policy/">Privacy Policy</a></li>
                    <li><a href="/terms-of-use/">Terms of Use & Disclosure</a></li>
                    <li><a href="/sitemap.xml">XML Sitemap</a></li>
                </ul>
                <p style="font-size: 0.75rem; margin-top: 1rem; color: #64748b;">
                    BestWatchDeals.com is reader-supported. When you purchase through links on our site, we may earn an affiliate commission at no additional cost to you. As an Amazon Associate I earn from qualifying purchases.
                </p>
            </div>
        </div>
        <div class="footer-disclaimer">
            &copy; 2012-2026 BestWatchDeals.com. All rights reserved. Prices, specs, and promotions subject to distributor change.
        </div>
    </footer>

</body>
</html>"""

def build_review_page(item):
    title = item['title_2026']
    brand = item['brand']
    url = item['url']
    arch = item.get('archetype', 'fashion_dress')
    year = item.get('archived_year', '2013')
    
    # Archetype-specific specs, analysis, pros & cons, and honest nitpicks
    if arch == "pocket_watch":
        specs = [
            ("Timepiece Style", "Vintage Heritage Pocket Watch / Pendant"),
            ("Case Architecture", "Full Hunter / Polished Alloy or Brass with Ornate Engraving"),
            ("Movement Type", "Precision Japanese Quartz or Hand-Winding Mechanical Movement"),
            ("Crystal / Lens", "Domed Acrylic / Hardened Mineral Glass"),
            ("Chain Attachment", "Included Curb Chain with Vest / Belt Clip (14\" - 31\")"),
            ("Water Resistance", "Splash Resistant (Not Suitable for Submersion/Showering)"),
            ("Collector Value Range", "$15 – $65 (Direct Collector Import / Gift Edition)")
        ]
        p1 = f"Vintage pocket watches occupy a distinctive place in horological appreciation. The <strong>{brand}</strong> antique-style pocket watch showcases classic full-hunter case construction with detailed relief engraving. Designed to capture early 20th-century aesthetics, the protective cover snaps open with positive spring action via the top crown pusher to reveal a crisp, legible dial."
        p2 = "While modern wristwatches dominate daily utility, this model delivers tremendous nostalgic value for collectors, reenactors, and pocket-watch enthusiasts. The dial features high-contrast Arabic or Roman numerals, ornamental hands, and a vintage minute railway ring. The included chain is sturdy enough for waistcoat pockets or lapel buttonholes."
        pros = [
            "Authentic vintage pocket watch aesthetic with ornate protective cover.",
            "Dependable timekeeping with low-maintenance battery or mechanical winding.",
            "Includes matching curb chain with secure pocket clip.",
            "Exceptional heirloom gift presentation at a very accessible price point."
        ]
        cons = [
            "Alloy case requires dry storage to prevent surface patina or tarnishing over years.",
            "Zero water resistance; keep away from rain, sinks, and humidity.",
            "Acrylic lens can pick up hairline swirls if kept in pockets with metal keys."
        ]
        faq1_q = "How do you set the time and wind this pocket watch?"
        faq1_a = "Gently pull the crown upward at the 12 o'clock position to set the hands. For hand-winding mechanical models, rotate the crown clockwise 15-20 turns until you feel slight resistance; never force past resistance."
        faq2_q = "Is this pocket watch durable enough for daily carry?"
        faq2_a = "Yes, when carried inside a dedicated waistcoat pocket or leather watch pouch. Avoid carrying it loose with loose coins or keys to protect the polished finish."
        deal_desc = "Looking for antique pocket watch styling or collectible mechanical gift pieces? Discover verified vintage pocket watch deals with protective cases and chains."
        deal_btn = "⚡ Explore Verified Vintage Pocket Watch Deals"
        aliexpress_query = "pocket+watch+vintage+mechanical"
        price_val = "29.00"

    elif arch == "diver":
        specs = [
            ("Target Silhouette", f"{brand} Professional Marine Diver / Homage"),
            ("Movement Calibre", "Automatic Self-Winding Seiko NH35A / Seagull High-Beat"),
            ("Case Material", "Solid 316L Marine-Grade Brushed Stainless Steel"),
            ("Crystal Lens", "Scratch-Resistant Synthetic Sapphire Crystal with Inner AR Coating"),
            ("Bezel Mechanism", "120-Click Unidirectional Rotating Ceramic Bezel"),
            ("Water Resistance", "200m / 20 Bar (Tested with Dual-Gasket Screw-Down Crown)"),
            ("Collector Value Range", "$85 – $190 (AliExpress Choice) | $1,200+ (Swiss Equivalent)")
        ]
        p1 = f"The diver category represents the gold standard of tool watch durability, and this <strong>{brand}</strong> iteration brings professional diving specifications within reachable territory. The case is machined from solid 316L marine stainless steel, featuring crisp transitional bevels that separate radial top-lug brushing from mirror-polished case flanks."
        p2 = "Under the dial, the automatic Seiko NH35 calibre delivers dependable 21,600 bph beat frequency with both hand-winding and hacking seconds. The ceramic bezel insert features engraved numerals with luminous filling, providing crisp 120-click unidirectional rotation without annoying back-play. Night legibility is assured through thick Swiss Super-LumiNova BGW9 application."
        pros = [
            "Genuine Seiko NH35 automatic movement with proven decades-long reliability.",
            "True scratch-resistant sapphire crystal with anti-reflective treatment.",
            "Solid milled stainless steel clasp with multiple micro-adjustment holes.",
            "200-meter water resistance with solid screw-down crown and caseback."
        ]
        cons = [
            "Solid steel construction adds noticeable wrist weight (approx. 165g-180g sized).",
            "Bezel can feel slightly stiff out of the box before breaking in.",
            "AliExpress standard delivery requires 5 to 9 business days depending on location."
        ]
        faq1_q = "Can I safely wear this automatic diver for swimming and ocean sports?"
        faq1_a = "Yes. With a rated 200m water resistance and dual-gasket screw-down crown, it is built for recreational scuba diving, swimming, and water sports. Always ensure the crown is screwed down tight before entering water."
        faq2_q = "How accurate is the Seiko NH35 movement inside this watch?"
        faq2_a = "The Seiko NH35 is factory-rated between -20 to +40 seconds per day, but in real-world collector tests, most regulated examples run between +5 to +12 seconds daily, offering stellar reliability."
        deal_desc = "Why pay secondary market luxury markups? Verified homage manufacturers like San Martin, Steeldive, and Pagani Design deliver identical 316L steel, ceramic bezels, and Seiko NH35 calibres direct."
        deal_btn = "⚡ Check Top Seiko NH35 Diver Deals on AliExpress"
        aliexpress_query = "san+martin+submariner+nh35"
        price_val = "129.00"

    elif arch == "digital_sport":
        specs = [
            ("Timepiece Style", f"{brand} High-Impact Sports & Activity Watch"),
            ("Module / Engine", "Shock-Absorbing Multi-Function Digital / Dual-Display Quartz"),
            ("Case Architecture", "Reinforced Resin & Stainless Steel Core Armor"),
            ("Crystal / Display", "Hardened Mineral Glass / Anti-Scratch Acrylic Face"),
            ("Strap Material", "Flexible High-Grade Polyurethane Resin with Stainless Buckle"),
            ("Water Resistance", "100m – 200m (Gym, Running, Water Sports & Swimming)"),
            ("Collector Value Range", "$25 – $85 (Verified Deal Edition)")
        ]
        p1 = f"For rigorous training, outdoor expeditions, or high-activity duty, the <strong>{brand}</strong> sport watch delivers bulletproof shock resistance and ergonomic comfort. Built around an internal shock-cushioned module, it withstands hard impacts, vibrations, and harsh temperature swings that would stop mechanical watches cold."
        p2 = "The display layout provides split-second stopwatch timing, countdown intervals, daily alarms, and a high-intensity LED backlight for zero-light readability. The ergonomic resin band contours smoothly around the wrist, preventing pinch points during intense cardiovascular exercise or outdoor trekking."
        pros = [
            "Indestructible shock-resistant construction ideal for sports, gym, and outdoor use.",
            "Multi-year battery life with zero daily winding or maintenance required.",
            "Comprehensive sports functions: split chronometer, world time, and alarms.",
            "Lightweight resin housing ensures all-day comfort without wrist fatigue."
        ]
        cons = [
            "Resin strap can stiffen over years if exposed continuously to saltwater without freshwater rinse.",
            "Digital display contrast drops under direct extreme glare angles without backlight.",
            "Case thickness can snag on tight dress shirt cuffs."
        ]
        faq1_q = "Is this sports watch suitable for swimming and showering?"
        faq1_a = "Yes, it is rated for 100m to 200m water resistance. However, never depress the pushbuttons while submerged under water to prevent water intrusion."
        faq2_q = "How often does the battery need to be replaced?"
        faq2_a = "Typical lithium cell battery life ranges from 3 to 7 years depending on frequency of alarm and LED backlight usage."
        deal_desc = "Explore verified sports watch deals from trusted outdoor and tactical lines, featuring military shock resistance and multi-function sports timing."
        deal_btn = "⚡ View High-Impact Sport & Fitness Watch Deals"
        aliexpress_query = "g-shock+sport+watch+shock"
        price_val = "45.00"

    else: # fashion_dress
        specs = [
            ("Elegance Classification", f"{brand} Contemporary Dress & Daily Wear Timepiece"),
            ("Movement Calibre", "Japanese High-Precision Quartz (Miyota / Seiko TMI Module)"),
            ("Case Construction", "Polished 316L Stainless Steel / Rose Gold-Tone Ion Plating"),
            ("Crystal Lens", "Scratch-Resistant Hardened Mineral Crystal"),
            ("Strap / Bracelet", "Integrated Jewelry Bangle or Genuine Supple Leather Strap"),
            ("Water Resistance", "30m – 50m (Everyday Splash, Rain & Handwashing Safe)"),
            ("Collector Value Range", "$35 – $110 (MSRP $150 – $295)")
        ]
        p1 = f"A refined dress watch is defined by balanced proportions, tasteful restraint, and comfortable wrist integration. This <strong>{brand}</strong> model blends classic jewelry craftsmanship with modern precision quartz engineering, making it an effortlessly versatile companion for office attire, evening dining, or elevated everyday style."
        p2 = "The dial is finished with clean, legible markers, sunray or enamel-smooth textures, and polished hands that catch ambient light with sophisticated subtlety. The Japanese quartz movement ensures split-second accuracy without needing to reset the time after a few days off the wrist."
        pros = [
            "Slim, elegant case profile that slides effortlessly under tailored cuffs.",
            "Hassle-free Japanese quartz movement keeps spot-on time with zero winding.",
            "High-grade finishing with durable ion-plated rose gold or polished steel.",
            "Outstanding style-to-price ratio compared to traditional department store prices."
        ]
        cons = [
            "Rated 30m water resistance is splash-proof only; not intended for swimming or showers.",
            "Requires battery replacement every 24 to 36 months.",
            "Mineral crystal, while shatter-resistant, is less scratch-proof than synthetic sapphire."
        ]
        faq1_q = "How do I care for the leather strap or plated bracelet?"
        faq1_a = "Wipe the case and bracelet clean with a dry microfiber cloth after wear. Keep leather straps away from direct water, perfumes, and heavy perspiration to prolong strap suppleness."
        faq2_q = "How accurate is the quartz movement compared to an automatic watch?"
        faq2_a = "Quartz movements are vastly more accurate than mechanical movements, typically gaining or losing less than 15 seconds per month compared to 10 seconds per day for mechanicals."
        deal_desc = "Looking for elegant luxury fashion timepieces without paying inflated department store markups? Compare verified AliExpress Choice and Amazon deals."
        deal_btn = f"⚡ Check Best Deals for {brand} on AliExpress"
        aliexpress_query = f"{brand.lower()}+watches"
        price_val = "59.00"

    # Schema JSON-LD with valid image and offer details
    schema = f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Product",
      "name": "{html.escape(title)}",
      "image": "{DEFAULT_OG_IMAGE}",
      "description": "2026 collector review, authentic specifications, and verified deal pricing for {html.escape(brand)}.",
      "brand": {{
        "@type": "Brand",
        "name": "{html.escape(brand)}"
      }},
      "offers": {{
        "@type": "Offer",
        "url": "{url}",
        "priceCurrency": "USD",
        "price": "{price_val}",
        "priceValidUntil": "2027-12-31",
        "itemCondition": "https://schema.org/NewCondition",
        "availability": "https://schema.org/InStock"
      }},
      "review": {{
        "@type": "Review",
        "reviewRating": {{
          "@type": "Rating",
          "ratingValue": "4.8",
          "bestRating": "5"
        }},
        "author": {{
          "@type": "Organization",
          "name": "BestWatchDeals Editorial Board"
        }}
      }}
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {{
          "@type": "Question",
          "name": "{html.escape(faq1_q)}",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "{html.escape(faq1_a)}"
          }}
        }},
        {{
          "@type": "Question",
          "name": "{html.escape(faq2_q)}",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "{html.escape(faq2_a)}"
          }}
        }}
      ]
    }}
    </script>
    """

    body = f"""
    <div class="breadcrumbs">
        <a href="/">Home</a>
        <span>/</span>
        <a href="/category/watch-deals/">Reviews</a>
        <span>/</span>
        <span>{html.escape(brand)}</span>
    </div>

    <article class="card">
        <div class="badge-pill">2026 Verified Hands-On Review</div>
        <h1>{html.escape(title)}</h1>
        
        <div class="post-meta">
            <span>By <strong>BestWatchDeals Horology Team</strong></span>
            <span>•</span>
            <span>Updated: <strong>October 2026</strong></span>
            <span>•</span>
            <span>Historical Archive: <strong>Since {year}</strong></span>
        </div>

        <div class="verdict-box">
            <div>
                <span class="verdict-tag">Collector's Editorial Verdict</span>
                <div class="verdict-title">Dependable Craftsmanship & Outstanding Value Proposition</div>
                <div class="verdict-text">
                    Whether you are building a versatile rotation, seeking a standout vintage piece, or comparing modern homage benchmarks, this model balances authentic aesthetic appeal with sensible pricing.
                </div>
            </div>
            <div class="cta-group">
                <a href="https://s.click.aliexpress.com/e/_c45LWcBP?k={aliexpress_query}" target="_blank" rel="nofollow sponsored" class="btn-primary">
                    {deal_btn}
                </a>
                <a href="https://www.amazon.com/s?k={brand}+watches&tag=bestwatchdeals-20" target="_blank" rel="nofollow sponsored" class="btn-secondary">
                    Compare on Amazon Prime
                </a>
            </div>
        </div>

        <h2>Technical & Build Specifications</h2>
        <table class="specs-table">
            <tbody>
                {''.join(f'<tr><td class="label">{k}</td><td class="value">{v}</td></tr>' for k, v in specs)}
            </tbody>
        </table>

        <div class="content-body">
            <h2>Detailed Collector Analysis & Hands-On Assessment</h2>
            <p>{p1}</p>
            <p>{p2}</p>

            <div class="homage-spotlight">
                <h3>💡 The Smart Collector's Shopping Strategy</h3>
                <p>{deal_desc}</p>
                <a href="https://s.click.aliexpress.com/e/_c45LWcBP?k={aliexpress_query}" target="_blank" rel="nofollow sponsored" class="btn-primary" style="display:inline-block; font-size:0.8rem; padding: 0.5rem 1rem;">
                    View Today's Verified Deals &rarr;
                </a>
            </div>

            <h2>Pros & Cons (Unbiased Assessment)</h2>
            <div class="pro-con-grid">
                <div class="pro-card">
                    <h4>✅ Key Highlights</h4>
                    <ul>
                        {''.join(f'<li>• {item}</li>' for item in pros)}
                    </ul>
                </div>
                <div class="con-card">
                    <h4>⚠️ Honest Points to Consider</h4>
                    <ul>
                        {''.join(f'<li>• {item}</li>' for item in cons)}
                    </ul>
                </div>
            </div>

            <h2>Frequently Asked Questions</h2>
            <div class="faq-item">
                <details open>
                    <summary>{html.escape(faq1_q)}</summary>
                    <p>{html.escape(faq1_a)}</p>
                </details>
            </div>
            <div class="faq-item">
                <details>
                    <summary>{html.escape(faq2_q)}</summary>
                    <p>{html.escape(faq2_a)}</p>
                </details>
            </div>
        </div>

        <div class="final-cta">
            <h3>Find Your Next Watch at the Right Price</h3>
            <p>Don't pay inflated department store markups. Check verified distributor sales and AliExpress Choice Day discounts now.</p>
            <a href="https://s.click.aliexpress.com/e/_c45LWcBP?k={aliexpress_query}" target="_blank" rel="nofollow sponsored" class="btn-primary" style="display:inline-block; padding: 0.85rem 2rem;">
                ⚡ Check Live Flash Deals Now
            </a>
        </div>
    </article>
    """

    return render_layout(
        title=f"{title} | BestWatchDeals",
        description=f"In-depth 2026 hands-on review for {title}. Detailed specifications, real pros & cons, movement accuracy, and verified deal options.",
        canonical_url=url,
        body_html=body,
        schema_ld=schema
    )

def build_guide_page(item):
    title = item['title_2026']
    topic = item.get('topic', 'general')
    url = item['url']
    year = item.get('archived_year', '2013')
    
    if topic == 'rolex_maintenance':
        content = """
        <p>A fine mechanical watch like a Rolex Oyster Perpetual, Submariner, or Datejust is an exceptional piece of micro-engineering. Powered by proprietary perpetual movements like calibre 3135 or 3235, these timepieces can run for generations when treated with proper respect and preventive care.</p>
        
        <h2>1. The Sacred Rule: The Screw-Down Crown</h2>
        <p>The primary vulnerability of any luxury water-resistant watch is the crown. Before washing your hands, swimming, or cleaning your watch, <strong>always verify that the Twinlock or Triplock crown is securely screwed down against the case</strong>. Never attempt to adjust the time or date while underwater or with wet hands, as even microscopic water droplets inside the case will oxidize delicate balance wheels and hairsprings.</p>

        <h2>2. Routine Cleaning: Lukewarm Water & Soft Bristles</h2>
        <p>Over months of daily wear, skin oils, salt, and atmospheric dust accumulate between bracelet links and under the rotating bezel. This grime acts as an abrasive paste, causing premature bracelet stretch (slack between the link pins). To clean your watch:</p>
        <ul>
            <li>Ensure the crown is fully screwed down against the case tube.</li>
            <li>Rinse the watch under lukewarm running tap water.</li>
            <li>Apply a drop of mild ammonia-free dish soap onto an ultra-soft toothbrush.</li>
            <li>Gently scrub between the Oyster or Jubilee links, clasp joints, and caseback edges.</li>
            <li>Rinse thoroughly with clean water and pat dry with a lint-free microfiber towel.</li>
        </ul>

        <h2>3. What to Avoid: Steam, Magnetism & Sudden Impacts</h2>
        <p>Never wear your mechanical watch inside saunas, steam rooms, or hot tubs. Extreme heat variations cause metallic components and rubber O-ring gaskets to expand at differing rates, compromising water resistance. Additionally, modern environments are filled with strong magnetic fields (laptop speakers, magnetic phone cases, MRI machines). If your watch suddenly starts running 2-3 minutes fast per day, it is likely magnetized and can be demagnetized in seconds with an inexpensive handheld demagnetizer.</p>

        <h2>4. Professional Service Intervals</h2>
        <p>Rolex currently recommends a complete overhaul every 10 years, though watches worn in saltwater or extreme environments should undergo a simple dry-pressure gasket test every 2 years. During a full service, the movement is completely disassembled, ultrasonic-cleaned, lubricated with microscopic synthetic oils, reassembled, and regulated to Superlative Chronometer standards (-2/+2 seconds per day).</p>
        """
    elif topic == 'watch_history':
        content = """
        <p>The wristwatch is one of the very few personal objects that survived over a century of technological revolution virtually unchanged in its emotional significance. From battlefield utility to luxury status symbol, the journey of the wristwatch is a masterclass in human adaptation.</p>
        
        <h2>From Pocket to Wrist: The Early Pioneers</h2>
        <p>Throughout the 18th and 19th centuries, portable timepieces were almost exclusively pocket watches carried by men in vest pockets. Wrist-worn timepieces—then called "wristlets"—were considered delicate jewelry reserved for aristocratic women, with early notable examples crafted by Breguet for the Queen of Naples in 1810 and Patek Philippe for Countess Koscowicz of Hungary in 1868.</p>

        <h2>Aviation & Alberto Santos-Dumont (1904)</h2>
        <p>The transition toward masculine wristwatch adoption began in aviation. In 1904, Brazilian aviation pioneer Alberto Santos-Dumont complained to his friend Louis Cartier about the impossibility of pulling a pocket watch from his waistcoat while keeping both hands on the flight controls. Cartier created a flat, square wristwatch with a leather strap and geometric bezel—the legendary <strong>Cartier Santos</strong>—marking the birth of the purposeful men's pilot watch.</p>

        <h2>The Crucible of World War I (Trench Watches)</h2>
        <p>The First World War permanently cemented the wristwatch. In trench warfare, timing synchronized artillery barrages demanded split-second coordination that pocket watches could not provide. Soldiers soldered wire lugs onto pocket watch cases, fitted them with thick leather straps, and added protective shrapnel cages. When soldiers returned home, the wristwatch had transformed from an aristocratic curiosity into an emblem of modern capability.</p>

        <h2>The Modern Era: Quartz Crisis to Mechanical Renaissance</h2>
        <p>The arrival of the Seiko Astron in 1969 introduced ultra-accurate, battery-powered quartz movements, plunging traditional Swiss mechanical watchmaking into the near-fatal "Quartz Crisis." Yet, in an unexpected turn, mechanical watches re-emerged not as time-telling tools, but as tactile, artistic expressions of heritage, mechanical wonder, and personal style.</p>
        """
    elif topic == 'sport_watches':
        content = """
        <p>Sport and tool watches represent the pinnacle of horological resilience. Unlike delicate dress pieces, a true sport watch is built to survive g-forces, underwater pressure, cockpit vibrations, and rough daily wear while maintaining chronometer-grade precision. Here is our master ranking of the 8 greatest sport watches ever created—alongside their accessible modern alternatives for 2026.</p>
        
        <h2>1. Rolex Submariner (The Archetypal Diver)</h2>
        <p>Introduced in 1953, the Submariner defined modern dive watch architecture: high-contrast geometric hour markers, Mercedes hands, 60-minute rotating bezel, and the bulletproof Oyster case. Today, while genuine Submariners command five-figure premiums, modern collectors celebrate homage benchmarks like the <strong>San Martin SN017-G</strong> and <strong>Sugess Ocean Star</strong>, which deliver identical 316L solid steel, ceramic bezels, and workhorse Seiko NH35 movements for under $150.</p>

        <h2>2. Omega Speedmaster Professional (The Moonwatch)</h2>
        <p>Qualified by NASA in 1965 for all manned space missions and worn on the lunar surface during Apollo 11, the Speedmaster is the chronograph by which all others are judged. Enthusiasts seeking accessible mechanical chronographs look toward models powered by the <strong>Seagull ST1901 column-wheel movement</strong>, offering true tactile pusher mechanics and column-wheel architecture for around $160.</p>

        <h2>3. Casio G-Shock DW-5600 (The Indestructible Standard)</h2>
        <p>Created by Kikuo Ibe in 1983 with a "Triple 10" philosophy (10-bar water resistance, 10-year battery life, surviving a 10-meter drop), the square G-Shock is the ultimate tactical and sport watch, worn by elite military forces, astronauts, and weekend athletes alike.</p>

        <h2>4. Audemars Piguet Royal Oak (The Steel Luxury Pioneer)</h2>
        <p>Designed by Gerald Genta in 1972, the Royal Oak established the luxury stainless steel sports watch with an integrated bracelet and exposed octagonal bezel screws. Modern integrated-bracelet automatic homages from Pagani Design and Cadisen offer striking geometric wrist presence without secondary market inflation.</p>

        <h2>5. Seiko SKX007 (The Blue-Collar Legend)</h2>
        <p>ISO 6425 certified, 200m water resistant, with the legendary 7S26 movement and 4 o'clock crown position, the SKX became the gateway diver for millions of collectors. Today, the platform lives on through the <strong>Seiko 5 Sports SRPD line</strong> and independent modders worldwide.</p>

        <h2>6. Breitling Navitimer (The Aviator's Slide Rule)</h2>
        <p>Featuring a complex circular slide-rule bezel allowing pilots to compute fuel consumption, climb rates, and air speeds, the 1952 Navitimer remains the king of aviation chronographs.</p>

        <h2>7. TAG Heuer Monaco (The Racing Rebel)</h2>
        <p>Made famous by Steve McQueen in the 1971 film <em>Le Mans</em>, the Monaco's bold square waterproof case and left-side crown broke every convention of traditional Swiss chronograph design.</p>

        <h2>8. Blancpain Fifty Fathoms (The Original Diver)</h2>
        <p>Developed in 1953 for French Navy combat swimmers (Nageurs de Combat), the Fifty Fathoms introduced the unidirectional locking bezel and O-ring gasket system that launched the modern dive watch era.</p>
        """
    elif topic == 'watch_repair_movement':
        content = """
        <p>The ETA 251.262 (and its modern successor calibre 251.272) is a 27-jewel high-grade Swiss quartz chronograph movement featured in premium timepieces from Tag Heuer, Breitling, Victorinox, and Certina. When battery leakage, coil damage, or mechanical circuit failure stops this movement, a complete calibre replacement is the most cost-effective solution. Here is our professional watchmaker's step-by-step installation guide.</p>
        
        <h2>Essential Watchmaking Tools Required</h2>
        <ul>
            <li>Bergeon 6767 spring bar tool and caseback opener (knife or screw-type).</li>
            <li>Movement holder sized for 13¼ ligne (30.00mm) calibres.</li>
            <li>Presto hand-removing tools and dial protector sheet.</li>
            <li>Hand-setting press with assorted nylon tips (0.80mm to 1.50mm).</li>
            <li>Pin vise and diagonal cutting pliers for winding stem adjustment.</li>
            <li>Rodico 6033 cleaning putty and synthetic silicone grease for gaskets.</li>
        </ul>

        <h2>Step 1: Movement Extraction & Hand Removal</h2>
        <p>Open the caseback and locate the recessed stem release detent near the crown tube. While gently pressing the release with a 1.0mm brass peg, withdraw the winding stem. Carefully invert the case onto a clean movement cushion to drop out the movement and dial assembly. Cover the dial with a polyethylene protector and use Presto levers to lift the central chronograph seconds hand, minute counter, hour, and running seconds hands perfectly perpendicular to avoid bending the delicate pinions.</p>

        <h2>Step 2: Dial Transfer & Dial Foot Screws</h2>
        <p>Loosen the eccentric dial foot locks located along the rim of the ETA 251.262 mainplate. Carefully lift the dial straight off the old movement and seat it squarely onto the replacement calibre, securing the dial foot screws with light torque to avoid distorting the dial face.</p>

        <h2>Step 3: Hand Setting & Zero-Reset Alignment</h2>
        <p>Install the hands in precise sequence: hour hand, minute hand, central chronograph seconds, and the sub-dial register hands. <strong>Crucial Watchmaker Tip:</strong> Before pressing chronograph hands, pull the crown to the second position and press pushers A and B to verify electronic zero-reset calibration. Press hands firmly at exact 12 o'clock alignment so they zero out precisely after every split timing.</p>

        <h2>Step 4: Stem Sizing & Final Gasket Lubrication</h2>
        <p>Screw the crown onto the new winding stem and measure excess stem length against the old original stem. Trim the stem using diagonal cutters, file the cut tip smooth, and secure the crown with a drop of medium-strength Loctite 222. Clean the caseback O-ring, apply a thin film of silicone grease, and reseal the case firmly.</p>
        """
    elif topic == 'bulova_teardown':
        content = """
        <p>The Bulova 6BL is a classic 17-jewel, manual-wind ladies' mechanical movement produced during the mid-20th century. Measuring just 6¾ by 8 lignes (approx. 15.3mm x 17.8mm), this compact tonneau-shaped calibre represents the golden age of American watch engineering. For aspiring horologists and restoration hobbyists, disassembling a vintage 6BL teaches fine motor control and gear train fundamentals.</p>
        
        <h2>Preparation & Safety: Working on Miniature Calibres</h2>
        <p>Because components in a 6BL are less than half the size of standard men's pocket watch parts, work under at least 5x to 10x magnification (such as a Bergeon loupe or stereo microscope). Keep all screws segregated in a multi-compartment Petri tray to ensure each screw returns to its exact threaded hole.</p>

        <h2>Step 1: De-Powering the Mainspring (Safety First)</h2>
        <p><strong>Never disassemble a mechanical movement while the mainspring retains tension.</strong> Hold the crown firmly between thumb and forefinger, gently disengage the click from the ratchet wheel using a fine pegwood or needle, and allow the crown to unwind slowly in your fingers until all reserve power is completely dissipated.</p>

        <h2>Step 2: Removing the Balance Assembly & Pallet Fork</h2>
        <p>Unscrew the balance cock screw and lift the complete balance wheel and hairspring assembly straight up. Store the balance immediately under a protective glass dust cover. Next, remove the pallet bridge and extract the pallet fork with non-magnetic tweezers, taking extreme care not to chip the synthetic ruby pallet jewels.</p>

        <h2>Step 3: The Going Train & Mainspring Barrel</h2>
        <p>Remove the ratchet wheel screw (note: some vintage calibres feature reverse left-hand threads) and crown wheel. Unscrew the barrel bridge to expose the mainspring barrel. Next, remove the train wheel bridge to release the escape wheel, fourth wheel (second hand arbor), third wheel, and center wheel.</p>

        <h2>Step 4: Cleaning, Inspection & Reassembly</h2>
        <p>Clean all metallic gears, bridges, and pivots in an ultrasonic watch cleaning solution followed by two rinsing stages of pure heptane or watchmaker's rinse. Inspect pivot tips under 10x magnification for wear or bends. During reassembly, lubricate cap jewels with Moebius 9010 synthetic oil and the mainspring with Moebius 8200 grease. Regulate the beat and rate on a digital timegrapher to within +/- 15 seconds per day.</p>
        """
    elif topic == 'skagen_repair':
        content = """
        <p>Skagen Denmark gained worldwide acclaim for its ultra-slim case profiles (often under 7mm thickness), minimalist Scandinavian dials, and flexible stainless steel Milanese mesh bracelets. While beautifully styled, these slim watches require specific handling techniques during battery replacement, crystal replacement, and mesh bracelet adjustment.</p>
        
        <h2>1. Opening the Ultra-Thin Snap-On Caseback</h2>
        <p>Most Skagen quartz watches feature press-fit snap casebacks without a screw mechanism. Because the cases are ultra-thin, prying with excessive force can bend the bezel or crush the movement spacer ring:</p>
        <ul>
            <li>Locate the tiny caseback pry notch, typically positioned between the 11 and 1 o'clock lugs.</li>
            <li>Use an ultra-thin, beveled case opener knife wrapped in a single layer of plastic wrap to prevent scratching the polished steel.</li>
            <li>Apply steady, gentle rotational leverage rather than raw upward force until the back pops free.</li>
        </ul>

        <h2>2. Identifying & Replacing the Correct Low-Profile Battery</h2>
        <p>Skagen utilizes Japanese Miyota or Seiko/Epson slim quartz movements. Common battery cells include the <strong>SR621SW (364)</strong> and <strong>SR626SW (377)</strong> silver oxide cells. Always use non-conductive plastic tweezers to insert the fresh cell; metal tweezers will bridge the positive and negative terminals, instantly draining the battery.</p>

        <h2>3. Closing the Caseback (The Critical Press Technique)</h2>
        <p>Many Skagen owners crack the mineral crystal when attempting to snap the caseback closed using thumb pressure. Due to the ultra-thin bezel, <strong>you must use a screw-down watch press with cupped nylon dies</strong>. Select a bottom die that supports only the outer metal rim of the case without touching the crystal, align the caseback notch with the winding stem, and apply smooth screw pressure until it clicks into place.</p>

        <h2>4. Adjusting the Milanese Mesh Clasp</h2>
        <p>Skagen's signature mesh bracelet uses a sliding friction clasp. To adjust: insert a small flat-blade screwdriver into the rectangular notch of the clasp clamp and lift upward. Slide the clasp along the mesh track to your wrist size, ensuring the inner crossbar aligns with one of the subtle groove indentations on the underside of the mesh before pressing the clamp closed firmly.</p>
        """
    elif topic == 'buying_guide':
        content = """
        <p>Navigating the global watch market in 2026 can be overwhelming. With thousands of brands spanning from $50 Chinese automatic homages to $50,000 Swiss haute horlogerie, understanding what truly creates lasting value is essential for making smart buying decisions. Here are the 5 core pillars of watch quality every collector must evaluate.</p>
        
        <h2>Pillar 1: Movement Calibre (The Mechanical Heart)</h2>
        <p>The movement dictates daily reliability and maintenance costs:</p>
        <ul>
            <li><strong>Workhorse Automatics (Seiko NH35, Miyota 8215/9015):</strong> Unbeatable reliability, hacking seconds, 40+ hour power reserves, and easily serviced or replaced anywhere in the world for under $50.</li>
            <li><strong>Swiss Mechanicals (ETA 2824-2, Sellita SW200-1):</strong> Smoother 28,800 bph beat rate (8 ticks per second), chronometer-grade regulation capability, found in watches from $500 to $3,000.</li>
            <li><strong>Meca-Quartz & Column-Wheel Chronographs (Seiko VK63, Seagull ST1901):</strong> Deliver mechanical chronograph sweeping hands with quartz accuracy or true vintage mechanical column-wheel action for under $180.</li>
        </ul>

        <h2>Pillar 2: Crystal Lens (Sapphire vs Mineral vs Acrylic)</h2>
        <p>Never pay more than $100 for a watch featuring standard mineral glass. <strong>Synthetic Sapphire Crystal</strong> rates 9 on the Mohs hardness scale (second only to diamond) and is virtually immune to everyday scratches from door frames, keys, and desk wear. Ensure the sapphire crystal has an anti-reflective (AR) coating on the underside to eliminate dial glare.</p>

        <h2>Pillar 3: Case Construction & Steel Grade</h2>
        <p>Demand <strong>Solid 316L Marine-Grade Stainless Steel</strong>. Avoid cheap "alloy" or zinc-plated cases that pit and corrode from skin perspiration over time. Check the lugs for crisp transitional chamfers and uniform brushed finishes, which indicate precise CNC machining rather than stamped sheet metal.</p>

        <h2>Pillar 4: Bracelet Quality (Milled vs Stamped Clasps)</h2>
        <p>A luxury watch's tactile feel is largely defined by its bracelet. Look for <strong>Solid End Links (SEL)</strong> that fit flush against the watch case without rattling, screw-pin link adjustments instead of push-pins, and a CNC-milled clasp with on-the-fly micro-adjustments rather than cheap stamped tin.</p>

        <h2>Pillar 5: Real-World Water Resistance Standards</h2>
        <p>Watch water resistance ratings are often misunderstood:</p>
        <ul>
            <li><strong>30m (3 Bar):</strong> Splash resistant only. Safe for rain and hand-washing; never swim with it.</li>
            <li><strong>50m (5 Bar):</strong> Suitable for brief shallow surface swimming, but avoid diving or high water pressure.</li>
            <li><strong>100m – 200m (10 – 20 Bar) with Screw-Down Crown:</strong> The true tool watch standard. Safe for swimming, snorkeling, water sports, and recreational diving.</li>
        </ul>
        """
    elif topic == 'deal_hunting':
        content = """
        <p>Retail watch prices (MSRP) are largely marketing fictions. Between distributor clearances, seasonal sale cycles, and direct factory hubs, informed collectors rarely pay retail price. Here is our strategic playbook for uncovering the internet's absolute best watch deals in 2026.</p>
        
        <h2>Channel 1: AliExpress Choice Days (The Secret Homage Goldmine)</h2>
        <p>For high-specification mechanical homage watches (San Martin, Pagani Design, Sugess, Addiesdive, Baltany), buying direct through official AliExpress stores during <strong>Choice Day sales (the 1st to 4th of every month)</strong> or seasonal festivals (11.11 Singles Day and Anniversary Sales in March) unlocks discounts of 40% to 75%. Combine store coupons with platform coupon codes and coin discounts to secure Seiko NH35 sapphire divers for as low as $65.</p>

        <h2>Channel 2: The Gray Market (Jomashop, Chrono24, Ashford)</h2>
        <p>The "gray market" consists of authentic brand-new watches purchased from authorized dealers who need to liquidate excess inventory without violating manufacturer minimum advertised price (MAP) policies. Sites like Jomashop offer 30% to 60% discounts on brands like Tissot, Hamilton, Citizen, and Seiko. The tradeoff: the watch comes with the gray market dealer's warranty rather than the manufacturer's factory warranty.</p>

        <h2>Channel 3: Amazon Prime Watch Outlets & Lightning Deals</h2>
        <p>Amazon remains ideal for mainstream brands (Casio, Seiko, Citizen Eco-Drive, Bulova, Fossil) where fast domestic shipping, easy 30-day no-questions-asked returns, and Amazon Prime customer service outweigh saving an extra $10 on international platforms. Bookmark Amazon Watch Outlet pages and track price drops during Prime Day and Black Friday.</p>

        <h2>Channel 4: Pre-Owned Platforms & Authenticity Guarantees</h2>
        <p>For luxury timepieces (Rolex, Omega, Breitling, Tudor), platforms with physical inspection guarantees (eBay Authenticity Guarantee, Chrono24 Certified) protect buyers against counterfeit parts and stolen goods. Always verify the seller's feedback score, check for original box and warranty papers (full set), and request timegrapher accuracy readings before wiring funds.</p>
        """
    elif topic == 'running_watches':
        content = """
        <p>Whether training for a 5K fun run or a full 42km marathon, a dedicated running watch delivers biometric telemetry, pace consistency, and interval timing that smartphones simply cannot match on the run. Here is our vetted collector review of the 10 best women's running and fitness watches for 2026.</p>
        
        <h2>1. Garmin Forerunner 265 (The Overall Champion)</h2>
        <p>With a brilliant AMOLED touchscreen, multi-band GPS tracking, heart rate variability (HRV) status, and comprehensive recovery metrics in a compact 42mm housing, the Forerunner 265 is the benchmark runner's tool.</p>

        <h2>2. Casio Baby-G BGD-565 (The Indestructible Classic)</h2>
        <p>For runners who demand zero distractions, no daily charging, and bulletproof shock resistance, the compact Baby-G square provides split-second stopwatch timing, 100m water resistance, and 3-year battery life in an ultra-lightweight resin case.</p>

        <h2>3. Coros Pace 3 (The Featherweight Value King)</h2>
        <p>Weighing just 30 grams with a breathable nylon strap, the Pace 3 provides dual-frequency satellite tracking and an astonishing 38 hours of continuous standard GPS workout battery life at an accessible price point.</p>

        <h2>4. Apple Watch Series 10 (Best Smartwatch Integration)</h2>
        <p>Featuring a redesigned ultra-thin case, wide-angle OLED display, ECG monitoring, and direct cellular connectivity, it seamlessly bridges everyday luxury smartwatch utility with fitness tracking.</p>

        <h2>5. Polar Pacer Pro (Advanced Running Power Metrics)</h2>
        <p>Designed specifically for dedicated track and road runners, the Pacer Pro calculates wrist-based running power in watts and offers specialized hill split tracking.</p>

        <h2>6. Garmin Lily 2 (Jewelry Aesthetics with Health Intelligence)</h2>
        <p>Combining an Italian leather or woven fabric band with a patterned display that illuminates on wrist flick, the Lily 2 measures sleep quality, hydration, and steps without looking like a bulky sports gadget.</p>

        <h2>7. Suunto Race S (Compact Mountain & Trail Precision)</h2>
        <p>Equipped with free offline topographic trail maps, sapphire crystal, and robust barometric altitude readings, the Race S is engineered for rugged trail runners.</p>

        <h2>8. Fitbit Charge 6 (Slim Profile Fitness Tracker)</h2>
        <p>For runners who wear an analog luxury watch on one wrist and want discreet fitness metrics on the other, the Charge 6 delivers Google Maps integration and heart rate tracking in a low-profile band.</p>

        <h2>9. Timex Ironman Classic 30 (The Nostalgic Workhorse)</h2>
        <p>Introduced in 1986 and continuously refined, the Ironman Classic 30 features the legendary Indiglo night-light, 30-lap memory recall, and 100m water resistance for under $45.</p>

        <h2>10. Amazfit Active (High-Value AMOLED Tracker)</h2>
        <p>Delivering an aluminum alloy bezel, 14-day battery life, and AI-driven training guidance, the Amazfit Active brings premium running metrics within budget territory.</p>
        """
    elif topic == 'womens_luxury':
        content = """
        <p>Women's luxury horology has evolved far beyond simply setting diamonds onto miniature cases. Today, discerning female collectors demand mechanical excellence, historical pedigree, versatile wrist ergonomics, and timeless design that transcends fleeting fashion cycles. Here is our master collector ranking of the top 10 luxury watches for women in 2026.</p>
        
        <h2>1. Cartier Tank Française (The Architectural Icon)</h2>
        <p>First created in 1917 and revitalized with modern beveled bracelet links, the Tank's clean rectangular lines, Roman numerals, blued steel sword hands, and sapphire cabochon crown remain the ultimate expression of understated Parisian chic.</p>

        <h2>2. Rolex Datejust 31 (The Benchmark of Daily Luxury)</h2>
        <p>Featuring the fluted 18k gold bezel, iconic Jubilee bracelet, and automatic calibre 2236 with Syloxi silicon hairspring, the Datejust 31 delivers 100m waterproof durability with timeless heirloom prestige.</p>

        <h2>3. Jaeger-LeCoultre Reverso Classic Duetto (Art Deco Ingenuity)</h2>
        <p>Originally designed in 1931 for polo players to protect their watch glass, the reversible case flips smoothly to reveal a second evening dial powered by a single hand-wound mechanical movement.</p>

        <h2>4. Omega Constellation Manhattan (The Star of Precision)</h2>
        <p>Instantly recognizable by its four signature "claws" gripping the bezel and integrated horizontal-link bracelet, the Constellation combines Master Chronometer accuracy with delicate dial artistry.</p>

        <h2>5. Chanel J12 (The High-Tech Ceramic Revolution)</h2>
        <p>Launched in 2000, the J12 transformed scratch-resistant glossy black and white ceramic into high-fashion horology, now powered by the manufacture automatic calibre 12.1.</p>

        <h2>6. Chopard Happy Sport (Diamonds in Motion)</h2>
        <p>Featuring free-floating diamonds that dance between two layers of sapphire crystal above the dial, the Happy Sport balances playful luxury with fine Swiss craftsmanship.</p>

        <h2>7. Patek Philippe Twenty~4 (Timeless Feminine Glamour)</h2>
        <p>Designed for the active modern woman, the Twenty~4 combines an articulated cambered bracelet with diamond markers and flawless Geneva finishing.</p>

        <h2>8. Bvlgari Serpenti Tubogas (Haute Joaillerie Coil)</h2>
        <p>Wrapping around the forearm in flexible gold and steel coils like a mythical serpent, the Serpenti is equal parts luxury sculpture and fine Swiss timepiece.</p>

        <h2>9. Audemars Piguet Royal Oak Frosted Gold (High-Impact Artistry)</h2>
        <p>Created using ancient Florentine hammer-beating techniques that impart a sparkling diamond-dust texture onto solid 18k gold, it represents the pinnacle of modern sports luxury.</p>

        <h2>10. Longines DolceVita (Accessible Classicism)</h2>
        <p>Embodying the Italian phrase <em>la dolce vita</em>, this elegant rectangular timepiece offers classic Art Deco proportions and Swiss heritage at a remarkably accessible luxury price point.</p>
        """
    elif topic == 'holiday_guide':
        content = """
        <p>Finding the perfect watch as a holiday gift demands balancing personal taste, mechanical pedigree, and genuine fair-market value. Whether you are shopping for a seasoned collector, an aspiring watchmaker, or someone looking for an elegant everyday luxury companion, our 2026 Holiday Gift Guide highlights the top timepieces across every budget category.</p>
        
        <h2>Category 1: Best Mechanical Homage Gifts Under $150</h2>
        <p>For enthusiasts who appreciate luxury design without the prohibitive Swiss price tag, modern AliExpress Choice homage watches deliver jaw-dropping value:</p>
        <ul>
            <li><strong>San Martin SN017-G Submariner Homage ($130 - $160):</strong> Machined from solid 316L stainless steel with a scratch-resistant sapphire crystal and the bulletproof automatic Seiko NH35 movement. Features ceramic bezel inserts and a fully milled clasp.</li>
            <li><strong>Pagani Design PD-1701 Moonwatch Homage ($75 - $95):</strong> Powered by the Seiko VK63 meca-quartz movement, offering mechanical stopwatch flyback action with quartz accuracy and classic Apollo 11 chronograph styling.</li>
            <li><strong>Steeldive SD1970 "Captain Willard" Diver ($85 - $110):</strong> Celebrated for phenomenal Swiss BGW9/C3 luminescence, 200m water resistance, and retro 1970s cushion-case styling.</li>
        </ul>

        <h2>Category 2: Iconic Heritage Classics Under $500</h2>
        <p>For timeless gifts with rich brand heritage:</p>
        <ul>
            <li><strong>Seiko 5 Sports SRPD Series ($220 - $295):</strong> The definitive automatic gateway watch, offering exhibition casebacks, day-date displays, and hundreds of custom modding options.</li>
            <li><strong>Citizen Promaster Eco-Drive Diver ($250 - $350):</strong> Solar-powered, ISO-certified for diving, and never requires a battery change.</li>
            <li><strong>Bulova Lunar Pilot Chronograph ($375 - $495):</strong> Powered by Bulova's proprietary 262kHz high-frequency quartz movement with historical lunar surface pedigree.</li>
        </ul>

        <h2>Category 3: Meaningful Keepsakes & Vintage Pocket Watches Under $60</h2>
        <p>For collectors, reenactors, or formal wedding gifts, vintage full-hunter pocket watches with matching vest chains deliver heirloom nostalgia in ornate presentation gift boxes.</p>
        """
    else:
        content = f"""
        <p>Understanding watch mechanics, maintenance standards, and genuine market values separates casual buyers from astute collectors. This guide explores essential principles, hands-on techniques, and buying strategies for {title}.</p>
        <h2>Essential Fundamentals</h2>
        <p>Whether examining mechanical movements, quartz modules, or case materials like 316L marine stainless steel and sapphire glass, quality construction always reveals itself in the details: tight tolerances, solid end links, clean pad printing, and reliable water-resistant gaskets.</p>
        <h2>Smart Deal Sourcing</h2>
        <p>Before purchasing any timepiece or replacement part, always compare authorized dealer pricing, gray market platforms, and verified direct manufacturer outlets (such as AliExpress Choice stores for mechanical homage pieces) to secure fair pricing without sacrificing quality.</p>
        """

    schema = f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{html.escape(title)}",
      "image": "{DEFAULT_OG_IMAGE}",
      "description": "Comprehensive horology guide and collector advice for {html.escape(title)}.",
      "author": {{
        "@type": "Organization",
        "name": "BestWatchDeals Editorial Board"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "BestWatchDeals",
        "logo": {{
          "@type": "ImageObject",
          "url": "https://bestwatchdeals.com/logo.png"
        }}
      }},
      "datePublished": "{year}-01-01",
      "dateModified": "2026-10-17"
    }}
    </script>
    """

    body = f"""
    <div class="breadcrumbs">
        <a href="/">Home</a>
        <span>/</span>
        <a href="/category/articles-and-information/">Guides</a>
        <span>/</span>
        <span>{html.escape(title)}</span>
    </div>

    <article class="card">
        <div class="badge-pill">Horology Master Guide</div>
        <h1>{html.escape(title)}</h1>
        <div class="post-meta">
            <span>By <strong>Senior Horology Editor</strong></span>
            <span>•</span>
            <span>Updated: <strong>October 2026</strong></span>
            <span>•</span>
            <span>Archive Reference: <strong>Since {year}</strong></span>
        </div>

        <div class="content-body" style="font-size: 1rem;">
            {content}
        </div>

        <div class="final-cta" style="margin-top: 2rem;">
            <h3>Explore Today's Handpicked Timepiece Deals</h3>
            <p>From workhorse automatic Seiko-powered divers to classic dress chronographs, discover verified direct deals updated daily.</p>
            <a href="https://s.click.aliexpress.com/e/_c45LWcBP" target="_blank" rel="nofollow sponsored" class="btn-primary" style="display:inline-block; padding: 0.85rem 2rem;">
                ⚡ Browse Verified Choice Deals
            </a>
        </div>
    </article>
    """

    return render_layout(
        title=f"{title} | BestWatchDeals",
        description=f"Expert horology guide: {title}. Professional tips, maintenance advice, historical context, and collector recommendations.",
        canonical_url=url,
        body_html=body,
        schema_ld=schema
    )

def build_hub_page(item, all_reviews, all_guides, all_hubs):
    title = item['title_2026']
    hub_name = item.get('hub_name', 'Watch Deals')
    url = item['url']
    path = item['path']

    # Determine tailored editorial content based on hub name
    hub_lower = (hub_name + " " + path).lower()
    
    if "rolex" in hub_lower:
        editorial_p = "Rolex stands at the summit of global horological recognition, with icons like the Submariner, GMT-Master II, and Datejust commanding massive waitlists and secondary market premiums. For collectors seeking authentic everyday wear, we analyze genuine heritage care protocols alongside the booming market of premium mechanical homages (crafted with solid 316L marine steel, synthetic sapphire crystals, and Seiko NH35 calibres) that deliver 95% of the aesthetic pleasure without the five-figure investment."
        sourcing_tip = "When exploring Rolex-inspired homages, brands like San Martin and Sugess offer ceramic bezels, 200m water resistance, and glide-lock style milled clasps that rival luxury finishing."
        deal_query = "san+martin+submariner+nh35"
        sort_archetype = "diver"
    elif "omega" in hub_lower:
        editorial_p = "From the lunar legacy of the Speedmaster Professional Moonwatch to the maritime durability of the Seamaster Diver 300M, Omega represents technical precision and Co-Axial innovation. Our collector reviews evaluate heritage reference values, professional chronograph maintenance, and top-tier accessible alternatives that celebrate Omega's iconic design language."
        sourcing_tip = "Speedmaster homages featuring the Seagull ST1901 column-wheel mechanical movement or Seiko VK63 meca-quartz deliver authentic tactile chronograph action at a fraction of luxury costs."
        deal_query = "pagani+design+speedmaster+chronograph"
        sort_archetype = "chronograph"
    elif "breitling" in hub_lower:
        editorial_p = "Breitling has served as the aviator's trusted instrument for nearly a century. Celebrated for complex circular slide-rule bezels on the Navitimer and rugged chronographs like the Chronomat and Superocean, Breitling's aviation DNA is unmistakable. We evaluate pre-owned market values and high-accuracy aviation timepieces built for serious wrist presence."
        sourcing_tip = "Look for aviation chronographs with high-contrast reverse-panda dials, anti-reflective domed sapphire crystals, and bidirectional slide-rule bezels for true pilot aesthetics."
        deal_query = "pilot+chronograph+watch+navitimer"
        sort_archetype = "chronograph"
    elif "seiko" in hub_lower:
        editorial_p = "Seiko revolutionized global watchmaking with the Quartz Crisis and remains the undisputed benchmark of accessible mechanical horology. Beyond Seiko's legendary Prospex diver line, their TMI NH35 automatic and NH34 GMT movements now power the world's most acclaimed independent microbrands, offering bulletproof reliability and hacking seconds for under $150."
        sourcing_tip = "Seiko NH35-powered watches from verified AliExpress Choice stores offer the greatest value-per-dollar in modern horology, featuring solid stainless steel and sapphire glass direct from manufacturer hubs."
        deal_query = "seiko+nh35+automatic+diver"
        sort_archetype = "diver"
    elif "tag heuer" in hub_lower:
        editorial_p = "Deeply rooted in motorsports and competitive racing, Tag Heuer's Carrera, Monaco, and Aquaracer represent dynamic athletic luxury. Our team evaluates genuine pre-owned value points, precision sports chronographs, and robust water-resistant watches built for high-speed lifestyles."
        sourcing_tip = "Motorsport-inspired chronographs with ceramic tachymeter bezels and textured racing dials provide exceptional wrist ergonomics and timing versatility."
        deal_query = "racing+chronograph+watch+quartz"
        sort_archetype = "chronograph"
    elif "audemars piguet" in hub_lower:
        editorial_p = "Audemars Piguet redefined luxury sports horology in 1972 with Gerald Genta's octagonal Royal Oak, pioneering high-end stainless steel with integrated bracelets. We analyze the geometric bevels, tapisserie dial textures, and contemporary integrated-bracelet alternatives that capture the iconic luxury steel aesthetic at sensible pricing."
        sourcing_tip = "Modern integrated-bracelet homage watches with brushed octagonal bezels and exposed hexagonal screws provide striking architectural wrist appeal."
        deal_query = "royal+oak+homage+automatic"
        sort_archetype = "fashion_dress"
    elif "bulova" in hub_lower:
        editorial_p = "Bulova holds an illustrious place in American horological history, from pioneering radio advertising to the historic Accutron electronic tuning-fork movements and the Lunar Pilot chronograph. We examine vintage Bulova calibres, restoration teardowns, and modern high-frequency quartz releases."
        sourcing_tip = "Vintage Bulova hand-winding calibres like the 6BL offer fantastic platforms for amateur watchmakers to learn delicate disassembly and movement servicing."
        deal_query = "bulova+watches+mens+womens"
        sort_archetype = "fashion_dress"
    elif "invicta" in hub_lower:
        editorial_p = "Invicta is renowned for its bold styling, oversized case silhouettes, and accessible automatic dive watches like the Pro Diver series. Powered by reliable Seiko NH35 automatic calibres, Invicta offers one of the most accessible entry gates into mechanical watch collecting."
        sourcing_tip = "The Invicta Pro Diver 8926OB remains an iconic budget diver benchmark, frequently discounted below $75 while offering genuine 200m water resistance."
        deal_query = "invicta+pro+diver+automatic"
        sort_archetype = "diver"
    elif "movado" in hub_lower:
        editorial_p = "Movado's Museum Watch—designed in 1947 by Bauhaus-influenced artist Nathan George Horwitt—is celebrated in modern art museums worldwide. Featuring a minimalist dial with a single gold dot at 12 o'clock representing the sun at high noon, it remains a timeless design classic."
        sourcing_tip = "Minimalist dial timepieces prioritize sleek case profiles and ultra-reliable Swiss or Japanese quartz modules for understated elegance."
        deal_query = "minimalist+museum+watch"
        sort_archetype = "fashion_dress"
    elif "mechanical" in hub_lower:
        editorial_p = "Mechanical and automatic timepieces represent miniature kinetic engineering powered solely by coiled mainsprings, gear trains, and the natural motion of your wrist. Our buying guide compares essential calibres—from workhorse Seiko NH35 and Miyota movements to Seagull column-wheel chronographs—helping you choose the most reliable automatic watch for your budget."
        sourcing_tip = "Always check for hacking seconds (the second hand stops when pulling the crown) and hand-winding capability when investing in modern automatic movements."
        deal_query = "automatic+mechanical+watch+nh35"
        sort_archetype = "diver"
    elif any(k in hub_lower for k in ["novelty", "pocket"]):
        editorial_p = "Novelty timepieces, steampunk accessories, and antique pocket watches blend historical romance with unique personal expression. From ornate full-hunter pocket watches with matching vest chains to skeletonized mechanical displays, explore distinctive timepieces ideal for collectors, gifts, and formal occasions."
        sourcing_tip = "Look for pocket watches with included vest curb chains and protective spring-loaded hunter covers to protect the crystal from accidental pocket scratches."
        deal_query = "pocket+watch+vintage+mechanical"
        sort_archetype = "pocket_watch"
    elif any(k in hub_lower for k in ["boys", "girls"]):
        editorial_p = "Selecting timepieces for young collectors demands impact resistance, reliable water protection, clear legible numerals, and skin-friendly silicone or resin bands. We evaluate durable digital watches and beginner analog models designed to withstand daily school, sports, and outdoor activities."
        sourcing_tip = "Prioritize watches with at least 50m to 100m water resistance and shock-absorbing resin bumpers to survive playground play and swimming."
        deal_query = "kids+digital+sport+watch+waterproof"
        sort_archetype = "digital_sport"
    elif any(k in hub_lower for k in ["holiday", "deal", "sales", "shop online"]):
        editorial_p = "Savvy watch collectors know that timing purchases around seasonal distributor promotions and AliExpress Choice Day events can unlock discounts of up to 80% off retail MSRP. We continually scan verified distributors, factory outlets, and authorized storefronts to curate the web's most trustworthy deals."
        sourcing_tip = "Combine distributor store coupons with platform-wide flash codes during major sale cycles to secure premium sapphire and automatic watches at historic low prices."
        deal_query = "watch+flash+deals+choice"
        sort_archetype = "fashion_dress"
    else:
        editorial_p = f"Welcome to the dedicated 2026 collector resource for <strong>{html.escape(hub_name)}</strong>. Whether you are tracking pre-owned secondary market valuations, researching movement specifications, or looking for high-value mechanical automatic alternatives powered by Seiko NH35 and Seagull calibres, our team tests and curates the best verified options."
        sourcing_tip = "Compare authorized dealer pricing against verified direct manufacturer stores on AliExpress Choice to secure sapphire crystal and solid steel construction without retail markups."
        deal_query = f"{hub_name.lower().replace(' ', '+')}+watches"
        sort_archetype = "fashion_dress"

    # Prioritize matched reviews
    matched_reviews = []
    hub_keywords = [w for w in hub_name.lower().split() if len(w) > 2]
    
    # 1. Exact brand or title matches
    for r in all_reviews:
        r_text = (r['title_2026'] + " " + r['brand'] + " " + r['path']).lower()
        if any(kw in r_text for kw in hub_keywords):
            matched_reviews.append(r)

    # 2. Archetype matches
    for r in all_reviews:
        if r not in matched_reviews and r.get('archetype') == sort_archetype:
            matched_reviews.append(r)
        if len(matched_reviews) >= 8:
            break

    # 3. Fallback general top reviews
    if len(matched_reviews) < 6:
        for r in all_reviews:
            if r not in matched_reviews:
                matched_reviews.append(r)
            if len(matched_reviews) >= 8:
                break

    # Related sibling hubs
    sibling_hubs = [h for h in all_hubs if h['path'] != path][:6]

    cards_html = []
    for r in matched_reviews[:12]:
        badge = r.get('archetype', 'Deal').replace('_', ' ').title()
        cards_html.append(f"""
        <div class="grid-item-card">
            <div>
                <div class="grid-badge">{badge} • {r['brand']}</div>
                <h3 class="grid-title"><a href="{r['path']}">{html.escape(r['title_2026'])}</a></h3>
                <p class="grid-desc">Hands-on collector assessment: movement calibre, finishing tolerances, and verified direct deal pricing.</p>
            </div>
            <div class="grid-footer">
                <span>Updated 2026</span>
                <a href="{r['path']}" class="grid-link">Read Review &rarr;</a>
            </div>
        </div>
        """)

    schema = f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "{html.escape(title)}",
      "image": "{DEFAULT_OG_IMAGE}",
      "description": "Curated collection and 2026 buying guide for {html.escape(hub_name)} watches and deals.",
      "url": "{url}"
    }}
    </script>
    """

    body = f"""
    <div class="breadcrumbs">
        <a href="/">Home</a>
        <span>/</span>
        <a href="/category/watch-deals/">Categories</a>
        <span>/</span>
        <span>{html.escape(hub_name)}</span>
    </div>

    <div class="card">
        <div class="badge-pill">2026 Curated Collector Hub</div>
        <h1>{html.escape(title)}</h1>
        <div class="post-meta">
            <span>Curated by <strong>BestWatchDeals Editorial Board</strong></span>
            <span>•</span>
            <span>Updated: <strong>October 2026</strong></span>
            <span>•</span>
            <span>Featured: <strong>{len(matched_reviews)} Active Benchmarks</strong></span>
        </div>

        <div class="content-body">
            <p>{editorial_p}</p>
        </div>

        <div class="verdict-box" style="margin: 1.5rem 0;">
            <div>
                <span class="verdict-tag">2026 Sourcing Recommendation</span>
                <div class="verdict-title">Smart Buying for {html.escape(hub_name)}</div>
                <div class="verdict-text">{sourcing_tip}</div>
            </div>
            <div class="cta-group">
                <a href="https://s.click.aliexpress.com/e/_c45LWcBP?k={deal_query}" target="_blank" rel="nofollow sponsored" class="btn-primary">
                    ⚡ View Live {html.escape(hub_name)} Deals
                </a>
            </div>
        </div>

        <h2>Featured Reviews & Buying Benchmarks</h2>
        <div class="items-grid">
            {''.join(cards_html)}
        </div>

        <h2>Related Brand & Category Hubs</h2>
        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem;">
            {''.join(f'<a href="{h["path"]}" style="background:#f1f5f9; padding:0.4rem 0.8rem; border-radius:6px; font-size:0.8rem; font-weight:600; color:#334155; border:1px solid #e2e8f0;">{h["title_2026"].split(" Watches")[0]} &rarr;</a>' for h in sibling_hubs)}
        </div>
    </div>
    """

    return render_layout(
        title=f"{title} | BestWatchDeals",
        description=f"Explore top-rated {hub_name} watches, collector benchmarks, mechanical movement comparisons, and verified deals for 2026.",
        canonical_url=url,
        body_html=body,
        schema_ld=schema
    )

def build_home_page(all_reviews, all_guides, all_hubs):
    url = "https://bestwatchdeals.com/"
    title = "Best Watch Deals & Reviews (2026): Luxury Timepieces & Verified Homages"
    description = "The premier independent watch collector portal. Authentic hands-on reviews, mechanical movement benchmarks, and verified AliExpress & Amazon watch deals."

    # Grid of top reviews
    review_cards = []
    for r in all_reviews[:12]:
        badge = r.get('archetype', 'Deal').replace('_', ' ').title()
        review_cards.append(f"""
        <div class="grid-item-card">
            <div>
                <div class="grid-badge">{badge} • {r['brand']}</div>
                <h3 class="grid-title"><a href="{r['path']}">{html.escape(r['title_2026'])}</a></h3>
                <p class="grid-desc">In-depth hands-on test: movement calibre, finishing tolerances, crystal durability, and live discounts.</p>
            </div>
            <div class="grid-footer">
                <span>Archive since {r.get('archived_year', '2013')}</span>
                <a href="{r['path']}" class="grid-link">Read Review &rarr;</a>
            </div>
        </div>
        """)

    # Grid of guides
    guide_cards = []
    for g in all_guides[:6]:
        guide_cards.append(f"""
        <div class="grid-item-card" style="border-left: 3px solid var(--brand-gold);">
            <div>
                <div class="grid-badge" style="color:var(--brand-gold-dark);">Horology Master Guide</div>
                <h3 class="grid-title"><a href="{g['path']}">{html.escape(g['title_2026'])}</a></h3>
                <p class="grid-desc">Essential watchmaker techniques, maintenance schedules, and collector buying strategies.</p>
            </div>
            <div class="grid-footer">
                <span>Free Guide</span>
                <a href="{g['path']}" class="grid-link">Read Guide &rarr;</a>
            </div>
        </div>
        """)

    schema = f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "BestWatchDeals",
      "url": "https://bestwatchdeals.com/",
      "image": "{DEFAULT_OG_IMAGE}",
      "description": "Independent horology reviews, watch maintenance manuals, and verified mechanical homage deal benchmarks.",
      "potentialAction": {{
        "@type": "SearchAction",
        "target": "https://bestwatchdeals.com/category/watch-deals/?q={{search_term_string}}",
        "query-input": "required name=search_term_string"
      }}
    }}
    </script>
    """

    body = f"""
    <!-- Hero Section -->
    <div class="card" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #ffffff; border: none; padding: 3rem 2rem; margin-bottom: 2.5rem;">
        <div class="badge-pill" style="background: rgba(16, 185, 129, 0.15); color: #34d399; border-color: #059669;">
            Established 2012 • 14 Years of Watch Authority
        </div>
        <h1 style="color: #ffffff; font-size: 2.4rem; max-width: 800px; margin-bottom: 1rem;">
            Honest Horology Reviews & Verified Mechanical Watch Deals
        </h1>
        <p style="color: #cbd5e1; font-size: 1.05rem; max-width: 650px; line-height: 1.7; margin-bottom: 2rem;">
            We test, disassemble, and review luxury timepieces, heritage classics, and high-value mechanical automatic homage watches—giving you the unvarnished truth on movements, finishing, and real-world deals.
        </p>
        <div style="display: flex; flex-wrap: wrap; gap: 1rem;">
            <a href="https://s.click.aliexpress.com/e/_c45LWcBP" target="_blank" rel="nofollow sponsored" class="btn-primary" style="padding: 0.85rem 1.75rem; font-size: 0.95rem;">
                ⚡ Explore Today's Top AliExpress Deals
            </a>
            <a href="/category/watch-deals/" class="btn-secondary" style="padding: 0.85rem 1.75rem; font-size: 0.95rem;">
                Browse All 150+ Reviews
            </a>
        </div>
    </div>

    <!-- Brand Silos Bar -->
    <div style="margin-bottom: 2.5rem;">
        <h2 style="margin-top: 0; margin-bottom: 1rem; font-size: 1.3rem;">Popular Brand Hubs & Silos</h2>
        <div style="display: flex; flex-wrap: wrap; gap: 0.6rem;">
            <a href="/watch-brands/rolex-watches/" style="background:#ffffff; border:1px solid #e2e8f0; padding:0.6rem 1.1rem; border-radius:8px; font-size:0.85rem; font-weight:700; color:#1e293b; box-shadow:0 1px 3px rgba(0,0,0,0.03);">Rolex Deals & Homages</a>
            <a href="/watch-brands/omega-watches/" style="background:#ffffff; border:1px solid #e2e8f0; padding:0.6rem 1.1rem; border-radius:8px; font-size:0.85rem; font-weight:700; color:#1e293b; box-shadow:0 1px 3px rgba(0,0,0,0.03);">Omega Speedmaster & Seamaster</a>
            <a href="/tag/seiko/" style="background:#ffffff; border:1px solid #e2e8f0; padding:0.6rem 1.1rem; border-radius:8px; font-size:0.85rem; font-weight:700; color:#1e293b; box-shadow:0 1px 3px rgba(0,0,0,0.03);">Seiko NH35 & Diver Deals</a>
            <a href="/watch-brands/breitling-watches-2/" style="background:#ffffff; border:1px solid #e2e8f0; padding:0.6rem 1.1rem; border-radius:8px; font-size:0.85rem; font-weight:700; color:#1e293b; box-shadow:0 1px 3px rgba(0,0,0,0.03);">Breitling Aviation Timepieces</a>
            <a href="/tag/tag-heuer/" style="background:#ffffff; border:1px solid #e2e8f0; padding:0.6rem 1.1rem; border-radius:8px; font-size:0.85rem; font-weight:700; color:#1e293b; box-shadow:0 1px 3px rgba(0,0,0,0.03);">Tag Heuer Chronograph Deals</a>
            <a href="/tag/mechanical-watches/" style="background:#ffffff; border:1px solid #e2e8f0; padding:0.6rem 1.1rem; border-radius:8px; font-size:0.85rem; font-weight:700; color:#1e293b; box-shadow:0 1px 3px rgba(0,0,0,0.03);">All Automatic Watches</a>
        </div>
    </div>

    <!-- Essential Pillar Guides -->
    <div style="margin-bottom: 2.5rem;">
        <h2 style="margin-bottom: 1rem; font-size: 1.3rem;">Master Watchmaking & Buying Guides</h2>
        <div class="items-grid">
            {''.join(guide_cards)}
        </div>
    </div>

    <!-- Latest Hands-On Reviews -->
    <div style="margin-bottom: 2.5rem;">
        <h2 style="margin-bottom: 1rem; font-size: 1.3rem;">Latest Hands-On Reviews & Deal Benchmarks</h2>
        <div class="items-grid">
            {''.join(review_cards)}
        </div>
    </div>
    """

    return render_layout(
        title=title,
        description=description,
        canonical_url=url,
        body_html=body,
        schema_ld=schema
    )

def build_legal_page(item):
    path = item['path']
    is_privacy = "privacy" in path
    title = "Privacy Policy | BestWatchDeals" if is_privacy else "Terms of Use & Affiliate Disclosure | BestWatchDeals"
    
    if is_privacy:
        content = """
        <h1>Privacy Policy</h1>
        <div class="post-meta">Effective Date: October 2026 • BestWatchDeals.com Compliance Team</div>
        <p>BestWatchDeals.com ("we," "our," or "us") respects your individual privacy and is committed to protecting any personal data collected while browsing our horology publication. This Privacy Policy outlines what information is collected, how it is used, how cookies operate, and your legal rights under international privacy frameworks including GDPR and CCPA.</p>
        
        <h2>1. Log Files and Automated Data Collection</h2>
        <p>Like standard web publishers hosted on global content delivery networks, BestWatchDeals.com collects non-identifiable technical log data. This includes internet protocol (IP) addresses, browser type, Internet Service Provider (ISP), date/time stamps, referring/exit pages, and click counts. We use this data exclusively to administer the site, optimize server response times, and analyze macro readership trends.</p>

        <h2>2. Cookies, Web Beacons and Advertising Partners</h2>
        <p>Our website utilizes standard cookies to improve page loading speed and support affiliate tracking functionality. Third-party advertising vendors (such as Google AdSense) and affiliate platforms (including AliExpress Portals and Amazon Associates) may deploy cookies or web beacons when you click an external merchant link to attribute referral commissions.</p>
        <p>You can choose to disable or selectively turn off our cookies or third-party cookies in your individual browser settings at any time. Disabling cookies will not affect your ability to read our reviews or guides.</p>

        <h2>3. Third-Party Websites and External Links</h2>
        <p>BestWatchDeals.com contains outbound hyperlinks to external e-commerce platforms and horology stores. Please be aware that once you leave our domain, we do not have control over other websites. We encourage readers to review the individual privacy policies of any merchant website they visit.</p>

        <h2>4. Data Retention & Contact Rights</h2>
        <p>We do not collect or store unencrypted financial information or payment card numbers. Any inquiries regarding privacy requests or data clarification may be directed to our editorial board at: <strong>editorial@bestwatchdeals.com</strong>.</p>
        """
    else:
        content = """
        <h1>Terms of Use & Affiliate Disclosure</h1>
        <div class="post-meta">Effective Date: October 2026 • BestWatchDeals.com Editorial Standards</div>
        
        <h2>1. FTC & Global Affiliate Relationship Disclosure</h2>
        <p>In accordance with the Federal Trade Commission (FTC) guidelines and international advertising transparency standards, please assume that hyperlinks leading to retail platforms on BestWatchDeals.com are affiliate links. BestWatchDeals.com participates in affiliate advertising programs—including AliExpress Portals, Admitad, and the Amazon Services LLC Associates Program—designed to provide a means for independent publishers to earn advertising fees by linking to commercial merchants.</p>
        <p><strong>Amazon Associates Program Disclosure:</strong> As an Amazon Associate I earn from qualifying purchases.</p>
        <p><strong>What this means for you:</strong> If you click an affiliate link on our site and make a purchase, we may receive a small referral commission directly from the retailer. <strong>This occurs at zero extra cost to you.</strong> The price you pay remains identical whether you utilize our links or navigate directly to the merchant.</p>
        
        <h2>2. Editorial Independence & Unbiased Verdicts</h2>
        <p>Our editorial integrity is not for sale. We do not accept paid compensation in exchange for positive reviews or altered technical ratings. Every watch evaluated on this website is assessed strictly on its horological merits: movement accuracy, finishing tolerances, crystal scratch resistance, water-resistance integrity, and value relative to retail price.</p>
        
        <h2>3. Price Accuracy and Product Availability Disclaimer</h2>
        <p>Horological market pricing, distributor coupons, AliExpress Choice Day promotions, and inventory levels fluctuate rapidly. While our editorial team audits deal pricing on a continuous basis, we cannot guarantee that a listed price will remain available at the exact moment of your purchase. Always verify final pricing, shipping costs, and return policies directly on the merchant's checkout page before completing an order.</p>

        <h2>4. Intellectual Property & Brand Trademarks</h2>
        <p>All brand names, trademarks, and registered logos (such as Rolex, Omega, Seiko, Breitling, Citizen, Bulova, etc.) referenced on this website are the property of their respective trademark owners. Their reference on BestWatchDeals.com is made solely under nominative fair use for descriptive, comparative, and editorial review purposes.</p>
        """

    body = f"""
    <div class="breadcrumbs">
        <a href="/">Home</a>
        <span>/</span>
        <span>Legal</span>
    </div>
    <div class="card content-body">
        {content}
    </div>
    """

    return render_layout(
        title=title,
        description=f"Official legal terms, privacy policies, and affiliate disclosures for BestWatchDeals.com.",
        canonical_url=item['url'],
        body_html=body
    )

def build_404_page():
    url = "https://bestwatchdeals.com/404.html"
    title = "404 - Watch Model or Page Not Found | BestWatchDeals"
    description = "The requested horology page or watch review could not be found. Explore our 2026 watch deals directory and master brand guides."

    body = """
    <div class="card" style="text-align: center; padding: 4rem 1.5rem;">
        <div class="badge-pill" style="background: var(--accent-rose-bg); color: var(--accent-rose); border-color: #fecdd3;">
            Error 404 • Missing Timepiece
        </div>
        <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">Looking for a Specific Watch Deal?</h1>
        <p style="color: #64748b; max-width: 550px; margin: 0 auto 2rem auto; font-size: 1rem;">
            The URL you requested may have been relocated, archived, or updated as part of our 2026 horology catalog refresh. Explore our core hubs below:
        </p>
        <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 0.75rem; margin-bottom: 2.5rem;">
            <a href="/" class="btn-primary" style="padding: 0.75rem 1.5rem;">Return to Homepage</a>
            <a href="/category/watch-deals/" class="btn-secondary" style="padding: 0.75rem 1.5rem;">Browse All Watch Deals</a>
            <a href="/category/articles-and-information/" class="btn-secondary" style="padding: 0.75rem 1.5rem;">Read Buying Guides</a>
        </div>
        
        <h2>Popular Brand Silos</h2>
        <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 0.5rem; max-width: 700px; margin: 1rem auto 0 auto;">
            <a href="/watch-brands/rolex-watches/" style="background:#f1f5f9; padding:0.5rem 1rem; border-radius:6px; font-size:0.85rem; font-weight:600; color:#334155; border:1px solid #e2e8f0;">Rolex Homages & Deals</a>
            <a href="/watch-brands/omega-watches/" style="background:#f1f5f9; padding:0.5rem 1rem; border-radius:6px; font-size:0.85rem; font-weight:600; color:#334155; border:1px solid #e2e8f0;">Omega Speedmaster Guides</a>
            <a href="/tag/seiko/" style="background:#f1f5f9; padding:0.5rem 1rem; border-radius:6px; font-size:0.85rem; font-weight:600; color:#334155; border:1px solid #e2e8f0;">Seiko Automatic NH35 Deals</a>
            <a href="/watch-brands/breitling-watches-2/" style="background:#f1f5f9; padding:0.5rem 1rem; border-radius:6px; font-size:0.85rem; font-weight:600; color:#334155; border:1px solid #e2e8f0;">Breitling Aviation Deals</a>
            <a href="/tag/mechanical-watches/" style="background:#f1f5f9; padding:0.5rem 1rem; border-radius:6px; font-size:0.85rem; font-weight:600; color:#334155; border:1px solid #e2e8f0;">Mechanical & Automatic Watches</a>
        </div>
    </div>
    """

    return render_layout(
        title=title,
        description=description,
        canonical_url=url,
        body_html=body
    )

def create_og_svg():
    # Branded luxury vector social sharing image
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="50%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <linearGradient id="gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#D4AF37"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <circle cx="950" cy="315" r="220" fill="none" stroke="#334155" stroke-width="2" stroke-dasharray="8 8"/>
  <circle cx="950" cy="315" r="180" fill="none" stroke="url(#gold)" stroke-width="4"/>
  <circle cx="950" cy="315" r="8" fill="#D4AF37"/>
  <line x1="950" y1="315" x2="950" y2="200" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <line x1="950" y1="315" x2="1030" y2="315" stroke="#EA580C" stroke-width="3" stroke-linecap="round"/>
  
  <rect x="100" y="100" width="220" height="36" rx="18" fill="rgba(16, 185, 129, 0.2)" stroke="#10B981" stroke-width="1.5"/>
  <text x="210" y="124" fill="#34D399" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" letter-spacing="1">ESTABLISHED 2012</text>
  
  <text x="100" y="220" fill="#FFFFFF" font-family="Arial, sans-serif" font-size="52" font-weight="900" letter-spacing="-1">
    BESTWATCH<tspan fill="#EA580C">DEALS</tspan>
  </text>
  
  <text x="100" y="280" fill="#D4AF37" font-family="Arial, sans-serif" font-size="28" font-weight="bold">
    2026 Master Horology &amp; Homage Deals Guide
  </text>
  
  <text x="100" y="340" fill="#94A3B8" font-family="Arial, sans-serif" font-size="20">
    • Seiko NH35 &amp; Seagull Movement Benchmarks
  </text>
  <text x="100" y="380" fill="#94A3B8" font-family="Arial, sans-serif" font-size="20">
    • Verified AliExpress Choice &amp; Amazon Prime Discounts
  </text>
  <text x="100" y="420" fill="#94A3B8" font-family="Arial, sans-serif" font-size="20">
    • Unbiased Hands-On Watch Reviews &amp; Care Manuals
  </text>
  
  <rect x="100" y="480" width="320" height="50" rx="8" fill="#EA580C"/>
  <text x="260" y="512" fill="#FFFFFF" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle">
    EXPLORE DAILY WATCH DEALS
  </text>
</svg>"""

def create_headers_file():
    # Cloudflare Pages security & caching headers
    return """/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  X-XSS-Protection: 1; mode=block
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/*.html
  Cache-Control: public, max-age=0, must-revalidate

/sitemap.xml
  Cache-Control: public, max-age=86400, must-revalidate
"""

def main():
    print("🚀 Initializing BestWatchDeals Ultra-Forensic Site Engine v3...")
    
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    os.makedirs(DIST_DIR, exist_ok=True)
    assets_dir = os.path.join(DIST_DIR, 'assets')
    os.makedirs(assets_dir, exist_ok=True)
    
    # Write SVG OG Image
    with open(os.path.join(assets_dir, 'og-bestwatchdeals.svg'), 'w', encoding='utf-8') as f:
        f.write(create_og_svg())
    print("✅ Created social asset: assets/og-bestwatchdeals.svg")

    # Write Cloudflare _headers
    with open(os.path.join(DIST_DIR, '_headers'), 'w', encoding='utf-8') as f:
        f.write(create_headers_file())
    print("✅ Created Cloudflare security & caching rules: _headers")
    
    urls = manifest['urls']
    print(f"Total manifest records: {len(urls)}")
    
    reviews = [u for u in urls if u.get('action') == 'REVIEW']
    guides = [u for u in urls if u.get('action') == 'GUIDE']
    hubs = [u for u in urls if u.get('action') == 'HUB']
    legals = [u for u in urls if u.get('action') == 'LEGAL']
    redirs = [u for u in urls if u.get('action') == 'REDIRECT']
    
    print(f"- Reviews to compile: {len(reviews)}")
    print(f"- In-Depth Educational Guides: {len(guides)}")
    print(f"- Brand & Category Hubs: {len(hubs)}")
    print(f"- Legal Compliance Pages: {len(legals)}")
    print(f"- 301 Redirect Rules: {len(redirs)}")
    
    sitemap_entries = ["https://bestwatchdeals.com/"]
    compiled_pages = 0

    # 1. Compile Reviews
    for r in reviews:
        html_out = build_review_page(r)
        clean_path = r['path'].strip('/')
        target_dir = os.path.join(DIST_DIR, clean_path)
        os.makedirs(target_dir, exist_ok=True)
        with open(os.path.join(target_dir, "index.html"), 'w', encoding='utf-8') as f:
            f.write(html_out)
        sitemap_entries.append(r['url'])
        compiled_pages += 1

    # 2. Compile Guides
    for g in guides:
        html_out = build_guide_page(g)
        clean_path = g['path'].strip('/')
        target_dir = os.path.join(DIST_DIR, clean_path)
        os.makedirs(target_dir, exist_ok=True)
        with open(os.path.join(target_dir, "index.html"), 'w', encoding='utf-8') as f:
            f.write(html_out)
        sitemap_entries.append(g['url'])
        compiled_pages += 1

    # 3. Compile Hubs
    for h in hubs:
        html_out = build_hub_page(h, reviews, guides, hubs)
        clean_path = h['path'].strip('/')
        target_dir = os.path.join(DIST_DIR, clean_path)
        os.makedirs(target_dir, exist_ok=True)
        with open(os.path.join(target_dir, "index.html"), 'w', encoding='utf-8') as f:
            f.write(html_out)
        sitemap_entries.append(h['url'])
        compiled_pages += 1

    # 4. Compile Legal Pages
    for l in legals:
        html_out = build_legal_page(l)
        clean_path = l['path'].strip('/')
        target_dir = os.path.join(DIST_DIR, clean_path)
        os.makedirs(target_dir, exist_ok=True)
        with open(os.path.join(target_dir, "index.html"), 'w', encoding='utf-8') as f:
            f.write(html_out)
        sitemap_entries.append(l['url'])
        compiled_pages += 1

    # 5. Compile Flagship Homepage
    home_html = build_home_page(reviews, guides, hubs)
    with open(os.path.join(DIST_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(home_html)
    compiled_pages += 1

    # 6. Compile Custom 404 Page
    page_404 = build_404_page()
    with open(os.path.join(DIST_DIR, "404.html"), 'w', encoding='utf-8') as f:
        f.write(page_404)
    print("✅ Created branded error page: 404.html")

    # 7. Generate Cloudflare _redirects
    redirect_lines = []
    for r in redirs:
        p_from = r['path']
        p_to = r.get('redirect_to', '/category/watch-deals/')
        redirect_lines.append(f"{p_from} {p_to} 301")
        if p_from.endswith('/'):
            redirect_lines.append(f"{p_from.rstrip('/')} {p_to} 301")
    
    with open(os.path.join(DIST_DIR, "_redirects"), 'w', encoding='utf-8') as f:
        f.write("\n".join(redirect_lines) + "\n")

    # 8. Generate robots.txt
    with open(os.path.join(DIST_DIR, "robots.txt"), 'w', encoding='utf-8') as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: https://bestwatchdeals.com/sitemap.xml\n")

    # 9. Generate sitemap.xml
    sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc in sitemap_entries:
        prio = "1.0" if loc == "https://bestwatchdeals.com/" else "0.8"
        sitemap_xml.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-10-17</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>{prio}</priority>\n  </url>")
    sitemap_xml.append('</urlset>')
    with open(os.path.join(DIST_DIR, "sitemap.xml"), 'w', encoding='utf-8') as f:
        f.write("\n".join(sitemap_xml) + "\n")

    print("\n🏆 ULTRA-FORENSIC MASTER BUILD v3 COMPLETE!")
    print(f"- Total Static HTML Pages: {compiled_pages} (+ 1 branded 404.html)")
    print(f"- Clean 301 Redirect Rules: {len(redirect_lines)}")
    print(f"- XML Sitemap URLs: {len(sitemap_entries)}")
    print(f"- Social Sharing Asset: {os.path.join(assets_dir, 'og-bestwatchdeals.svg')}")
    print(f"- Output Directory: {DIST_DIR}")

if __name__ == '__main__':
    main()
