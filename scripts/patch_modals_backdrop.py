path = 'C:/Users/ITss-Advice/Documents/GitHub/siwasup-cobroker-os/modals.js'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

old_str = 'class="fixed inset-0 z-50 bg-neutral-950/60 backdrop-blur-xs flex items-center justify-center px-3 pt-10 pb-6 sm:p-6 hidden modal-backdrop"'
new_str = 'class="fixed inset-0 z-50 bg-slate-950/45 backdrop-blur-sm flex items-center justify-center px-3 pt-10 pb-6 sm:p-6 hidden modal-backdrop"'

if old_str in c:
    c = c.replace(old_str, new_str)
    print("Found and replaced backdrop class in modals.js")
else:
    print("old_str not found directly, trying regex...")
    import re
    c = re.sub(r'id="property-detail-modal"[^>]*class="([^"]*)"', 'id="property-detail-modal"\n      onclick="if(event.target === this) closePropertyDetailModal()"\n      class="fixed inset-0 z-50 bg-slate-950/45 backdrop-blur-sm flex items-center justify-center px-3 pt-10 pb-6 sm:p-6 hidden modal-backdrop"', c)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("modals.js saved successfully.")
