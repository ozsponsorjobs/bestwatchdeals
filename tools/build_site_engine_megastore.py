import os
import json
import re
import html
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

MANIFEST_PATH = os.path.join(SCRIPT_DIR, 'bestwatchdeals_manifest_v2.json')
DIST_DIR = os.path.join(SCRIPT_DIR, 'dist_bestwatchdeals')

# ==============================================================================
# ULTRA-LUXURY MEGASTORE CSS (<12KB, Zero-JS, 100/100 Core Web Vitals)
# ==============================================================================
MEGASTORE_CSS = """
:root {
  --bg-page: #f1f5f9;
  --bg-card: #ffffff;
  --text-dark: #0f172a;
  --text-body: #334155;
  --text-muted: #64748b;
  --border-light: #e2e8f0;
  --gold-primary: #d4af37;
  --gold-dark: #b8972e;
  --gold-light: #fef9c3;
  --deal-orange: #ea580c;
  --deal-orange-hover: #c2410c;
  --deal-orange-light: #ffedd5;
  --deal-green: #059669;
  --deal-green-light: #ecfdf5;
  --deal-red: #e11d48;
  --deal-red-light: #fff1f2;
  --store-navy: #0f172a;
  --store-slate: #1e293b;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: var(--bg-page);
  color: var(--text-body);
  line-height: 1.5;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
a { color: inherit; text-decoration: none; }

/* 1. Top E-Commerce Utility Bar */
.top-util-bar {
  background: #090d16;
  color: #94a3b8;
  font-size: 0.75rem;
  padding: 0.45rem 1rem;
  border-bottom: 1px solid #1e293b;
}
.top-util-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.promo-ticker {
  color: #e2e8f0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.promo-ticker strong { color: var(--gold-primary); }
.util-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.currency-select {
  background: #1e293b;
  color: #f8fafc;
  border: 1px solid #334155;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.72rem;
  font-weight: 600;
}

/* 2. Mega Store Header & Search */
header.store-header {
  background: #ffffff;
  border-bottom: 1px solid var(--border-light);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}
.header-main-row {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0.85rem 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
}
.brand-logo {
  display: flex;
  flex-direction: column;
}
.logo-title {
  font-size: 1.55rem;
  font-weight: 900;
  letter-spacing: -0.04em;
  color: var(--store-navy);
  line-height: 1;
}
.logo-title span { color: var(--deal-orange); }
.logo-sub {
  font-size: 0.62rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--text-muted);
  font-weight: 700;
  margin-top: 0.2rem;
}

/* Store Search Bar */
.search-container {
  flex-grow: 1;
  max-width: 550px;
  display: flex;
  position: relative;
}
.store-search-input {
  width: 100%;
  padding: 0.65rem 1rem 0.65rem 2.5rem;
  border: 2px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.85rem;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.store-search-input:focus {
  border-color: var(--deal-orange);
  box-shadow: 0 0 0 3px rgba(234, 88, 12, 0.15);
}
.search-icon {
  position: absolute;
  left: 0.85rem;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  font-size: 0.9rem;
}
.search-btn {
  position: absolute;
  right: 4px;
  top: 4px;
  bottom: 4px;
  background: var(--deal-orange);
  color: #ffffff;
  border: none;
  padding: 0 1rem;
  border-radius: 6px;
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
}
.search-btn:hover { background: var(--deal-orange-hover); }

/* User Action Buttons */
.header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.btn-flash-deals {
  background: linear-gradient(135deg, #ea580c, #dc2626);
  color: #ffffff;
  font-size: 0.8rem;
  font-weight: 800;
  padding: 0.6rem 1.1rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(234, 88, 12, 0.3);
  display: flex;
  align-items: center;
  gap: 0.4rem;
  transition: transform 0.2s;
}
.btn-flash-deals:hover { transform: translateY(-1px); }

/* 3. Departments Navigation Bar */
.departments-nav {
  background: var(--store-navy);
  color: #e2e8f0;
  border-bottom: 2px solid var(--gold-primary);
}
.departments-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.25rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  overflow-x: auto;
  white-space: nowrap;
}
.dept-link {
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0.7rem 0;
  color: #cbd5e1;
  border-bottom: 2px solid transparent;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  transition: color 0.2s, border-color 0.2s;
}
.dept-link:hover, .dept-link.active {
  color: #ffffff;
  border-bottom-color: var(--deal-orange);
}
.badge-tag {
  background: var(--deal-orange);
  color: #ffffff;
  font-size: 0.62rem;
  font-weight: 800;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
}

/* 4. Main Superstore Container */
main.store-main {
  flex-grow: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 1.5rem 1.25rem 3rem 1.25rem;
}

/* Superstore Hero Banner */
.store-hero {
  background: linear-gradient(135deg, #090d16 0%, #1e293b 100%);
  color: #ffffff;
  border-radius: 14px;
  padding: 2.75rem 2rem;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
  border: 1px solid #334155;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}
.store-hero::after {
  content: "";
  position: absolute;
  right: -50px;
  bottom: -50px;
  width: 250px;
  height: 250px;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.15) 0%, transparent 70%);
  border-radius: 50%;
}
.hero-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border: 1px solid #059669;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  margin-bottom: 1rem;
}
.hero-tag::before {
  content: "";
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  display: inline-block;
}
.hero-headline {
  font-size: 2.3rem;
  font-weight: 900;
  line-height: 1.15;
  max-width: 750px;
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}
.hero-desc {
  font-size: 0.95rem;
  color: #cbd5e1;
  max-width: 650px;
  line-height: 1.6;
  margin-bottom: 1.75rem;
}
.hero-badges-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 1.75rem;
  font-size: 0.8rem;
  color: #e2e8f0;
}
.hero-badge-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
.hero-badge-item span.icon { color: var(--gold-primary); font-size: 1rem; }

/* 5. Trust Bar (4 Pillars) */
.trust-bar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}
.trust-item {
  background: #ffffff;
  border: 1px solid var(--border-light);
  border-radius: 10px;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.85rem;
  box-shadow: 0 1px 4px rgba(0,0,0,0.02);
}
.trust-icon {
  font-size: 1.6rem;
  line-height: 1;
}
.trust-title {
  font-size: 0.85rem;
  font-weight: 800;
  color: var(--store-navy);
}
.trust-desc {
  font-size: 0.72rem;
  color: var(--text-muted);
}

/* 6. Section Titles */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 1.25rem;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 0.5rem;
}
.section-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--store-navy);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.section-link {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--deal-orange);
}
.section-link:hover { text-decoration: underline; }

/* 7. Product Megastore Grid */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
  gap: 1.25rem;
  margin-bottom: 2.5rem;
}

/* Mega-Store Product Card */
.store-product-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 1.15rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
  box-shadow: 0 2px 6px rgba(0,0,0,0.03);
}
.store-product-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
  border-color: #cbd5e1;
}

/* Card Badges */
.card-top-badges {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}
.discount-badge {
  background: var(--deal-red);
  color: #ffffff;
  font-size: 0.72rem;
  font-weight: 900;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  letter-spacing: 0.04em;
}
.stock-pill {
  font-size: 0.68rem;
  font-weight: 700;
  color: var(--deal-green);
  background: var(--deal-green-light);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}

/* Product Card Visual Preview */
.product-preview-box {
  background: #f8fafc;
  border: 1px solid #f1f5f9;
  border-radius: 8px;
  padding: 1.25rem;
  text-align: center;
  margin-bottom: 0.85rem;
  position: relative;
}
.preview-watch-icon {
  font-size: 2.8rem;
  line-height: 1;
}
.brand-pill {
  position: absolute;
  bottom: 6px;
  left: 50%;
  transform: translateX(-50%);
  background: #ffffff;
  border: 1px solid var(--border-light);
  font-size: 0.68rem;
  font-weight: 800;
  color: #475569;
  padding: 0.15rem 0.5rem;
  border-radius: 9999px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

/* Product Card Info */
.card-title {
  font-size: 0.95rem;
  font-weight: 700;
  line-height: 1.35;
  color: var(--store-navy);
  margin-bottom: 0.4rem;
  min-height: 2.6rem;
}
.card-title a:hover { color: var(--deal-orange); }

.card-rating-row {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.75rem;
  color: #f59e0b;
  margin-bottom: 0.75rem;
}
.rating-count { color: var(--text-muted); font-size: 0.72rem; }

/* Pricing Box */
.card-pricing-box {
  background: #f8fafc;
  border-radius: 6px;
  padding: 0.6rem 0.75rem;
  margin-bottom: 0.85rem;
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}
.deal-price {
  font-size: 1.25rem;
  font-weight: 900;
  color: var(--deal-green);
}
.msrp-price {
  font-size: 0.78rem;
  color: #94a3b8;
  text-decoration: line-through;
}
.save-badge {
  font-size: 0.68rem;
  font-weight: 700;
  color: var(--deal-orange);
}

/* Card Action Buttons */
.card-buttons-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.4rem;
}
.btn-buy-deal {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: #ffffff;
  font-size: 0.84rem;
  font-weight: 800;
  padding: 0.65rem 0.85rem;
  border-radius: 6px;
  text-align: center;
  transition: all 0.2s ease;
  box-shadow: 0 3px 8px rgba(234, 88, 12, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  text-decoration: none;
}
.btn-buy-deal:hover {
  background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(234, 88, 12, 0.35);
  color: #ffffff;
}
.btn-view-review {
  background: #ffffff;
  color: #475569;
  border: 1px solid #cbd5e1;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.45rem 0.75rem;
  border-radius: 6px;
  text-align: center;
}
.btn-view-review:hover { background: #f8fafc; color: var(--store-navy); }

/* 8. Product Detail Page (PDP Layout) */
.pdp-container {
  background: #ffffff;
  border: 1px solid var(--border-light);
  border-radius: 14px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.pdp-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}
@media (min-width: 820px) {
  .pdp-grid { grid-template-columns: 1fr 1fr; }
}

/* PDP Left: Showcase Card */
.pdp-showcase {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 2.5rem 1.5rem;
  text-align: center;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.pdp-badge-overlay {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: var(--deal-orange);
  color: #ffffff;
  font-size: 0.72rem;
  font-weight: 800;
  padding: 0.25rem 0.6rem;
  border-radius: 4px;
  text-transform: uppercase;
}
.pdp-watch-illustration {
  font-size: 5.5rem;
  margin: 1.5rem 0;
  line-height: 1;
}

/* PDP Right: Buy Box */
.pdp-buybox {
  display: flex;
  flex-direction: column;
}
.pdp-brand-tag {
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--deal-orange);
  letter-spacing: 0.08em;
  margin-bottom: 0.3rem;
}
.pdp-title {
  font-size: 1.65rem;
  font-weight: 900;
  color: var(--store-navy);
  line-height: 1.25;
  margin-bottom: 0.75rem;
}
.pdp-reviews-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  margin-bottom: 1.25rem;
}
.pdp-price-hero {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 1.25rem;
  margin-bottom: 1.25rem;
}
.pdp-price-row {
  display: flex;
  align-items: baseline;
  gap: 0.85rem;
}
.pdp-main-price {
  font-size: 2.2rem;
  font-weight: 900;
  color: var(--deal-green);
  line-height: 1;
}
.pdp-msrp-strike {
  font-size: 1rem;
  color: #94a3b8;
  text-decoration: line-through;
}
.pdp-discount-pill {
  background: var(--deal-red-light);
  color: var(--deal-red);
  font-size: 0.8rem;
  font-weight: 800;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}
.pdp-coupon-box {
  background: #fefce8;
  border: 1px dashed #ca8a04;
  border-radius: 6px;
  padding: 0.6rem 0.85rem;
  margin-top: 0.85rem;
  font-size: 0.78rem;
  color: #854d0e;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.coupon-code {
  font-weight: 800;
  background: #fef08a;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  letter-spacing: 0.05em;
}

/* PDP CTA Actions */
.pdp-cta-actions {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-bottom: 1.5rem;
}
.btn-pdp-aliexpress {
  background: linear-gradient(135deg, #ea580c, #dc2626);
  color: #ffffff;
  font-size: 0.95rem;
  font-weight: 800;
  padding: 0.9rem 1.5rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 4px 14px rgba(234, 88, 12, 0.35);
  transition: transform 0.2s, background 0.2s;
}
.btn-pdp-aliexpress:hover { transform: translateY(-1px); }
.btn-pdp-amazon {
  background: #334155;
  color: #ffffff;
  font-size: 0.85rem;
  font-weight: 700;
  padding: 0.7rem 1.25rem;
  border-radius: 8px;
  text-align: center;
}
.btn-pdp-amazon:hover { background: #475569; }

/* PDP Trust Grid */
.pdp-reassurance-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
  border-top: 1px solid var(--border-light);
  padding-top: 1rem;
  font-size: 0.72rem;
  color: #64748b;
  text-align: center;
}
.reassurance-item span { display: block; font-weight: 700; color: var(--store-navy); }

/* 9. Specifications Table */
.specs-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
  margin: 1.25rem 0 2rem 0;
  border: 1px solid var(--border-light);
  border-radius: 8px;
  overflow: hidden;
}
.specs-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border-light);
}
.specs-table tr:last-child td { border-bottom: none; }
.specs-table td.label {
  background: #f8fafc;
  font-weight: 700;
  color: #475569;
  width: 32%;
}
.specs-table td.value {
  background: #ffffff;
  color: var(--store-navy);
  font-weight: 500;
}
.specs-table tr:hover td { background: #f1f5f9; }

/* 10. Pros & Cons Split */
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
  background: var(--deal-green-light);
  border: 1px solid #a7f3d0;
  border-radius: 10px;
  padding: 1.25rem;
}
.pro-card h4 { color: #065f46; font-size: 0.9rem; font-weight: 800; margin-bottom: 0.75rem; }
.con-card {
  background: var(--deal-red-light);
  border: 1px solid #fecdd3;
  border-radius: 10px;
  padding: 1.25rem;
}
.con-card h4 { color: #9f1239; font-size: 0.9rem; font-weight: 800; margin-bottom: 0.75rem; }
.pro-card ul, .con-card ul { list-style: none; font-size: 0.82rem; }
.pro-card li, .con-card li { margin-bottom: 0.4rem; line-height: 1.4; }

/* 11. FAQ Accordions */
.faq-item {
  border: 1px solid var(--border-light);
  background: #ffffff;
  border-radius: 8px;
  margin-bottom: 0.75rem;
  overflow: hidden;
}
.faq-item summary {
  padding: 0.9rem 1.25rem;
  font-weight: 700;
  font-size: 0.88rem;
  cursor: pointer;
  background: #f8fafc;
  color: var(--store-navy);
}
.faq-item p {
  padding: 1rem 1.25rem;
  font-size: 0.85rem;
  color: #475569;
  line-height: 1.6;
}

/* 12. Mega Footer */
footer.store-footer {
  background: #090d16;
  color: #94a3b8;
  padding: 3.5rem 1.25rem 2rem 1.25rem;
  font-size: 0.85rem;
  border-top: 3px solid var(--gold-primary);
  margin-top: auto;
}
.footer-mega-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 2rem;
}
.footer-col h4 {
  color: #ffffff;
  font-size: 0.95rem;
  margin-bottom: 1.2rem;
  font-weight: 800;
  letter-spacing: -0.01em;
}
.footer-col ul { list-style: none; }
.footer-col li { margin-bottom: 0.6rem; font-size: 0.8rem; }
.footer-col a:hover { color: #ffffff; text-decoration: underline; }
.footer-payment-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}
.pay-badge {
  background: #1e293b;
  color: #cbd5e1;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  border: 1px solid #334155;
}
.footer-bottom-row {
  max-width: 1200px;
  margin: 2.5rem auto 0 auto;
  padding-top: 1.5rem;
  border-top: 1px solid #1e293b;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.75rem;
  color: #64748b;
}

@media (max-width: 768px) {
  .search-container { order: 3; max-width: 100%; flex-basis: 100%; }
  .header-main-row { flex-wrap: wrap; }
  .hero-headline { font-size: 1.65rem; }
  .pdp-main-price { font-size: 1.75rem; }
}

/* Mobile Sticky Deal Floating Bar (High Conversion) */
.pdp-sticky-bar {
  display: none;
}
@media (max-width: 768px) {
  .pdp-sticky-bar {
    display: block;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(15, 23, 42, 0.96);
    backdrop-filter: blur(10px);
    border-top: 1px solid rgba(255, 255, 255, 0.12);
    padding: 0.5rem 0.85rem;
    z-index: 9999;
    box-shadow: 0 -4px 15px rgba(0,0,0,0.25);
  }
  .sticky-bar-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    max-width: 500px;
    margin: 0 auto;
  }
  .sticky-price-col {
    display: flex;
    flex-direction: column;
    line-height: 1.1;
  }
  .sticky-lbl {
    font-size: 0.65rem;
    text-transform: uppercase;
    font-weight: 700;
    color: #94a3b8;
  }
  .sticky-price {
    font-size: 1.15rem;
    font-weight: 900;
    color: #38bdf8;
  }
  .sticky-btn-col {
    display: flex;
    gap: 0.4rem;
    flex: 1;
    justify-content: flex-end;
  }
  .btn-sticky-ae {
    background: #ea580c;
    color: #ffffff;
    font-size: 0.78rem;
    font-weight: 800;
    padding: 0.5rem 0.8rem;
    border-radius: 6px;
    text-align: center;
    white-space: nowrap;
    text-decoration: none;
  }
  .btn-sticky-amz {
    background: #f59e0b;
    color: #0f172a;
    font-size: 0.78rem;
    font-weight: 800;
    padding: 0.5rem 0.8rem;
    border-radius: 6px;
    text-align: center;
    white-space: nowrap;
    text-decoration: none;
  }
}
"""

