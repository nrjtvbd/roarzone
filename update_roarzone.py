import requests
import re
import json
import base64

def get_token():
    url = "https://tv.roarzone.info/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://tv.roarzone.info/'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        html = response.text

        # ১. সাধারণ রেগুলার এক্সপ্রেশন (আবার চেষ্টা)
        patterns = [
            r'token=([a-zA-Z0-9\._-]{20,})',
            r'["\']token["\']\s*[:=]\s*["\']([a-zA-Z0-9\._-]+)["\']',
            r'[\?&]token=([^"\'&\s>]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                return match.group(1)

        # ২. প্লেয়ার আইফ্রেম (iframe) থেকে টোকেন খোঁজা
        # আপনার পাঠানো HTML-এ 'player.php?stream=...' ছিল
        iframe_match = re.search(r'src=["\']player\.php\?stream=([^"\'\s>]+)["\']', html)
        if iframe_match:
            # যদি আইফ্রেম থাকে, তবে প্লেয়ার পেজটি ভিজিট করে টোকেন আনা
            player_url = f"https://tv.roarzone.info/player.php?stream={iframe_match.group(1)}"
            player_res = requests.get(player_url, headers=headers, timeout=10)
            token_in_player = re.search(r'token=([a-zA-Z0-9\._-]{20,})', player_res.text)
            if token_in_player:
                return token_in_player.group(1)

        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    token = get_token()
    if not token:
        print("❌ Still No Token! Site is hiding it very well.")
        return

    print(f"✅ Success! Token Found: {token}")

    channels = [
        {"id": "edge2/tsports", "title": "T Sports", "cat": "sports"},
        {"id": "edge2/star-sports-1", "title": "Star Sports 1", "cat": "sports"},
        {"id": "edge2/star-sports-2", "title": "Star Sports 2", "cat": "sports"},
        {"id": "edge2/gazi", "title": "Gazi TV", "cat": "sports"},
        {"id": "bk/15", "title": "Sa Tv", "cat": "bangla"}
    ]

    # ফাইল আপডেট লজিক
    m3u_content = "#EXTM3U\n"
    json_data = {"status": "success", "response": []}

    for ch in channels:
        url = f"https://edge2.roarzone.info:8447/roarzone/{ch['id']}/index.m3u8?token={token}"
        m3u_content += f"#EXTINF:-1, {ch['title']}\n{url}\n"
        json_data["response"].append({"title": ch['title'], "url": url, "category": ch['cat']})

    with open("RoarZone.m3u", "w", encoding="utf-8") as f: f.write(m3u_content)
    with open("RoarZone_data.json", "w", encoding="utf-8") as f: json.dump(json_data, f, indent=2)
    
    print("✅ Files Updated Successfully!")

if __name__ == "__main__":
    main()
