import requests
import re
import sys
import json

def get_token():
    # Roarzone-এর প্লেয়ার পেজ থেকে টোকেন সংগ্রহের চেষ্টা
    url = "https://tv.roarzone.info/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # HTML সোর্স থেকে টোকেন খোঁজা
        token_match = re.search(r'token=([a-zA-Z0-9\._-]+)', response.text)
        if token_match:
            return token_match.group(1)
        return None
    except:
        return None

def main():
    token = get_token()
    if not token:
        print("❌ Token extraction failed!")
        sys.exit(1)

    print(f"✅ Token Found: {token}")

    # আপনার দেওয়া HTML সোর্স থেকে নেওয়া চ্যানেল লিস্ট
    channels = [
        {"title": "T Sports", "id": "edge2/tsports"},
        {"title": "Star Sports 1", "id": "edge2/star-sports-1"},
        {"title": "Star Sports 2", "id": "edge2/star-sports-2"},
        {"title": "Gazi TV", "id": "edge2/gazi"},
        {"title": "Sony Ten 1", "id": "edge2/sony-sports-1-hd"},
        {"title": "Sony Ten 2", "id": "edge2/sony-sports-2-hd"},
        {"title": "Sony Ten 3", "id": "edge2/sony-sports-3-hd"},
        {"title": "Sony SIX", "id": "edge2/sony-sports-5-hd"},
        {"title": "Sony MAX HD", "id": "edge3/sony-max-hd"},
        {"title": "Zee TV HD", "id": "edge3/zee-tv-hd"}
        # আপনি চাইলে এখানে আরও ID যোগ করতে পারেন (HTML-এর data-stream অংশ থেকে)
    ]

    # playlist.m3u তৈরি
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in channels:
            # RoarZone এর সঠিক পোর্ট ও লিঙ্ক ফরম্যাট
            stream_url = f"https://edge2.roarzone.info:8447/roarzone/{ch['id']}/index.m3u8?token={token}"
            f.write(f"#EXTINF:-1, {ch['title']}\n")
            f.write(f"{stream_url}\n")
    
    print("🚀 Playlist updated successfully!")

if __name__ == "__main__":
    main()