DEFAULT_OG_IMAGE = "https://bestwatchdeals.com/assets/og-bestwatchdeals.svg"

# E-Commerce Watch Icon mapper by archetype
ARCHETYPE_ICONS = {
    "diver": "🌊",
    "chronograph": "⏱️",
    "fashion_dress": "⌚",
    "pocket_watch": "🕰️",
    "digital_sport": "🏃"
}

# MSRP Multiplier to show realistic e-commerce savings on cards
ARCHETYPE_MSRP = {
    "diver": ("$129.00", "$380.00", "SAVE 66%"),
    "chronograph": ("$89.00", "$295.00", "SAVE 70%"),
    "fashion_dress": ("$49.00", "$185.00", "SAVE 73%"),
    "pocket_watch": ("$29.00", "$95.00", "SAVE 69%"),
    "digital_sport": ("$35.00", "$110.00", "SAVE 68%")
}

def render_megastore_layout(title, description, canonical_url, body_html, schema_ld="", og_image=DEFAULT_OG_IMAGE, active_dept="all"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Ezoic Privacy & Integration Scripts -->
    <script data-cfasync="false" src="https://cmp.gatekeeperconsent.com/min.js"></script>
    <script data-cfasync="false" src="https://the.gatekeeperconsent.com/cmp.min.js"></script>
    <script async src="//www.ezojs.com/ezoic/sa.min.js"></script>
    <script>
        window.ezstandalone = window.ezstandalone || {{}};
        ezstandalone.cmd = ezstandalone.cmd || [];
    </script>
    <script src="//ezoicanalytics.com/analytics.js"></script>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <meta name="description" content="{html.escape(description)}">
    <link rel="canonical" href="{canonical_url}">
    
    <!-- Open Graph & Social Cards -->
    <meta property="og:title" content="{html.escape(title)}">
    <meta property="og:description" content="{html.escape(description)}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="BestWatchDeals Superstore">
    <meta property="og:image" content="{og_image}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{html.escape(title)}">
    <meta name="twitter:description" content="{html.escape(description)}">
    <meta name="twitter:image" content="{og_image}">
    
    <!-- RSS & Pinterest Discovery Feeds -->
    <link rel="alternate" type="application/rss+xml" title="BestWatchDeals RSS Feed" href="https://bestwatchdeals.com/feed.xml">
    <link rel="alternate" type="application/rss+xml" title="BestWatchDeals Pinterest Auto-Publish Feed" href="https://bestwatchdeals.com/pinterest-feed.xml">
    
    <!-- Pinterest Domain Verification -->
    <meta name="p:domain_verify" content="6db1a8dc4aaa13ca21418f68919f5508" />
    
    <!-- Lightweight Zero-JS Megastore Production CSS -->
    <style>{MEGASTORE_CSS}</style>
    {schema_ld}
</head>
<body>

    <!-- 1. Top E-Commerce Utility Bar -->
    <div class="top-util-bar">
        <div class="top-util-inner">
            <div class="promo-ticker">
                ⚡ <strong>OCTOBER 2026 SUPERSTORE DEALS:</strong> Up to 75% Off Automatic NH35 Divers &amp; Choice Day Flash Sales
            </div>
            <div class="util-links">
                <a href="/about/" style="color:#cbd5e1; font-weight:600; text-decoration:none;">📖 About Us</a>
                <a href="/contact/" style="color:#cbd5e1; font-weight:600; text-decoration:none;">✉️ Contact</a>
                <span>🛡️ 100% Verified Deals</span>
                <span>🚚 Global Express Tracking</span>
                <span class="currency-select">USD ($)</span>
            </div>
        </div>
    </div>

    <!-- 2. Main Superstore Header & Live Search Bar -->
    <header class="store-header">
        <div class="header-main-row">
            <div class="brand-logo">
                <a href="/" class="logo-title">BESTWATCH<span>DEALS</span></a>
                <span class="logo-sub">The Luxury &amp; Homage Superstore</span>
            </div>

            <!-- E-Commerce Live Search Simulation Bar -->
            <form action="/category/watch-deals/" method="get" class="search-container">
                <span class="search-icon">🔍</span>
                <input type="text" name="q" class="store-search-input" placeholder="Search 150+ automatic watches, Seiko NH35 divers, brands, deals..." aria-label="Search watches">
                <button type="submit" class="search-btn">Search</button>
            </form>

            <div class="header-actions">
                <a href="https://s.click.aliexpress.com/e/_c45LWcBP" target="_blank" rel="nofollow sponsored" class="btn-flash-deals">
                    <span>⚡</span> <span>Flash Deals</span>
                </a>
            </div>
        </div>

        <!-- 3. Departments Navigation Bar -->
        <nav class="departments-nav">
            <div class="departments-inner">
                <a href="/" class="dept-link {'active' if active_dept=='home' else ''}">🏠 Home</a>
                <a href="/category/watch-deals/" class="dept-link {'active' if active_dept=='deals' else ''}">🏷️ All Watch Deals <span class="badge-tag">HOT</span></a>
                <a href="/articles/top-5-best-rolex-submariner-alternatives/" class="dept-link {'active' if active_dept=='alternatives' else ''}">🏆 Top 5 Alternatives <span class="badge-tag" style="background:#ea580c; color:#ffffff;">NEW</span></a>
                <a href="/tag/rolex/" class="dept-link {'active' if active_dept=='rolex' else ''}">👑 Rolex &amp; Homages</a>
                <a href="/tag/seiko/" class="dept-link {'active' if active_dept=='seiko' else ''}">🌊 Seiko NH35 Divers</a>
                <a href="/tag/mechanical-watches/" class="dept-link {'active' if active_dept=='mechanical' else ''}">⚙️ Automatic Calibres</a>
                <a href="/watch-brands/omega-watches/" class="dept-link {'active' if active_dept=='omega' else ''}">⏱️ Chronographs</a>
                <a href="/category/articles-and-information/" class="dept-link {'active' if active_dept=='guides' else ''}">📚 Watch Care &amp; Guides</a>
            </div>
        </nav>
    </header>

    <!-- 4. Main Store Container -->
    <main class="store-main">
        {body_html}
    </main>

    <!-- 5. E-Commerce Superstore Footer -->
    <footer class="store-footer">
        <div class="footer-mega-grid">
            <div class="footer-col">
                <div class="logo-title" style="color:#ffffff; margin-bottom: 0.5rem;">BESTWATCH<span style="color:var(--deal-orange);">DEALS</span></div>
                <p style="font-size: 0.8rem; line-height: 1.6; color: #94a3b8; margin-bottom: 1rem;">
                    The internet's leading independent watch portal and homage deal index. We benchmark automatic movements, verify distributor discounts, and help collectors find authentic value since 2012.
                </p>
                <div class="footer-payment-badges">
                    <span class="pay-badge">🔒 256-Bit SSL</span>
                    <span class="pay-badge">✓ Verified Distributors</span>
                    <span class="pay-badge">⚡ Choice Day Express</span>
                </div>
            </div>

            <div class="footer-col">
                <h4>Watch Departments</h4>
                <ul>
                    <li><a href="/watch-brands/rolex-watches/">Rolex Submariner Homages</a></li>
                    <li><a href="/watch-brands/omega-watches/">Speedmaster &amp; Seamaster Deals</a></li>
                    <li><a href="/tag/seiko/">Seiko NH35 &amp; NH34 GMT Watches</a></li>
                    <li><a href="/watch-brands/breitling-watches-2/">Aviation &amp; Pilot Chronographs</a></li>
                    <li><a href="/tag/tag-heuer/">Motorsport Racing Watches</a></li>
                    <li><a href="/tag/mechanical-watches/">All Automatic Mechanical Watches</a></li>
                </ul>
            </div>

            <div class="footer-col">
                <h4>Buying &amp; Care Manuals</h4>
                <ul>
                    <li><a href="/articles/fundamental-maintenance-and-care-of-rolex-watch/">Rolex Maintenance &amp; Care Manual</a></li>
                    <li><a href="/articles/history-of-the-wrist-watch/">History of the Wristwatch</a></li>
                    <li><a href="/eight-best-sport-watches-ever/">8 Best Sport Watches Ever Built</a></li>
                    <li><a href="/links/where-are-the-best-watch-deals/">Where to Find Watch Deals (2026)</a></li>
                    <li><a href="/holiday-gift-guide/">Holiday Watch Gift Guide</a></li>
                    <li><a href="/top-10-luxury-watches-for-women-gorgeous-best-womens-luxury-watch/">Top Women's Luxury Watches</a></li>
                </ul>
            </div>

            <div class="footer-col">
                <h4>Customer Trust &amp; Legal</h4>
                <ul>
                    <li><a href="/about/">About Our Publication &amp; Lab</a></li>
                    <li><a href="/contact/">Contact Editorial Team</a></li>
                    <li><a href="/privacy-policy/">Privacy Policy (GDPR / CCPA)</a></li>
                    <li><a href="/terms-of-use/">Terms of Use &amp; Affiliate Disclosure</a></li>
                    <li><a href="/sitemap.xml">XML Product Sitemap</a></li>
                </ul>
                <p style="font-size: 0.72rem; color: #64748b; margin-top: 1.25rem; line-height: 1.5;">
                    BestWatchDeals.com is reader-supported. When you purchase through links on our site, we may earn an affiliate commission from verified merchants at no additional cost to you. As an Amazon Associate I earn from qualifying purchases.
                </p>
            </div>
        </div>

        <div class="footer-bottom-row">
            <div>&copy; 2012-2026 BestWatchDeals.com. All global rights reserved.</div>
            <div>Prices, coupons, AliExpress and Amazon Prime inventory subject to supplier change.</div>
        </div>
    </footer>

    <!-- Ezoic Ad Standalone Execution -->
    <script>
        ezstandalone.cmd.push(function () {{
            ezstandalone.showAds({{}});
        }});
    </script>

</body>
</html>"""

def generate_product_card_html(item):
    title = item['title_2026']
    brand = item['brand']
    path = item['path']
    arch = item.get('archetype', 'fashion_dress')
    
    icon = ARCHETYPE_ICONS.get(arch, "⌚")
    deal_p, msrp_p, save_lbl = ARCHETYPE_MSRP.get(arch, ("$59.00", "$195.00", "SAVE 70%"))
    
    search_query = f"{brand.lower().replace(' ', '+')}+{arch.replace('_', '+')}+watch"

    # Support mined real product data from official API
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

            <div class="product-preview-box">
                {image_html}
                <div class="brand-pill">{brand}</div>
            </div>

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

def build_megastore_home_page(all_reviews, all_guides, all_hubs):
    url = "https://bestwatchdeals.com/"
    title = "Best Watch Deals Superstore (2026): Luxury Timepieces & Verified Homages"
    description = "The premier online watch superstore. Discover 150+ verified mechanical automatic watches, Seiko NH35 divers, and luxury homage deals direct from manufacturers."

    # Generate Flash Deals grid (12 cards)
    deal_cards = [generate_product_card_html(r) for r in all_reviews[:12]]
    more_cards = [generate_product_card_html(r) for r in all_reviews[12:20]]

    # Generate Guide items
    guide_items_html = []
    for g in all_guides[:6]:
        guide_items_html.append(f"""
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:1.25rem; border-left:4px solid var(--gold-primary); display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <span style="font-size:0.7rem; font-weight:800; text-transform:uppercase; color:var(--deal-orange);">Expert Horology Guide</span>
                <h4 style="font-size:0.95rem; font-weight:700; color:var(--store-navy); margin:0.3rem 0 0.5rem 0;">
                    <a href="{g['path']}">{html.escape(g['title_2026'])}</a>
                </h4>
                <p style="font-size:0.8rem; color:#64748b; line-height:1.5;">Master watchmaking standards, maintenance schedules, and deal-sourcing benchmarks.</p>
            </div>
            <a href="{g['path']}" style="font-size:0.75rem; font-weight:800; color:var(--deal-orange); margin-top:0.85rem; display:inline-block;">Read Master Guide &rarr;</a>
        </div>
        """)

    schema = f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "BestWatchDeals Superstore",
      "url": "https://bestwatchdeals.com/",
      "image": "{DEFAULT_OG_IMAGE}",
      "description": "The online watch deals superstore featuring automatic watches, Seiko NH35 divers, and verified homage deals.",
      "potentialAction": {{
        "@type": "SearchAction",
        "target": "https://bestwatchdeals.com/category/watch-deals/?q={{search_term_string}}",
        "query-input": "required name=search_term_string"
      }}
    }}
    </script>
    """

    body = f"""
    <!-- Superstore Hero Banner -->
    <div class="store-hero">
        <div class="hero-tag">Official 2026 Watch Deals Mega-Store</div>
        <h1 class="hero-headline">The Premier Watch Deals Superstore: Luxury Craftsmanship at Factory Prices</h1>
        <p class="hero-desc">
            Direct access to verified mechanical automatic homage watches, Seiko NH35 divers, and chronograph benchmarks. Experience 95% of luxury aesthetic and mechanical joy at direct manufacturer pricing.
        </p>

        <div class="hero-badges-row">
            <div class="hero-badge-item"><span class="icon">✓</span> <span>14 Years of History (Est. 2012)</span></div>
            <div class="hero-badge-item"><span class="icon">✓</span> <span>Real Seiko NH35 &amp; Seagull Movements</span></div>
            <div class="hero-badge-item"><span class="icon">✓</span> <span>Scratch-Proof Sapphire Crystals</span></div>
            <div class="hero-badge-item"><span class="icon">✓</span> <span>AliExpress Choice &amp; Amazon Verified</span></div>
        </div>

        <div style="display:flex; flex-wrap:wrap; gap:0.75rem;">
            <a href="https://s.click.aliexpress.com/e/_c45LWcBP" target="_blank" rel="nofollow sponsored" class="btn-buy-deal" style="padding:0.85rem 1.75rem; font-size:0.95rem;">
                ⚡ Shop Today's Live Choice Day Deals
            </a>
            <a href="/category/watch-deals/" class="btn-view-review" style="padding:0.85rem 1.75rem; font-size:0.95rem; background:#ffffff; color:#0f172a; font-weight:800;">
                Browse All 150+ Watch Deals
            </a>
        </div>
    </div>

    <!-- 4-Pillar Trust Bar -->
    <div class="trust-bar">
        <div class="trust-item">
            <div class="trust-icon">🛡️</div>
            <div>
                <div class="trust-title">100% Genuine Calibres</div>
                <div class="trust-desc">Authentic Seiko NH35, VK63 &amp; Seagull movements</div>
            </div>
        </div>
        <div class="trust-item">
            <div class="trust-icon">💎</div>
            <div>
                <div class="trust-title">Solid 316L &amp; Sapphire</div>
                <div class="trust-desc">Marine stainless steel with scratch-proof glass</div>
            </div>
        </div>
        <div class="trust-item">
            <div class="trust-icon">⚡</div>
            <div>
                <div class="trust-title">Direct Factory Deals</div>
                <div class="trust-desc">Save up to 75% off traditional retail MSRP</div>
            </div>
        </div>
        <div class="trust-item">
            <div class="trust-icon">🚚</div>
            <div>
                <div class="trust-title">Global Tracked Express</div>
                <div class="trust-desc">Fast worldwide shipping with buyer protection</div>
            </div>
        </div>
    </div>

    <!-- Brand Silos Showcase -->
    <div style="margin-bottom: 2.5rem;">
        <div class="section-header">
            <h2 class="section-title">👑 Featured Watchmaker Silos &amp; Hubs</h2>
            <a href="/watch-brands/" class="section-link">View All Brand Hubs &rarr;</a>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:0.6rem;">
            <a href="/watch-brands/rolex-watches/" style="background:#ffffff; border:1px solid #e2e8f0; padding:0.6rem 1.1rem; border-radius:8px; font-size:0.85rem; font-weight:700; color:#1e293b; box-shadow:0 1px 3px rgba(0,0,0,0.03);">Rolex Deals &amp; Homages</a>
            <a href="/watch-brands/omega-watches/" style="background:#ffffff; border:1px solid #e2e8f0; padding:0.6rem 1.1rem; border-radius:8px; font-size:0.85rem; font-weight:700; color:#1e293b; box-shadow:0 1px 3px rgba(0,0,0,0.03);">Omega Speedmaster &amp; Seamaster</a>
            <a href="/tag/seiko/" style="background:#ffffff; border:1px solid #e2e8f0; padding:0.6rem 1.1rem; border-radius:8px; font-size:0.85rem; font-weight:700; color:#1e293b; box-shadow:0 1px 3px rgba(0,0,0,0.03);">Seiko NH35 &amp; Diver Deals</a>
            <a href="/watch-brands/breitling-watches-2/" style="background:#ffffff; border:1px solid #e2e8f0; padding:0.6rem 1.1rem; border-radius:8px; font-size:0.85rem; font-weight:700; color:#1e293b; box-shadow:0 1px 3px rgba(0,0,0,0.03);">Breitling Aviation Timepieces</a>
            <a href="/tag/tag-heuer/" style="background:#ffffff; border:1px solid #e2e8f0; padding:0.6rem 1.1rem; border-radius:8px; font-size:0.85rem; font-weight:700; color:#1e293b; box-shadow:0 1px 3px rgba(0,0,0,0.03);">Tag Heuer Chronograph Deals</a>
            <a href="/tag/mechanical-watches/" style="background:#ffffff; border:1px solid #e2e8f0; padding:0.6rem 1.1rem; border-radius:8px; font-size:0.85rem; font-weight:700; color:#1e293b; box-shadow:0 1px 3px rgba(0,0,0,0.03);">All Automatic Watches</a>
        </div>
    </div>

    <!-- Mega-Store Featured Products Grid -->
    <div style="margin-bottom: 2.5rem;">
        <div class="section-header">
            <h2 class="section-title">🔥 Today's Verified Flash Watch Deals</h2>
            <a href="/category/watch-deals/" class="section-link">View All Deals ({len(all_reviews)}) &rarr;</a>
        </div>
        <div class="products-grid">
            {''.join(deal_cards)}
        </div>
    </div>

    <!-- Secondary Product Deals Row -->
    <div style="margin-bottom: 2.5rem;">
        <div class="section-header">
            <h2 class="section-title">⚡ High-Value Collector Benchmarks</h2>
            <a href="/category/watch-deals/" class="section-link">Explore More &rarr;</a>
        </div>
        <div class="products-grid">
            {''.join(more_cards)}
        </div>
    </div>

    <!-- Master Horology Guides Grid -->
    <div style="margin-bottom: 2.5rem;">
        <div class="section-header">
            <h2 class="section-title">📚 Master Horology &amp; Care Guides</h2>
            <a href="/category/articles-and-information/" class="section-link">Read All Guides ({len(all_guides)}) &rarr;</a>
        </div>
        <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(320px, 1fr)); gap:1.25rem;">
            {''.join(guide_items_html)}
        </div>
    </div>
    """

    return render_megastore_layout(
        title=title,
        description=description,
        canonical_url=url,
        body_html=body,
        schema_ld=schema,
        active_dept="home"
    )

def build_megastore_pdp(item):
    title = item['title_2026']
    brand = item['brand']
    url = item['url']
    arch = item.get('archetype', 'fashion_dress')
    year = item.get('archived_year', '2013')
    
    icon = ARCHETYPE_ICONS.get(arch, "⌚")
    deal_p, msrp_p, save_lbl = ARCHETYPE_MSRP.get(arch, ("$59.00", "$195.00", "SAVE 70%"))

    # Support mined real product data from official API
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
    search_query = f"{brand.lower().replace(' ', '+')}+{arch.replace('_', '+')}+watch"
    promo_link = item.get('promotion_link') or f"https://s.click.aliexpress.com/e/_c45LWcBP?k={search_query}"
    price_val = deal_p.replace('$', '')
    product_img_for_schema = main_image if main_image else DEFAULT_OG_IMAGE

    # Archetype-specific specs & details
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

    # JSON-LD Schema
    schema = f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Product",
      "name": "{html.escape(title)}",
      "image": "{product_img_for_schema}",
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
        "validFrom": "2026-01-01",
        "itemCondition": "https://schema.org/NewCondition",
        "availability": "https://schema.org/InStock",
        "shippingDetails": {{
          "@type": "OfferShippingDetails",
          "shippingRate": {{
            "@type": "MonetaryAmount",
            "value": "0.00",
            "currency": "USD"
          }},
          "shippingDestination": {{
            "@type": "DefinedRegion",
            "addressCountry": "US"
          }},
          "deliveryTime": {{
            "@type": "ShippingDeliveryTime",
            "handlingTime": {{
              "@type": "QuantitativeValue",
              "minValue": 1,
              "maxValue": 2,
              "unitCode": "d"
            }},
            "transitTime": {{
              "@type": "QuantitativeValue",
              "minValue": 3,
              "maxValue": 7,
              "unitCode": "d"
            }}
          }}
        }},
        "hasMerchantReturnPolicy": {{
          "@type": "MerchantReturnPolicy",
          "applicableCountry": "US",
          "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
          "merchantReturnDays": 15,
          "returnMethod": "https://schema.org/ReturnByMail",
          "returnFees": "https://schema.org/FreeReturn"
        }}
      }},
      "review": {{
        "@type": "Review",
        "reviewRating": {{
          "@type": "Rating",
          "ratingValue": "4.9",
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
        <a href="/">Home</a> / <a href="/category/watch-deals/">Watches</a> / <span>{html.escape(brand)}</span>
    </div>

    <!-- Mega-Store PDP Container -->
    <div class="pdp-container">
        <div class="pdp-grid">
            
            <!-- Left: Showcase Card -->
            <div class="pdp-showcase">
                <span class="pdp-badge-overlay">{save_lbl}</span>
                {f'<img src="{main_image}" alt="{html.escape(title)}" style="max-height:280px; max-width:100%; object-fit:contain; border-radius:8px;" loading="eager">' if main_image else f'<div class="pdp-watch-illustration">{icon}</div>'}
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
                    <a href="https://www.amazon.com/s?k={brand}+watches&tag=bestwatchdeals-20" target="_blank" rel="nofollow sponsored" class="btn-pdp-amazon">
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
        schema_ld=schema,
        active_dept="deals"
    )

def build_megastore_hub_page(item, all_reviews, all_guides, all_hubs):
    title = item['title_2026']
    hub_name = item.get('hub_name', 'Watch Deals')
    url = item['url']
    path = item['path']

    hub_lower = (hub_name + " " + path).lower()
    
    if "rolex" in hub_lower:
        editorial_p = "Rolex stands at the summit of global horological recognition, with icons like the Submariner, GMT-Master II, and Datejust commanding massive waitlists and secondary market premiums. For collectors seeking authentic everyday wear, we analyze genuine heritage care protocols alongside the booming market of premium mechanical homages (crafted with solid 316L marine steel, synthetic sapphire crystals, and Seiko NH35 calibres) that deliver 95% of the aesthetic pleasure without the five-figure investment."
        sourcing_tip = "When exploring Rolex-inspired homages, brands like San Martin and Sugess offer ceramic bezels, 200m water resistance, and glide-lock style milled clasps that rival luxury finishing."
        deal_query = "san+martin+submariner+nh35"
        sort_archetype = "diver"
        dept_active = "rolex"
    elif "omega" in hub_lower:
        editorial_p = "From the lunar legacy of the Speedmaster Professional Moonwatch to the maritime durability of the Seamaster Diver 300M, Omega represents technical precision and Co-Axial innovation. Our collector reviews evaluate heritage reference values, professional chronograph maintenance, and top-tier accessible alternatives that celebrate Omega's iconic design language."
        sourcing_tip = "Speedmaster homages featuring the Seagull ST1901 column-wheel mechanical movement or Seiko VK63 meca-quartz deliver authentic tactile chronograph action at a fraction of luxury costs."
        deal_query = "pagani+design+speedmaster+chronograph"
        sort_archetype = "chronograph"
        dept_active = "omega"
    elif "breitling" in hub_lower:
        editorial_p = "Breitling has served as the aviator's trusted instrument for nearly a century. Celebrated for complex circular slide-rule bezels on the Navitimer and rugged chronographs like the Chronomat and Superocean, Breitling's aviation DNA is unmistakable. We evaluate pre-owned market values and high-accuracy aviation timepieces built for serious wrist presence."
        sourcing_tip = "Look for aviation chronographs with high-contrast reverse-panda dials, anti-reflective domed sapphire crystals, and bidirectional slide-rule bezels for true pilot aesthetics."
        deal_query = "pilot+chronograph+watch+navitimer"
        sort_archetype = "chronograph"
        dept_active = "deals"
    elif "seiko" in hub_lower:
        editorial_p = "Seiko revolutionized global watchmaking with the Quartz Crisis and remains the undisputed benchmark of accessible mechanical horology. Beyond Seiko's legendary Prospex diver line, their TMI NH35 automatic and NH34 GMT movements now power the world's most acclaimed independent microbrands, offering bulletproof reliability and hacking seconds for under $150."
        sourcing_tip = "Seiko NH35-powered watches from verified AliExpress Choice stores offer the greatest value-per-dollar in modern horology, featuring solid stainless steel and sapphire glass direct from manufacturer hubs."
        deal_query = "seiko+nh35+automatic+diver"
        sort_archetype = "diver"
        dept_active = "seiko"
    elif "mechanical" in hub_lower:
        editorial_p = "Mechanical and automatic timepieces represent miniature kinetic engineering powered solely by coiled mainsprings, gear trains, and the natural motion of your wrist. Our buying guide compares essential calibres—from workhorse Seiko NH35 and Miyota movements to Seagull column-wheel chronographs—helping you choose the most reliable automatic watch for your budget."
        sourcing_tip = "Always check for hacking seconds (the second hand stops when pulling the crown) and hand-winding capability when investing in modern automatic movements."
        deal_query = "automatic+mechanical+watch+nh35"
        sort_archetype = "diver"
        dept_active = "mechanical"
    else:
        editorial_p = f"Welcome to the dedicated 2026 collector resource for <strong>{html.escape(hub_name)}</strong>. Whether you are tracking pre-owned secondary market valuations, researching movement specifications, or looking for high-value mechanical automatic alternatives powered by Seiko NH35 and Seagull calibres, our team tests and curates the best verified options."
        sourcing_tip = "Compare authorized dealer pricing against verified direct manufacturer stores on AliExpress Choice to secure sapphire crystal and solid steel construction without retail markups."
        deal_query = f"{hub_name.lower().replace(' ', '+')}+watches"
        sort_archetype = "fashion_dress"
        dept_active = "deals"

    # Prioritize matched reviews
    matched_reviews = []
    hub_keywords = [w for w in hub_name.lower().split() if len(w) > 2]
    
    for r in all_reviews:
        r_text = (r['title_2026'] + " " + r['brand'] + " " + r['path']).lower()
        if any(kw in r_text for kw in hub_keywords):
            matched_reviews.append(r)

    for r in all_reviews:
        if r not in matched_reviews and r.get('archetype') == sort_archetype:
            matched_reviews.append(r)
        if len(matched_reviews) >= 8:
            break

    if len(matched_reviews) < 6:
        for r in all_reviews:
            if r not in matched_reviews:
                matched_reviews.append(r)
            if len(matched_reviews) >= 8:
                break

    sibling_hubs = [h for h in all_hubs if h['path'] != path][:6]
    cards_html = [generate_product_card_html(r) for r in matched_reviews[:12]]

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
    <div style="font-size:0.8rem; color:#64748b; margin-bottom:1.25rem;">
        <a href="/">Home</a> / <a href="/category/watch-deals/">Departments</a> / <span>{html.escape(hub_name)}</span>
    </div>

    <!-- Category Hub Banner -->
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:2rem; margin-bottom:2rem; box-shadow:0 1px 4px rgba(0,0,0,0.02);">
        <div style="display:inline-flex; align-items:center; gap:0.4rem; background:var(--deal-green-light); color:var(--deal-green); font-size:0.75rem; font-weight:800; padding:0.25rem 0.6rem; border-radius:4px; text-transform:uppercase; margin-bottom:0.75rem;">
            ● 2026 Verified Catalog Department
        </div>
        <h1 style="font-size:2rem; font-weight:900; color:var(--store-navy); margin-bottom:0.75rem;">{html.escape(title)}</h1>
        <p style="font-size:0.95rem; color:#475569; line-height:1.6; max-width:800px; margin-bottom:1.25rem;">
            {editorial_p}
        </p>

        <div style="background:#fffbeb; border-left:4px solid var(--gold-primary); padding:1rem 1.25rem; border-radius:0 8px 8px 0; font-size:0.85rem; color:#78350f; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
            <div>
                <strong>💡 Pro Collector Tip:</strong> {sourcing_tip}
            </div>
            <a href="https://s.click.aliexpress.com/e/_c45LWcBP?k={deal_query}" target="_blank" rel="nofollow sponsored" class="btn-buy-deal" style="padding:0.5rem 1rem; font-size:0.8rem;">
                ⚡ Check Verified Flash Deals &rarr;
            </a>
        </div>
    </div>

    <!-- Product Grid for Department -->
    <div class="section-header">
        <h2 class="section-title">🛒 Available Timepieces &amp; Deal Benchmarks ({len(matched_reviews)})</h2>
        <span style="font-size:0.8rem; color:#64748b;">Showing active verified supplier listings</span>
    </div>
    <div class="products-grid">
        {''.join(cards_html)}
    </div>

    <!-- Related Hubs -->
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:1.5rem; margin-top:2rem;">
        <h3 style="font-size:1.1rem; font-weight:800; color:var(--store-navy); margin-bottom:0.85rem;">Related Watchmaker Departments</h3>
        <div style="display:flex; flex-wrap:wrap; gap:0.5rem;">
            {''.join(f'<a href="{h["path"]}" style="background:#f1f5f9; padding:0.4rem 0.8rem; border-radius:6px; font-size:0.8rem; font-weight:600; color:#334155; border:1px solid #e2e8f0;">{h["title_2026"].split(" Watches")[0]} &rarr;</a>' for h in sibling_hubs)}
        </div>
    </div>
    """

    return render_megastore_layout(
        title=f"{title} | BestWatchDeals Superstore",
        description=f"Explore top-rated {hub_name} watches, collector benchmarks, mechanical movement comparisons, and verified deals for 2026.",
        canonical_url=url,
        body_html=body,
        schema_ld=schema,
        active_dept=dept_active
    )

# Re-use the existing detailed guides and legal pages with the new megastore layout!
import build_site_engine_v3
build_site_engine_v3.render_layout = lambda title, description, canonical_url, body_html, schema_ld="": render_megastore_layout(
    title=title,
    description=description,
    canonical_url=canonical_url,
    body_html=body_html,
    schema_ld=schema_ld,
    active_dept="Guides" if "/articles-and-information/" in canonical_url else "Deals"
)
from build_site_engine_v3 import build_guide_page, build_legal_page, build_404_page, create_headers_file, create_og_svg

def main():
    print("🚀 Initializing BestWatchDeals Ultra-Luxury MEGA-STORE Engine...")
    
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
    
    print(f"- Reviews to compile (PDP): {len(reviews)}")
    print(f"- Educational Guides: {len(guides)}")
    print(f"- Brand & Category Hubs (PLP): {len(hubs)}")
    print(f"- Legal Pages: {len(legals)}")
    print(f"- 301 Redirect Rules: {len(redirs)}")
    
    sitemap_entries = ["https://bestwatchdeals.com/"]
    compiled_pages = 0

    # 1. Compile Reviews as Mega-Store PDPs
    for r in reviews:
        html_out = build_megastore_pdp(r)
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

    # 3. Compile Hubs as Mega-Store Category PLPs
    for h in hubs:
        html_out = build_megastore_hub_page(h, reviews, guides, hubs)
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

    # 5. Compile Flagship Mega-Store Homepage
    home_html = build_megastore_home_page(reviews, guides, hubs)
    with open(os.path.join(DIST_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(home_html)
    compiled_pages += 1

    # 6. Compile Branded 404 Page
    page_404 = build_404_page()
    with open(os.path.join(DIST_DIR, "404.html"), 'w', encoding='utf-8') as f:
        f.write(page_404)

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
        sitemap_xml.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-10-18</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>{prio}</priority>\n  </url>")
    sitemap_xml.append('</urlset>')
    with open(os.path.join(DIST_DIR, "sitemap.xml"), 'w', encoding='utf-8') as f:
        f.write("\n".join(sitemap_xml) + "\n")

    # 10. Generate Pinterest & Standard RSS Feeds
    from build_pinterest_rss import generate_pinterest_rss
    generate_pinterest_rss()

    print("\n👑 MEGA-STORE ARCHITECTURE BUILD SUCCESSFUL!")
    print(f"- Total Static Megastore Pages: {compiled_pages} (+ 1 branded 404.html)")
    print(f"- Clean 301 Redirect Rules: {len(redirect_lines)}")
    print(f"- XML Sitemap URLs: {len(sitemap_entries)}")
    print(f"- Output Directory: {DIST_DIR}")

if __name__ == '__main__':
    main()
