import streamlit as st
import datetime
import urllib.parse
import sqlite3
import pandas as pd
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont
import io

# ۱. تنظیمات صفحه
st.set_page_config(
    page_title="سامانه هوشمند آکادمی ۲۰",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ۲. تزریق استایل با کنتراست فوق‌العاده بالا و راست‌به‌چپ تمیز
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');
    
    * {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl;
        text-align: right;
    }

    /* رنگ زمینه اصلی */
    .stApp {
        background-color: #0b0f19 !important;
        color: #ffffff !important;
    }

    /* هدر طلایی-فیروزه‌ای */
    .header-card {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        border: 2px solid #0284c7;
        border-radius: 18px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 0 25px rgba(2, 132, 199, 0.25);
        margin-bottom: 25px;
    }

    /* وضوح کامل کادرهای ورودی و متن‌ها */
    label, p, span, h1, h2, h3, h4, div {
        color: #ffffff !important;
        font-weight: 600;
    }

    input, textarea, select {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 10px !important;
    }

    /* کارت‌های شاخص تحلیلی */
    .metric-card {
        background: #111827;
        border: 1px solid #38bdf8;
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        margin-bottom: 15px;
    }
    .metric-num {
        font-size: 26px;
        font-weight: 900;
        color: #38bdf8 !important;
    }
    .metric-txt {
        font-size: 13px;
        color: #94a3b8 !important;
    }

    /* دکمه اختصاصی تلگرام */
    .tg-button {
        display: block;
        width: 100%;
        background: linear-gradient(90deg, #0284c7, #0369a1);
        color: #ffffff !important;
        text-align: center;
        font-size: 16px;
        font-weight: 800;
        padding: 14px;
        border-radius: 12px;
        text-decoration: none;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ۳. آماده‌سازی دیتابیس لوکال SQLite
conn = sqlite3.connect("konkur_academy.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, name TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, report_date DATE,
    satisfaction INT, study_hours REAL, total_tests INT, correct_tests INT,
    wrong_tests INT, percentage REAL, screen_time TEXT, social_time TEXT, details TEXT
)''')
conn.commit()

# ۴. تولید پوستر کارنامه تصویری (Image Generation با کنتراست بالا)
def generate_report_card(name, date_str, satisfaction, study_hours, total_tests, percentage, screen_time):
    img = Image.new('RGB', (850, 520), color='#0b0f19')
    draw = ImageDraw.Draw(img)

    # حاشیه نئونی فیروزه‌ای
    draw.rectangle([(15, 15), (835, 505)], outline='#0284c7', width=3)
    draw.rectangle([(30, 30), (820, 110)], fill='#111827', outline='#38bdf8', width=1)

    draw.text((280, 45), "ACADEMY 20 - STUDY REPORT", fill='#38bdf8')
    draw.text((240, 75), f"Student: {name}   |   Date: {date_str}", fill='#ffffff')

    # باکس‌های اطلاعاتی داخل کارنامه
    draw.rectangle([(50, 140), (400, 240)], fill='#1e293b')
    draw.text((70, 160), f"Study Duration: {study_hours} Hours", fill='#ffffff')
    draw.text((70, 200), f"Satisfaction Score: {satisfaction} / 10", fill='#facc15')

    draw.rectangle([(450, 140), (800, 240)], fill='#1e293b')
    draw.text((470, 160), f"Total Tests: {total_tests}", fill='#ffffff')
    draw.text((470, 200), f"Total Score: {percentage}%", fill='#4ade80')

    draw.rectangle([(50, 270), (800, 360)], fill='#1e293b')
    draw.text((70, 290), f"Digital Wellness / Screen Time: {screen_time}", fill='#f87171')
    draw.text((70, 325), "Monitored via Academy 20 Tracking Core", fill='#94a3b8')

    draw.text((230, 420), "Consultant: Dr. Khashayar Ashkboos", fill='#38bdf8')
    draw.text((310, 450), "Telegram: @Kh_Ashkboos", fill='#94a3b8')

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

# ۵. مدیریت نشست (Session State)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['name'] = ''

# صفحه ورود و ثبت نام
if not st.session_state['logged_in']:
    st.markdown("""
    <div class="header-card">
        <h2 style="color: #38bdf8 !important; margin-bottom: 5px;">👑 سامانه هوشمند آکادمی ۲۰</h2>
        <p style="color: #ffffff !important; margin: 0;">مدیریت، پایش و تحلیل علمی فرآیند کنکور | <b>دکتر خشایار اشکبوس</b></p>
    </div>
    """, unsafe_allow_html=True)

    tab_login, tab_reg = st.tabs(["🔑 ورود دانش‌آموز", "📝 ثبت‌نام دانش‌آموز جدید"])
    
    with tab_login:
        col_u, col_p = st.columns(2)
        u_in = col_u.text_input("نام کاربری:", key="l_user")
        p_in = col_p.text_input("رمز عبور:", type="password", key="l_pass")
        if st.button("ورود به داشبورد تحصیلی", use_container_width=True):
            c.execute("SELECT name FROM users WHERE username=? AND password=?", (u_in, p_in))
            res = c.fetchone()
            if res:
                st.session_state['logged_in'] = True
                st.session_state['username'] = u_in
                st.session_state['name'] = res[0]
                st.rerun()
            else:
                st.error("نام کاربری یا رمز عبور اشتباه است.")

    with tab_reg:
        name_in = st.text_input("نام و نام خانوادگی:")
        u_new = st.text_input("نام کاربری دلخواه (مثلاً کد ملی یا شماره همراه):")
        p_new = st.text_input("رمز عبور دلخواه:", type="password")
        if st.button("ثبت‌نام و عضویت در سامانه", use_container_width=True):
            if name_in and u_new and p_new:
                try:
                    c.execute("INSERT INTO users VALUES (?, ?, ?)", (u_new, p_new, name_in))
                    conn.commit()
                    st.success("حساب کاربری با موفقیت ساخته شد! اکنون وارد شوید.")
                except:
                    st.error("این نام کاربری قبلاً ثبت شده است.")
            else:
                st.warning("لطفاً همه فیلدها را پر کنید.")
    st.stop()

# ----------------- بخش اصلی سامانه (پس از ورود) -----------------
# هدر اصلی کاربر
st.markdown(f"""
<div class="header-card" style="padding: 15px;">
    <h3 style="margin: 0; color: #38bdf8 !important;">داشبورد نظارت مطالعاتی | آکادمی ۲۰</h3>
    <p style="margin: 5px 0 0 0; color: #ffffff !important;">دانش‌آموز کوشا: <b>{st.session_state['name']}</b></p>
</div>
""", unsafe_allow_html=True)

# تب‌های اصلی بالا (حل مشکل دیده نشدن در موبایل)
main_tab1, main_tab2, main_tab3 = st.tabs([
    "📝 ثبت گزارش کار روزانه", 
    "📈 تحلیل هفتگی و ماهانه (نمودارها)", 
    "⚙️ تنظیمات و خروج"
])

# ----------------- تب ۱: فرم ثبت گزارش روزانه -----------------
with main_tab1:
    c_d1, c_d2 = st.columns(2)
    rep_date = c_d1.date_input("تاریخ ثبت گزارش:", datetime.date.today())
    satisfaction = c_d2.slider("⭐️ کیفیت و رضایت از مطالعه امروز (۱ تا ۱۰):", 1, 10, 8)

    st.markdown("#### 📚 ثبت ریز پارت‌های درسی")
    num_slots = st.number_input("تعداد پارت‌های مطالعه امروز:", min_value=1, max_value=12, value=3)
    
    subjects = ["زیست‌شناسی", "شیمی", "فیزیک", "ریاضیات", "زمین‌شناسی", "فارسی", "دینی", "عربی", "زبان", "سایر"]
    
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
            src_study = c_src1.text_input("منبع درسنامه", key=f"src_s_{i}")
            src_test = c_src2.text_input("منبع تست", key=f"src_t_{i}")

            st.caption("آمار تست‌ها:")
            tc, tw, tu, td = st.columns(4)
            c_val = tc.number_input("صحیح", min_value=0, value=0, key=f"c_{i}")
            w_val = tw.number_input("غلط", min_value=0, value=0, key=f"w_{i}")
            u_val = tu.number_input("نزده", min_value=0, value=0, key=f"u_{i}")
            d_val = td.number_input("شک‌دار", min_value=0, value=0, key=f"d_{i}")

            notes = st.text_input("مبحث و توضیحات پارت", key=f"nt_{i}")

            s_tests = c_val + w_val + u_val
            total_tests += s_tests
            total_c += c_val
            total_w += w_val
            parts_summary.append(f"{i+1}. {subj} ({st_t.strftime('%H:%M')} تا {et_t.strftime('%H:%M')}) | {s_tests} تست ({c_val}ص/{w_val}غ)")

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
        st.success("✅ گزارش شما ذخیره شد و در بخش نمودارها اضافه گردید!")

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
        st.markdown(f'<a href="{tg_url}" target="_blank" class="tg-button">🚀 ارسال مستقیم به تلگرام مشاور</a>', unsafe_allow_html=True)

    with col_out2:
        img_bytes = generate_report_card(st.session_state['name'], str(rep_date), satisfaction, study_hours, total_tests, overall_perc, screen_t)
        st.image(img_bytes, caption="کارنامه گرافیکی اختصاصی شما", use_container_width=True)
        st.download_button("📥 دانلود کارت تصویری (PNG)", img_bytes, file_name=f"report_{rep_date}.png", mime="image/png", use_container_width=True)

# ----------------- تب ۲: نمودارهای تحلیلی هفتگی و ماهانه -----------------
with main_tab2:
    st.markdown("### 📈 داشبورد تحلیل و مقایسه عملکرد")
    
    df = pd.read_sql_query("SELECT * FROM reports WHERE username=? ORDER BY report_date ASC", 
                           conn, params=(st.session_state['username'],))

    if df.empty:
        st.info("⚠️ هنوز گزارشی ثبت نکرده‌اید! ابتدا در تب اول یک گزارش ثبت کنید تا نمودارها فعال شوند.")
    else:
        df['report_date'] = pd.to_datetime(df['report_date'])
        
        c_filter1, c_filter2 = st.columns([1, 2])
        time_frame = c_filter1.radio("انتخاب بازه تحلیلی:", ["۷ روز اخیر (هفتگی)", "۳۰ روز اخیر (ماهانه)"], horizontal=True)
        days = 7 if "۷" in time_frame else 30
        
        filtered_df = df[df['report_date'] >= (datetime.datetime.now() - datetime.timedelta(days=days))]

        # کارت‌های شاخص
        st.markdown(f"""
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <div class="metric-card" style="flex:1;">
                <div class="metric-num">{filtered_df['study_hours'].sum():.1f}</div>
                <div class="metric-txt">ساعت مطالعه کل بازه</div>
            </div>
            <div class="metric-card" style="flex:1;">
                <div class="metric-num">{filtered_df['total_tests'].sum()}</div>
                <div class="metric-txt">مجموع تست‌های بازه</div>
            </div>
            <div class="metric-card" style="flex:1;">
                <div class="metric-num">{filtered_df['percentage'].mean():.1f}%</div>
                <div class="metric-txt">میانگین درصد تست‌ها</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ۱. نمودار میله‌ای ساعت مطالعه
        fig_hours = px.bar(
            filtered_df, x='report_date', y='study_hours',
            title=f"روند ساعت مطالعه روزانه ({time_frame})",
            labels={'study_hours': 'ساعت مطالعه', 'report_date': 'تاریخ'},
            color_discrete_sequence=['#38bdf8']
        )
        fig_hours.update_layout(template="plotly_dark", plot_bgcolor='#111827', paper_bgcolor='#111827')
        st.plotly_chart(fig_hours, use_container_width=True)

        # ۲. نمودار خطی تعداد تست
        fig_tests = px.line(
            filtered_df, x='report_date', y='total_tests',
            title=f"روند پیشرفت تعداد تست‌ها ({time_frame})",
            labels={'total_tests': 'تعداد تست', 'report_date': 'تاریخ'},
            markers=True, color_discrete_sequence=['#4ade80']
        )
        fig_tests.update_layout(template="plotly_dark", plot_bgcolor='#111827', paper_bgcolor='#111827')
        st.plotly_chart(fig_tests, use_container_width=True)

        # ارسال تحلیل به تلگرام
        summary_share = f"""📊 تحلیل عملکرد {time_frame} | آکادمی ۲۰
👤 دانش‌آموز: {st.session_state['name']}
⏳ مجموع ساعت مطالعه: {filtered_df['study_hours'].sum():.1f} ساعت
📝 کل تست‌های زده‌شده: {filtered_df['total_tests'].sum()} تست
🎯 میانگین درصد آزمون‌ها: {filtered_df['percentage'].mean():.1f}%
━━━━━━━━━━━━━━━━━━━━
👨‍🏫 مشاور: دکتر خشایار اشکبوس | @Kh_Ashkboos"""

        tg_share_link = "https://t.me/share/url?url=" + urllib.parse.quote(summary_share)
        st.markdown(f'<a href="{tg_share_link}" target="_blank" class="tg-button">📤 ارسال خلاصه آمار هفتگی/ماهانه به تلگرام</a>', unsafe_allow_html=True)

# ----------------- تب ۳: خروج از حساب -----------------
with main_tab3:
    st.markdown(f"### حساب کاربری: {st.session_state['name']}")
    st.write(f"نام کاربری: `{st.session_state['username']}`")
    if st.button("خروج از حساب کاربری", use_container_width=True):
        st.session_state['logged_in'] = False
        st.rerun()
