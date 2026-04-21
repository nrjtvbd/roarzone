import requests
import json
import os

# GitHub Secrets theke API URL neya hobe
API_URL = os.getenv("API_URL")
M3U_FILE = "sys_config_cache_v9.m3u"
JSON_FILE = "internal_data_v9.json"

def update_roarzone():
    if not API_URL:
        print("❌ Error: API_URL environment variable-ti pawa jayni!")
        return

    try:
        print("🌐 Fetching data from Monirul's API...")
        response = requests.get(API_URL, timeout=15)
        response.raise_for_status()
        data = response.json()

        # JSON theke channel list neya
        channels = data.get("response", [])
        if not channels:
            print("❌ No channels found in API.")
            return

        m3u_lines = ["#EXTM3U"]
        json_payload = {"status": "active", "updated": True, "payload": []}

        for ch in channels:
            name = ch.get("name", "Unknown")
            url = ch.get("url", "")
            logo = ch.get("logo", "")
            group = ch.get("group", "bangla")

            if url:
                # M3U Format
                m3u_lines.append(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}')
                m3u_lines.append(url)
                
                # Internal JSON Format
                json_payload["payload"].append({
                    "name": name,
                    "src": url,
                    "type": group,
                    "logo": logo
                })

        # File save kora
        with open(M3U_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(m3u_lines))
        
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(json_payload, f, indent=2)

        print(f"✅ Success! {len(channels)} channels updated.")

    except Exception as e:
        print(f"❌ Failed to update: {str(e)}")

if __name__ == "__main__":
    update_roarzone()
