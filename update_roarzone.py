import requests
import re
import sys

def get_roarzone_token():
    url = "https://tv.roarzone.info/"
    # ব্রাউজারকে হুবহু নকল করার জন্য এই হেডারগুলো জরুরি
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'Referer': 'https://tv.roarzone.info/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        print("Connecting to Roarzone...")
        response = requests.get(url, headers=headers, timeout=20)
        
        # যদি সার্ভার ব্লক করে (যেমন 403 Forbidden)
        if response.status_code != 200:
            print(f"Error: Server returned status code {response.status_code}")
            return None

        # আপনার দেওয়া ডাটা অনুযায়ী টোকেন খোঁজার প্যাটার্ন
        # এটি HTML সোর্স থেকে 'token=...' অংশটি খুঁজে বের করবে
        html_content = response.text
        token_match = re.search(r'token=([a-zA-Z0-9.-]+)', html_content)
        
        if token_match:
            token = token_match.group(1)
            print(f"Token Successfully Found: {token}")
            return token
        else:
            print("Token not found in HTML source. The site structure might have changed.")
            # লগের জন্য HTML এর প্রথম ৫০০ ক্যারেক্টার প্রিন্ট করা হচ্ছে
            print("HTML Preview:", html_content[:500]) 
            return None

    except Exception as e:
        print(f"Network error occurred: {e}")
        return None

def create_m3u(token):
    channels = [
        {"name": "STAR SPORTS 1 HD", "id": "star-sports-1"},
        {"name": "STAR SPORTS 2 HD", "id": "star-sports-2"},
        {"name": "T-SPORTS HD", "id": "t-sports-hd"},
        {"name": "SONY TEN 1", "id": "sony-ten-1"}
    ]
    
    try:
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for ch in channels:
                # পোর্ট ৮৪৪৭ সহ সঠিক লিঙ্ক তৈরি
                link = f"https://edge2.roarzone.info:8447/roarzone/edge2/{ch['id']}/index.m3u8?token={token}"
                f.write(f"#EXTINF:-1, {ch['name']}\n")
                f.write(f"{link}\n")
        print("playlist.m3u has been updated with new token.")
    except Exception as e:
        print(f"Failed to write file: {e}")

if __name__ == "__main__":
    found_token = get_roarzone_token()
    if found_token:
        create_m3u(found_token)
    else:
        print("Script finished without finding a token.")
        sys.exit(1) # এটি গিটহাবকে লাল ক্রস দেখাবে যাতে আপনি বুঝতে পারেন টোকেন মেলেনি
