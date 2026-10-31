import re

# 1. Patch modals.js
modals_path = 'C:/Users/ITss-Advice/Documents/GitHub/siwasup-cobroker-os/modals.js'
with open(modals_path, 'r', encoding='utf-8') as f:
    modals_content = f.read()

# Remove detail-external-link
old_link = re.search(r'<a id="detail-external-link"[^>]*>[\s\S]*?ดูหน้าเว็บเดิม[\s\S]*?</a>', modals_content)
if old_link:
    print('Found detail-external-link, removing...')
    modals_content = modals_content[:old_link.start()] + modals_content[old_link.end():]
else:
    print('detail-external-link not found by regex')

# Add onerror to detail-main-img
old_img = '<img id="detail-main-img" src="" alt="" class="w-full h-full object-cover">'
new_img = '<img id="detail-main-img" src="" alt="" onerror="this.onerror=null; this.src=\'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=600\';" class="w-full h-full object-cover">'
if old_img in modals_content:
    print('Adding onerror fallback to detail-main-img...')
    modals_content = modals_content.replace(old_img, new_img)

# Add touch-action & smooth scroll to modal body
old_scroll = '<div class="flex-1 overflow-y-auto p-4 sm:p-5 space-y-4 custom-scrollbar">'
new_scroll = '<div class="flex-1 overflow-y-auto p-4 sm:p-5 space-y-4 custom-scrollbar" style="touch-action: pan-y !important; -webkit-overflow-scrolling: touch; overscroll-behavior: contain;">'
if old_scroll in modals_content:
    print('Adding smooth touch scroll to detail modal body...')
    modals_content = modals_content.replace(old_scroll, new_scroll)

with open(modals_path, 'w', encoding='utf-8') as f:
    f.write(modals_content)

print('modals.js successfully patched.')

# 2. Patch catalog.html and index.html
for file_name in ['catalog.html', 'index.html']:
    file_path = f'C:/Users/ITss-Advice/Documents/GitHub/siwasup-cobroker-os/{file_name}'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix mock bank round-robin loop:
    # Instead of assigning mock banks, assign 'Siwasup' to legacy properties without bank_source
    old_bank_loop = """      // Distribute realistic bank sources across mock properties if missing
      const banks = ['SAM', 'SCB', 'KBANK', 'TTB', 'Siwasup', 'KTB', 'GSB', 'PAMCO'];
      allProperties.forEach((p, idx) => {
        if (!p.bank_source) {
          p.bank_source = banks[idx % banks.length];
        }"""
    
    new_bank_loop = """      // Preserve genuine bank source or label legacy company listings as 'Siwasup'
      allProperties.forEach((p) => {
        if (!p.bank_source) {
          p.bank_source = 'Siwasup';
        }"""

    if old_bank_loop in content:
        print(f'Replacing mock bank loop in {file_name}...')
        content = content.replace(old_bank_loop, new_bank_loop)
    else:
        # Try regex replace in case of whitespace difference
        content = re.sub(
            r"// Distribute realistic bank sources[\s\S]*?p\.bank_source = banks\[idx % banks\.length\];\s*}",
            "// Preserve genuine bank source or label legacy company listings as 'Siwasup'\n      allProperties.forEach((p) => {\n        if (!p.bank_source) {\n          p.bank_source = 'Siwasup';\n        }",
            content
        )

    # Fix closePropertyDetailModal to explicitly unlock scroll
    old_close = """    function closePropertyDetailModal() {
      const modal = document.getElementById('property-detail-modal');
      if (modal) modal.classList.add('hidden');
    }"""

    new_close = """    function closePropertyDetailModal() {
      const modal = document.getElementById('property-detail-modal');
      if (modal) modal.classList.add('hidden');
      if (typeof unlockBodyScroll === 'function') {
        unlockBodyScroll();
      }
      document.body.classList.remove('modal-open');
      document.body.style.top = '';
    }"""

    if old_close in content:
        print(f'Patching closePropertyDetailModal in {file_name}...')
        content = content.replace(old_close, new_close)

    # Fix body.modal-open touch-action
    content = content.replace(
        "touch-action: none !important;",
        "touch-action: pan-y !important;"
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'{file_name} successfully patched.')
