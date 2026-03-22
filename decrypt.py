import zipfile
import os
import shutil

# --- CONFIGURATION ---
zip_filename = 'roarzone_main.zip'
extract_folder = 'temp_roar'
zip_password = os.getenv("ZIP_PASS")

def main():
    if not zip_password:
        print("❌ Error: ZIP_PASS not set.")
        return

    try:
        # ১. জিপ ফাইল আনজিপ করা
        with zipfile.ZipFile(zip_filename) as zf:
            zf.extractall(path=extract_folder, pwd=zip_password.encode('utf-8'))
            print("✅ Successfully decrypted files.")

        # ২. আনজিপ করা ফোল্ডারে ঢুকে স্ক্রিপ্ট রান করা
        original_dir = os.getcwd()
        script_path = os.path.join(extract_folder, "update_roarzone.py")
        
        if os.path.exists(script_path):
            os.chdir(extract_folder)
            os.system("python update_roarzone.py")
            
            # ৩. তৈরি হওয়া আউটপুট ফাইলগুলো মেইন ডিরেক্টরিতে মুভ করা
            # এখানে আপনার আউটপুট ফাইলগুলোর নাম নিশ্চিত করুন
            output_files = ['RoarZone.m3u', 'RoarZone_data.json'] 
            for f in output_files:
                if os.path.exists(f):
                    shutil.move(f, os.path.join(original_dir, f))
            
            os.chdir(original_dir)
            print("🚀 Script execution and file moving complete.")
        else:
            print("❌ Error: update_roarzone.py not found!")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
    
    finally:
        if os.path.exists(extract_folder):
            shutil.rmtree(extract_folder)
            print("🧹 Cleanup done.")

if __name__ == "__main__":
    main()
