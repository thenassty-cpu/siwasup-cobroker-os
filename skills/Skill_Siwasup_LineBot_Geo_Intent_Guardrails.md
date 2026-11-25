# Skill: Siwasup LINE Bot — Nationwide Geo Search & Intent Guardrails

**Category:** AI Bot / Search / Production Guardrails  
**Last Updated:** 2026-11-26  
**Key Files:** `scripts/line_gemini_webhook.py`, `data/thai_geo_centroids.json`, `catalog.html`, `sw.js`, `offline_log_exporter.html`

---

## 1. Real Production Failure Patterns & Fixes (Lessons Learned 2026-11-25/26)

| Case / User | Real Query | What Went Wrong | Root Fix Applied |
| :--- | :--- | :--- | :--- |
| **Oil (`SW-APP-601`)** | `"ขอลิงก์บ้าน คานหามอยุธยา"` | `resolve_catalog_link_request()` matched `"ขอลิงก์บ้าน"` early and returned generic `?ref=...&view=client` without searching `คานหาม อยุธยา`. | Only treat as generic catalog link when there is **no** location/budget/extra filter; otherwise route to Geo Search + filtered `catalog.html` URL + Flex Carousel. |
| **Poppy (`SW-APP-873`)** | `"ขอลิงค์ข้อมูลบ้าน โซนประชาอุทิศ 5 หลัง"` | Started with `"ข้อมูลบ้าน"` (not `"บ้าน"`) and `"ประชาอุทิศ"` wasn't in Landmark table → fell into `m_link` (`CLIENT_LINK_GEN`), creating customer **`คุณข้อมูลบ้านโซนประชาอุทิศ`**. | Added `"ข้อมูล"`, `"ทรัพย์"`, and search-indicator words (`โซน`, `แถว`, `ย่าน`, `ทำเล`, `หลัง`, `แปลง`, `งบ`, `ล้าน`) to `is_prop_or_cmd_link` + added Thonburi/Pracha Uthit landmarks + parsed requested count (`5 หลัง`). |
| **Gool (`SW001`)** | `"ขอลิงค์สำหรับ agent ที่จะดูในระบบ ว่าไหนเป็นทรัพย์ธนาคารไหน"`, `"ขอลิงค์ตัวแทน"`, `"มุม agent"` | `m_link` parsed `"สำหรับ"` as customer **`คุณสำหรับ`**; `resolve_catalog_link_request` gave `?view=client` (hiding banks). | Added `_is_agent_view_req` (`AGENT_VIEW_PORTAL_LINK`) returning `catalog.html` (no `view=client`) & `launchpad.html` with LINE Login instructions; blocked `สำหรับ/ตัวแทน/เอเจน` from becoming customer names. |
| **Bai Tong (`SW-APP-905`) & Z (`SW-APP-267`)** | `"ขอลิ้งค์3หลังส่งให้คุณ5ที"`, `"ขอลิ้ง3หลังให้คุณหนึ่งที"` | Glued Thai text with no spaces caused `tokens[0]` to become **`คุณ3หลังส่งให้คุณ5ที`** / **`คุณ3หลังให้คุณหนึ่งที`**. | Upgraded `parse_agent_link_input()` to extract `(?:ส่งให้|ให้)?คุณ\s*([0-9]+|[ก-๙a-zA-Z0-9_]+)` and strip trailing polite particles (`ที`, `หน่อย`, `ด้วย`, `ครับ`, `ค่ะ`, `นะ`), separating prefix notes (`3หลัง`). |
| **Ambiguous Short Provinces** | `"ขอลิงก์บ้านเลย"`, `"ลิงก์ คุณตาก"` | Raw substring match on 1-syllable provinces (`เลย`, `ตาก`, `ตราด`, `น่าน`, `ตรัง`, `แพร่`, `นนท์`) collided with Thai verbs/particles or client names. | Added `_SHORT_AMBIGUOUS_PROVS` requiring a geo prefix (`จ.`, `จังหวัด`, `โซน`) or whitespace boundary, and skipped geo detection when argument starts with `คุณ...`. |
| **Conflicting Distant Zones** | `"ขอบ้าน ทุ่งครุ มีนบุรี"` | Returned an arbitrary OR-mix across opposite sides of the city (or stopped at the first zone). | Added `_detect_conflicting_zones(threshold_km=20.0)` to pause and ask the user to confirm which zone to prioritize (`GEO_CONFLICT_CONFIRM`). |

---

## 2. Nationwide 4-Layer Geo Architecture
1. **Static Memory Centroids (`data/thai_geo_centroids.json`):**
   - 77 provinces, 924 districts, 7,436 subdistricts with 100% populated `lat`/`lng` (zero external API latency).
   - Greedy Longest-Match + hierarchical verification (`province → district → subdistrict`) in `_extract_thai_geo()` so concatenated strings like `"คานหามอยุธยา"` resolve cleanly to `ต.คานหาม อ.อุทัย จ.พระนครศรีอยุธยา`.
   - Duplicate subdistricts (e.g. `ท่าข้าม`) without a specified province trigger `GEO_AMBIGUOUS_CONFIRM` asking the user to pick the province.
2. **Cross-Province Haversine Radius Search (`_find_nearest_siwasup_props`):**
   - No hard province lock — calculates Haversine distance against all active properties (`latitude`/`longitude`, safely casting PAMCO string coords to `float()`).
   - **Tier 1 (`0–5 km`)**: Direct target area.
   - **Tier 2 (`5–15 km`)**: Neighboring districts / cross-province border zones.
   - Ranks by `distance_km ASC`, displays `~X.X กม.`, and attaches **Flex Carousel Cards** (`build_property_flex_carousel`).
3. **1.6-Second Multi-Message Debounce (`_MSG_DEBOUNCE_BUF`):**
   - Buffers rapid consecutive text messages from the same `user_id` for `1.6s` (using the latest `reply_token`) before processing, so multi-line bursts like `"ขอลิงก์บ้าน"` + `"คานหามอยุธยา"` are evaluated as a single complete intent.
4. **Landmark & Industrial Estate Aliases (`_THAI_SPECIAL_ZONE_COORDS`):**
   - Maps real-estate & industrial hotspots (`โรจนะ`, `นวนคร`, `ไฮเทค`, `อมตะนคร`, `อมตะซิตี้`, `อีสเทิร์นซีบอร์ด`, `แหลมฉบัง`, `มาบตาพุด`, `ประชาอุทิศ`, `ทุ่งครุ`, `ศาลายา`, `เวสต์เกต`, etc.) directly to `(province, district, lat, lng)`.
5. **Catalog Deep-Link Filter (`catalog.html` + `sw.js`):**
   - `checkUrlParameters()` reads `?q=`, `?province=`, `?cat=`, `?budget=` and updates `#search-input`, `#filter-category` (supporting grouped `'บ้าน'` = SDH+TH), `#filter-upcountry-province` (including `0 หลัง` provinces), and `updateMiniBarSummary()`.
   - Always bump `CACHE_NAME` in `sw.js` and deploy both **Cloudflare R2** and **GitHub Pages** when updating `catalog.html`.
