import requests
import re
import json
import os

# আপনার চ্যানেলের তথ্য ও পাথ
CHANNELS = [
    {"name": "T Sports", "path": "edge2/tsports"},
    {"name": "Gazi TV", "path": "edge1/gtv"}
]

def fetch_token():
    # একদম আপনার ব্রাউজারের মতো হেডার ব্যবহার করছি
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
        'Referer': 'https://tv.roarzone.net/',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    try:
        # টোকেন সংগ্রহের জন্য প্লেয়ার পেজ রিকোয়েস্ট
        res = requests.get("https://tv.roarzone.net/player.php?stream=tsports", headers=headers, timeout=20)
        # রেগুলার এক্সপ্রেশন দিয়ে টোকেন খুঁজে বের করা
        match = re.search(r'token=([a-zA-Z0-9\._-]{30,})', res.text)
        return match.group(1) if match else None
    except:
        return None

def main():
    token = fetch_token()
    if token:
        print(f"✅ Token Found: {token[:15]}...")
        
        api_data = {
            "status": "success",
            "channels": []
        }

        for ch in CHANNELS:
            # ঠিক আপনার দেওয়া ফরম্যাট অনুযায়ী লিঙ্ক জেনারেট
            finalUrl = f"https://edge2.roarzone.net:444/roarzone/{ch['path']}/tracks-v1a1/mono.m3u8?token={token}"
            
            api_data["channels"].append({
                "name": ch["name"],
                "url": finalUrl
            })

        with open('api.json', 'w') as f:
            json.dump(api_data, f, indent=4)
        print("🚀 API updated with your exact format!")
    else:
        # এটিই এখন আপনার এরর দিচ্ছে কারণ GitHub IP ব্লকড
        print("❌ Token Fetch Failed. GitHub IP might be blocked by Cloudflare.")

if __name__ == "__main__":
    main()
