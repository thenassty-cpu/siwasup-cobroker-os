import re

with open(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Top Role Utility Bar from black neutral-900 to Heritage Red gradient with Gold border
old_bar = '<div class="bg-neutral-900 text-neutral-300 text-xs py-1.5 px-3 sm:px-4 border-b border-neutral-800">'
new_bar = '<div class="bg-gradient-to-r from-[#8B0000] via-[#700000] to-[#8B0000] text-neutral-100 text-xs py-1.5 px-3 sm:px-4 border-b border-[#C2A460]/40 shadow-xs">'

content = content.replace(old_bar, new_bar)

# 2. Update Top Bar Buttons and Selects from neutral-900/800 to Burgundy & Gold
old_btn_pattern = 'bg-neutral-900 hover:bg-neutral-800 border border-neutral-800 text-neutral-300'
new_btn_pattern = 'bg-[#5C0000] hover:bg-[#780000] border border-[#C2A460]/40 text-neutral-100'

content = content.replace(old_btn_pattern, new_btn_pattern)

# Also other button text variants
content = content.replace(
    'bg-neutral-900 hover:bg-neutral-800 border border-neutral-800 text-neutral-200',
    'bg-[#5C0000] hover:bg-[#780000] border border-[#C2A460]/40 text-neutral-100'
)
content = content.replace(
    'bg-neutral-900 hover:bg-neutral-800 border border-neutral-800 text-[#E5C985]',
    'bg-[#5C0000] hover:bg-[#780000] border border-[#C2A460]/40 text-[#FFE885]'
)

# Mobile role select
content = content.replace(
    'class="lg:hidden bg-neutral-900 text-white font-semibold text-[11px] px-2 py-1 rounded-lg border border-neutral-700',
    'class="lg:hidden bg-[#5C0000] text-white font-semibold text-[11px] px-2 py-1 rounded-lg border border-[#C2A460]/50'
)

# Desktop role tabs container
content = content.replace(
    '<div class="hidden lg:flex items-center bg-neutral-900 p-0.5 rounded-lg border border-neutral-800 text-[11px] ml-1">',
    '<div class="hidden lg:flex items-center bg-[#500000] p-0.5 rounded-lg border border-[#C2A460]/40 text-[11px] ml-1">'
)

with open(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("[OK] Updated index.html: Added Heritage Red, replaced black bars with Burgundy & Gold trims!")
