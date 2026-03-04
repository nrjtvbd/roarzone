import requests
import re
import json
import random
import time

def get_token():
    url = "https://tv.roarzone.info/"
    
    # বিভিন্ন ধরণের ব্রাউজার হেডার যা একেক বার একেক রকম দেখাবে
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    ]

    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/', # গুগল থেকে আসছে বলে মনে হবে
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        session = requests.Session()
        # সাইটে যাওয়ার আগে একটু সময় নেওয়া (মানুষের মতো আচরণ)
        time.sleep(random.uniform(1, 3))
        
        response = session.get(url, headers=headers, timeout=20)
        
        # HTML এর ভেতরে টোকেন খোঁজার জন্য ৪টি আলাদা পদ্ধতি
        patterns = [
            r'token=([a-zA-Z0-9\._-]+)',
            r'["\']token["\']\s*[:=]\s*["\']([a-zA-Z0-9\._-]+)["\']',
            r'token\s*=\s*[\'"](.*?)[\'"]',
            r'id=["\']token["\']\s+value=["\'](.*?)["\']'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response.text)
            if match:
                return match.group(1)
        
        # যদি টোকেন না পায় তবে লগের জন্য পেজের কিছু অংশ প্রিন্ট করা
        print("Debug: Page title -", re.search(r'<title>(.*?)</title>', response.text).group(1) if '<title>' in response.text else "No title")
        return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    token = get_token()
    if not token:
        print("❌ Token not found! Server is still blocking.")
        return

    print(f"✅ Token Found: {token}")

    # আপনার প্রয়োজনীয় আইডিগুলো
    channels = [
        {"id": "edge2/tsports", "title": "T Sports", "cat": "sports"},
        {"id": "edge2/star-sports-1", "title": "Star Sports 1", "cat": "sports"},
        {"id": "edge2/star-sports-2", "title": "Star Sports 2", "cat": "sports"},
        {"id": "edge2/gazi", "title": "Gazi TV", "cat": "sports"},
        {"id": "bk/15", "title": "Sa Tv", "cat": "bangla"}
    ]

    json_output = {"status": "success", "response": []}

    with open("RoarZone.m3u", "w", encoding="utf-8") as m3u:
        m3u.write("#EXTM3U\n")
        for ch in channels:
            final_url = f"https://edge2.roarzone.info:8447/roarzone/{ch['id']}/index.m3u8?token={token}"
            m3u.write(f"#EXTINF:-1, {ch['title']}\n{final_url}\n")
            json_output["response"].append({"title": ch['title'], "url": final_url, "category": ch['cat']})

    with open("RoarZone_data.json", "w", encoding="utf-8") as jf:
        json.dump(json_output, jf, indent=2)

    print("✅ Files generated successfully!")

if __name__ == "__main__":
    main()
