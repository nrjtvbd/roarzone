import requests
import re
import os

def get_roarzone_token():
    url = "https://tv.roarzone.info/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'Referer': 'https://tv.roarzone.info/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # টোকেন খুঁজে বের করার উন্নত লজিক
        token_match = re.search(r'token=([a-zA-Z0-9.-]+)', response.text)
        if token_match:
            return token_match.group(1)
    except Exception as e:
        print(f"Error fetching token: {e}")
    return None

def create_playlist():
    token = get_roarzone_token()
    if not token:
        print("Failed to get token. Script stopping.")
        return

    # আপনার ৯১টি চ্যানেলের আইডি এখানে যোগ করুন (উদাহরণ স্বরূপ ৫টি দেওয়া হলো)
    channels = [
        {"name": "STAR SPORTS 1 HD", "id": "star-sports-1"},
        {"name": "STAR SPORTS 2 HD", "id": "star-sports-2"},
        {"name": "T-SPORTS HD", "id": "t-sports-hd"},
        {"name": "SONY TEN 1", "id": "sony-ten-1"},
        {"name": "SONY TEN 2", "id": "sony-ten-2"}
        # এভাবে আপনার সব চ্যানেলের আইডি যোগ করুন
    ]

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in channels:
            # Roarzone এর নতুন ইউআরএল ফরম্যাট এবং পোর্ট ৮৪৪৭
            stream_url = f"https://edge2.roarzone.info:8447/roarzone/edge2/{ch['id']}/index.m3u8?token={token}"
            f.write(f"#EXTINF:-1, {ch['name']}\n")
            f.write(f"{stream_url}\n")
    print("Playlist updated successfully!")

if __name__ == "__main__":
    create_playlist()
