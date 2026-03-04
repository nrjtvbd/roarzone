import requests
import re
import json
import os

def get_token():
    url = "https://tv.roarzone.info/"
    # ব্রাউজার হেডার আরও শক্তিশালী করা হয়েছে
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)
        
        # ১. সরাসরি URL থেকে টোকেন খোঁজা
        token_match = re.search(r'token=([a-zA-Z0-9\._-]+)', response.text)
        if token_match:
            return token_match.group(1)
        
        # ২. জাভাস্ক্রিপ্ট ভেরিয়েবল থেকে টোকেন খোঁজা
        token_match = re.search(r'["\']?token["\']?\s*[:=]\s*["\']([a-zA-Z0-9\._-]+)["\']', response.text)
        if token_match:
            return token_match.group(1)
            
        return None
    except Exception as e:
        print(f"Network Error: {e}")
        return None

def main():
    token = get_token()
    if not token:
        print("❌ Token not found! Site might be blocking automated requests.")
        return

    print(f"✅ Token Found: {token}")

    channels = [
        {"id": "edge2/tsports", "title": "T Sports", "cat": "sports"},
        {"id": "edge2/star-sports-1", "title": "Star Sports 1", "cat": "sports"},
        {"id": "edge2/star-sports-2", "title": "Star Sports 2", "cat": "sports"},
        {"id": "edge2/gazi", "title": "Gazi TV", "cat": "sports"},
        {"id": "bk/15", "title": "Sa Tv", "cat": "bangla"}
    ]

    json_output = {"status": "success", "response": []}

    # RoarZone.m3u তৈরি
    with open("RoarZone.m3u", "w", encoding="utf-8") as m3u:
        m3u.write("#EXTM3U\n")
        for ch in channels:
            final_url = f"https://edge2.roarzone.info:8447/roarzone/{ch['id']}/index.m3u8?token={token}"
            m3u.write(f"#EXTINF:-1, {ch['title']}\n{final_url}\n")
            json_output["response"].append({"title": ch['title'], "url": final_url, "category": ch['cat']})

    # RoarZone_data.json তৈরি
    with open("RoarZone_data.json", "w", encoding="utf-8") as jf:
        json.dump(json_output, jf, indent=2)

    print("✅ Success! RoarZone.m3u and RoarZone_data.json updated.")

if __name__ == "__main__":
    main()
