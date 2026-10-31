import json, re

with open(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\siwasup_agents.js", "r", encoding="utf-8") as f:
    text = f.read()

match = re.search(r"const SIWASUP_AGENTS_SEED = (\[.*?\]);", text, re.DOTALL)
if match:
    agents = json.loads(match.group(1))
    sorted_agents = sorted(agents, key=lambda x: x.get("totalPoints", 0), reverse=True)
    
    with open(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\top20_agents.txt", "w", encoding="utf-8") as out:
        out.write("=== 20 ALPHA AGENTS (LEADERBOARD RANKING) ===\n\n")
        for i, a in enumerate(sorted_agents[:20], 1):
            code = a.get("code")
            name = a.get("name")
            nick = a.get("nickname") or "-"
            tier = a.get("tierName")
            total = a.get("totalPoints", 0)
            perf = a.get("performancePoints", 0)
            act = a.get("activityPoints", 0)
            start = a.get("startDate", "-")
            out.write(f"{i:02d}. [{code}] {name} (ชื่อเล่น: {nick}) | ยศ: {tier} | แต้มรวม: {total} (ขาย: {perf}, กิจกรรม: {act}) | วันเริ่มงาน: {start}\n")
    print("Done!")
