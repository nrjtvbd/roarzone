import requests
import re
import sys

def get_roarzone_token():
    url = "https://tv.roarzone.info/"
    session = requests.Session()
    # ব্রাউজারকে হুবহু নকল করার জন্য এই হেডারগুলো দেওয়া হয়েছে
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://tv.roarzone.info/'
    }
    
    try:
        response = session.get(url, headers=headers, timeout=15)
        # সব ধরণের টোকেন ফরম্যাট চেক করা হচ্ছে
        patterns = [
            r'token=([a-zA-Z0-9\._-]+)', 
            r'["\']token["\']\s*[:=]\s*["\']([a-zA-Z0-9\._-]+)["\']',
            r'[\?&]token=([^"\'&\s>]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response.text)
            if match:
                token = match.group(1)
                print(f"Token found: {token}")
                return token
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    token = get_roarzone_token()
    if not token:
        print("Failed to find token. Check site source.")
        sys.exit(1) # এটি গিটহাবে লাল ক্রস দেখাবে যাতে আমরা লগ দেখতে পারি

    # আপনার চ্যানেল আইডিগুলো এখানে দিন
    channels = [
        {"name": "STAR SPORTS 1 HD", "id": "star-sports-1"},
        {"name": "STAR SPORTS 2 HD", "id": "star-sports-2"},
        {"name": "T-SPORTS HD", "id": "t-sports-hd"}
    ]

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in channels:
            # আপনার স্নিফিং ডাটা অনুযায়ী পোর্ট ৮৪৪৭
            f.write(f"#EXTINF:-1, {ch['name']}\n")
            f.write(f"https://edge2.roarzone.info:8447/roarzone/edge2/{ch['id']}/index.m3u8?token={token}\n")
    print("Success: playlist.m3u updated.")

if __name__ == "__main__":
    main()
