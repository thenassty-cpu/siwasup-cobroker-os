import os
import re

base_dir = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
files_to_update = [
    "admin_lobby_manager.html",
    "agent_registration.html",
    "agent_onboarding_qr.html",
    "gool_executive_dashboard.html",
    "agent_profile.html",
    "executive_quick_hub.html"
]

old_word = "ศิวาสัพย์"
new_word = "ศิวาทรัพย์"

for fname in files_to_update:
    path = os.path.join(base_dir, fname)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        cnt = content.count(old_word)
        if cnt > 0:
            content = content.replace(old_word, new_word)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Replaced {cnt} occurrences in {fname}")
        else:
            print(f"No occurrences in {fname}")
