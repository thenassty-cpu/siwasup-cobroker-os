import re

path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\agent_profile.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# Add tierStarClient
old_tier_badge_inner = '''          <!-- Big Circular Emblem (36px on mobile, 40px on tablet) -->
          <img id="tierEmblemImg" 
               src="assets/badges/Golden__001_lion_web.png" 
               alt="Golden Emblem" 
               class="w-9 h-9 sm:w-10 sm:h-10 object-contain rounded-full bg-slate-900 border border-black shadow-xs shrink-0" 
               onerror="this.onerror=null; this.src='assets/badges/Golden__001_lion.png';" />
          <div class="leading-tight text-left min-w-0 pr-1">'''

new_tier_badge_inner = '''          <!-- Big Circular Emblem (36px on mobile, 40px on tablet) -->
          <img id="tierEmblemImg" 
               src="assets/badges/Golden__001_lion_web.png" 
               alt="Golden Emblem" 
               class="w-9 h-9 sm:w-10 sm:h-10 object-contain rounded-full bg-slate-900 border border-black shadow-xs shrink-0" 
               onerror="this.onerror=null; this.src='assets/badges/Golden__001_lion.png';" />
          <span id="tierStarClient" class="hidden text-slate-950 font-bold pl-2 text-xs shrink-0">✦</span>
          <div class="leading-tight text-left min-w-0 pr-1">'''

html = html.replace(old_tier_badge_inner, new_tier_badge_inner)

# Update setMode
old_set_mode_logic = '''        // Hide animal emblem on client view
        if (tierEmblemImg) tierEmblemImg.classList.add("hidden");
      } else {
        // AGENT VIEW: Show consent box, show share button, hide client call
        if (ctrlBar) ctrlBar.classList.remove("hidden");
        if (execBox) execBox.classList.remove("hidden");
        consentBox.classList.remove("hidden");
        btnShare.classList.remove("hidden");
        btnClientCall.classList.add("hidden");

        // Show Golden Emblem for agent view
        if (tierEmblemImg) tierEmblemImg.classList.remove("hidden");'''

new_set_mode_logic = '''        // Hide animal emblem on client view, show clean prestige star
        if (tierEmblemImg) tierEmblemImg.classList.add("hidden");
        const star = document.getElementById("tierStarClient");
        if (star) star.classList.remove("hidden");
      } else {
        // AGENT VIEW: Show consent box, show share button, hide client call
        if (ctrlBar) ctrlBar.classList.remove("hidden");
        if (execBox) execBox.classList.remove("hidden");
        consentBox.classList.remove("hidden");
        btnShare.classList.remove("hidden");
        btnClientCall.classList.add("hidden");

        // Show Golden Emblem for agent view
        if (tierEmblemImg) tierEmblemImg.classList.remove("hidden");
        const star = document.getElementById("tierStarClient");
        if (star) star.classList.add("hidden");'''

html = html.replace(old_set_mode_logic, new_set_mode_logic)

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: tierStarClient integrated and setMode refined!")
