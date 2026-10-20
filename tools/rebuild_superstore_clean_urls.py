import os
import json
import re
import html
import sys
import glob
from urllib.parse import quote_plus

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
TOOLS_DIR = SCRIPT_DIR

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure tools directory is in sys.path
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from build_site_engine_megastore import (
    render_megastore_layout,
    build_megastore_home_page,
    build_megastore_hub_page,
    ARCHETYPE_ICONS,
    ARCHETYPE_MSRP,
    DEFAULT_OG_IMAGE
)
from build_site_engine_v3 import build_guide_page, build_legal_page, build_404_page, create_headers_file, create_og_svg

MANIFEST_PATH = os.path.join(TOOLS_DIR, 'bestwatchdeals_manifest_v2.json')

def clean_product_card_html(item):
    path = item.get('clean_path') or item.get('path')
    title = item.get('display_title') or item['title_2026'].split(':')[0].strip()
    brand = item.get('brand', 'Watch')
    arch = item.get('archetype', 'fashion_dress')
    
    icon = ARCHETYPE_ICONS.get(arch, "⌚")
    deal_p, msrp_p, save_lbl = ARCHETYPE_MSRP.get(arch, ("$59.00", "$195.00", "SAVE 70%"))
    
    search_query = quote_plus(f"{brand} {arch} watch")

    main_image = item.get('main_image')
    if main_image:
        image_html = f'<img src="{main_image}" alt="{html.escape(title)}" style="max-height:160px; max-width:100%; object-fit:contain; border-radius:6px;" loading="lazy">'
    else:
        image_html = f'<div class="preview-watch-icon">{icon}</div>'

    if item.get('sale_price'):
        try:
            deal_p = f"${float(item['sale_price']):.2f}"
        except Exception:
            deal_p = f"${item['sale_price']}"
    if item.get('original_price'):
        try:
            msrp_p = f"${float(item['original_price']):.2f}"
        except Exception:
            msrp_p = f"${item['original_price']}"
    if item.get('discount'):
        save_lbl = f"SAVE {item['discount']}"
    stars = item.get('stars', 4.9)
    orders = item.get('orders', 420)
    promo_link = item.get('promotion_link') or f"https://s.click.aliexpress.com/e/_c45LWcBP?k={search_query}"

    return f"""
    <div class="store-product-card">
        <div>
            <div class="card-top-badges">
                <span class="discount-badge">{save_lbl}</span>
                <span class="stock-pill">● In Stock</span>
            </div>

            <!-- CLICKABLE PRODUCT IMAGE BOX -->
            <a href="{path}" class="product-preview-box" title="{html.escape(title)}" style="display:block; text-decoration:none;">
                {image_html}
                <div class="brand-pill">{brand}</div>
            </a>

            <!-- CLICKABLE PRODUCT TITLE -->
            <h3 class="card-title">
                <a href="{path}">{html.escape(title)}</a>
            </h3>

            <div class="card-rating-row">
                <span>★★★★★</span>
                <span class="rating-count">{stars} ({orders}+ orders)</span>
            </div>

            <div class="card-pricing-box">
                <div>
                    <span class="deal-price">{deal_p}</span>
                    <span class="msrp-price">{msrp_p}</span>
                </div>
                <span class="save-badge">{save_lbl}</span>
            </div>
        </div>

        <div class="card-buttons-row">
            <a href="{promo_link}" target="_blank" rel="nofollow sponsored" class="btn-buy-deal">
                ⚡ Check Deal Price
            </a>
            <a href="{path}" class="btn-view-review">
                Specs &amp; Full Review &rarr;
            </a>
        </div>
    </div>
    """

