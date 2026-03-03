import requests
import re

def get_roarzone_token():
    # Roarzone এর পেজ থেকে লেটেস্ট টোকেন খোঁজা
    url = "https://tv.roarzone.info/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'Referer': 'https://tv.roarzone.info/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # রেগুলার এক্সপ্রেশন দিয়ে টোকেন অংশটি বের করা
        token_match = re.search(r'token=([a-zA-Z0-9-]+)', response.text)
        if token_match:
            return token_match.group(1)
    except:
        pass
    return None

def create_m3u_file():
    token = get_roarzone_token()
    if not token:
        print("Token not found!")
        return

    # আপনার চ্যানেলের লিস্ট (উদাহরণস্বরূপ কয়েকটি দেওয়া হলো)
    channels = [
        {"name": "STAR SPORTS 1 HD", "id": "star-sports-1"},
        {"name": "STAR SPORTS 2 HD", "id": "star-sports-2"},
        {"name": "T-SPORTS HD", "id": "t-sports-hd"}
    ]

    # playlist.m3u ফাইল তৈরি করা
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in channels:
            # Roarzone এর ফরম্যাট অনুযায়ী লিঙ্ক তৈরি
            stream_url = f"https://edge2.roarzone.info:8447/roarzone/edge2/{ch['id']}/index.m3u8?token={token}"
            f.write(f"#EXTINF:-1, {ch['name']}\n")
            f.write(f"{stream_url}\n")

if __name__ == "__main__":
    create_m3u_file()
