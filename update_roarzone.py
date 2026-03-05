import requests
import re
import json
import os

# --- CONFIGURATION ---
AUTH_KEY = "Rayhan52247S"  # প্লেলিস্টের লিঙ্কের সিকিউরিটির জন্য

def get_token():
    url = "https://tv.roarzone.info/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://tv.roarzone.info/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        iframe_match = re.search(r'src=["\']player\.php\?stream=([^"\'\s>]+)["\']', response.text)
        if iframe_match:
            player_url = f"https://tv.roarzone.info/player.php?stream={iframe_match.group(1)}"
            player_res = requests.Session().get(player_url, headers=headers, timeout=10)
            token_in_player = re.search(r'token=([a-zA-Z0-9\._-]{20,})', player_res.text)
            if token_in_player:
                return token_in_player.group(1)
        return None
    except:
        return None

def extract_channels_from_file(filename):
    channels = []
    if not os.path.exists(filename):
        print(f"❌ {filename} file-ti paowa jayni!")
        return channels

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
    pattern = r'data-title="([^"]+)"\s+data-tags="([^"]+)"\s+data-stream="([^"]+)"'
    matches = re.findall(pattern, content)

    for match in matches:
        title, cat, stream_id = match
        channels.append({
            "id": stream_id,
            "title": title.title(),
            "cat": cat
        })
    return channels

def main():
    token = get_token()
    if not token:
        print("❌ Token find korte somossya hochchhe!")
        return

    channels = extract_channels_from_file("roarzone.txt")
    
    if not channels:
        print("❌ roarzone.txt theke kono channel extract kora jayni!")
        return

    m3u_content = "#EXTM3U\n"
    json_data = {
        "status": "success",
        "total_channels": len(channels),
        "response": []
    }

    for ch in channels:
        # লিঙ্কের শেষে key= যোগ করা হয়েছে
        url = f"https://edge2.roarzone.info:8447/roarzone/{ch['id']}/index.m3u8?token={token}&key={AUTH_KEY}"
        
        m3u_content += f"#EXTINF:-1, {ch['title']}\n{url}\n"
        
        json_data["response"].append({
            "id": ch['id'],
            "title": ch['title'],
            "url": url,
            "category": ch['cat']
        })

    with open("RoarZone.m3u", "w", encoding="utf-8") as f: f.write(m3u_content)
    with open("RoarZone_data.json", "w", encoding="utf-8") as f: json.dump(json_data, f, indent=2)
    
    print(f"✅ Mot {len(channels)}ti channel sofolvabe update hoyeche!")

if __name__ == "__main__":
    main()
