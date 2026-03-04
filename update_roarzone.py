import requests
import re
import json

def get_token():
    url = "https://tv.roarzone.info/"
    try:
        res = requests.get(url, timeout=15)
        token = re.search(r'token=([a-zA-Z0-9\._-]+)', res.text)
        return token.group(1) if token else None
    except:
        return None

def create_files(token):
    # আপনার সেই ৯১টি চ্যানেলের আইডি ও নাম
    channels = [
        {"title": "T Sports", "id": "edge2/tsports"},
        {"title": "Star Sports 1", "id": "edge2/star-sports-1"},
        # ... বাকি চ্যানেলগুলো এখানে যোগ হবে
    ]

    # JSON ফাইল অটো তৈরি (যদি আপনার অ্যাপের জন্য লাগে)
    data = {
        "status": "success",
        "Last_update": "2026-03-05",
        "channels": []
    }

    # M3U প্লেলিস্ট তৈরি
    with open("RoarZone.m3u", "w") as m3u:
        m3u.write("#EXTM3U\n")
        for ch in channels:
            url = f"https://edge2.roarzone.info:8447/roarzone/{ch['id']}/index.m3u8?token={token}"
            m3u.write(f"#EXTINF:-1, {ch['title']}\n{url}\n")
            data["channels"].append({"title": ch['title'], "url": url})

    # JSON সেভ করা
    with open("RoarZone_data.json", "w") as j:
        json.dump(data, j, indent=2)

if __name__ == "__main__":
    t = get_token()
    if t:
        create_files(t)
        print("✅ Files updated!")
