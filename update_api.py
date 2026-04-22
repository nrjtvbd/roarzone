import requests
import re
import json
import os

# আপনার কাঙ্ক্ষিত বেস ইউআরএল এবং চ্যানেলের পাথ
API_BASE_URL = "https://edge2.roarzone.net:444/roarzone"
CHANNELS = {
    "tsports": "edge2/tsports",
    "gtv": "edge1/gtv",
    "gazitv": "edge1/gtv" # উদাহরণস্বরূপ
}

def get_live_api():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
        'Referer': 'https://tv.roarzone.net/'
    }
    
    try:
        # ১. টোকেন সংগ্রহ
        response = requests.get("https://tv.roarzone.net/player.php?stream=tsports", headers=headers, timeout=15)
        token_match = re.search(r'token=([a-zA-Z0-9\._-]{30,})', response.text)
        
        if token_match:
            token = token_match.group(1)
            print(f"✅ Token Found: {token[:10]}...")
            
            # ২. আপনার ফরম্যাট অনুযায়ী JSON ডাটা তৈরি
            api_output = {
                "status": "success",
                "last_updated": os.popen('date').read().strip(),
                "links": {}
            }
            
            for slug, path in CHANNELS.items():
                # আপনার সেই নির্দিষ্ট ইউআরএল ফরম্যাট
                final_api_url = f"{API_BASE_URL}/{path}/tracks-v1a1/mono.m3u8?token={token}"
                api_output["links"][slug] = final_api_url
            
            # ৩. api.json ফাইলে সেভ করা
            with open('api.json', 'w') as f:
                json.dump(api_output, f, indent=4)
            print("🚀 api.json generated successfully!")
            return True
        else:
            print("⚠️ Token not found. GitHub IP restricted.")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    get_live_api()
