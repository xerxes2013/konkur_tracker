import streamlit as st
import datetime
import urllib.parse
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont
import io
import random

# ═══════════════════════════════════════════════════════
# ۱. تنظیمات صفحه
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="سامانه هوشمند آکادمی ۲۰ | دکتر اشکبوس",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════
# ۲. استایل‌های نئونی فوق‌مدرن و انیمیشن‌های سایبرپانک
# ═══════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');
    
    * {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl;
        text-align: right;
    }

    @keyframes neonGlow {
        0%, 100% { box-shadow: 0 0 15px rgba(56, 189, 248, 0.4), inset 0 0 15px rgba(56, 189, 248, 0.2); }
        50% { box-shadow: 0 0 35px rgba(168, 85, 247, 0.6), inset 0 0 20px rgba(168, 85, 247, 0.3); }
    }

    @keyframes floatEffect {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }

    .stApp {
        background: radial-gradient(circle at 10% 10%, #0d1527 0%, #060913 60%, #020408 100%) !important;
        color: #ffffff !important;
    }

    /* هدر کهکشانی */
    .hero-header {
        position: relative;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.85) 100%);
        backdrop-filter: blur(16px);
        border-radius: 24px;
        padding: 24px;
        text-align: center;
        margin-bottom: 24px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        animation: neonGlow 5s infinite alternate;
    }

    .hero-title {
        font-size: 28px;
        font-weight: 900;
        background: linear-gradient(90deg, #38bdf8, #c084fc, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }

    /* کارت‌های KPI تحلیلی */
    .stat-card {
        background: linear-gradient(145deg, rgba(17, 24, 39, 0.85), rgba(30, 41, 59, 0.7));
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 18px;
        padding: 16px;
        text-align: center;
        transition: 0.3s;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    }
    .stat-card:hover {
        transform: translateY(-4px);
        border-color: #38bdf8;
        box-shadow: 0 12px 30px rgba(56, 189, 248, 0.3);
    }

    /* XP و سطح‌بندی */
    .xp-bar-container {
        background: #1e293b;
        border-radius: 12px;
        height: 18px;
        width: 100%;
        overflow: hidden;
        margin-top: 6px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .xp-bar-fill {
        background: linear-gradient(90deg, #06b6d4, #a855f7);
        height: 100%;
        border-radius: 12px;
        transition: width 0.8s ease-in-out;
    }

    /* تایمر پومودورو */
    .pomo-box {
        background: rgba(15, 23, 42, 0.8);
        border: 1px dashed #38bdf8;
        border-radius: 16px;
        padding: 14px;
        text-align: center;
        margin-bottom: 18px;
    }

    /* دکمه اختصاصی تلگرام با افکت پالس */
    .tg-button {
        display: block;
        width: 100%;
        background: linear-gradient(90deg, #0284c7, #2563eb);
        color: #ffffff !important;
        text-align: center;
        font-size: 16px;
        font-weight: 800;
        padding: 14px;
        border-radius: 14px;
        text-decoration: none;
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.4);
        transition: 0.3s;
        margin-top: 10px;
    }
    .tg-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 28px rgba(2, 132, 199, 0.7);
    }

    /* اصلاح وضوح Selectbox و فیلدها */
    div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        color: white !important;
        border-radius: 12px !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
    }
    input, textarea {
        background-color: #1e293b !important;
        color: white !important;
        border-radius: 12px !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# ۳. دیتابیس لوکال SQLite
# ═══════════════════════════════════════════════════════
conn = sqlite3.connect("konkur_academy.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, name TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, report_date DATE,
    satisfaction INT, study_hours REAL, total_tests INT, correct_tests INT,
    wrong_tests INT, percentage REAL, screen_time TEXT, social_time TEXT, details TEXT, subjects_json TEXT
)''')
conn.commit()

# ═══════════════════════════════════════════════════════
# ۴. سیستم گیمیفیکیشن و سطح‌بندی (XP & Rank)
# ═══════════════════════════════════════════════════════
def calculate_gamification(total_hours, total_tests):
    # فرمول تجربه: هر ساعت ۵۰ اکس‌پی، هر تست ۲ اکس‌پی
    xp = int((total_hours * 50) + (total_tests * 2))
    levels = [
        (0, "🌱 داوطلب آغازین", 500),
        (500, "📘 جنگجوی نیمه‌شب", 1500),
        (1500, "⚔️ فاتح قلم‌چی", 3500),
        (3500, "🎯 شکارچی درصد ۱۰۰", 7000),
        (7000, "👑 اسطوره تجربی آکادمی ۲۰", 15000),
    ]
    cur_lvl, next_xp = levels[0][1], levels[0][2]
    progress = 0.0
    for i, (req, name, nxt) in enumerate(levels):
        if xp >= req:
            cur_lvl = name
            next_xp = nxt
            prev = req
            progress = min(1.0, max(0.0, (xp - prev) / (next_xp - prev)))
    return xp, cur_lvl, int(progress * 100)

# ═══════════════════════════════════════════════════════
# ۵. موتور رندر تصویر پوستر روزانه (High-Res Poster)
# ═══════════════════════════════════════════════════════
def generate_report_card(name, date_str, satisfaction, study_hours, total_tests, percentage, screen_time):
    W, H = 880, 560
    img = Image.new('RGB', (W, H), color='#090d16')
    draw = ImageDraw.Draw(img)

    # حاشیه‌های شیشه‌ای نئونی چندلایه
    draw.rectangle([(15, 15), (W-15, H-15)], outline='#38bdf8', width=2)
    draw.rectangle([(18, 18), (W-18, H-18)], outline='#818cf8', width=1)
    
    # سربرگ سلطنتی
    draw.rectangle([(35, 35), (W-35, 115)], fill='#111827', outline='#38bdf8', width=2)
    draw.text((W//2 - 180, 50), "★ ACADEMY 20 • SMART STUDY LOG ★", fill='#38bdf8')
    draw.text((W//2 - 150, 80), f"Student: {name}  |  Date: {date_str}", fill='#f8fafc')

    # ویجت ساعت مطالعه و رضایت
    draw.rectangle([(45, 140), (420, 260)], fill='#161f33', outline='#38bdf8', width=1)
    draw.text((65, 160), "STUDY DURATION", fill='#94a3b8')
    draw.text((65, 190), f"{study_hours} Hours", fill='#38bdf8')
    draw.text((65, 225), f"Satisfaction: {satisfaction} / 10 ⭐", fill='#facc15')

    # ویجت تست و درصد
    draw.rectangle([(460, 140), (W-45, 260)], fill='#161f33', outline='#4ade80', width=1)
    draw.text((480, 160), "TESTING PERFORMANCE", fill='#94a3b8')
    draw.text((480, 190), f"{total_tests} Tests Solved", fill='#f8fafc')
    draw.text((480, 225), f"Net Score: {percentage}%", fill='#4ade80')

    # اسکرین تایم
    draw.rectangle([(45, 280), (W-45, 390)], fill='#1f1624', outline='#f87171', width=1)
    draw.text((65, 300), "DIGITAL MONITORING (SCREEN TIME)", fill='#94a3b8')
    draw.text((65, 335), f"Phone Usage: {screen_time}", fill='#f87171')
    draw.text((65, 360), "Verified & Approved by Academy Core AI", fill='#64748b')

    # فوتر برندینگ
    draw.text((W//2 - 170, 480), "Mentor: Dr. Khashayar Ashkboos", fill='#38bdf8')
    draw.text((W//2 - 110, 510), "Telegram: @Kh_Ashkboos", fill='#64748b')

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

# ═══════════════════════════════════════════════════════
# ۶. مدیریت ورود و نشست
# ═══════════════════════════════════════════════════════
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['name'] = ''

if not st.session_state['logged_in']:
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">👑 سامانه هوشمند آکادمی ۲۰</div>
        <p style="color:#94a3b8; font-size:14px; margin:0;">پلتفرم رهگیری، تحلیل و جهش رتبه کنکور | <b>دکتر خشایار اشکبوس</b></p>
    </div>
    """, unsafe_allow_html=True)

    t_in, t_up = st.tabs(["🔑 ورود به سامانه", "📝 ثبت‌نام دانش‌آموز جدید"])
    with t_in:
        c1, c2 = st.columns(2)
        u = c1.text_input("نام کاربری:")
        p = c2.text_input("رمز عبور:", type="password")
        if st.button("ورود به پنل هوشمند", use_container_width=True):
            c.execute("SELECT name FROM users WHERE username=? AND password=?", (u, p))
            row = c.fetchone()
            if row:
                st.session_state['logged_in'] = True
                st.session_state['username'] = u
                st.session_state['name'] = row[0]
                st.rerun()
            else:
                st.error("نام کاربری یا رمز عبور اشتباه است.")
    with t_up:
        n_up = st.text_input("نام و نام خانوادگی:")
        u_up = st.text_input("نام کاربری جدید:")
        p_up = st.text_input("رمز عبور جدید:", type="password")
        if st.button("ثبت‌نام رسمی", use_container_width=True):
            if n_up and u_up and p_up:
                try:
                    c.execute("INSERT INTO users VALUES (?, ?, ?)", (u_up, p_up, n_up))
                    conn.commit()
                    st.success("حساب کاربری با موفقیت ایجاد شد! اکنون وارد شوید.")
                except:
                    st.error("این نام کاربری قبلاً استفاده شده است.")
    st.stop()

# ═══════════════════════════════════════════════════════
# ۷. بارگذاری داده‌های تاریخی و رتبه کاربر
# ═══════════════════════════════════════════════════════
df_user = pd.read_sql_query("SELECT * FROM reports WHERE username=? ORDER BY report_date ASC", conn, params=(st.session_state['username'],))
tot_hours = df_user['study_hours'].sum() if not df_user.empty else 0
tot_tests = df_user['total_tests'].sum() if not df_user.empty else 0
xp, rank_title, xp_percent = calculate_gamification(tot_hours, tot_tests)

# هدر بالای صفحه
st.markdown(f"""
<div class="hero-header">
    <div class="hero-title">داشبورد فرماندهی مطالعه | آکادمی ۲۰</div>
    <p style="color:#cbd5e1; margin:4px 0;">دانش‌آموز کوشا: <b>{st.session_state['name']}</b> | جایگاه: <b style="color:#38bdf8;">{rank_title}</b></p>
    <div style="max-width: 400px; margin: 10px auto 0 auto;">
        <div style="display:flex; justify-content:space-between; font-size:12px; color:#94a3b8;">
            <span>امتیاز تلاش (XP): {xp}</span>
            <span>پیشرفت سطح: {xp_percent}%</span>
        </div>
        <div class="xp-bar-container">
            <div class="xp-bar-fill" style="width: {xp_percent}%;"></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# تب‌های اصلی سامانه
tab1, tab2, tab3 = st.tabs(["📝 ثبت گزارش پارت‌ها", "📊 تحلیل سبد مطالعه و هوش‌مصنوعی", "⚙️ پروفایل"])

# ═══════════════════════════════════════════════════════
# تب ۱: ثبت پارت‌ها و خلاقیت زمان
# ═══════════════════════════════════════════════════════
with tab1:
    col_d, col_s = st.columns([1, 1])
    rep_date = col_d.date_input("📅 تاریخ ثبت گزارش:", datetime.date.today())
    satisfaction = col_s.slider("⭐️ میزان رضایت امروز از ۱ تا ۱۰:", 1, 10, 8)

    # ویجت تایمر پومودورو درون‌برنامه‌ای
    with st.expander("⏱ تایمر تمرکز پومودورو / زمان‌گیر آزمون (اختیاری)", expanded=False):
        st.markdown("""
        <div class="pomo-box">
            <h4 style="color:#38bdf8; margin:0;">قانون ۲۵ دقیقه تست سرعتی + ۵ دقیقه تحلیل</h4>
            <p style="font-size:13px; color:#94a3b8; margin:6px 0;">برای تست‌های زمان‌دار زیست و شیمی از این تایم استاندارد استفاده کن.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 📚 ثبت ریز فعالیت‌های درسی")
    num_slots = st.number_input("تعداد پارت‌های مطالعه امروز:", min_value=1, max_value=12, value=3)

    subjects = ["زیست‌شناسی", "شیمی", "فیزیک", "ریاضیات", "زمین‌شناسی", "فارسی", "دینی", "عربی", "زبان", "سایر"]
    total_tests, total_c, total_w = 0, 0, 0
    total_minutes = 0
    parts_summary = []
    subject_hours_dict = {}

    for i in range(int(num_slots)):
        with st.expander(f"📌 پارت درسی {i+1}", expanded=(i == 0)):
            c_s1, c_s2 = st.columns([2, 1])
            subj = c_s1.selectbox(f"درس (پارت {i+1})", subjects, key=f"s_{i}")
            if subj == "سایر":
                subj = c_s1.text_input("نام درس دلخواه", key=f"cs_{i}")
            test_type = c_s2.radio("نوع تست", ["آموزشی", "زمان‌دار"], horizontal=True, key=f"tt_{i}")

            # انتخاب هوشمند زمان با تفکیک ساعت و دقیقه
            c_t1, c_t2 = st.columns(2)
            st_t = c_t1.time_input("ساعت شروع", datetime.time(8, 0), key=f"st_{i}")
            et_t = c_t2.time_input("ساعت پایان", datetime.time(9, 30), key=f"et_{i}")

            dur = (datetime.datetime.combine(datetime.date.today(), et_t) - 
                   datetime.datetime.combine(datetime.date.today(), st_t)).total_seconds() / 60
            if dur <= 0: dur += 24 * 60
            total_minutes += dur
            subject_hours_dict[subj] = subject_hours_dict.get(subj, 0) + (dur / 60)

            c_src1, c_src2 = st.columns(2)
            src_study = c_src1.text_input("منبع درسنامه", key=f"src_s_{i}")
            src_test = c_src2.text_input("منبع تست", key=f"src_t_{i}")

            tc, tw, tu, td = st.columns(4)
            c_val = tc.number_input("صحیح", 0, key=f"c_{i}")
            w_val = tw.number_input("غلط", 0, key=f"w_{i}")
            u_val = tu.number_input("نزده", 0, key=f"u_{i}")
            d_val = td.number_input("شک‌دار", 0, key=f"d_{i}")

            notes = st.text_input("مبحث و نکات مهم این پارت", key=f"nt_{i}")
            s_tests = c_val + w_val + u_val
            total_tests += s_tests; total_c += c_val; total_w += w_val
            parts_summary.append(f"{i+1}. {subj} ({st_t.strftime('%H:%M')}-{et_t.strftime('%H:%M')}) | {s_tests} تست ({c_val}ص/{w_val}غ)")

    st.markdown("#### 📱 کنترل دیجیتال و مصرف گوشی")
    c_sc1, c_sc2 = st.columns(2)
    screen_t = c_sc1.text_input("کل مصرف گوشی امروز:", "۱:۴۵")
    social_t = c_sc2.text_input("مدت زمان در تلگرام/اینستاگرام:", "۳۵ دقیقه")

    study_hours = round(total_minutes / 60, 2)
    overall_perc = round(((total_c * 3 - total_w) / (total_tests * 3)) * 100, 1) if total_tests > 0 else 0.0

    # ارزیاب خودکار هوش مصنوعی
    ai_comment = "عالی پیش رفتی! تعادل ساعت مطالعه و تست بسیار مطلوب بود."
    if study_hours > 7 and total_tests < 60:
        ai_comment = "⚠️ ساعت مطالعه‌ات بالا بود اما حجم تست کمه؛ سعی کن سرعت ورود به تست‌ها رو بیشتر کنی."
    elif overall_perc >= 75 and total_tests > 80:
        ai_comment = "🔥 فوق‌العاده! دقت تست‌زنی بالای ۷۵٪ با حجم تست عالی؛ فرمول رتبه‌برتری یعنی همین!"

    st.info(f"🤖 **تحلیلگر هوشمند آکادمی ۲۰:** {ai_comment}")

    if st.button("💾 ثبت نهایی گزارش در پرونده تحصیلی", use_container_width=True):
        c.execute('''INSERT INTO reports (username, report_date, satisfaction, study_hours, 
                    total_tests, correct_tests, wrong_tests, percentage, screen_time, social_time, details, subjects_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (st.session_state['username'], rep_date, satisfaction, study_hours,
                   total_tests, total_c, total_w, overall_perc, screen_t, social_t, "\n".join(parts_summary), str(subject_hours_dict)))
        conn.commit()
        st.balloons()
        st.success("✅ گزارش ثبت شد و امتیاز تجربه (XP) به حساب شما اضافه گردید!")

    st.markdown("---")
    st.markdown("#### 📤 کارنامه تصویری و ارسال به تلگرام")
    col_out1, col_out2 = st.columns(2)

    report_text = f"""📊 گزارش کار شبانه | آکادمی ۲۰
👤 دانش‌آموز: {st.session_state['name']}
📅 تاریخ: {rep_date} | ⭐ رضایت: {satisfaction}/10
⏳ مجموع مطالعه: {study_hours} ساعت
📝 کل تست‌ها: {total_tests} (✅ صحیح: {total_c} | ❌ غلط: {total_w})
🎯 درصد خالص: {overall_perc}%
📱 اسکرین‌تایم گوشی: {screen_t} (مجازی: {social_t})
━━━━━━━━━━━━━━━━━━━━
📚 ریز پارت‌های مطالعه:
""" + "\n".join(parts_summary) + f"""
━━━━━━━━━━━━━━━━━━━━
💡 تحلیل هوشمند: {ai_comment}
👨‍🏫 مشاور: دکتر خشایار اشکبوس | @Kh_Ashkboos"""

    with col_out1:
        st.text_area("متن آماده ارسال به مشاور:", report_text, height=190)
        tg_url = "https://t.me/share/url?url=" + urllib.parse.quote(report_text)
        st.markdown(f'<a href="{tg_url}" target="_blank" class="tg-button">🚀 ارسال مستقیم به تلگرام مشاور</a>', unsafe_allow_html=True)

    with col_out2:
        img_bytes = generate_report_card(st.session_state['name'], str(rep_date), satisfaction, study_hours, total_tests, overall_perc, screen_t)
        st.image(img_bytes, caption="پیش‌نمایش کارنامه گرافیکی", use_container_width=True)
        st.download_button("📥 دانلود کارت تصویری (PNG)", img_bytes, file_name=f"report_{rep_date}.png", mime="image/png", use_container_width=True)

# ═══════════════════════════════════════════════════════
# تب ۲: داشبورد تحلیلی و بالانس سبد مطالعه
# ═══════════════════════════════════════════════════════
with tab2:
    st.markdown("### 📈 داشبورد پایش عملکرد و تعادل دروس")

    if df_user.empty:
        st.info("⚠️ هنوز گزارشی ثبت نشده است. پس از اولین ثبت، نمودارهای پیشرفته فعال می‌شوند.")
    else:
        df_user['report_date'] = pd.to_datetime(df_user['report_date'])
        time_frame = st.radio("بازه بررسی:", ["۷ روز اخیر (هفتگی)", "۳۰ روز اخیر (ماهانه)"], horizontal=True)
        days = 7 if "۷" in time_frame else 30
        f_df = df_user[df_user['report_date'] >= (pd.Timestamp(datetime.date.today() - datetime.timedelta(days=days)))]

        if f_df.empty:
            st.warning("در این بازه گزارشی یافت نشد.")
        else:
            # کارت‌های شاخص
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"""<div class="stat-card"><div style="font-size:24px; font-weight:900; color:#38bdf8;">{f_df['study_hours'].sum():.1f}</div><div style="font-size:12px; color:#94a3b8;">ساعت مطالعه کل</div></div>""", unsafe_allow_html=True)
            c2.markdown(f"""<div class="stat-card"><div style="font-size:24px; font-weight:900; color:#4ade80;">{f_df['total_tests'].sum()}</div><div style="font-size:12px; color:#94a3b8;">مجموع تست‌ها</div></div>""", unsafe_allow_html=True)
            c3.markdown(f"""<div class="stat-card"><div style="font-size:24px; font-weight:900; color:#facc15;">{f_df['percentage'].mean():.1f}%</div><div style="font-size:12px; color:#94a3b8;">میانگین درصد</div></div>""", unsafe_allow_html=True)
            c4.markdown(f"""<div class="stat-card"><div style="font-size:24px; font-weight:900; color:#c084fc;">{round(f_df['total_tests'].sum() / max(1, f_df['study_hours'].sum()), 1)}</div><div style="font-size:12px; color:#94a3b8;">سرعت تست بر ساعت</div></div>""", unsafe_allow_html=True)

            g1, g2 = st.columns(2)
            with g1:
                fig_h = px.bar(f_df, x='report_date', y='study_hours', title="📊 نوسان ساعت مطالعه روزانه",
                               labels={'study_hours': 'ساعت مطالعه', 'report_date': 'تاریخ'},
                               color_discrete_sequence=['#38bdf8'])
                fig_h.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_h, use_container_width=True)

            with g2:
                fig_t = px.line(f_df, x='report_date', y='total_tests', title="📈 پیشرفت حجم تست‌زنی",
                                labels={'total_tests': 'تعداد تست', 'report_date': 'تاریخ'},
                                markers=True, color_discrete_sequence=['#4ade80'])
                fig_t.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_t, use_container_width=True)

# ═══════════════════════════════════════════════════════
# تب ۳: خروج و وضعیت حساب
# ═══════════════════════════════════════════════════════
with tab3:
    st.markdown(f"""
    <div style="background:#111827; border:1px solid #38bdf8; border-radius:16px; padding:20px;">
        <h3>پروفایل تحصیلی: {st.session_state['name']}</h3>
        <p style="color:#94a3b8;">نام کاربری: <code>{st.session_state['username']}</code></p>
        <p style="color:#94a3b8;">سطح و جایگاه: <b style="color:#38bdf8;">{rank_title}</b> ({xp} XP)</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚪 خروج از حساب کاربری", use_container_width=True):
        st.session_state['logged_in'] = False
        st.rerun()
