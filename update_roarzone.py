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
    {"id": "edge2/ptv-sports", "title": "PTV Sports", "cat": "sports"},
    {"id": "edge2/a-sports", "title": "ASPORTS", "cat": "sports"},
    {"id": "edge2/sony-sports-1-hd", "title": "Sony Ten 1", "cat": "sports"},
    {"id": "edge2/sony-sports-2-hd", "title": "Sony Ten 2", "cat": "sports"},
    {"id": "edge2/sony-sports-3-hd", "title": "Sony Ten 3", "cat": "sports"},
    {"id": "edge2/sony-sports-5-hd", "title": "Sony SIX", "cat": "sports"},
    {"id": "edge2/star-sports-select-1", "title": "Star Sports Select 1", "cat": "sports"},
    {"id": "edge2/star-sports-select-2", "title": "Star Sports Select 2", "cat": "sports"},
    {"id": "edge3/euro-sport-hd", "title": "Euro Sports", "cat": "sports"},
    {"id": "bk/dubai-sports", "title": "Dubai Sports", "cat": "sports"},
    {"id": "edge3/sony-ten-cricket", "title": "Ten Cricket", "cat": "sports"},
    {"id": "edge2/star-gold", "title": "Star Gold", "cat": "hindi"},
    {"id": "edge3/sony-entertainment-television-hd", "title": "Sony TV", "cat": "hindi"},
    {"id": "edge3/sony-max", "title": "Sony Max", "cat": "hindi"},
    {"id": "edge3/sony-max-hd", "title": "Sony Max HD", "cat": "hindi"},
    {"id": "edge2/colors", "title": "Colors", "cat": "hindi"},
    {"id": "edge3/sony-max-2", "title": "Sony Max 2", "cat": "hindi"},
    {"id": "edge3/zee-tv-hd", "title": "ZEE TV", "cat": "hindi"},
    {"id": "edge3/zee-cinema-hd", "title": "Zee Cinema", "cat": "hindi"},
    {"id": "edge3/zee-bollywood", "title": "ZEE Bollywood", "cat": "hindi"},
    {"id": "edge3/zee-action", "title": "Zee Action", "cat": "hindi"},
    {"id": "bk/67", "title": "Star Plus", "cat": "hindi"},
    {"id": "edge3/tv-hd", "title": "And TV HD", "cat": "hindi"},
    {"id": "edge3/pictures-hd", "title": "And Pictures", "cat": "hindi"},
    {"id": "edge3/hum", "title": "Hum TV", "cat": "hindi"},
    {"id": "edge3/zee-anmol", "title": "Zee Anmol", "cat": "hindi"},
    {"id": "edge3/hum-masala", "title": "Hum Masala", "cat": "hindi"},
    {"id": "edge3/hum-sitaray", "title": "Hum Sitarey", "cat": "hindi"},
    {"id": "edge3/b4u-movies-apac", "title": "B4U Movies", "cat": "hindi"},
    {"id": "edge3/sony-sab-hd", "title": "Sony SAB", "cat": "hindi"},
    {"id": "edge3/discovery-hd", "title": "Discovery HD", "cat": "documentary"},
    {"id": "edge3/discovery-science", "title": "Discovery Science", "cat": "documentary"},
    {"id": "edge3/discovery-turbo", "title": "Discovery Turbo", "cat": "documentary"},
    {"id": "edge3/investigation-discovery-hd", "title": "Discovery HD Investigation", "cat": "documentary"},
    {"id": "edge3/cnn", "title": "CNN", "cat": "documentary"},
    {"id": "edge3/sony-bbc-earth-hd", "title": "Sony BBC Earth HD", "cat": "documentary"},
    {"id": "bk/35", "title": "Natgeo", "cat": "documentary"},
    {"id": "edge3/animal-planet-hd", "title": "Animal Planet", "cat": "documentary"},
    {"id": "edge2/star-jalsha", "title": "Star Jalsha", "cat": "inbangla"},
    {"id": "edge2/jalsha-movies", "title": "Star Jalsha Movies", "cat": "inbangla"},
    {"id": "edge3/zee-bangla", "title": "Zee Bangla", "cat": "inbangla"},
    {"id": "edge3/zee-bangla-cinema", "title": "ZEE Bangla Cinema", "cat": "inbangla"},
    {"id": "edge2/colors-bangla", "title": "Colors Bangla", "cat": "inbangla"},
    {"id": "edge3/sony-aath", "title": "Sony Aath", "cat": "inbangla"},
    {"id": "edge3/cartoon-network-hd", "title": "Cartoon Network HD", "cat": "kids"},
    {"id": "edge3/cartoon-network", "title": "Cartoon Network", "cat": "kids"},
    {"id": "bk/55", "title": "Nick", "cat": "kids"},
    {"id": "edge3/pogo", "title": "POGO", "cat": "kids"},
    {"id": "edge3/discovery-kids", "title": "Discovery Kids", "cat": "kids"},
    {"id": "edge3/sony-yay", "title": "Sony Yay", "cat": "kids"},
    {"id": "bk/starmovies", "title": "Star Movies", "cat": "english"},
    {"id": "edge3/zee-cafe", "title": "Zee Cafe HD", "cat": "english"},
    {"id": "edge3/sony-pix-hd", "title": "Sony Pix", "cat": "english"},
    {"id": "bk/85", "title": "DW NEWS", "cat": "english"},
    {"id": "bk/89", "title": "Al Jazeera", "cat": "english"},
    {"id": "edge3/tlc-hd", "title": "TLC HD", "cat": "english"},
    {"id": "bk/1", "title": "BTV World", "cat": "bangla"},
    {"id": "bk/10", "title": "NTV", "cat": "bangla"},
    {"id": "bk/11", "title": "RTV", "cat": "bangla"},
    {"id": "bk/12", "title": "Atn Bangla", "cat": "bangla"},
    {"id": "bk/13", "title": "Channel I", "cat": "bangla"},
    {"id": "bk/14", "title": "Ekushey Tv", "cat": "bangla"},
    {"id": "bk/16", "title": "Banglavision", "cat": "bangla"},
    {"id": "bk/17", "title": "Maasranga Tv", "cat": "bangla"},
    {"id": "bk/18", "title": "Independent Tv", "cat": "bangla"},
    {"id": "bk/19", "title": "Somoy Tv", "cat": "bangla"},
    {"id": "bk/20", "title": "Channel 24", "cat": "bangla"},
    {"id": "bk/21", "title": "Ekattor Tv", "cat": "bangla"},
    {"id": "bk/22", "title": "News 24", "cat": "bangla"},
    {"id": "bk/23", "title": "Dbc News", "cat": "bangla"},
    {"id": "bk/15", "title": "Sa Tv", "cat": "bangla"},
    {"id": "bk/88", "title": "Sangsad Tv", "cat": "bangla"},
    {"id": "bk/99", "title": "Btv Chittagong", "cat": "bangla"},
    {"id": "edge3/hbo-hd", "title": "HBO HD", "cat": "english"},
    {"id": "edge3/movies-now-hd", "title": "Movies Now HD", "cat": "english"},
    {"id": "edge3/mnx-hd", "title": "MNX HD", "cat": "english"},
    {"id": "edge3/romedy-now-hd", "title": "Romedy Now HD", "cat": "english"},
    {"id": "edge3/star-movies-hd", "title": "Star Movies HD (Edge)", "cat": "english"},
    {"id": "edge3/wb-tv", "title": "WB TV", "cat": "english"},
    {"id": "edge3/mtv-hd", "title": "MTV HD", "cat": "music"},
    {"id": "edge3/mtv-beats", "title": "MTV Beats", "cat": "music"},
    {"id": "edge3/9xm", "title": "9XM", "cat": "music"},
    {"id": "edge3/zoom", "title": "Zoom TV", "cat": "music"},
    {"id": "edge3/v-h1-hd", "title": "VH1 HD", "cat": "music"},
    {"id": "edge3/nick-hd", "title": "Nick HD", "cat": "kids"},
    {"id": "edge3/nick-jr", "title": "Nick Jr", "cat": "kids"},
    {"id": "edge3/sonic-nickelodeon", "title": "Sonic Nickelodeon", "cat": "kids"},
    {"id": "edge3/disney-channel", "title": "Disney Channel", "cat": "kids"},
    {"id": "edge3/disney-junior", "title": "Disney Junior", "cat": "kids"},
    {"id": "edge3/hungama", "title": "Hungama", "cat": "kids"},
    {"id": "edge3/nat-geo-wild-hd", "title": "Nat Geo Wild HD", "cat": "documentary"},
    {"id": "edge3/history-tv18-hd", "title": "History TV18 HD", "cat": "documentary"},
    {"id": "edge3/jalsha-movies-hd", "title": "Jalsha Movies HD", "cat": "inbangla"},
    {"id": "edge3/sun-bangla", "title": "Sun Bangla", "cat": "inbangla"},
    {"id": "bk/gazi", "title": "GTV (Backup)", "cat": "bangla"}
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
