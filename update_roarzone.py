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

def get_token_with_selenium():
    print("🌐 Launching Headless Chrome to bypass Cloudflare...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless") # ব্রাউজার উইন্ডো দেখাবে না
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # প্লেয়ার পেজে সরাসরি হিট করা
        player_url = "https://tv.roarzone.net/player.php?stream=tsports"
        driver.get(player_url)
        
        # ক্লাউডফ্লেয়ার চ্যালেঞ্জ সলভ হওয়ার জন্য ১০ সেকেন্ড অপেক্ষা
        print("⏳ Waiting for JavaScript challenge to complete...")
        time.sleep(12) 
        
        page_source = driver.page_source
        
        # টোকেন খোঁজা
        token_match = re.search(r'token=([a-zA-Z0-9\._-]{35,})', page_source)
        
        if token_match:
            tk = token_match.group(1)
            print(f"✅ Success: Token extracted via Selenium! ({tk[:15]}...)")
            return tk
        else:
            print("❌ Selenium-ও টোকেন খুঁজে পায়নি। পেজ সোর্স চেক করা দরকার।")
            
    except Exception as e:
        print(f"❌ Selenium Error: {str(e)}")
    finally:
        driver.quit()
    
    return None

def extract_channels_from_file(filename):
    channels = []
    if not os.path.exists(filename):
        print(f"❌ {filename} নট ফাউন্ড!")
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = r'data-title="([^"]+)"\s+data-tags="([^"]+)"\s+data-stream="([^"]+)"'
    matches = re.findall(pattern, content)
    for title, cat, stream_id in matches:
        channels.append({"id": stream_id, "title": title.title(), "cat": cat})
    return channels

def main():
    print("🚀 Starting Selenium Update Mode...")
    token = get_token_with_selenium()
    
    if not token:
        return

    channels = extract_channels_from_file("roarzone.txt")
    if not channels: return

    m3u_content = "#EXTM3U\n"
    json_data = {"status": "active", "updated": True, "payload": []}

    for ch in channels:
        url = f"https://edge2.roarzone.net:8447/roarzone/edge2/{ch['id']}/index.m3u8?token={token}"
        m3u_content += f"#EXTINF:-1, {ch['title']}\n{url}\n"
        json_data["payload"].append({"uid": ch['id'], "name": ch['title'], "src": url, "type": ch['cat']})

    with open(M3U_FILENAME, "w", encoding="utf-8") as f: f.write(m3u_content)
    with open(JSON_FILENAME, "w", encoding="utf-8") as f: json.dump(json_data, f, indent=2)
    
    print(f"✅ সাকসেস! {len(channels)}টি চ্যানেল আপডেট হয়েছে।")

if __name__ == "__main__":
    main()
