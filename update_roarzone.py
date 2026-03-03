import requests
import re

def get_roarzone_token():
    # Roarzone এর পেজ থেকে টোকেন সংগ্রহ
    url = "https://tv.roarzone.info/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://tv.roarzone.info/',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        # টোকেন খোঁজার জন্য শক্তিশালী Regex
        # আপনার দেওয়া ডাটা অনুযায়ী টোকেন ফরম্যাট: 6b08b8dc...
        token_match = re.search(r'token=([a-zA-Z0-9.-]+)', response.text)
        
        if token_match:
            return token_match.group(1)
        else:
            # যদি টোকেন না পায় তবে পেজ সোর্স প্রিন্ট করবে লগ দেখার জন্য
            print("Token not found in HTML. Check if site structure changed.")
            return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def main():
    token = get_roarzone_token()
    if not token:
        print("Stopping: No token found.")
        return

    channels = [
        {"name": "STAR SPORTS 1 HD", "id": "star-sports-1"},
        {"name": "STAR SPORTS 2 HD", "id": "star-sports-2"},
        {"name": "T-SPORTS HD", "id": "t-sports-hd"}
        # এখানে আপনার বাকি আইডিগুলো যোগ করুন
    ]

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in channels:
            # আপনার স্নিফিং ডাটা অনুযায়ী পোর্ট ৮৪৪৭
            stream_url = f"https://edge2.roarzone.info:8447/roarzone/edge2/{ch['id']}/index.m3u8?token={token}"
            f.write(f"#EXTINF:-1, {ch['name']}\n")
            f.write(f"{stream_url}\n")
    print("Playlist updated successfully!")

if __name__ == "__main__":
    main()
