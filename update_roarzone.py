import re
import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
M3U_FILENAME = "sys_config_cache_v9.m3u"
JSON_FILENAME = "internal_data_v9.json"

def get_token_v444():
    print("🌐 Launching Browser to fetch Port 444 Token...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Inspect data অনুযায়ী লেটেস্ট ইউজার এজেন্ট
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        # সরাসরি প্লেয়ার পেজ লোড করা
        target_url = "https://tv.roarzone.net/player.php?stream=gazi"
        driver.get(target_url)
        
        print("⏳ Waiting for Cloudflare and Token generation (20s)...")
        time.sleep(20) # জাভাস্ক্রিপ্ট রান হওয়ার জন্য পর্যাপ্ত সময়
        
        page_source = driver.page_source
        
        # আপনার ইনস্পেক্ট ডাটা অনুযায়ী নতুন দীর্ঘ টোকেন ফরম্যাট খোঁজা
        # এটি টোকেনের ৩টি অংশ (hash-hash-timestamp-timestamp) ক্যাপচার করবে
        token_match = re.search(r'token=([a-zA-Z0-9]{30,}-[a-zA-Z0-9]{30,}-\d+-\d+)', page_source)
        
        if not token_match:
            # ব্যাকআপ প্যাটার্ন যদি ফরম্যাট কিছুটা ভিন্ন হয়
            token_match = re.search(r'token=([a-zA-Z0-9\._-]{40,})', page_source)

        if token_match:
            tk = token_match.group(1)
            print(f"✅ Success! Port 444 Token: {tk[:20]}...")
            driver.quit()
            return tk
        else:
            print("❌ টোকেন পাওয়া যায়নি। সোর্স কোডে অন্য কিছু আছে কি না পরীক্ষা করুন।")
            driver.quit()
            
    except Exception as e:
        print(f"❌ Selenium Error: {str(e)}")
    
    return None

def extract_channels(filename):
    channels = []
    if not os.path.exists(filename):
        print(f"❌ {filename} খুঁজে পাওয়া যায়নি!")
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    # roarzone.txt থেকে চ্যানেল আইডি এবং টাইটেল নেওয়া
    pattern = r'data-title="([^"]+)"\s+data-tags="([^"]+)"\s+data-stream="([^"]+)"'
    matches = re.findall(pattern, content)
    for title, cat, stream_id in matches:
        channels.append({"id": stream_id, "title": title.title(), "cat": cat})
    return channels

def main():
    print("🚀 Starting Port 444 Bypass Mode...")
    token = get_token_v444()
    
    if not token:
        print("🛑 টোকেন ছাড়া আপডেট সম্ভব নয়।")
        return

    channels = extract_channels("roarzone.txt")
    if not channels: return

    m3u_content = "#EXTM3U\n"
    json_data = {"status": "active", "updated": True, "payload": []}

    for ch in channels:
        # আপনার ইনস্পেক্ট ডাটা অনুযায়ী নতুন URL Structure (Port 444)
        # Format: https://edge2.roarzone.net:444/roarzone/edge2/{id}/index.m3u8?token={token}
        url = f"https://edge2.roarzone.net:444/roarzone/edge2/{ch['id']}/index.m3u8?token={token}"
        
        m3u_content += f"#EXTINF:-1, {ch['title']}\n{url}\n"
        json_data["payload"].append({
            "uid": ch['id'],
            "name": ch['title'],
            "src": url,
            "type": ch['cat']
        })

    with open(M3U_FILENAME, "w", encoding="utf-8") as f: f.write(m3u_content)
    with open(JSON_FILENAME, "w", encoding="utf-8") as f: json.dump(json_data, f, indent=2)
    
    print(f"✅ সাকসেস! Port 444 ব্যবহার করে {len(channels)}টি চ্যানেল আপডেট হয়েছে।")

if __name__ == "__main__":
    main()
