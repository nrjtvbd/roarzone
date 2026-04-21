import re
import json
import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

# --- CONFIGURATION ---
M3U_FILENAME = "sys_config_cache_v9.m3u"
JSON_FILENAME = "internal_data_v9.json"

def get_token_smart():
    print("🌐 Launching Undetected Chrome to bypass Cloudflare...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless') # GitHub Actions এর জন্য হেডলেস মোড
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    try:
        # Undetected Chromedriver সেশন শুরু
        driver = uc.Chrome(options=options)
        
        # Roarzone প্লেয়ার পেজ
        player_url = "https://tv.roarzone.net/player.php?stream=tsports"
        driver.get(player_url)
        
        print("⏳ Waiting for Cloudflare challenge to solve automatically...")
        # ক্লাউডফ্লেয়ার চ্যালেঞ্জ এবং জাভাস্ক্রিপ্ট লোড হতে সময় দিন
        time.sleep(20) 
        
        page_source = driver.page_source
        
        # টোকেন খোঁজার নতুন এবং শক্তিশালী Regex
        # এটি 'token=' এর পর থাকা দীর্ঘ ক্যারেক্টারগুলো ধরবে
        token_match = re.search(r'token=([a-zA-Z0-9\._-]{35,})', page_source)
        
        if token_match:
            tk = token_match.group(1)
            print(f"✅ Success: Smart Token extracted! ({tk[:15]}...)")
            driver.quit()
            return tk
        else:
            print("❌ Still no token found. Printing partial page source for debug...")
            # সোর্সে 'token' শব্দটি আছে কি না চেক করা
            if 'token' in page_source.lower():
                print("⚠️ 'token' word found but regex failed. Checking alternative patterns...")
                alt_match = re.search(r'token=([^"\'\s&]+)', page_source)
                if alt_match:
                    print("✅ Alternative Token found!")
                    driver.quit()
                    return alt_match.group(1)
            
    except Exception as e:
        print(f"❌ Smart Update Error: {str(e)}")
    
    return None

def extract_channels_from_file(filename):
    channels = []
    if not os.path.exists(filename):
        print(f"❌ {filename} not found!")
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = r'data-title="([^"]+)"\s+data-tags="([^"]+)"\s+data-stream="([^"]+)"'
    matches = re.findall(pattern, content)
    for title, cat, stream_id in matches:
        channels.append({"id": stream_id, "title": title.title(), "cat": cat})
    return channels

def main():
    print("🚀 Starting Smart Selenium Mode (Undetected)...")
    token = get_token_smart()
    
    if not token:
        print("🛑 Token extraction failed again. Process stopped.")
        return

    channels = extract_channels_from_file("roarzone.txt")
    if not channels: return

    m3u_content = "#EXTM3U\n"
    json_data = {"status": "active", "updated": True, "payload": []}

    for ch in channels:
        # নতুন URL স্ট্রাকচার অনুযায়ী লিঙ্ক তৈরি
        url = f"https://edge2.roarzone.net:8447/roarzone/edge2/{ch['id']}/index.m3u8?token={token}"
        m3u_content += f"#EXTINF:-1, {ch['title']}\n{url}\n"
        json_data["payload"].append({"uid": ch['id'], "name": ch['title'], "src": url, "type": ch['cat']})

    with open(M3U_FILENAME, "w", encoding="utf-8") as f: f.write(m3u_content)
    with open(JSON_FILENAME, "w", encoding="utf-8") as f: json.dump(json_data, f, indent=2)
    
    print(f"✅ সাকসেস! ফাইলগুলো আপডেট হয়েছে।")

if __name__ == "__main__":
    main()