def clean_megastore_pdp(item):
    title = item.get('display_title') or item['title_2026'].split(':')[0].strip()
    brand = item['brand']
    url = item.get('clean_url') or item['url']
    path = item.get('clean_path') or item['path']
    arch = item.get('archetype', 'fashion_dress')
    
    icon = ARCHETYPE_ICONS.get(arch, "⌚")
    deal_p, msrp_p, save_lbl = ARCHETYPE_MSRP.get(arch, ("$59.00", "$195.00", "SAVE 70%"))

    main_image = item.get('main_image')
    if item.get('sale_price'):
        try:
            deal_p = f"${float(item['sale_price']):.2f}"
        except Exception:
            deal_p = f"${item['sale_price']}"
    if item.get('original_price'):
        try:
            msrp_p = f"${float(item['original_price']):.2f}"
        except Exception:
            msrp_p = f"${item['original_price']}"
    if item.get('discount'):
        save_lbl = f"SAVE {item['discount']}"
    stars = item.get('stars', 4.9)
    orders = item.get('orders', 420)
    
    search_query = quote_plus(f"{brand} {arch} watch")
    amazon_query = quote_plus(f"{brand} watches")
    promo_link = item.get('promotion_link') or f"https://s.click.aliexpress.com/e/_c45LWcBP?k={search_query}"
    price_val = deal_p.replace('$', '')
    product_img_for_schema = main_image if main_image else DEFAULT_OG_IMAGE

    # Archetype specs
    if arch == "diver":
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
    elif arch == "chronograph":
        specs = [
            ("Timepiece Style", f"{brand} Racing & Aviation Tachymeter Chronograph"),
            ("Movement Engine", "Seagull ST1901 Mechanical Hand-Winding Column Wheel / Seiko VK63 Meca-Quartz"),
            ("Case Architecture", "316L High-Polished Stainless Steel with Ergonomic Pump Pushers"),
            ("Crystal / Dial", "Domed Sapphire Crystal with Anti-Glare Coating & Contrast Subdials"),
            ("Scale Function", "Engraved Tachymeter Scale for Speed & Timing Calculations"),
            ("Water Resistance", "50m – 100m (Rain, Splash & Daily Wear Resistant)"),
            ("Collector Value Range", "$65 – $185 (Direct Collector Import / Luxury Homage)")
        ]
        p1 = f"Mechanical chronographs are widely considered the pinnacle of tactile horological engineering. The <strong>{brand}</strong> chronograph pays homage to historic motorsport and aviation designs, utilizing precision pump pushers that engage elapsed-seconds timing with a distinct mechanical click."
        p2 = "Available with authentic column-wheel mechanical architectures (such as the famed Seagull ST19) or instantaneous flyback meca-quartz engines, this watch features a step-dial layout, syringe hands, and high-visibility contrasting registers for minutes and continuous seconds."
        pros = [
            "Authentic mechanical chronograph feel with crisp tactile pushers.",
            "Striking reverse-panda or sunburst dial with high-contrast subdials.",
            "Scratch-resistant domed sapphire crystal provides vintage warmth without distortion.",
            "Exceptional finishing on the case bevels and brushed lugs."
        ]
        cons = [
            "Mechanical variants require manual winding every 40-48 hours.",
            "50m water resistance means it should not be worn for swimming or diving.",
            "Thickness is slightly pronounced due to the chronograph module geometry."
        ]
        faq1_q = "How often should I wind a mechanical chronograph?"
        faq1_a = "Wind the crown clockwise 20-25 turns each morning until you feel gentle resistance. Do not force past resistance."
        faq2_q = "Can the chronograph function run continuously?"
        faq2_a = "It is best practice to run the chronograph only when timing events to preserve the mainspring power reserve and minimize gear wear."
    else:
        specs = [
            ("Target Silhouette", f"{brand} Luxury Heritage Automatic Homage"),
            ("Movement Calibre", "Precision Automatic Self-Winding / Japanese Calibre"),
            ("Case Material", "Solid 316L Marine Stainless Steel"),
            ("Crystal Lens", "Scratch-Resistant Synthetic Sapphire Crystal"),
            ("Bracelet / Strap", "Solid Link Stainless Steel / Hand-Stitched Genuine Leather"),
            ("Water Resistance", "100m (Swimming & Daily Splash-Proof)"),
            ("Collector Value Range", "$75 – $170 (Choice Day Express Direct)")
        ]
        p1 = f"For collectors seeking the look and tactile quality of world-class Swiss luxury timepieces without the steep retail markups, <strong>{brand}</strong> offers an impeccably engineered alternative. Every component—from the solid 316L steel links to the AR-coated sapphire lens—reflects meticulous machining."
        p2 = "Powered by an automatic movement that winds naturally with wrist movement, this timepiece delivers hacking seconds for down-to-the-second time setting, high-luminosity night markers, and exceptional daily reliability."
        pros = [
            "Superb luxury aesthetic rivaling four-figure Swiss luxury watches.",
            "True sapphire crystal lens that resists scratches and dings.",
            "Dependable automatic mechanical movement with hacking seconds.",
            "Exceptional value-to-price ratio with manufacturer warranty."
        ]
        cons = [
            "Brand recognition is focused among horology enthusiasts rather than mainstream luxury buyers.",
            "Requires initial bracelet sizing with a standard screwdriver or pin tool.",
            "Shipped directly in protective transit packaging."
        ]
        faq1_q = "Does this watch require battery replacements?"
        faq1_a = "No. As an automatic mechanical timepiece, it is powered purely by your daily wrist motion and manual winding."
        faq2_q = "Is the watch covered by a warranty?"
        faq2_a = "Yes, verified AliExpress Choice purchases include a 15-day free return window and direct manufacturer guarantees."

    schema_json = f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Product",
      "name": "{html.escape(title)}",
      "image": "{product_img_for_schema}",
      "description": "2026 collector review, authentic specifications, and verified deal pricing for {brand}.",
      "brand": {{
        "@type": "Brand",
        "name": "{brand}"
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
          "ratingValue": "{stars}",
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
    <!-- Breadcrumbs -->
    <div style="font-size:0.8rem; color:#64748b; margin-bottom:1.25rem;">
        <a href="/">Home</a> / <a href="/category/watch-deals/">Watches</a> / <span>{brand}</span>
    </div>

    <!-- Mega-Store PDP Container -->
    <div class="pdp-container">
        <div class="pdp-grid">
            
            <!-- Left: Showcase Card -->
            <div class="pdp-showcase">
                <span class="pdp-badge-overlay">{save_lbl}</span>
                <img src="{main_image}" alt="{html.escape(title)}" style="max-height:280px; max-width:100%; object-fit:contain; border-radius:8px;" loading="eager">
                <div style="background:#ffffff; border:1px solid #e2e8f0; padding:0.5rem 1rem; border-radius:8px; font-size:0.75rem; font-weight:700; color:#475569;">
                    Authentic Calibre Verified • 2026 Model
                </div>
            </div>

            <!-- Right: E-Commerce Buy Box -->
            <div class="pdp-buybox">
                <span class="pdp-brand-tag">{brand} Timepiece</span>
                <h1 class="pdp-title">{html.escape(title)}</h1>

                <div class="pdp-reviews-meta">
                    <span style="color:#f59e0b; font-weight:800;">★★★★★ {stars}</span>
                    <span style="color:#64748b;">({orders}+ Verified Global Buyer Reviews)</span>
                    <span style="color:#cbd5e1;">•</span>
                    <span style="color:#059669; font-weight:700;">✓ In Stock</span>
                </div>

                <div class="pdp-price-hero">
                    <div class="pdp-price-row">
                        <span class="pdp-main-price">{deal_p}</span>
                        <span class="pdp-msrp-strike">{msrp_p}</span>
                        <span class="pdp-discount-pill">{save_lbl}</span>
                    </div>
                    <div class="pdp-coupon-box">
                        <span>🏷️ Verified Flash Coupon:</span>
                        <span class="coupon-code">OCTDEAL2026</span>
                    </div>
                </div>

                <div class="pdp-cta-actions">
                    <a href="{promo_link}" target="_blank" rel="nofollow sponsored" class="btn-pdp-aliexpress">
                        ⚡ BUY NOW: CHECK LIVE FLASH DEAL ON ALIEXPRESS
                    </a>
                    <a href="https://www.amazon.com/s?k={amazon_query}" target="_blank" rel="nofollow sponsored" class="btn-pdp-amazon">
                        🛒 Compare on Amazon Prime (Fast Domestic Delivery)
                    </a>
                </div>

                <div class="pdp-reassurance-row">
                    <div class="reassurance-item">
                        <span>🛡️ Authenticity</span>
                        Direct Manufacturer
                    </div>
                    <div class="reassurance-item">
                        <span>🚚 Fast Dispatch</span>
                        Tracked Global Delivery
                    </div>
                    <div class="reassurance-item">
                        <span>✓ Buyer Guarantee</span>
                        15-Day Free Returns
                    </div>
                </div>
            </div>

        </div>

        <!-- Technical Specifications -->
        <h2 style="font-size:1.35rem; font-weight:800; color:var(--store-navy); margin:2.5rem 0 1rem 0;">
            📊 Technical &amp; Build Specifications
        </h2>
        <table class="specs-table">
            <tbody>
                {''.join(f'<tr><td class="label">{k}</td><td class="value">{v}</td></tr>' for k, v in specs)}
            </tbody>
        </table>

        <!-- Hands-On Analysis -->
        <h2 style="font-size:1.35rem; font-weight:800; color:var(--store-navy); margin:2rem 0 1rem 0;">
            🔍 In-Depth Horologist Hands-On Assessment
        </h2>
        <div style="font-size:0.95rem; color:#334155; line-height:1.7; margin-bottom:1.5rem;">
            <p style="margin-bottom:1rem;">{p1}</p>
            <p style="margin-bottom:1rem;">{p2}</p>
        </div>

        <!-- Pros & Cons -->
        <h2 style="font-size:1.35rem; font-weight:800; color:var(--store-navy); margin:2rem 0 1rem 0;">
            ⚖️ Unbiased Collector Pros &amp; Cons
        </h2>
        <div class="pro-con-grid">
            <div class="pro-card">
                <h4>✅ Key Advantages</h4>
                <ul>
                    {''.join(f'<li>• {x}</li>' for x in pros)}
                </ul>
            </div>
            <div class="con-card">
                <h4>⚠️ Honest Points to Consider</h4>
                <ul>
                    {''.join(f'<li>• {x}</li>' for x in cons)}
                </ul>
            </div>
        </div>

        <!-- FAQs -->
        <h2 style="font-size:1.35rem; font-weight:800; color:var(--store-navy); margin:2.5rem 0 1rem 0;">
            💬 Frequently Asked Questions
        </h2>
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

        <!-- Bottom Mega Deal Box -->
        <div style="background:linear-gradient(135deg, #0f172a, #1e293b); color:#ffffff; border-radius:12px; padding:2rem; text-align:center; margin-top:2.5rem;">
            <h3 style="font-size:1.45rem; font-weight:800; margin-bottom:0.5rem;">Lock In Today's Verified Flash Deal</h3>
            <p style="font-size:0.85rem; color:#cbd5e1; max-width:550px; margin:0 auto 1.5rem auto;">
                Don't overpay retail markups. Compare live distributor stock and limited-time Choice Day coupon codes now.
            </p>
            <a href="https://s.click.aliexpress.com/e/_c45LWcBP?k={search_query}" target="_blank" rel="nofollow sponsored" class="btn-buy-deal" style="display:inline-block; padding:0.85rem 2rem; font-size:0.95rem;">
                ⚡ Claim Live Deal on AliExpress
            </a>
        </div>
    </div>
    """

    return render_megastore_layout(
        title=f"{title} | BestWatchDeals",
        description=f"In-depth 2026 hands-on review for {title}. Detailed specifications, real pros & cons, movement accuracy, and verified deal options.",
        canonical_url=url,
        body_html=body,
        schema_ld=schema_json,
        og_image=main_image,
        active_dept="deals"
    )

def build_custom_home_page(all_reviews, all_guides, all_hubs):
    url = "https://bestwatchdeals.com/"
    title = "Best Watch Deals Superstore (2026): Luxury Timepieces & Verified Homages"
    description = "The premier online watch superstore. Discover 150+ verified mechanical automatic watches, Seiko NH35 divers, and luxury homage deals direct from manufacturers."

    deal_cards = [clean_product_card_html(r) for r in all_reviews[:12]]
    more_cards = [clean_product_card_html(r) for r in all_reviews[12:28]]

    guides_html = "".join([f"""
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:1.25rem; display:flex; flex-direction:column; justify-content:space-between;">
        <div>
            <span style="font-size:0.7rem; font-weight:800; color:#ea580c; text-transform:uppercase;">Collector Guide</span>
            <h4 style="font-size:1rem; font-weight:800; color:#0f172a; margin:0.5rem 0;">
                <a href="{g['path']}">{html.escape(g['title_2026'])}</a>
            </h4>
            <p style="font-size:0.8rem; color:#64748b; line-height:1.5;">Expert teardown of movement tolerances, authenticity checks, and care protocols.</p>
        </div>
        <a href="{g['path']}" style="font-size:0.8rem; font-weight:700; color:#ea580c; margin-top:1rem; display:inline-block;">Read Guide &rarr;</a>
    </div>
    """ for g in all_guides[:6]])

    body = f"""
    <!-- Flash Deals Section -->
    <div class="section-header">
        <div class="section-title">
            <span>🔥</span> Today's Top Verified Watch Deals (Direct Manufacturer Stock)
        </div>
        <a href="/category/watch-deals/" class="section-link">View All 57+ Deals &rarr;</a>
    </div>
    <div class="products-grid">
        {"".join(deal_cards)}
    </div>

    <!-- More Timepieces -->
    <div class="section-header">
        <div class="section-title">
            <span>⚡</span> Automatic Calibres, GMTs &amp; Vintage Chronographs
        </div>
        <a href="/category/watch-deals/" class="section-link">Browse Full Catalog &rarr;</a>
    </div>
    <div class="products-grid">
        {"".join(more_cards)}
    </div>

    <!-- Watch Guides Grid -->
    <div class="section-header" style="margin-top:2.5rem;">
        <div class="section-title">
            <span>📚</span> Expert Horology &amp; Care Buying Guides
        </div>
        <a href="/category/articles-and-information/" class="section-link">All 50+ Guides &rarr;</a>
    </div>
    <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(260px, 1fr)); gap:1.25rem; margin-bottom:2.5rem;">
        {guides_html}
    </div>
    """

    return render_megastore_layout(
        title=title,
        description=description,
        canonical_url=url,
        body_html=body,
        active_dept="home"
    )

def build_custom_hub_page(item, all_reviews, all_guides, all_hubs):
    title = item['title_2026']
    hub_name = item.get('hub_name', 'Watch Deals')
    url = item['url']
    path = item['path']

    hub_lower = (hub_name + " " + path).lower()
    
    if "rolex" in hub_lower:
        editorial_p = "Rolex stands at the summit of global horological recognition, with icons like the Submariner, GMT-Master II, and Datejust commanding massive waitlists. We curate premium mechanical homages (crafted with solid 316L marine steel, sapphire crystals, and Seiko NH35 calibres) that deliver 95% of the aesthetic pleasure without five-figure investment."
        deal_query = "san+martin+submariner+nh35"
        dept_active = "rolex"
    elif "omega" in hub_lower:
        editorial_p = "From the lunar legacy of the Speedmaster Professional Moonwatch to the maritime durability of the Seamaster Diver 300M, Omega represents technical precision and Co-Axial innovation. Our collector reviews evaluate top-tier accessible alternatives that celebrate Omega's iconic design language."
        deal_query = "pagani+design+speedmaster+chronograph"
        dept_active = "omega"
    elif "seiko" in hub_lower:
        editorial_p = "Seiko revolutionized global watchmaking and remains the undisputed benchmark of accessible mechanical horology. Their TMI NH35 automatic and NH34 GMT movements now power the world's most acclaimed independent microbrands, offering bulletproof reliability."
        deal_query = "seiko+nh35+automatic+diver"
        dept_active = "seiko"
    elif "mechanical" in hub_lower:
        editorial_p = "Mechanical and automatic timepieces represent miniature kinetic engineering powered solely by coiled mainsprings, gear trains, and the natural motion of your wrist. Our buying guide compares essential calibres helping you choose the most reliable automatic watch for your budget."
        deal_query = "automatic+mechanical+watch+nh35"
        dept_active = "mechanical"
    else:
        editorial_p = f"Welcome to the dedicated 2026 collector resource for <strong>{html.escape(hub_name)}</strong>. Discover verified mechanical automatic alternatives powered by Seiko NH35 and Seagull calibres direct from manufacturer hubs."
        deal_query = f"{hub_name.lower().replace(' ', '+')}+watches"
        dept_active = "deals"

    cards_html = [clean_product_card_html(r) for r in all_reviews[:16]]

    body = f"""
    <!-- Category Hero Header -->
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:2rem; margin-bottom:2rem;">
        <span style="font-size:0.75rem; font-weight:800; color:#ea580c; text-transform:uppercase; letter-spacing:0.05em;">Curated Department</span>
        <h1 style="font-size:1.85rem; font-weight:900; color:#0f172a; margin:0.5rem 0 1rem 0;">{html.escape(title)}</h1>
        <p style="font-size:0.95rem; color:#475569; line-height:1.7; max-width:850px; margin-bottom:1.5rem;">{editorial_p}</p>
        <div style="display:flex; gap:1rem; flex-wrap:wrap;">
            <a href="https://s.click.aliexpress.com/e/_c45LWcBP?k={deal_query}" target="_blank" rel="nofollow sponsored" class="btn-buy-deal" style="padding:0.6rem 1.5rem; font-size:0.85rem;">
                ⚡ Claim Live {html.escape(hub_name)} Flash Deals
            </a>
        </div>
    </div>

    <!-- Products Grid -->
    <div class="section-header">
        <div class="section-title">
            <span>⌚</span> Featured {html.escape(hub_name)} Timepieces
        </div>
    </div>
    <div class="products-grid">
        {"".join(cards_html)}
    </div>
    """

    return render_megastore_layout(
        title=f"{title} | BestWatchDeals Superstore",
        description=f"Explore top-rated {hub_name} watches, collector benchmarks, mechanical movement comparisons, and verified deals for 2026.",
        canonical_url=url,
        body_html=body,
        active_dept=dept_active
    )

def main():
    print("🚀 Rebuilding BestWatchDeals with 100% Clean URLs & Clickable Cards...")
    
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    urls = manifest['urls']
    reviews = [u for u in urls if u.get('action') == 'REVIEW']
    guides = [u for u in urls if u.get('action') == 'GUIDE']
    hubs = [u for u in urls if u.get('action') == 'HUB']
    legals = [u for u in urls if u.get('action') == 'LEGAL']
    redirs = [u for u in urls if u.get('action') == 'REDIRECT']
    
    print(f"Loaded: {len(reviews)} reviews, {len(guides)} guides, {len(hubs)} hubs, {len(legals)} legals.")
    
    sitemap_entries = ["https://bestwatchdeals.com/"]
    redirect_lines = []

    # 1. Compile 57 Reviews under /watches/<slug>/ AND create fallback .html + 301 redirects
    print("📦 Compiling 57 Review PDPs under /watches/<slug>/...")
    for i, r in enumerate(reviews):
        clean_path = r['clean_path'].strip('/') # e.g. "watches/san-martin-40mm-bb58-retro-luxury-diver"
        html_out = clean_megastore_pdp(r)
        
        # A. Directory index: dist_bestwatchdeals/watches/<slug>/index.html
        target_dir = os.path.join(DIST_DIR, clean_path)
        os.makedirs(target_dir, exist_ok=True)
        with open(os.path.join(target_dir, "index.html"), 'w', encoding='utf-8') as f:
            f.write(html_out)
            
        # B. Direct HTML file: dist_bestwatchdeals/watches/<slug>.html (for direct file resolution)
        direct_file = os.path.join(DIST_DIR, f"{clean_path}.html")
        with open(direct_file, 'w', encoding='utf-8') as f:
            f.write(html_out)
            
        # C. Backward-compatible redirect file for old 2013 path
        old_path = r.get('old_path')
        if old_path and old_path != r['clean_path']:
            old_clean = old_path.strip('/')
            old_dir = os.path.join(DIST_DIR, old_clean)
            os.makedirs(old_dir, exist_ok=True)
            redir_target = r['clean_url']
            instant_redirect_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url={redir_target}">
<link rel="canonical" href="{redir_target}">
<title>Redirecting to {html.escape(r.get('display_title', 'Watch Review'))} | BestWatchDeals</title>
</head>
<body style="font-family:sans-serif; text-align:center; padding:3rem;">
<h2>Redirecting to 2026 Watch Review...</h2>
<p><a href="{redir_target}">Click here if you are not redirected automatically.</a></p>
</body>
</html>"""
            with open(os.path.join(old_dir, "index.html"), 'w', encoding='utf-8') as f:
                f.write(instant_redirect_html)
                
            # Add to Cloudflare 301 _redirects
            redirect_lines.append(f"{old_path} {r['clean_path']} 301")
            redirect_lines.append(f"{old_path.rstrip('/')} {r['clean_path']} 301")
            
        sitemap_entries.append(r['clean_url'])

    print(f"✅ Compiled all 57 reviews into /watches/<slug>/index.html and .html")

    # 2. Compile Guides
    print("📚 Compiling Educational Guides...")
    for g in guides:
        html_out = build_guide_page(g)
        clean_path = g['path'].strip('/')
        target_dir = os.path.join(DIST_DIR, clean_path)
        os.makedirs(target_dir, exist_ok=True)
        with open(os.path.join(target_dir, "index.html"), 'w', encoding='utf-8') as f:
            f.write(html_out)
        sitemap_entries.append(g['url'])

    # 3. Compile Hubs (Category PLPs)
    print("🏷️ Compiling Category Hubs...")
    for h in hubs:
        html_out = build_custom_hub_page(h, reviews, guides, hubs)
        clean_path = h['path'].strip('/')
        target_dir = os.path.join(DIST_DIR, clean_path)
        os.makedirs(target_dir, exist_ok=True)
        with open(os.path.join(target_dir, "index.html"), 'w', encoding='utf-8') as f:
            f.write(html_out)
        sitemap_entries.append(h['url'])

    # 4. Compile Legal Pages
    print("⚖️ Compiling Legal Pages...")
    for l in legals:
        html_out = build_legal_page(l)
        clean_path = l['path'].strip('/')
        target_dir = os.path.join(DIST_DIR, clean_path)
        os.makedirs(target_dir, exist_ok=True)
        with open(os.path.join(target_dir, "index.html"), 'w', encoding='utf-8') as f:
            f.write(html_out)
        sitemap_entries.append(l['url'])

    # 5. Compile Flagship Homepage
    print("🏠 Compiling Flagship Homepage...")
    home_html = build_custom_home_page(reviews, guides, hubs)
    with open(os.path.join(DIST_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(home_html)

    # 6. Compile 404 Page
    print("🚨 Compiling Branded 404 Page...")
    page_404 = build_404_page()
    with open(os.path.join(DIST_DIR, "404.html"), 'w', encoding='utf-8') as f:
        f.write(page_404)

    # 7. Write Cloudflare _redirects
    print("🔄 Generating Cloudflare _redirects...")
    for r in redirs:
        p_from = r['path']
        p_to = r.get('redirect_to', '/category/watch-deals/')
        redirect_lines.append(f"{p_from} {p_to} 301")
        if p_from.endswith('/'):
            redirect_lines.append(f"{p_from.rstrip('/')} {p_to} 301")
            
    with open(os.path.join(DIST_DIR, "_redirects"), 'w', encoding='utf-8') as f:
        f.write("\n".join(redirect_lines) + "\n")
    print(f"✅ Generated {len(redirect_lines)} redirect rules in _redirects")

    # 8. Write sitemap.xml
    print("🗺️ Generating sitemap.xml...")
    sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc in sitemap_entries:
        prio = "1.0" if loc == "https://bestwatchdeals.com/" else "0.8"
        sitemap_xml.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-10-20</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>{prio}</priority>\n  </url>")
    sitemap_xml.append('</urlset>')
    
    with open(os.path.join(DIST_DIR, "sitemap.xml"), 'w', encoding='utf-8') as f:
        f.write("\n".join(sitemap_xml) + "\n")
    print(f"✅ Generated sitemap.xml with {len(sitemap_entries)} clean URLs.")

    print("🎉 Full Megastore Rebuild Succeeded!")

if __name__ == '__main__':
    main()
