import re
import json
import os
import time
from seleniumwire import webdriver # নেটওয়ার্ক ইন্টারসেপ্ট করার জন্য
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
M3U_FILENAME = "sys_config_cache_v9.m3u"
JSON_FILENAME = "internal_data_v9.json"

# চ্যানেল লিস্ট (এখানে আপনার প্রয়োজনীয় আইডিগুলো বসান)
CHANNELS_LIST = [
    {"id": "tsports", "title": "T Sports", "cat": "Sports"},
    {"id": "gazi", "title": "Gazi TV", "cat": "Sports"},
    {"id": "somoy", "title": "Somoy TV", "cat": "News"},
    {"id": "atnnews", "title": "ATN News", "cat": "News"},
    {"id": "independent", "title": "Independent TV", "cat": "News"},
]

def get_token_by_intercept():
    print("🌐 Launching Network Interceptor to catch Token...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36")

    # সিলেনিয়াম ওয়্যার ড্রাইভার শুরু
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # প্লেয়ার পেজে হিট করা
        driver.get("https://tv.roarzone.net/player.php?stream=gazi")
        print("⏳ Analyzing Network Traffic for Token (30s)...")
        time.sleep(30) # ভিডিও লোড হওয়ার এবং টোকেন জেনারেট হওয়ার সময়
        
        # সব নেটওয়ার্ক রিকোয়েস্ট চেক করা
        for request in driver.requests:
            if request.response:
                # ইউআরএল-এ টোকেন আছে কি না দেখা
                match = re.search(r'token=([a-zA-Z0-9]{30,}-[a-zA-Z0-9]{30,}-\d+-\d+)', request.url)
                if not match:
                    match = re.search(r'token=([a-zA-Z0-9\._-]{40,})', request.url)
                
                if match:
                    found_token = match.group(1)
                    print(f"✅ Success! Intercepted Token: {found_token[:25]}...")
                    driver.quit()
                    return found_token
                    
        print("❌ Network ট্রাফিকে কোনো টোকেন পাওয়া যায়নি।")
        
    except Exception as e:
        print(f"❌ Interceptor Error: {str(e)}")
    finally:
        driver.quit()
    return None

def main():
    print("🚀 Starting Advanced Port 444 Update...")
    token = get_token_by_intercept()
    
    if not token:
        print("🛑 Token রিফ্রেশ করা সম্ভব হয়নি।")
        return

    m3u_content = "#EXTM3U\n"
    json_data = {"status": "active", "updated": True, "payload": []}

    for ch in CHANNELS_LIST:
        # Port 444 ফরম্যাট (আপনার ইনস্পেক্ট ডাটা অনুযায়ী)
        url = f"https://edge2.roarzone.net:444/roarzone/edge2/{ch['id']}/index.m3u8?token={token}"
        
        m3u_content += f"#EXTINF:-1, {ch['title']}\n{url}\n"
        json_data["payload"].append({
            "uid": ch['id'],
            "name": ch['title'],
            "src": url,
            "type": ch['cat']
        })

    with open(M3U_FILENAME, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    with open(JSON_FILENAME, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)
    
    print(f"✅ সাকসেস! {len(CHANNELS_LIST)}টি চ্যানেল আপডেট হয়েছে।")

if __name__ == "__main__":
    main()
