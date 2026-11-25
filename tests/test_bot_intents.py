"""Regression tests for Siwasup LINE Bot Geo Search, Intent Routing, Client Link Parser & Lobby Code Backfill."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import line_gemini_webhook as w  # noqa: E402


def run_tests():
    # 1. Concatenated & Nationwide Geo Extraction
    g1 = w._extract_thai_geo("คานหามอยุธยา")
    assert g1 and g1["province"] == "พระนครศรีอยุธยา" and g1["district"] == "อุทัย" and g1["subdistrict"] == "คานหาม", g1

    g_roj = w._extract_thai_geo("ขอลิงก์บ้าน โรจนะ")
    assert g_roj and g_roj["province"] == "พระนครศรีอยุธยา" and g_roj["district"] == "อุทัย", g_roj

    g_nava = w._extract_thai_geo("หาบ้าน นวนคร")
    assert g_nava and g_nava["province"] == "ปทุมธานี" and g_nava["district"] == "คลองหลวง", g_nava

    g_pu = w._extract_thai_geo("ขอลิงค์ข้อมูลบ้าน โซนประชาอุทิศ 5 หลัง")
    assert g_pu and g_pu["province"] == "กรุงเทพมหานคร" and g_pu["district"] == "ทุ่งครุ", g_pu

    # 2. Ambiguous Short Provinces Guard
    assert w._extract_thai_geo("ขอลิงก์บ้านเลย") is None
    g_loei = w._extract_thai_geo("บ้าน จ.เลย")
    assert g_loei and g_loei["province"] == "เลย", g_loei
    g_tak = w._extract_thai_geo("บ้าน ตาก")
    assert g_tak and g_tak["province"] == "ตาก", g_tak

    # 3. Cross-Province Haversine Radius Search + Flex Carousel
    near = w._find_nearest_siwasup_props(g_pu["lat"], g_pu["lng"], allowed_cats=["บ้านเดี่ยว", "บ้านแฝด", "ทาวน์โฮม", "ทาวน์เฮ้าส์"], limit=5)
    assert len(near) == 5, len(near)
    fps = [fp for fp in (w.find_property_by_id_or_code(p["code"]) for p in near) if fp]
    flex = w.build_property_flex_carousel(fps, agent_ref="SA000")
    assert flex and len(flex["contents"]["contents"]) == 5

    # 4. Generic Catalog Link vs Geo/Agent-View Bypass
    dm = {"id": "SW-APP-601", "name": "ออย"}
    assert w.resolve_catalog_link_request("ขอลิงก์บ้าน", dm) is not None
    assert w.resolve_catalog_link_request("ขอลิงก์บ้าน คานหามอยุธยา", dm) is None
    assert w.resolve_catalog_link_request("ขอลิงค์สำหรับ agent ที่จะดูในระบบ ว่าไหนเป็นทรัพย์ธนาคารไหน", dm) is None
    assert w.resolve_catalog_link_request("ขอลิงค์ตัวแทน", dm) is None
    assert w.resolve_catalog_link_request("มุม agent", dm) is None

    # 5. Glued / Numeric Client Name Parser
    assert w.parse_agent_link_input("3หลังส่งให้คุณ5ที") == ("5", "3หลัง", "")
    assert w.parse_agent_link_input("3หลังให้คุณหนึ่งที") == ("หนึ่ง", "3หลัง", "")
    assert w.parse_agent_link_input("ส่งให้คุณAหน่อย") == ("A", "", "")

    # 6. Conflicting Distant Zones (>20km) Gate
    assert w._detect_conflicting_zones("ขอบ้าน ทุ่งครุ มีนบุรี") == ["ทุ่งครุ", "มีนบุรี"]
    assert w._detect_conflicting_zones("ขอลิงก์บ้าน คานหามอยุธยา") == []
    assert w._detect_conflicting_zones("ประชาอุทิศ ทุ่งครุ") == []

    # 7. search_properties() does not hit TOO_VAGUE on nationwide geo
    res, mode = w.search_properties("หาบ้าน คานหามอยุธยา", "test_uid_reg")
    assert mode != "TOO_VAGUE_NEEDS_MORE_INFO" and len(res) > 0, (mode, len(res))

    # 8. Lobby SA/SW Code Auto-Backfill
    mock_store = {
        "approved": [
            {"id": "app_office_004", "name": "Ton"},
            {"id": "app_office_001", "name": "Gool"},
            {"id": "SW-APP-252", "name": "Bua"},
            {"id": "SW-APP-866", "name": "Lily", "nickname": "ลิลลี่"},
            {"id": "SW-APP-905", "name": "Baitong", "affiliation": "office", "permissions": {"standardAdmin": True}},
        ]
    }
    assert w._ensure_approved_member_codes(mock_store) is True
    codes = {m["id"]: m["code"] for m in mock_store["approved"]}
    assert codes["app_office_004"] == "SA000"
    assert codes["app_office_001"] == "SW001"
    assert codes["SW-APP-252"] == "SA001"
    assert codes["SW-APP-866"] == "SA002"
    assert codes["SW-APP-905"] == "SA003"

    print("ALL 8 REGRESSION TEST SUITES PASSED!")


if __name__ == "__main__":
    run_tests()
