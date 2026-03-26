import zipfile
import os
import subprocess

# GitHub Secret থেকে পাসওয়ার্ড নেওয়া
password = os.environ.get('ZIP_PASS')
zip_file = 'roarzone_main.zip'

try:
    with zipfile.ZipFile(zip_file, 'r') as z:
        # পাসওয়ার্ড দিয়ে আনজিপ করা
        z.extractall(pwd=password.encode())
    
    # এবার আপডেট স্ক্রিপ্টটি রান করা
    subprocess.run(['python', 'update_roarzone.py'], check=True)

    # নতুন নাম অনুযায়ী ফাইলগুলো মেইন ডিরেক্টরিতে নিশ্চিত করা
    # (যদি আপনার স্ক্রিপ্ট সরাসরি রুট ডিরেক্টরিতে সেভ না করে থাকে)
    files_to_move = ['sys_config_cache_v9.m3u', 'internal_data_v9.json']
    for f in files_to_move:
        if os.path.exists(f):
            print(f"✅ {f} তৈরি হয়েছে।")
        else:
            print(f"❌ {f} খুঁজে পাওয়া যায়নি!")

    print("🚀 Script execution and file moving complete.")

except Exception as e:
    print(f"❌ An error occurred: {e}")
finally:
    # ক্লিনআপ
    if os.path.exists('update_roarzone.py'): os.remove('update_roarzone.py')
    if os.path.exists('roarzone.txt'): os.remove('roarzone.txt')
    print("🧹 Cleanup done.")
