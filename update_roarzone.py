import requests
import re
import os

def get_roarzone_token():
    """Roarzone ওয়েবসাইট থেকে লেটেস্ট স্ট্রিমিং টোকেন খুঁজে বের করে"""
    url = "https://tv.roarzone.info/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'Referer': 'https://tv.roarzone.info/'
    }
    
    try:
        print("Fetching Roarzone page...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # টোকেন খোঁজার জন্য রেগুলার এক্সপ্রেশন
        # এটি 'token=...' ফরম্যাটের যেকোনো আলফানিউমেরিক স্ট্রিং খুঁজে নেবে
        token_match = re.search(r'token=([a-zA-Z0-9\._-]+)', response.text)
        
        if token_match:
            token = token_match.group(1)
            print(f"Success! Found Token: {token}")
            return token
        else:
            print("Error: Could not find token in the page source.")
            return None
            
    except Exception as e:
        print(f"Network Error: {e}")
        return None

def create_playlist(token):
    """টোকেন ব্যবহার করে m3u প্লেলিস্ট তৈরি করে"""
    
    # আপনার চ্যানেলের লিস্ট এখানে যুক্ত করুন (ID গুলো ওয়েবসাইট থেকে নেওয়া)
    channels = [
        {"name": "STAR SPORTS 1 HD", "id": "star-sports-1"},
        {"name": "STAR SPORTS 2 HD", "id": "star-sports-2"},
        {"name": "T-SPORTS HD", "id": "t-sports-hd"},
        {"name": "SONY TEN 1", "id": "sony-ten-1"},
        {"name": "SONY TEN 2", "id": "sony-ten-2"},
        {"name": "SONY TEN 3", "id": "sony-ten-3"},
        {"name": "SONY SIX", "id": "sony-six-hd"},
        {"name": "PARY TIMES", "id": "pary-times"},
        # আপনার বাকি চ্যানেলগুলো এই ফরম্যাটে এখানে যোগ করতে পারেন
    ]

    filename = "playlist.m3u"
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for ch in channels:
                # Roarzone এর নতুন ফরম্যাট অনুযায়ী পোর্ট ৮৪৪৭ সহ লিঙ্ক
                stream_url = f"https://edge2.roarzone.info:8447/roarzone/edge2/{ch['id']}/index.m3u8?token={token}"
                f.write(f"#EXTINF:-1, {ch['name']}\n")
                f.write(f"{stream_url}\n")
        
        print(f"Successfully updated {filename} with {len(channels)} channels.")
        
    except Exception as e:
        print(f"File Error: Could not write to {filename}. Error: {e}")

if __name__ == "__main__":
    # ১. টোকেন সংগ্রহ করা
    current_token = get_roarzone_token()
    
    # ২. যদি টোকেন পাওয়া যায় তবেই প্লেলিস্ট তৈরি করা
    if current_token:
        create_playlist(current_token)
    else:
        print("Script failed: No token available to update playlist.")
