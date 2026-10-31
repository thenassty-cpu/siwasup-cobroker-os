import re

for file_name in ['catalog.html', 'index.html']:
    path = f'C:/Users/ITss-Advice/Documents/GitHub/siwasup-cobroker-os/{file_name}'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix body.modal-open CSS
    # Remove position: fixed, width: 100%, height: 100% so background doesn't vanish/shift
    old_css = """    body.modal-open {
      overflow: hidden !important;
      position: fixed !important;
      width: 100% !important;
      height: 100% !important;
      touch-action: pan-y !important;
      -webkit-overflow-scrolling: auto !important;
    }"""
    
    new_css = """    body.modal-open {
      overflow: hidden !important;
      overscroll-behavior: contain !important;
    }"""

    if old_css in content:
        content = content.replace(old_css, new_css)
        print(f"[{file_name}] Fixed body.modal-open CSS")
    else:
        # Regex replacement in case of small whitespace difference
        content = re.sub(
            r'body\.modal-open\s*\{[\s\S]*?\}',
            'body.modal-open {\n      overflow: hidden !important;\n      overscroll-behavior: contain !important;\n    }',
            content
        )
        print(f"[{file_name}] Replaced body.modal-open via regex")

    # 2. Fix .modal-backdrop CSS to elegant semi-transparent frosted bokeh glass
    old_backdrop = """    .modal-backdrop {
      position: fixed;
      inset: 0;
      z-index: 50;
      background-color: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(4px);
      -webkit-backdrop-filter: blur(4px);"""

    new_backdrop = """    .modal-backdrop {
      position: fixed;
      inset: 0;
      z-index: 50;
      background-color: rgba(15, 23, 42, 0.45);
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);"""

    if old_backdrop in content:
        content = content.replace(old_backdrop, new_backdrop)
        print(f"[{file_name}] Fixed .modal-backdrop frosted glass background")

    # 3. Fix lockBodyScroll and unlockBodyScroll JS
    old_lock_js = """    function lockBodyScroll() {
      if (isBodyScrollLocked) return;
      modalSavedScrollY = window.scrollY || window.pageYOffset || 0;
      isBodyScrollLocked = true;
      document.body.classList.add('modal-open');
      document.body.style.top = `-${modalSavedScrollY}px`;
    }

    function unlockBodyScroll() {
      if (!isBodyScrollLocked) return;
      const visibleModals = document.querySelectorAll('.modal-backdrop:not(.hidden)');
      if (visibleModals.length > 0) return;

      isBodyScrollLocked = false;
      document.body.classList.remove('modal-open');
      const scrollY = modalSavedScrollY;
      document.body.style.top = '';
      window.scrollTo(0, scrollY);
    }"""

    new_lock_js = """    function lockBodyScroll() {
      if (isBodyScrollLocked) return;
      isBodyScrollLocked = true;
      document.body.classList.add('modal-open');
    }

    function unlockBodyScroll() {
      const visibleModals = document.querySelectorAll('.modal-backdrop:not(.hidden)');
      if (visibleModals.length > 0) return;

      isBodyScrollLocked = false;
      document.body.classList.remove('modal-open');
      document.body.style.top = '';
    }"""

    if old_lock_js in content:
        content = content.replace(old_lock_js, new_lock_js)
        print(f"[{file_name}] Fixed lockBodyScroll / unlockBodyScroll JS")
    else:
        # Regex replacement
        content = re.sub(
            r'function lockBodyScroll\(\)\s*\{[\s\S]*?window\.scrollTo\(0, scrollY\);\s*\}',
            new_lock_js.strip(),
            content
        )
        print(f"[{file_name}] Fixed lockBodyScroll via regex")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("catalog.html & index.html patched successfully.")
