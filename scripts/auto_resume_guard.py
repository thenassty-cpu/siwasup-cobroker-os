import subprocess
import sys
import os
import time
import json

def is_process_running(script_name):
    try:
        output = subprocess.check_output('wmic process get commandline', shell=True).decode('utf-8', errors='ignore')
        for line in output.splitlines():
            if script_name.lower() in line.lower() and "auto_resume_guard" not in line.lower():
                return True
    except Exception:
        pass
    return False

def main():
    base_dir = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
    data_dir = os.path.join(base_dir, "data")
    state_file = os.path.join(data_dir, "r2_images_sync_state.json")
    crawler_script = os.path.join(base_dir, "scripts", "overnight_r2_crawler.py")
    server_script = os.path.join(base_dir, "scripts", "dashboard_live_server.py")
    python_exe = sys.executable

    # Check total target vs state
    done_count = 0
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                done_count = len(json.load(f))
        except Exception:
            pass

    # If already fully done (10,672), do not re-run crawler
    if done_count < 10672:
        if not is_process_running("overnight_r2_crawler.py"):
            print(f"[Guardian] Crawler not running. Resuming from {done_count}/10672 properties...")
            subprocess.Popen([python_exe, crawler_script], creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        else:
            print(f"[Guardian] Crawler is already actively running ({done_count}/10672).")
    else:
        print("[Guardian] All 10,672 properties have already been synced!")

    # Check live dashboard server
    if not is_process_running("dashboard_live_server.py"):
        print("[Guardian] Dashboard server not running. Starting server on port 8080...")
        subprocess.Popen([python_exe, server_script], creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    else:
        print("[Guardian] Dashboard server is already running on port 8080.")

if __name__ == '__main__':
    main()
