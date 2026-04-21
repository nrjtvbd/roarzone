import cloudscraper
import re
import json
import os
import time

# --- CONFIGURATION ---
M3U_FILENAME = "sys_config_cache_v9.m3u"
JSON_FILENAME = "internal_data_v9.json"

def get_token():
    print("🌐 Bypassing Cloudflare Protection...")
    
    # Cloudscraper ব্রাউজারের মতো আচরণ করে চ্যালেঞ্জ সলভ করার চেষ্টা করবে
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    # আপনার নতুন তথ্য অনুযায়ী ডোমেইন এবং হেডার
    base_url = "https://tv.roarzone.net/"
    headers = {
        'Referer': 'https://tv.roarzone.net/',
        'Origin': 'https://tv.roarzone.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'
    }

    try:
        # ১. মেইন পেজ থেকে কুকি সংগ্রহ
        scraper.get(base_url, timeout=20)
        time.sleep(2) 

        # ২. প্লেয়ার পেজ থেকে টোকেন সংগ্রহ (T-Sports কে স্যাম্পল ধরে)
        player_url = "https://tv.roarzone.net/player.php?stream=tsports"
        response = scraper.get(player_url, headers=headers, timeout=20)
        
        # Roarzone-এর নতুন দীর্ঘ টোকেন প্যাটার্ন
        token_match = re.search(r'token=([a-zA-Z0-9\._-]{35,})', response.text)
        
        if token_match:
            tk = token_match.group(1)
            print(f"✅ Success: Token Received! ({tk[:15]}...)")
            return tk
        else:
            print("❌ Token pattern not found in player page.")
            # ডিবাগিংয়ের জন্য রেসপন্স চেক (ঐচ্ছিক)
            # print(response.text[:500]) 
            
    except Exception as e:
        print(f"❌ Scraper Error: {str(e)}")
    
    return None

def extract_channels_from_file(filename):
    channels = []
    if not os.path.exists(filename):
        print(f"❌ {filename} খুঁজে পাওয়া যায়নি!")
        return []

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # আপনার roarzone.txt এর HTML সোর্স থেকে ডেটা নেওয়া
    pattern = r'data-title="([^"]+)"\s+data-tags="([^"]+)"\s+data-stream="([^"]+)"'
    matches = re.findall(pattern, content)

    for title, cat, stream_id in matches:
        channels.append({
            "id": stream_id,
            "title": title.title(),
            "cat": cat
        })
    return channels

def main():
    print("🚀 Starting Direct Update (No Decrypt Mode)...")
    
    token = get_token()
    if not token:
        print("🛑 টোকেন ছাড়া আপডেট সম্ভব নয়।")
        return

    channels = extract_channels_from_file("roarzone.txt")
    if not channels:
        return

    m3u_content = "#EXTM3U\n"
    json_data = {"status": "active", "updated": True, "payload": []}

    for ch in channels:
        # নতুন edge2 ডোমেইন এবং ৮৪৪৭ পোর্ট নিশ্চিত করা হয়েছে
        url = f"https://edge2.roarzone.net:8447/roarzone/edge2/{ch['id']}/index.m3u8?token={token}"
        
        m3u_content += f"#EXTINF:-1, {ch['title']}\n{url}\n"
        json_data["payload"].append({
            "uid": ch['id'],
            "name": ch['title'],
            "src": url,
            "type": ch['cat']
        })

    # ফাইল সেভ করা
    with open(M3U_FILENAME, "w", encoding="utf-8") as f: 
        f.write(m3u_content)
    with open(JSON_FILENAME, "w", encoding="utf-8") as f: 
        json.dump(json_data, f, indent=2)
    
    print(f"✅ সফল! {len(channels)}টি চ্যানেল আপডেট হয়েছে।")

if __name__ == "__main__":
    main()
