import requests
import re
import json
import os
import time

# --- CONFIGURATION ---
M3U_FILE = "sys_config_cache_v9.m3u"
JSON_FILE = "internal_data_v9.json"

CHANNELS = [
    {"id": "tsports", "name": "T Sports", "group": "Sports"},
    {"id": "gazi", "name": "Gazi TV", "group": "Sports"},
    {"id": "somoy", "name": "Somoy TV", "group": "News"},
    {"id": "atnnews", "name": "ATN News", "group": "News"}
]

def get_roar_token():
    print("🌐 Attempting to fetch token via direct API handshake...")
    
    # এটি একটি আসল ব্রাউজারের হেডার অনুকরণ করে
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Referer': 'https://tv.roarzone.net/',
        'Origin': 'https://tv.roarzone.net',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    session = requests.Session()
    
    try:
        # ১. প্রথমে মেইন সাইট ভিজিট করে কুকি সংগ্রহ করা
        session.get("https://tv.roarzone.net/", headers=headers, timeout=15)
        
        # ২. প্লেয়ার পেজ থেকে টোকেন এক্সট্রাক্ট করা
        response = session.get("https://tv.roarzone.net/player.php?stream=tsports", headers=headers, timeout=15)
        html = response.text
        
        # টোকেন খোঁজার প্যাটার্ন (Regex)
        token_match = re.search(r'token=([a-zA-Z0-9]{30,}-[a-zA-Z0-9]{30,}-\d+-\d+)', html)
        if not token_match:
            token_match = re.search(r'token=([a-zA-Z0-9\._-]{40,})', html)
            
        if token_match:
            tk = token_match.group(1)
            print(f"✅ Success! Token Extracted: {tk[:20]}...")
            return tk
        else:
            print("❌ HTML-এ টোকেন পাওয়া যায়নি। প্রোটেকশন বেশি কড়া।")
            
    except Exception as e:
        print(f"❌ Handshake Error: {e}")
    return None

def main():
    token = get_roar_token()
    if not token:
        return

    m3u_lines = ["#EXTM3U"]
    json_payload = {"status": "active", "updated": True, "payload": []}

    for ch in CHANNELS:
        # Port 444 এবং Edge2 পাথ ব্যবহার করা হয়েছে
        stream_url = f"https://edge2.roarzone.net:444/roarzone/edge2/{ch['id']}/index.m3u8?token={token}"
        
        m3u_lines.append(f'#EXTINF:-1 group-title="{ch["group"]}", {ch["name"]}')
        m3u_lines.append(stream_url)
        
        json_payload["payload"].append({
            "name": ch["name"],
            "src": stream_url,
            "type": ch["group"]
        })

    with open(M3U_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(json_payload, f, indent=2)
    
    print(f"✅ Playlist updated with {len(CHANNELS)} channels.")

if __name__ == "__main__":
    main()
