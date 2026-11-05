import json
import os
import glob

REPO_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"

# 1. Check all_properties.json
all_prop_path = os.path.join(REPO_DIR, "siwasup_all_properties.json")
if os.path.exists(all_prop_path):
    with open(all_prop_path, "r", encoding="utf-8") as f:
        props = json.load(f)
    banks = {}
    ttb_props = []
    for p in props:
        b = p.get("bank_source") or p.get("b") or "Unknown"
        banks[b] = banks.get(b, 0) + 1
        if "ttb" in str(b).lower() or "tmb" in str(b).lower():
            ttb_props.append(p)

    print("=== BANKS IN siwasup_all_properties.json ===")
    for k, v in sorted(banks.items(), key=lambda x: x[1], reverse=True):
        print(f"  {k}: {v}")
    print(f"  -> Total TTB items in master JSON: {len(ttb_props)}")

# 2. Search for TTB raw data in repo
print("\n=== SEARCHING TTB FILES IN REPO ===")
for root, dirs, files in os.walk(REPO_DIR):
    for file in files:
        if "ttb" in file.lower() or "tmb" in file.lower():
            fpath = os.path.join(root, file)
            print(f"  Found file: {fpath} ({os.path.getsize(fpath)} bytes)")
