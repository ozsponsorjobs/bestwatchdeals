"""
Batch Pinterest Comparison Pin Generator for BestWatchDeals
Creates 800x1200 viral infographic Pins comparing luxury retail icons vs smart verified alternatives.
"""

import io
import os
import json
import requests
import sys
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

MANIFEST_PATH = 'bestwatchdeals_manifest_v2.json'
OUTPUT_DIR = os.path.join('dist_bestwatchdeals', 'assets', 'pins')
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"

def get_luxury_counterpart(title, brand):
    t = (title + " " + brand).lower()
    if "bb58" in t or "bb54" in t or "tudor" in t:
        return "Tudor Black Bay 58", "$4,000+"
    elif "moon" in t or "speedmaster" in t or "1701" in t:
        return "Omega Speedmaster Moonwatch", "$7,600+"
    elif "daytona" in t or "1644" in t:
        return "Rolex Cosmograph Daytona", "$35,000+"
    elif "submariner" in t or "diver" in t or "sn0008" in t or "sn017" in t:
        return "Rolex Submariner Date", "$14,500+"
    elif "gmt" in t or "1662" in t or "1682" in t:
        return "Rolex GMT-Master II Pepsi", "$18,000+"
    elif "willard" in t or "1970" in t:
        return "Seiko Prospex Willard SLA033", "$4,250+"
    elif "datejust" in t or "c8185" in t:
        return "Rolex Datejust 41 Fluted", "$11,000+"
    elif "1963" in t or "pilot" in t:
        return "Breitling Aviator 8 Chrono", "$5,800+"
    elif "royal oak" in t:
        return "Audemars Piguet Royal Oak", "$48,000+"
    elif "prx" in t or "polo" in t:
        return "Tissot PRX Powermatic 80", "$725+"
    elif "aquanaut" in t or "5167" in t:
        return "Patek Philippe Aquanaut 5167", "$65,000+"
    elif "skeleton" in t or "tourbillon" in t:
        return "Hublot Big Bang Skeleton", "$22,000+"
    elif "micro rotor" in t or "dress" in t:
        return "Patek Philippe Calatrava", "$28,000+"
    elif "military" in t or "field" in t:
        return "IWC Pilot Mark XVIII Heritage", "$5,200+"
    else:
        return "Swiss Luxury Horology", "$4,500+"

def get_specs_for_item(brand, sale_p):
    specs = [
        "Solid 316L Marine Stainless Steel Architecture",
        "Bulletproof Japanese Automatic / VK63 Movement",
        "Anti-Reflective Scratch-Resistant Sapphire Crystal",
        "Direct Factory Deal with Comprehensive Buyer Protection"
    ]
    return specs

