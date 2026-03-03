import requests
import re
import json

def get_roarzone_link(channel_slug):
    # Roarzone এর মূল পেজ যেখানে প্লেয়ার থাকে
    page_url = f"https://tv.roarzone.info/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'Referer': 'https://tv.roarzone.info/',
        'Accept': '*/*'
    }

    try:
        # ১. প্রথমে পেজটি লোড করা হচ্ছে ভেতরের স্ক্রিপ্ট থেকে লিঙ্ক খোঁজার জন্য
        response = requests.get(page_url, headers=headers, timeout=10)
        content = response.text

        # ২. রেগুলার এক্সপ্রেশন ব্যবহার করে 'index.m3u8?token=...' অংশটি খুঁজে বের করা
        # Roarzone সাধারণত তাদের সোর্স কোডে বা কোনো JS ফাইলে এই লিঙ্কটি রাখে
        pattern = r'https://[\w\d\.-]+:8447/[\w\d\.-/]+index\.m3u8\?token=[\w\d-]+'
        links = re.findall(pattern, content)

        if links:
            # যদি একাধিক লিঙ্ক থাকে, তবে আপনার কাঙ্ক্ষিত চ্যানেলটি (যেমন star-sports-1) ফিল্টার করা
            for link in links:
                if channel_slug in link:
                    return link
            return links[0] # কিছু না পেলে প্রথম লিঙ্কটিই দিবে
        else:
            return "No link found. Server might be using advanced protection."

    except Exception as e:
        return f"Error: {str(e)}"

# উদাহরণ হিসেবে Star Sports 1 এর লিঙ্ক বের করা
channel_id = "star-sports-1"
final_link = get_roarzone_link(channel_id)

print(f"Updated M3U8 Link: {final_link}")
