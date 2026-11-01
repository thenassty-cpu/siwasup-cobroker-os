import re

admin_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\admin_lobby_manager.html"
with open(admin_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Clear DEFAULT_DATA pending in admin_lobby_manager.html
text = re.sub(r'const DEFAULT_DATA = \{\s*pending:\s*\[[\s\S]*?\],\s*approved:', 'const DEFAULT_DATA = {\n      pending: [],\n      approved:', text)

# 2. Remove simulate applicant button
text = re.sub(r'<button onclick="addSimulatedApplicant\(\)"[\s\S]*?</button>', '', text)

with open(admin_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Cleaned admin_lobby_manager.html")

# 3. Clean agent_registration.html
reg_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\agent_registration.html"
with open(reg_path, "r", encoding="utf-8") as f:
    reg_text = f.read()

# Remove the quick simulation bar
reg_text = re.sub(r'<!-- Quick Simulation Bar[\s\S]*?</div>\s*</div>\s*</div>', '</div>', reg_text)

with open(reg_path, "w", encoding="utf-8") as f:
    f.write(reg_text)

print("Cleaned agent_registration.html")