def generate_pin_for_item(item, index):
    raw_title = item.get('product_name') or item['title_2026'].split(':')[0]
    brand = item['brand']
    sale_p = item.get('sale_price', '89.00')
    disc = item.get('discount', '50%')
    discount_label = f"Save {disc}" if "%" in str(disc) else f"Save {disc}%"
    img_url = item.get('main_image', '')
    
    lux_name, lux_price = get_luxury_counterpart(raw_title, brand)
    specs = get_specs_for_item(brand, sale_p)
    
    W, H = 800, 1200
    img = Image.new("RGB", (W, H), color="#0B1120") # Deep Midnight Navy
    draw = ImageDraw.Draw(img)
    
    # Fonts
    font_top = ImageFont.truetype(FONT_BOLD, 19)
    font_main = ImageFont.truetype(FONT_BOLD, 35)
    font_sub = ImageFont.truetype(FONT_BOLD, 21)
    font_comp_lbl = ImageFont.truetype(FONT_BOLD, 17)
    font_comp_val = ImageFont.truetype(FONT_BOLD, 26)
    font_specs = ImageFont.truetype(FONT_BOLD, 20)
    font_cta = ImageFont.truetype(FONT_BOLD, 23)

    # 1. Top Ribbon
    draw.rectangle([(0, 0), (W, 52)], fill="#070A13")
    draw.text((W//2, 26), "BESTWATCHDEALS.COM • 2026 HOROLOGY VALUE AUDIT", fill="#D4AF37", font=font_top, anchor="mm")
    
    # 2. Main Hook Title
    draw.text((W//2, 92), "THE SMART LUXURY ALTERNATIVE", fill="#F8FAFC", font=font_main, anchor="mm")
    draw.text((W//2, 132), "Why pay thousands when you get 95% the build quality?", fill="#94A3B8", font=font_sub, anchor="mm")
    
    # 3. Versus Comparison Cards
    # Left Card: Luxury Icon MSRP
    draw.rounded_rectangle([(40, 165), (385, 255)], radius=12, fill="#1E293B", outline="#334155", width=2)
    draw.text((212, 192), f"LUXURY ICON: {lux_name[:24]}", fill="#F87171", font=font_comp_lbl, anchor="mm")
    draw.text((212, 226), lux_price, fill="#F8FAFC", font=font_comp_val, anchor="mm")
    
    # Right Card: The Smart Alternative Choice
    draw.rounded_rectangle([(415, 165), (760, 255)], radius=12, fill="#064E3B", outline="#10B981", width=2)
    draw.text((587, 192), f"SMART CHOICE: {brand[:20]}", fill="#34D399", font=font_comp_lbl, anchor="mm")
    draw.text((587, 226), f"${sale_p} ({discount_label})", fill="#FFFFFF", font=font_comp_val, anchor="mm")

    # 4. Central Product Image Showcase Box
    prod_box = [(40, 275), (760, 775)]
    draw.rounded_rectangle(prod_box, radius=16, fill="#FFFFFF", outline="#E2E8F0", width=2)
    
    if img_url:
        try:
            r = requests.get(img_url, timeout=10)
            pimg = Image.open(io.BytesIO(r.content)).convert("RGBA")
            pimg.thumbnail((700, 480), Image.Resampling.LANCZOS)
            px = 40 + (720 - pimg.width) // 2
            py = 275 + (500 - pimg.height) // 2
            img.paste(pimg, (px, py), pimg if pimg.mode == 'RGBA' else None)
        except Exception:
            pass
            
    # Corner Badge on Image
    draw.rounded_rectangle([(60, 295), (230, 338)], radius=8, fill="#EA580C")
    draw.text((145, 316), "VERIFIED CHOICE", fill="#FFFFFF", font=ImageFont.truetype(FONT_BOLD, 16), anchor="mm")

    # 5. Engineering Specs Breakdown Box
    draw.rounded_rectangle([(40, 795), (760, 1070)], radius=14, fill="#1E293B", outline="#334155", width=2)
    draw.text((70, 825), "BUILD SPECIFICATION BENCHMARK:", fill="#D4AF37", font=ImageFont.truetype(FONT_BOLD, 20))
    
    y_spec = 865
    for s in specs:
        # Draw vector green circle with white checkmark
        cx, cy = 80, y_spec + 12
        draw.ellipse([(cx-10, cy-10), (cx+10, cy+10)], fill="#10B981")
        draw.line([(cx-5, cy), (cx-2, cy+4), (cx+5, cy-4)], fill="#FFFFFF", width=2)
        draw.text((105, y_spec), s, fill="#F1F5F9", font=font_specs)
        y_spec += 45

    # 6. Bottom High-Converting Action Bar
    draw.rounded_rectangle([(40, 1090), (760, 1165)], radius=12, fill="#EA580C")
    draw.text((W//2, 1127), "READ FULL COLLECTOR REVIEW & VERIFIED DEALS >>", fill="#FFFFFF", font=font_cta, anchor="mm")

    out_file = os.path.join(OUTPUT_DIR, f"pin_{index}.jpg")
    img.save(out_file, "JPEG", quality=92)
    return out_file

def main():
    print("🚀 Generating 57 High-Impact Pinterest Comparison Infographic Pins...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    reviews = [u for u in manifest['urls'] if u.get('action') == 'REVIEW']
    
    for i, r in enumerate(reviews, 1):
        pin_path = generate_pin_for_item(r, i)
        print(f"  [{i}/{len(reviews)}] Created: {pin_path}")
        
    print(f"\n🎉 Successfully generated {len(reviews)} Pinterest comparison Pins!")

if __name__ == '__main__':
    main()
