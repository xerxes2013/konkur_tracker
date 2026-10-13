import streamlit as st
import datetime
import urllib.parse
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageDraw
import io
import random

# ═══════════════════════════════════════════════════════
# ۱. تنظیمات صفحه
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="سامانه هوشمند آکادمی ۲۰",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════
# ۲. استایل‌های پیشرفته با انیمیشن و گلس‌مورفیزم
# ═══════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');
    
    * {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl;
        text-align: right;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes floatUp {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
    }
    
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(56, 189, 248, 0.35); }
        50% { box-shadow: 0 0 45px rgba(56, 189, 248, 0.75); }
    }

    @keyframes shimmer {
        0% { background-position: -300% 0; }
        100% { background-position: 300% 0; }
    }

    @keyframes rotateGlow {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* پس‌زمینه کهکشانی */
    .stApp {
        background: radial-gradient(circle at 15% 5%, #1e2447 0%, #0b0f19 42%, #05070f 100%) !important;
        color: #ffffff !important;
    }

    /* ذرات نورانی شناور */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            radial-gradient(2px 2px at 20% 30%, rgba(56,189,248,0.45), transparent),
            radial-gradient(1.5px 1.5px at 65% 70%, rgba(74,222,128,0.4), transparent),
            radial-gradient(1.5px 1.5px at 82% 22%, rgba(250,204,21,0.4), transparent),
            radial-gradient(1px 1px at 40% 82%, rgba(248,113,113,0.4), transparent),
            radial-gradient(1.2px 1.2px at 12% 65%, rgba(168,85,247,0.4), transparent);
        background-size: 550px 550px, 420px 420px, 630px 630px, 320px 320px, 480px 480px;
        pointer-events: none;
        z-index: 0;
        opacity: 0.7;
    }

    /* هدر اصلی با حاشیه گرادیانت متحرک */
    .hero-header {
        position: relative;
        background: linear-gradient(135deg, rgba(17,24,39,0.9) 0%, rgba(30,41,59,0.85) 100%);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-radius: 22px;
        padding: 26px 22px;
        text-align: center;
        margin-bottom: 26px;
        overflow: hidden;
        border: 1px solid rgba(56, 189, 248, 0.25);
        box-shadow: 0 10px 40px rgba(2, 132, 199, 0.18), inset 0 1px 0 rgba(255,255,255,0.06);
    }

    .hero-header::before {
        content: '';
        position: absolute;
        inset: -2px;
        border-radius: 22px;
        padding: 2px;
        background: linear-gradient(90deg, #38bdf8, #4ade80, #facc15, #f472b6, #38bdf8);
        background-size: 300% 100%;
        animation: gradientShift 8s linear infinite;
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
        opacity: 0.85;
    }

    .hero-title {
        font-size: 26px;
        font-weight: 900;
        background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 6px 0;
    }

    .hero-sub {
        color: #cbd5e1 !important;
        font-size: 14px;
        margin: 0;
    }

    /* کارت‌های شاخص */
    .metric-card {
        position: relative;
        background: linear-gradient(145deg, rgba(17,24,39,0.85), rgba(30,41,59,0.75));
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(56, 189, 248, 0.28);
        border-radius: 18px;
        padding: 18px 14px;
        text-align: center;
        transition: all 0.35s cubic-bezier(.2,.9,.3,1.3);
        overflow: hidden;
        box-shadow: 0 8px 26px rgba(0,0,0,0.35);
    }

    .metric-card:hover {
        transform: translateY(-6px) scale(1.02);
        border-color: rgba(56, 189, 248, 0.7);
        box-shadow: 0 14px 36px rgba(56, 189, 248, 0.35);
    }

    .metric-card::after {
        content: '';
        position: absolute;
        top: 0; left: -60%;
        width: 60%; height: 100%;
        background: linear-gradient(120deg, transparent, rgba(255,255,255,0.08), transparent);
        transition: 0.6s;
    }

    .metric-card:hover::after {
        left: 120%;
    }

    .metric-num {
        font-size: 30px;
        font-weight: 900;
        background: linear-gradient(90deg, #38bdf8, #4ade80);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
    }

    .metric-txt {
        font-size: 12.5px;
        color: #94a3b8 !important;
        margin-top: 6px;
    }

    .metric-icon {
        font-size: 22px;
        display: block;
        margin-bottom: 4px;
    }

    /* Streak Flame */
    .streak-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(90deg, rgba(251,146,60,0.15), rgba(248,113,113,0.15));
        border: 1px solid rgba(251,146,60,0.55);
        padding: 10px 18px;
        border-radius: 14px;
        font-weight: 800;
        color: #fb923c !important;
        animation: pulseGlow 2.5s ease-in-out infinite;
    }

    /* جعبه انگیزشی */
    .motivation-box {
        background: linear-gradient(135deg, rgba(56,189,248,0.12), rgba(168,85,247,0.12));
        border-right: 4px solid #38bdf8;
        border-radius: 12px;
        padding: 14px 18px;
        margin: 18px 0;
        font-style: italic;
        color: #e2e8f0 !important;
        font-size: 14.5px;
    }

    /* لیبل‌ها و متن‌ها */
    label, p, span, h1, h2, h3, h4, div {
        color: #ffffff !important;
        font-weight: 600;
    }

    input, textarea, select {
        background-color: rgba(30,41,59,0.85) !important;
        color: #ffffff !important;
        border: 1px solid rgba(56,189,248,0.35) !important;
        border-radius: 12px !important;
        transition: 0.25s;
    }

    input:focus, textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 3px rgba(56,189,248,0.18) !important;
    }

    /* دکمه‌ها */
    .stButton > button {
        background: linear-gradient(90deg, #0284c7, #7c3aed) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        padding: 12px 20px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(124,58,237,0.28) !important;
        letter-spacing: 0.3px;
    }

    .stButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 10px 30px rgba(124,58,237,0.55) !important;
        filter: brightness(1.08);
    }

    /* دکمه تلگرام */
    .tg-button {
        display: block;
        width: 100%;
        background: linear-gradient(90deg, #0088cc, #005f8f);
        color: #ffffff !important;
        text-align: center;
        font-size: 16px;
        font-weight: 800;
        padding: 14px;
        border-radius: 12px;
        text-decoration: none;
        box-shadow: 0 6px 18px rgba(2,132,199,0.45);
        margin-top: 15px;
        transition: all 0.3s;
        position: relative;
        overflow: hidden;
    }

    .tg-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 28px rgba(2,132,199,0.75);
        filter: brightness(1.1);
    }

    .tg-button::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(120deg, transparent 30%, rgba(255,255,255,0.25), transparent 70%);
        transform: translateX(-100%);
        transition: 0.7s;
    }

    .tg-button:hover::before {
        transform: translateX(100%);
    }

    /* تب‌ها */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(17,24,39,0.6);
        padding: 8px;
        border-radius: 14px;
        border: 1px solid rgba(56,189,248,0.18);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        padding: 10px 16px !important;
        font-weight: 700 !important;
        transition: 0.25s;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #0284c7, #7c3aed) !important;
        color: #ffffff !important;
    }

    /* اسکرول‌بار */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: #0b0f19; }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #38bdf8, #7c3aed);
        border-radius: 10px;
    }

    /* گلس کارت عمومی */
    .glass-card {
        background: rgba(17,24,39,0.72);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(56,189,248,0.22);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.28);
    }

    /* بج‌ها */
    .badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 999px;
        font-weight: 800;
        font-size: 13px;
        margin: 3px;
        border: 1px solid;
    }
    .badge-bronze { color:#fb923c; border-color:#fb923c; background:rgba(251,146,60,0.12); }
    .badge-silver { color:#cbd5e1; border-color:#cbd5e1; background:rgba(203,213,225,0.12); }
    .badge-gold   { color:#facc15; border-color:#facc15; background:rgba(250,204,21,0.12); }
    .badge-diamond{ color:#38bdf8; border-color:#38bdf8; background:rgba(56,189,248,0.12); }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# ۳. دیتابیس
# ═══════════════════════════════════════════════════════
conn = sqlite3.connect("konkur_academy.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, name TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, report_date DATE,
    satisfaction INT, study_hours REAL, total_tests INT, correct_tests INT,
    wrong_tests INT, percentage REAL, screen_time TEXT, social_time TEXT, details TEXT
)''')
conn.commit()

# ═══════════════════════════════════════════════════════
# ۴. جملات انگیزشی
# ═══════════════════════════════════════════════════════
MOTIVATIONS = [
    "🌟 هر تستی که می‌زنی، یک قدم به رویاهات نزدیک‌تر می‌شی.",
    "🔥 موفقیت حاصل تکرارهای کوچک روزانه است، نه یک‌شبه معجزه.",
    "🚀 امروزت رو بساز، چون فردا از همین امروزها ساخته می‌شه.",
    "💎 فشارِ امروز، الماسِ فردا رو می‌سازه.",
    "🎯 تمرکز روی پیشرفت، نه کمال. همین کافیه.",
    "⚡ تو از دیروز خودت قوی‌تری؛ همین کافیه برای ادامه دادن.",
    "🌈 سختی‌های امروز، پله‌های افتخار فردا هستن.",
    "👑 کسی که هر روز تلاش می‌کنه، شکست نمی‌خوره؛ فقط یاد می‌گیره.",
]

# ═══════════════════════════════════════════════════════
# ۵. تولید پوستر گرافیکی حرفه‌ای
# ═══════════════════════════════════════════════════════
def draw_gradient_bg(img, color_top, color_bottom):
    w, h = img.size
    for y in range(h):
        ratio = y / h
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        ImageDraw.Draw(img).line([(0, y), (w, y)], fill=(r, g, b))


def generate_report_card(name, date_str, satisfaction, study_hours, total_tests, percentage, screen_time):
    W, H = 900, 560
    img = Image.new('RGB', (W, H), color='#0b0f19')
    draw_gradient_bg(img, (11, 15, 25), (20, 26, 48))
    draw = ImageDraw.Draw(img)

    # حاشیه گرادیانی
    for i, col in enumerate([(56,189,248), (124,58,237), (244,114,182)]):
        draw.rectangle([(12+i, 12+i), (W-12-i, H-12-i)], outline=col, width=1)

    # هدر
    draw.rectangle([(30, 30), (W-30, 118)], fill='#0f1729', outline='#38bdf8', width=2)
    draw.text((W//2 - 200, 48), "  ACADEMY 20  •  STUDY REPORT  ", fill='#38bdf8')
    draw.text((W//2 - 230, 78), f"Student: {name}     |     Date: {date_str}", fill='#ffffff')

    # کارت‌های داده
    # کارت ۱ - مطالعه
    draw.rectangle([(40, 145), (440, 265)], fill='#111c30', outline='#38bdf8', width=1)
    draw.text((60, 165), "⏳  STUDY DURATION", fill='#94a3b8')
    draw.text((60, 200), f"{study_hours} Hours", fill='#38bdf8')
    draw.text((60, 235), f"⭐ Satisfaction: {satisfaction}/10", fill='#facc15')

    # کارت ۲ - تست
    draw.rectangle([(460, 145), (W-40, 265)], fill='#111c30', outline='#4ade80', width=1)
    draw.text((480, 165), "📝  TESTS & SCORE", fill='#94a3b8')
    draw.text((480, 200), f"Total Tests: {total_tests}", fill='#ffffff')
    draw.text((480, 235), f"Net Score: {percentage}%", fill='#4ade80')

    # کارت ۳ - اسکرین تایم
    draw.rectangle([(40, 285), (W-40, 400)], fill='#1a1220', outline='#f87171', width=1)
    draw.text((60, 305), "📱  DIGITAL WELLNESS", fill='#94a3b8')
    draw.text((60, 340), f"Screen Time: {screen_time}", fill='#f87171')
    draw.text((60, 370), "Monitored via Academy 20 Tracking Core", fill='#64748b')

    # پیشرفت خطی
    draw.rectangle([(40, 420), (W-40, 445)], fill='#1e293b')
    bar_w = int((W-80) * min(max(percentage, 0), 100) / 100)
    draw.rectangle([(40, 420), (40+bar_w, 445)], fill='#4ade80')
    draw.text((60, 452), f"Progress: {percentage}%", fill='#e2e8f0')

    # فوتر
    draw.text((W//2 - 200, 500), "Consultant: Dr. Khashayar Ashkboos", fill='#38bdf8')
    draw.text((W//2 - 130, 528), "Telegram: @Kh_Ashkboos", fill='#94a3b8')

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()


# ═══════════════════════════════════════════════════════
# ۶. توابع کمکی (Streak / Level)
# ═══════════════════════════════════════════════════════
def compute_streak(df):
    if df.empty:
        return 0
    dates = sorted(set(pd.to_datetime(df['report_date']).dt.date), reverse=True)
    today = datetime.date.today()
    streak = 0
    check = today
    if dates and dates[0] != today:
        if dates[0] == today - datetime.timedelta(days=1):
            check = today - datetime.timedelta(days=1)
        else:
            return 0
    for d in dates:
        if d == check:
            streak += 1
            check -= datetime.timedelta(days=1)
        elif d < check:
            break
    return streak


def get_level(total_hours):
    levels = [
        (0,  "🌱 نوآموز",      "badge-bronze"),
        (10, "📘 کوشا",         "badge-silver"),
        (30, "⚔️ سخت‌کوش",     "badge-silver"),
        (60, "🥇 حرفه‌ای",      "badge-gold"),
        (100,"💎 افسانه‌ای",     "badge-diamond"),
    ]
    current = levels[0]
    for threshold, name, badge in levels:
        if total_hours >= threshold:
            current = (threshold, name, badge)
    return current[1], current[2]


# ═══════════════════════════════════════════════════════
# ۷. نشست
# ═══════════════════════════════════════════════════════
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['name'] = ''
if 'celebrate' not in st.session_state:
    st.session_state['celebrate'] = False

# ═══════════════════════════════════════════════════════
# ۸. صفحه ورود / ثبت‌نام
# ═══════════════════════════════════════════════════════
if not st.session_state['logged_in']:
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">👑 سامانه هوشمند آکادمی ۲۰</div>
        <p class="hero-sub">مدیریت، پایش و تحلیل علمی فرآیند کنکور | <b>دکتر خشایار اشکبوس</b></p>
    </div>
    """, unsafe_allow_html=True)

    tab_login, tab_reg = st.tabs(["🔑 ورود دانش‌آموز", "📝 ثبت‌نام دانش‌آموز جدید"])

    with tab_login:
        col_u, col_p = st.columns(2)
        u_in = col_u.text_input("نام کاربری:", key="l_user")
        p_in = col_p.text_input("رمز عبور:", type="password", key="l_pass")
        if st.button("🚀 ورود به داشبورد تحصیلی", use_container_width=True):
            c.execute("SELECT name FROM users WHERE username=? AND password=?", (u_in, p_in))
            res = c.fetchone()
            if res:
                st.session_state['logged_in'] = True
                st.session_state['username'] = u_in
                st.session_state['name'] = res[0]
                st.rerun()
            else:
                st.error("❌ نام کاربری یا رمز عبور اشتباه است.")

    with tab_reg:
        name_in = st.text_input("نام و نام خانوادگی:")
        u_new = st.text_input("نام کاربری دلخواه (کد ملی یا شماره همراه):")
        p_new = st.text_input("رمز عبور دلخواه:", type="password")
        if st.button("✨ ثبت‌نام و عضویت در سامانه", use_container_width=True):
            if name_in and u_new and p_new:
                try:
                    c.execute("INSERT INTO users VALUES (?, ?, ?)", (u_new, p_new, name_in))
                    conn.commit()
                    st.success("🎉 حساب کاربری با موفقیت ساخته شد! اکنون وارد شوید.")
                except:
                    st.error("⚠️ این نام کاربری قبلاً ثبت شده است.")
            else:
                st.warning("لطفاً همه فیلدها را پر کنید.")
    st.stop()

# ═══════════════════════════════════════════════════════
# ۹. داشبورد اصلی
# ═══════════════════════════════════════════════════════
# محاسبه Streak و Level
df_all = pd.read_sql_query("SELECT * FROM reports WHERE username=? ORDER BY report_date ASC",
                           conn, params=(st.session_state['username'],))
streak = compute_streak(df_all)
total_hours_all = df_all['study_hours'].sum() if not df_all.empty else 0
level_name, level_badge = get_level(total_hours_all)
motivation = random.choice(MOTIVATIONS)

st.markdown(f"""
<div class="hero-header">
    <div class="hero-title">داشبورد نظارت مطالعاتی | آکادمی ۲۰</div>
    <p class="hero-sub">دانش‌آموز کوشا: <b>{st.session_state['name']}</b></p>
</div>
""", unsafe_allow_html=True)

# نوار بالایی: Streak + Level
col_s, col_l, col_m = st.columns([1, 1, 2])
with col_s:
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div class="streak-badge">🔥 {streak} روز متوالی</div>
        <div class="metric-txt" style="margin-top:8px;">زنجیره مطالعه</div>
    </div>
    """, unsafe_allow_html=True)

with col_l:
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <span class="badge {level_badge}" style="font-size:15px;">{level_name}</span>
        <div class="metric-txt" style="margin-top:8px;">سطح فعلی</div>
    </div>
    """, unsafe_allow_html=True)

with col_m:
    st.markdown(f"""
    <div class="glass-card" style="display:flex; align-items:center; gap:12px; height:100%;">
        <div style="font-size:26px;">💬</div>
        <div style="font-size:13.5px; color:#e2e8f0;">{motivation}</div>
    </div>
    """, unsafe_allow_html=True)

# تب‌های اصلی
main_tab1, main_tab2, main_tab3 = st.tabs([
    "📝 ثبت گزارش کار روزانه",
    "📈 تحلیل هفتگی و ماهانه",
    "⚙️ تنظیمات و خروج"
])

# ═══════════════════════════════════════════════════════
# تب ۱: فرم ثبت گزارش
# ═══════════════════════════════════════════════════════
with main_tab1:
    c_d1, c_d2 = st.columns(2)
    rep_date = c_d1.date_input("📅 تاریخ ثبت گزارش:", datetime.date.today())
    satisfaction = c_d2.slider("⭐️ کیفیت و رضایت از مطالعه امروز (۱ تا ۱۰):", 1, 10, 8)

    st.markdown("#### 📚 ثبت ریز پارت‌های درسی")
    num_slots = st.number_input("تعداد پارت‌های مطالعه امروز:", min_value=1, max_value=12, value=3)

    subjects = ["زیست‌شناسی", "شیمی", "فیزیک", "ریاضیات", "زمین‌شناسی",
                "فارسی", "دینی", "عربی", "زبان", "سایر"]

    total_tests, total_c, total_w = 0, 0, 0
    total_minutes = 0
    parts_summary = []

    for i in range(int(num_slots)):
        with st.expander(f"📌 پارت درسی {i+1}", expanded=(i == 0)):
            col_s1, col_s2 = st.columns([2, 1])
            subj = col_s1.selectbox(f"درس (پارت {i+1})", subjects, key=f"s_{i}")
            if subj == "سایر":
                subj = col_s1.text_input("نام درس انتخابی", key=f"cs_{i}")
            test_type = col_s2.radio("نوع تست", ["آموزشی", "زمان‌دار"], horizontal=True, key=f"tt_{i}")

            c_t1, c_t2 = st.columns(2)
            st_t = c_t1.time_input("ساعت شروع", datetime.time(8, 0), key=f"st_{i}")
            et_t = c_t2.time_input("ساعت پایان", datetime.time(9, 30), key=f"et_{i}")

            dur = (datetime.datetime.combine(datetime.date.today(), et_t) -
                   datetime.datetime.combine(datetime.date.today(), st_t)).seconds / 60
            if dur > 0:
                total_minutes += dur

            c_src1, c_src2 = st.columns(2)
            c_src1.text_input("منبع درسنامه", key=f"src_s_{i}")
            c_src2.text_input("منبع تست", key=f"src_t_{i}")

            st.caption("آمار تست‌ها:")
            tc, tw, tu, td = st.columns(4)
            c_val = tc.number_input("صحیح", min_value=0, value=0, key=f"c_{i}")
            w_val = tw.number_input("غلط", min_value=0, value=0, key=f"w_{i}")
            tu.number_input("نزده", min_value=0, value=0, key=f"u_{i}")
            td.number_input("شک‌دار", min_value=0, value=0, key=f"d_{i}")

            st.text_input("مبحث و توضیحات پارت", key=f"nt_{i}")

            s_tests = c_val + w_val
            total_tests += s_tests
            total_c += c_val
            total_w += w_val
            parts_summary.append(
                f"{i+1}. {subj} ({st_t.strftime('%H:%M')} تا {et_t.strftime('%H:%M')}) | {s_tests} تست ({c_val}ص/{w_val}غ)"
            )

    st.markdown("#### 📱 کنترل مصرف تلفن همراه (اسکرین‌تایم)")
    c_sc1, c_sc2 = st.columns(2)
    screen_t = c_sc1.text_input("کل مصرف گوشی امروز:", "۲:۱۵")
    social_t = c_sc2.text_input("مدت زمان در شبکه‌های مجازی:", "۴۵ دقیقه")

    study_hours = round(total_minutes / 60, 2)
    overall_perc = round(((total_c * 3 - total_w) / (total_tests * 3)) * 100, 1) if total_tests > 0 else 0.0

    if st.button("💾 ثبت نهایی گزارش در دیتابیس", use_container_width=True):
        c.execute('''INSERT INTO reports (username, report_date, satisfaction, study_hours,
                    total_tests, correct_tests, wrong_tests, percentage, screen_time, social_time, details)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (st.session_state['username'], rep_date, satisfaction, study_hours,
                   total_tests, total_c, total_w, overall_perc, screen_t, social_t, "\n".join(parts_summary)))
        conn.commit()
        st.balloons()
        st.success("✅ گزارش شما ذخیره شد و به بخش نمودارها اضافه گردید! 🎉")

    st.markdown("---")
    st.markdown("#### 📤 کارنامه تصویری و ارسال به تلگرام")

    col_out1, col_out2 = st.columns(2)

    report_text = f"""📊 گزارش کار شبانه | آکادمی ۲۰
👤 دانش‌آموز: {st.session_state['name']}
📅 تاریخ: {rep_date} | ⭐ رضایت: {satisfaction}/10
⏳ مجموع ساعت مطالعه: {study_hours} ساعت
📝 کل تست‌ها: {total_tests} (✅ صحیح: {total_c} | ❌ غلط: {total_w})
🎯 درصد خالص: {overall_perc}%
📱 اسکرین‌تایم گوشی: {screen_t} (فضای مجازی: {social_t})
━━━━━━━━━━━━━━━━━━━━
📚 ریز پارت‌های مطالعه:
""" + "\n".join(parts_summary) + f"""
━━━━━━━━━━━━━━━━━━━━
👨‍🏫 مشاور: دکتر خشایار اشکبوس | @Kh_Ashkboos"""

    with col_out1:
        st.text_area("متن آماده جهت کپی:", report_text, height=200)
        tg_url = "https://t.me/share/url?url=" + urllib.parse.quote(report_text)
        st.markdown(f'<a href="{tg_url}" target="_blank" class="tg-button">🚀 ارسال مستقیم به تلگرام مشاور</a>',
                    unsafe_allow_html=True)

    with col_out2:
        img_bytes = generate_report_card(st.session_state['name'], str(rep_date), satisfaction,
                                         study_hours, total_tests, overall_perc, screen_t)
        st.image(img_bytes, caption="کارنامه گرافیکی اختصاصی شما", use_container_width=True)
        st.download_button("📥 دانلود کارت تصویری (PNG)", img_bytes,
                           file_name=f"report_{rep_date}.png", mime="image/png", use_container_width=True)

# ═══════════════════════════════════════════════════════
# تب ۲: نمودارها
# ═══════════════════════════════════════════════════════
with main_tab2:
    st.markdown("### 📈 داشبورد تحلیل و مقایسه عملکرد")

    if df_all.empty:
        st.info("⚠️ هنوز گزارشی ثبت نکرده‌اید! ابتدا در تب اول یک گزارش ثبت کنید تا نمودارها فعال شوند.")
    else:
        df_all['report_date'] = pd.to_datetime(df_all['report_date'])

        c_filter1, c_filter2 = st.columns([1, 2])
        time_frame = c_filter1.radio("انتخاب بازه تحلیلی:",
                                     ["۷ روز اخیر (هفتگی)", "۳۰ روز اخیر (ماهانه)"],
                                     horizontal=True)
        days = 7 if "۷" in time_frame else 30

        filtered_df = df_all[df_all['report_date'] >=
                             (pd.Timestamp(datetime.date.today() - datetime.timedelta(days=days)))]

        if filtered_df.empty:
            st.warning("در این بازه گزارشی ثبت نشده است.")
        else:
            sum_hours = filtered_df['study_hours'].sum()
            sum_tests = filtered_df['total_tests'].sum()
            avg_perc = filtered_df['percentage'].mean()
            avg_sat = filtered_df['satisfaction'].mean()

            # کارت‌های شاخص
            st.markdown(f"""
            <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; margin-bottom:22px;">
                <div class="metric-card">
                    <span class="metric-icon">⏳</span>
                    <div class="metric-num">{sum_hours:.1f}</div>
                    <div class="metric-txt">ساعت مطالعه کل بازه</div>
                </div>
                <div class="metric-card">
                    <span class="metric-icon">📝</span>
                    <div class="metric-num">{sum_tests}</div>
                    <div class="metric-txt">مجموع تست‌های بازه</div>
                </div>
                <div class="metric-card">
                    <span class="metric-icon">🎯</span>
                    <div class="metric-num">{avg_perc:.1f}%</div>
                    <div class="metric-txt">میانگین درصد خالص</div>
                </div>
                <div class="metric-card">
                    <span class="metric-icon">⭐</span>
                    <div class="metric-num">{avg_sat:.1f}</div>
                    <div class="metric-txt">میانگین رضایت (از ۱۰)</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # چیدمان ۲ ستونی: گیج + میله‌ای
            g1, g2 = st.columns([1, 2])

            # گیج دایره‌ای درصد
            with g1:
                gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=float(avg_perc),
                    number={'suffix': "%", 'font': {'color': '#38bdf8', 'size': 34}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickcolor': '#94a3b8'},
                        'bar': {'color': "#4ade80"},
                        'bgcolor': "#1e293b",
                        'borderwidth': 0,
                        'steps': [
                            {'range': [0, 40], 'color': 'rgba(248,113,113,0.18)'},
                            {'range': [40, 70], 'color': 'rgba(250,204,21,0.18)'},
                            {'range': [70, 100], 'color': 'rgba(74,222,128,0.18)'},
                        ],
                        'threshold': {
                            'line': {'color': "#38bdf8", 'width': 3},
                            'thickness': 0.8,
                            'value': float(avg_perc),
                        }
                    },
                    title={'text': "درصد خالص میانگین", 'font': {'color': '#cbd5e1', 'size': 14}}
                ))
                gauge.update_layout(template="plotly_dark", height=280,
                                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                    font={'family': 'Vazirmatn'})
                st.plotly_chart(gauge, use_container_width=True)

            # نمودار میله‌ای ساعت مطالعه
            with g2:
                fig_hours = px.bar(
                    filtered_df, x='report_date', y='study_hours',
                    title=f"📊 روند ساعت مطالعه روزانه ({time_frame})",
                    labels={'study_hours': 'ساعت مطالعه', 'report_date': 'تاریخ'},
                    color='study_hours',
                    color_continuous_scale=['#0ea5e9', '#7c3aed', '#f472b6']
                )
                fig_hours.update_layout(
                    template="plotly_dark",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font={'family': 'Vazirmatn'},
                    coloraxis_showscale=False,
                    height=280
                )
                fig_hours.update_traces(marker_line_width=0, marker_line_color='#38bdf8')
                st.plotly_chart(fig_hours, use_container_width=True)

            # نمودار خطی تعداد تست‌ها
            fig_tests = px.line(
                filtered_df, x='report_date', y='total_tests',
                title=f"📈 روند پیشرفت تعداد تست‌ها ({time_frame})",
                labels={'total_tests': 'تعداد تست', 'report_date': 'تاریخ'},
                markers=True, color_discrete_sequence=['#4ade80']
            )
            fig_tests.update_traces(line=dict(width=3), marker=dict(size=9, line=dict(width=2, color='#0b0f19')))
            fig_tests.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font={'family': 'Vazirmatn'}
            )
            st.plotly_chart(fig_tests, use_container_width=True)

            # نمودار رضایت
            fig_sat = px.area(
                filtered_df, x='report_date', y='satisfaction',
                title="⭐ نمودار رضایت روزانه",
                labels={'satisfaction': 'امتیاز رضایت', 'report_date': 'تاریخ'},
                color_discrete_sequence=['#facc15']
            )
            fig_sat.update_traces(line=dict(width=2.5), fillcolor='rgba(250,204,21,0.15)')
            fig_sat.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font={'family': 'Vazirmatn'}
            )
            st.plotly_chart(fig_sat, use_container_width=True)

            # اشتراک در تلگرام
            summary_share = f"""📊 تحلیل عملکرد {time_frame} | آکادمی ۲۰
👤 دانش‌آموز: {st.session_state['name']}
⏳ مجموع ساعت مطالعه: {sum_hours:.1f} ساعت
📝 کل تست‌های زده‌شده: {sum_tests} تست
🎯 میانگین درصد آزمون‌ها: {avg_perc:.1f}%
⭐ میانگین رضایت: {avg_sat:.1f}/10
🔥 زنجیره مطالعه: {streak} روز متوالی
━━━━━━━━━━━━━━━━━━━━
👨‍🏫 مشاور: دکتر خشایار اشکبوس | @Kh_Ashkboos"""

            tg_share_link = "https://t.me/share/url?url=" + urllib.parse.quote(summary_share)
            st.markdown(f'<a href="{tg_share_link}" target="_blank" class="tg-button">📤 ارسال خلاصه آمار به تلگرام</a>',
                        unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# تب ۳: خروج
# ═══════════════════════════════════════════════════════
with main_tab3:
    st.markdown(f"""
    <div class="glass-card">
        <h3 style="margin:0 0 10px 0;">حساب کاربری: {st.session_state['name']}</h3>
        <p style="color:#94a3b8 !important;">نام کاربری: <code style="color:#38bdf8;">{st.session_state['username']}</code></p>
        <p style="color:#94a3b8 !important;">سطح: <span class="badge {level_badge}">{level_name}</span>
           &nbsp;|&nbsp; 🔥 زنجیره: <b style="color:#fb923c;">{streak} روز</b>
           &nbsp;|&nbsp; ⏳ کل مطالعه: <b style="color:#38bdf8;">{total_hours_all:.1f} ساعت</b></p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 خروج از حساب کاربری", use_container_width=True):
        st.session_state['logged_in'] = False
        st.rerun()
