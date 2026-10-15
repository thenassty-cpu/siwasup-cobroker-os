-- ==============================================================================
-- 🏢 SIWASUP CO-BROKER OS (PHASE 1 - SUPABASE MASTER SCHEMA & RLS)
-- Project: บริษัท ศิวาทรัพย์ แอสเซท จำกัด (Siwasup Asset Co., Ltd.)
-- Database: PostgreSQL (Supabase Free Tier)
-- Created: 14 ตุลาคม 2569
-- ==============================================================================

-- 1. ตารางคลังทรัพย์ (Assets: ศิวาทรัพย์ + NPA ธนาคาร)
CREATE TABLE IF NOT EXISTS public.assets (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT DEFAULT 'อสังหาฯ',               -- ทาวน์โฮม, คอนโด, บ้านเดี่ยว, ที่ดิน
    bank_source TEXT DEFAULT 'Siwasup',           -- Siwasup, SAM, SCB, KBANK, TTB, KTB, GSB
    price NUMERIC NOT NULL,
    status TEXT DEFAULT 'available',              -- available, booked, sold, hidden
    specs TEXT,                                   -- สเปก 3 นอน 3 น้ำ
    location TEXT,                                -- ทำเล เช่น บางใหญ่, รัชดา
    main_image TEXT,
    gallery TEXT[],
    description TEXT,
    sold_at TIMESTAMPTZ,                          -- บันทึกเวลาขาย เพื่อทำป้าย SOLD OUT ค้าง 7 วัน
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. ตารางโปรไฟล์ผู้ใช้งานและตัวแทน (Profiles & Agents 125 ท่าน)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    nickname TEXT,
    phone TEXT,
    role TEXT DEFAULT 'trainee',                  -- admin, employee, free_agent, trainee
    tier TEXT DEFAULT 'trainee',                  -- trainee, active, silver, gold, diamond
    commission_rate NUMERIC DEFAULT 0.03,         -- พนักงาน: 0.01, Free Agent: 0.03 - 0.05
    agent_code TEXT UNIQUE NOT NULL,              -- เช่น S02 ถึง S126
    referred_by TEXT,                             -- รหัสผู้ชวนมาสมัคร (MGM Referral)
    activity_points INTEGER DEFAULT 0,            -- คะแนนกิจกรรม (วัดความขยัน)
    performance_points INTEGER DEFAULT 0,         -- คะแนนผลงาน (วัดยอดขาย)
    total_points INTEGER DEFAULT 0,               -- คะแนนรวม
    trainee_listings_count INTEGER DEFAULT 0,     -- ส่งทรัพย์เข้าพอร์ต (ต้องครบ 3 เพื่อปลดล็อก)
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2.1 ตารางบันทึกประวัติการแจกแต้มตัวแทนอัตโนมัติ (Event-Driven Point Transactions Log)
CREATE TABLE IF NOT EXISTS public.agent_point_transactions (
    id TEXT PRIMARY KEY,
    agent_code TEXT NOT NULL,
    track TEXT NOT NULL,                          -- activity, performance
    rule_key TEXT NOT NULL,                       -- meeting_checkin, vinyl_download, vinyl_field_proof, smart_share_click, mgm_referral, etc.
    points INTEGER NOT NULL,
    property_id TEXT,
    gps_coordinates TEXT,
    meta JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. ตารางการจอง / นัดหมาย / ยื่นต่อรองราคาธนาคาร (Bookings & Leads)
CREATE TABLE IF NOT EXISTS public.bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id TEXT REFERENCES public.assets(id),
    client_name TEXT NOT NULL,
    client_phone TEXT NOT NULL,
    agent_ref TEXT,                               -- ดักจับจาก ?ref=AG-xxx
    channel_source TEXT DEFAULT 'direct',         -- facebook, tiktok, line, qr_sign, direct
    type TEXT DEFAULT 'inquiry',                  -- inquiry (นัดชม), offer (ยื่นต่อรองราคา), booking (วางมัดจำ)
    offer_price NUMERIC,                          -- ราคาที่ยื่นต่อรอง
    status TEXT DEFAULT 'pending',                -- pending, negotiating, approved, rejected, paid
    deposit_amount NUMERIC,                       -- ยอดเงินมัดจำ
    payment_slip_url TEXT,                        -- ลิงก์สลิปเงินมัดจำใน Supabase Storage
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. ตารางทรัพย์ฝากขายจากบุคคลทั่วไป (Consignments - Lead Magnet)
CREATE TABLE IF NOT EXISTS public.consignments (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    property_type TEXT NOT NULL,
    price NUMERIC NOT NULL,
    size_detail TEXT,
    owner_name TEXT NOT NULL,
    owner_phone TEXT NOT NULL,
    photo_urls TEXT[],
    status TEXT DEFAULT 'pending',                -- pending (รอโทร), contacted (คุยแล้ว), converted (ชวนเป็น Agent สำเร็จ)
    agent_referred_by TEXT,                       -- ในกรณีที่ Trainee ส่งการบ้าน
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==============================================================================
-- 🔒 นโยบายความปลอดภัยระดับแถวข้อมูล (ROW LEVEL SECURITY - RLS)
-- ==============================================================================

ALTER TABLE public.assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.consignments ENABLE ROW LEVEL SECURITY;

-- Assets: คนทั่วไปอ่านได้เฉพาะทรัพย์ที่ไม่ถูกซ่อน (hidden)
CREATE POLICY "Public can view active assets" 
ON public.assets FOR SELECT 
USING (status != 'hidden');

-- Profiles: สมาชิกอ่านโปรไฟล์ตัวเองได้เท่านั้น ส่วน Admin อ่านได้ทุกคน
CREATE POLICY "Users can view own profile" 
ON public.profiles FOR SELECT 
USING (auth.uid() = user_id OR EXISTS (
    SELECT 1 FROM public.profiles WHERE user_id = auth.uid() AND role = 'admin'
));

-- Bookings: ลูกค้าทั่วไปสามารถ Insert ได้ (Frictionless), Agent ดูเฉพาะเคสของตนเอง
CREATE POLICY "Public can insert bookings" 
ON public.bookings FOR INSERT 
WITH CHECK (true);

CREATE POLICY "Agents can view their own bookings" 
ON public.bookings FOR SELECT 
USING (agent_ref = (
    SELECT agent_code FROM public.profiles WHERE user_id = auth.uid()
) OR EXISTS (
    SELECT 1 FROM public.profiles WHERE user_id = auth.uid() AND role = 'admin'
));

-- Consignments: บุคคลทั่วไป Insert ส่งบ้านได้, เฉพาะ Admin (บัว/เจี๊ยบ) เท่านั้นที่เปิดดูได้
CREATE POLICY "Public can submit consignments" 
ON public.consignments FOR INSERT 
WITH CHECK (true);

CREATE POLICY "Only Admin can view and manage consignments" 
ON public.consignments FOR ALL 
USING (EXISTS (
    SELECT 1 FROM public.profiles WHERE user_id = auth.uid() AND role = 'admin'
));
