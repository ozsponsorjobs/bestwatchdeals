"""
Pinterest RSS Feed Generator for BestWatchDeals
Generates Pinterest-optimized RSS 2.0 XML feed with media:content and enclosure tags.
"""

import json
import os
import sys
import html
import datetime
import xml.etree.ElementTree as ET

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MANIFEST_PATH = os.path.join(SCRIPT_DIR, 'bestwatchdeals_manifest_v2.json')
DIST_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))

def generate_pinterest_rss():
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    reviews = [u for u in manifest['urls'] if u.get('action') == 'REVIEW']
    guides = [u for u in manifest['urls'] if u.get('action') == 'GUIDE']
    
    now = datetime.datetime.now(datetime.timezone.utc)
    
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0"',
        '     xmlns:content="http://purl.org/rss/1.0/modules/content/"',
        '     xmlns:wfw="http://wellformedweb.org/CommentAPI/"',
        '     xmlns:dc="http://purl.org/dc/elements/1.1/"',
        '     xmlns:atom="http://www.w3.org/2005/Atom"',
        '     xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"',
        '     xmlns:slash="http://purl.org/rss/1.0/modules/slash/"',
        '     xmlns:media="http://search.yahoo.com/mrss/">',
        '  <channel>',
        '    <title>Best Watch Deals &amp; Luxury Timepieces (2026)</title>',
        '    <atom:link href="https://bestwatchdeals.com/pinterest-feed.xml" rel="self" type="application/rss+xml" />',
        '    <link>https://bestwatchdeals.com/</link>',
        '    <description>Daily verified watch deals, automatic movement benchmarks, Seiko NH35 divers, and luxury homages. Verified direct factory prices.</description>',
        '    <language>en-US</language>',
        f'    <lastBuildDate>{now.strftime("%a, %d %b %Y %H:%M:%S +0000")}</lastBuildDate>',
        '    <sy:updatePeriod>hourly</sy:updatePeriod>',
        '    <sy:updateFrequency>1</sy:updateFrequency>',
    ]
    
    # Process reviews first (high conversion image pins)
    item_count = 0
    base_time = now - datetime.timedelta(days=7)
    
    for i, r in enumerate(reviews):
        title = r.get('display_title') or r.get('product_name') or r['title_2026'].split(':')[0]
        url = r.get('clean_url') or r['url']
        brand = r.get('brand', 'Horology')
        # Use the generated high-impact comparison Pin graphic!
        img_url = f"https://bestwatchdeals.com/assets/pins/pin_{i+1}.jpg"
        sale_p = r.get('sale_price', '89.00')
        orig_p = r.get('original_price', '199.00')
        disc = r.get('discount', '50%')
        stars = r.get('stars', 4.9)
        orders = r.get('orders', 420)
        
        # Stagger publication dates slightly so Pinterest ingests in orderly fashion
        item_time = base_time + datetime.timedelta(hours=i * 3)
        pub_date = item_time.strftime("%a, %d %b %Y %H:%M:%S +0000")
        
        clean_desc = (
            f"Luxury Watch Alternative: Why pay thousands for retail luxury? Discover the {title} for only ${sale_p} (Save {disc}). "
            f"Features solid 316L marine stainless steel, scratch-resistant sapphire crystal, and reliable movement. Rated {stars}/5.0 by {orders}+ verified buyers. "
            f"Read the full hands-on collector review and verified deal benchmarks at BestWatchDeals."
        )
        
        cdata_content = f"""<![CDATA[
<p><img src="{img_url}" alt="{html.escape(title)}" /></p>
<p><strong>{html.escape(title)}</strong> - The Smart Luxury Alternative.</p>
<p>• <strong>Sale Price:</strong> ${sale_p} (MSRP: ${orig_p} - Save {disc})</p>
<p>• <strong>Verified Rating:</strong> ★★★★★ {stars}/5.0 ({orders}+ orders)</p>
<p>{clean_desc}</p>
<p><a href="{url}">Click here to read the full review and check live deals &rarr;</a></p>
]]>"""

        xml_lines.extend([
            '    <item>',
            f'      <title>{html.escape(title)}: The Smart Luxury Alternative - Best Watch Deals</title>',
            f'      <link>{url}</link>',
            f'      <guid isPermaLink="true">{url}</guid>',
            f'      <pubDate>{pub_date}</pubDate>',
            f'      <dc:creator><![CDATA[BestWatchDeals Editorial Board]]></dc:creator>',
            f'      <description><![CDATA[{clean_desc}]]></description>',
            f'      <content:encoded>{cdata_content}</content:encoded>',
            f'      <enclosure url="{img_url}" length="0" type="image/jpeg" />',
            f'      <media:content url="{img_url}" medium="image">',
            f'        <media:title type="html">{html.escape(title)}</media:title>',
            '      </media:content>',
            '    </item>'
        ])
        item_count += 1
        
    # Process guides
    for j, g in enumerate(guides):
        title = g['title_2026']
        url = g['url']
        item_time = base_time + datetime.timedelta(hours=(len(reviews) + j) * 3)
        pub_date = item_time.strftime("%a, %d %b %Y %H:%M:%S +0000")
        img_url = "https://bestwatchdeals.com/assets/og-bestwatchdeals.svg"
        
        clean_desc = f"Master Horology Guide: {title}. Expert watchmaker techniques, maintenance schedules, movement comparisons, and collector buying strategies."
        
        cdata_content = f"""<![CDATA[
<p><img src="{img_url}" alt="{html.escape(title)}" /></p>
<p><strong>{html.escape(title)}</strong></p>
<p>{clean_desc}</p>
<p><a href="{url}">Read the full horology guide at BestWatchDeals &rarr;</a></p>
]]>"""

        xml_lines.extend([
            '    <item>',
            f'      <title>{html.escape(title)}</title>',
            f'      <link>{url}</link>',
            f'      <guid isPermaLink="true">{url}</guid>',
            f'      <pubDate>{pub_date}</pubDate>',
            f'      <dc:creator><![CDATA[Senior Horology Editor]]></dc:creator>',
            f'      <description><![CDATA[{clean_desc}]]></description>',
            f'      <content:encoded>{cdata_content}</content:encoded>',
            f'      <enclosure url="{img_url}" length="0" type="image/svg+xml" />',
            f'      <media:content url="{img_url}" medium="image">',
            f'        <media:title type="html">{html.escape(title)}</media:title>',
            '      </media:content>',
            '    </item>'
        ])
        item_count += 1

    xml_lines.extend([
        '  </channel>',
        '</rss>'
    ])
    
    rss_content = "\n".join(xml_lines)
    
    # Validate XML parsing
    try:
        ET.fromstring(rss_content)
        print("✅ RSS XML Validation Passed! XML is 100% well-formed.")
    except Exception as e:
        print(f"❌ XML Syntax Error: {e}")
        return
        
    os.makedirs(DIST_DIR, exist_ok=True)
    
    # Save as pinterest-feed.xml, feed.xml, and rss.xml for maximum compatibility
    targets = ['pinterest-feed.xml', 'feed.xml', 'rss.xml']
    for t in targets:
        target_path = os.path.join(DIST_DIR, t)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(rss_content)
        print(f"✅ Saved feed: {target_path}")
        
    print(f"\n🎉 Total Pinterest RSS Items Generated: {item_count}")

if __name__ == '__main__':
    generate_pinterest_rss()
