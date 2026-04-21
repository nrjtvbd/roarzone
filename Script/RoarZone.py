import undetected_chromedriver as uc
import re
import json
import time
import os

# --- CONFIGURATION ---
M3U_FILE = "sys_config_cache_v9.m3u"
JSON_FILE = "internal_data_v9.json"

CHANNELS = [
    {"id": "tsports", "name": "T Sports", "group": "Sports"},
    {"id": "gazi", "name": "Gazi TV", "group": "Sports"}
]

def get_token_undetected():
    print("🚀 Launching Undetected Chromedriver...")
    
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # আমরা হেডলেস মোড সরাসরি দেব না, ভার্চুয়াল ডিসপ্লে ব্যবহার করব
    
    try:
        driver = uc.Chrome(options=options, version_main=123) # আপনার ক্রোমের ভার্সন অনুযায়ী
        
        print("🌐 Visiting RoarZone Player...")
        driver.get("https://tv.roarzone.net/player.php?stream=tsports")
        
        # ক্লাউডফ্লেয়ার চ্যালেঞ্জ সলভ হওয়ার জন্য পর্যাপ্ত সময় দিন
        print("⏳ Waiting for Cloudflare Challenge (30s)...")
        time.sleep(30)
        
        page_source = driver.page_source
        
        # টোকেন খোঁজা
        token_match = re.search(r'token=([a-zA-Z0-9]{30,}-[a-zA-Z0-9]{30,}-\d+-\d+)', page_source)
        if not token_match:
            token_match = re.search(r'token=([a-zA-Z0-9\._-]{40,})', page_source)
            
        if token_match:
            tk = token_match.group(1)
            print(f"✅ Success! Token Found: {tk[:20]}...")
            driver.quit()
            return tk
        else:
            print("❌ Undetected Mode-এও টোকেন পাওয়া যায়নি।")
            driver.quit()
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    return None

def main():
    token = get_token_undetected()
    if not token:
        return

    m3u_lines = ["#EXTM3U"]
    json_payload = {"status": "active", "updated": True, "payload": []}

    for ch in CHANNELS:
        url = f"https://edge2.roarzone.net:444/roarzone/edge2/{ch['id']}/index.m3u8?token={token}"
        m3u_lines.append(f'#EXTINF:-1 group-title="{ch["group"]}", {ch["name"]}\n{url}')
        json_payload["payload"].append({"name": ch["name"], "src": url, "type": ch["group"]})

    with open(M3U_FILE, "w", encoding="utf-8") as f: f.write("\n".join(m3u_lines))
    with open(JSON_FILE, "w", encoding="utf-8") as f: json.dump(json_payload, f, indent=2)
    print("✅ Files Updated!")

if __name__ == "__main__":
    main()
