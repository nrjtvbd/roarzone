import zipfile
import os
import shutil

# --- CONFIGURATION ---
zip_filename = 'roarzone_main.zip'  # আপনার জিপ ফাইলের নাম
extract_folder = 'temp_roar'        # যেখানে ফাইল আনজিপ হবে
zip_password = os.getenv("ZIP_PASS") # গিটহাব সিক্রেট থেকে পাসওয়ার্ড নেবে

def main():
    if not zip_password:
        print("❌ Error: ZIP_PASS environment variable is not set in GitHub Secrets.")
        return

    try:
        # জিপ ফাইলটি পাসওয়ার্ড দিয়ে আনজিপ করা
        with zipfile.ZipFile(zip_filename) as zf:
            zf.extractall(path=extract_folder, pwd=zip_password.encode('utf-8'))
            print("✅ Successfully decrypted and extracted files.")

        # আনজিপ করা ফোল্ডার থেকে প্রধান স্ক্রিপ্টটি রান করা
        script_path = os.path.join(extract_folder, "update_roarzone.py")
        
        if os.path.exists(script_path):
            print(f"🚀 Running {script_path}...")
            # বর্তমান ডিরেক্টরি সাময়িকভাবে পরিবর্তন করে রান করা যাতে পাথ এরর না হয়
            os.chdir(extract_folder)
            os.system("python update_roarzone.py")
            os.chdir("..") 
        else:
            print(f"❌ Error: update_roarzone.py not found inside the zip!")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
    
    finally:
        # নিরাপত্তার জন্য আনজিপ করা ফাইলগুলো মুছে ফেলা
        if os.path.exists(extract_folder):
            shutil.rmtree(extract_folder)
            print("🧹 Cleanup done: Secret files removed.")

if __name__ == "__main__":
    main()
