import requests
import re
import json
import os

# আপনার চ্যানেলের তথ্য
CHANNELS = [
    {"name": "T Sports", "path": "edge2/tsports"},
    {"name": "Gazi TV", "path": "edge1/gtv"},
    {"name": "Star Sports 1", "path": "edge2/ss1"}
]

def fetch_token():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
        'Referer': 'https://tv.roarzone.net/'
    }
    try:
        # T Sports প্লেয়ার পেজ থেকে টোকেন খোঁজা
        res = requests.get("https://tv.roarzone.net/player.php?stream=tsports", headers=headers, timeout=20)
        match = re.search(r'token=([a-zA-Z0-9\._-]{30,})', res.text)
        return match.group(1) if match else None
    except Exception as e:
        print(f"Error fetching token: {e}")
        return None

def main():
    token = fetch_token()
    if token:
        print(f"✅ Token Found: {token[:15]}...")
        
        api_data = {
            "status": "success",
            "last_updated": os.popen('date').read().strip(),
            "channels": []
        }

        for ch in CHANNELS:
            # আপনার দেওয়া নতুন ফরম্যাট: port 444 এবং tracks-v1a1 পথ
            url = f"https://edge2.roarzone.net:444/roarzone/{ch['path']}/tracks-v1a1/mono.m3u8?token={token}"
            api_data["channels"].append({
                "name": ch["name"],
                "url": url
            })

        # api.json ফাইলে সেভ করা
        with open('api.json', 'w') as f:
            json.dump(api_data, f, indent=4)
        print("🚀 api.json file updated!")
    else:
        print("❌ Token Fetch Failed. Cloudflare might have blocked GitHub IP.")

if __name__ == "__main__":
    main()
