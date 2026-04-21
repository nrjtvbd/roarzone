import re
import json
import os
import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
M3U_FILE = "sys_config_cache_v9.m3u"
JSON_FILE = "internal_data_v9.json"

CHANNELS_LIST = [
    {"id": "tsports", "title": "T Sports", "cat": "Sports"},
    {"id": "gazi", "title": "Gazi TV", "cat": "Sports"},
    {"id": "somoy", "title": "Somoy TV", "cat": "News"},
    {"id": "atnnews", "title": "ATN News", "cat": "News"}
]

def get_fresh_token():
    print("🌐 Launching Real-Time Network Interceptor...")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Sora-sori player page-e hit kora
        driver.get("https://tv.roarzone.net/player.php?stream=tsports")
        print("⏳ Waiting for player to generate token (25s)...")
        time.sleep(25) 
        
        # Network request gulo check kora
        for request in driver.requests:
            if "token=" in request.url:
                # Token extract korar regex
                match = re.search(r'token=([a-zA-Z0-9\._-]{30,})', request.url)
                if match:
                    tk = match.group(1)
                    print(f"✅ Success! Fresh Token Found: {tk[:20]}...")
                    driver.quit()
                    return tk
                    
        print("❌ No token found in network logs.")
    except Exception as e:
        print(f"❌ Selenium Error: {e}")
    finally:
        driver.quit()
    return None

def main():
    token = get_fresh_token()
    if not token:
        print("🛑 Token refresh failed. Exiting.")
        return

    m3u_lines = ["#EXTM3U"]
    json_payload = {"status": "active", "updated": True, "payload": []}

    for ch in CHANNELS_LIST:
        # Port 444 ekhon standard
        url = f"https://edge2.roarzone.net:444/roarzone/edge2/{ch['id']}/index.m3u8?token={token}"
        
        m3u_lines.append(f'#EXTINF:-1 group-title="{ch["cat"]}", {ch["title"]}')
        m3u_lines.append(url)
        
        json_payload["payload"].append({
            "name": ch["title"],
            "src": url,
            "type": ch["cat"]
        })

    with open(M3U_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))
    
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(json_payload, f, indent=2)

    print(f"✅ Successfully updated {len(CHANNELS_LIST)} channels with fresh token.")

if __name__ == "__main__":
    main()
