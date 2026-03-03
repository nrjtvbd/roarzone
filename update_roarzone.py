import requests
import re
import sys

def get_roarzone_token():
    url = "https://tv.roarzone.info/"
    # সেশন ব্যবহার করা হচ্ছে যাতে কুকি সেভ থাকে
    session = requests.Session()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://tv.roarzone.info/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin'
    }

    try:
        # ১. প্রথমে সাইটে প্রবেশ করে কুকি সংগ্রহ করা
        response = session.get(url, headers=headers, timeout=20)
        
        # ২. রেগুলার এক্সপ্রেশন যা আপনার দেওয়া ডাটা ফরম্যাটকে সাপোর্ট করে
        # এটি HTML সোর্সে থাকা সব 'token=' এর ভ্যালু খুঁজবে
        content = response.text
        token_match = re.search(r'token=([a-zA-Z0-9\._-]+)', content)
        
        if token_match:
            token = token_match.group(1)
            print(f"Token found: {token}")
            return token
        else:
            # যদি সরাসরি না পাওয়া যায়, তবে স্ক্রিপ্ট ট্যাগগুলোর ভেতর খোঁজা
            print("Direct token not found. Checking script tags...")
            script_tokens = re.findall(r'["\']?token["\']?\s*[:=]\s*["\']([a-zA-Z0-9\._-]+)["\']', content)
            if script_tokens:
                print(f"Token found in script: {script_tokens[0]}")
                return script_tokens[0]
                
        print("Could not find any token in the source code.")
        return None

    except Exception as e:
        print(f"Connection Error: {e}")
        return None

def main():
    token = get_roarzone_token()
    if not token:
        print("Stopping script: Token missing.")
        sys.exit(1) # এটি গিটহাবে লাল ক্রস দেখাবে

    # আপনার চ্যানেল লিস্ট
    channels = [
        {"name": "STAR SPORTS 1 HD", "id": "star-sports-1"},
        {"name": "STAR SPORTS 2 HD", "id": "star-sports-2"},
        {"name": "T-SPORTS HD", "id": "t-sports-hd"}
    ]

    try:
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for ch in channels:
                # আপনার দেওয়া পোর্ট ৮৪৪৭ ব্যবহার করা হয়েছে
                stream_url = f"https://edge2.roarzone.info:8447/roarzone/edge2/{ch['id']}/index.m3u8?token={token}"
                f.write(f"#EXTINF:-1, {ch['name']}\n")
                f.write(f"{stream_url}\n")
        print("Success: playlist.m3u updated!")
    except Exception as e:
        print(f"File Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
