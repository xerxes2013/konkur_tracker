import streamlit as st
import datetime
import urllib.parse
import sqlite3
import pandas as pd
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont
import io

# تنظیمات اولیه صفحه
st.set_page_config(page_title="سامانه آکادمی ۲۰ | دکتر اشکبوس", page_icon="👑", layout="wide")

# استایل فوق‌مدرن Glassmorphism و راست‌به‌چپ
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');
    * { font-family: 'Vazirmatn', sans-serif !important; direction: rtl; text-align: right; }
    .stApp { background: radial-gradient(circle at 10% 20%, #0f172a 0%, #020617 90%); color: #f8fafc; }
    .header-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));
        border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 20px; padding: 20px;
        text-align: center; box-shadow: 0 10px 30px -10px rgba(2, 132, 199, 0.3); margin-bottom: 25px;
    }
    .metric-box {
        background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px; padding: 15px; text-align: center;
    }
    .tg-btn {
        display: block; width: 100%; background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: white !important; text-align: center; font-size: 16px; font-weight: 800;
        padding: 14px; border-radius: 14px; text-decoration: none; margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- پایگاه داده SQLite -----------------
conn = sqlite3.connect("konkur_academy.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, name TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, report_date DATE,
    satisfaction INT, study_hours REAL, total_tests INT, correct_tests INT,
    wrong_tests INT, percentage REAL, screen_time TEXT, social_time TEXT, details TEXT
)''')
conn.commit()

# ----------------- تابع ساخت عکس کارنامه (Image Generation) -----------------
def generate_report_card(name, date_str, satisfaction, total_tests, percentage, screen_time, study_hours):
    img = Image.new('RGB', (800, 600), color='#0f172a')
    draw = ImageDraw.Draw(img)
    
    # کادر گرادیان شیشه‌ای
    draw.rectangle([(20, 20), (780, 580)], outline='#38bdf8', width=3)
    draw.rectangle([(40, 40), (760, 120)], fill='#1e293b')
    
    draw.text((300, 55), "ACADEMY 20 REPORT", fill='#38bdf8')
    draw.text((260, 85), f"Student: {name} | Date: {date_str}", fill='#94a3b8')
    
    # باکس‌های آماری
    draw.rectangle([(60, 160), (380, 260)], fill='#1e293b')
    draw.text((100, 180), f"Study Hours: {study_hours} hrs", fill='#f8fafc')
    draw.text((100, 220), f"Satisfaction: {satisfaction}/10", fill='#facc15')
    
    draw.rectangle([(420, 160), (740, 260)], fill='#1e293b')
    draw.text((460, 180), f"Total Tests: {total_tests}", fill='#f8fafc')
    draw.text((460, 220), f"Accuracy: {percentage}%", fill='#4ade80')

    draw.rectangle([(60, 290), (740, 390)], fill='#1e293b')
    draw.text((100, 330), f"Screen Time Today: {screen_time}", fill='#f87171')

    draw.text((220, 500), "Consultant: Dr. Khashayar Ashkboos", fill='#38bdf8')
    draw.text((300, 530), "Telegram: @Kh_Ashkboos", fill='#64748b')

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

# ----------------- احراز هویت (Login / Register) -----------------
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['name'] = ''

if not st.session_state['logged_in']:
    st.markdown("""
    <div class="header-card">
        <h2 style="color: #f8fafc; font-weight: 900;">سامانه جامع مشاوره تحصیلی آکادمی ۲۰</h2>
        <p style="color: #94a3b8;">دکتر خشایار اشکبوس (رتبه ۲۰ کنکور تجربی)</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab_log, tab_reg = st.tabs(["🔑 ورود به سامانه", "📝 ثبت‌نام دانش‌آموز جدید"])
    
    with tab_log:
        u_log = st.text_input("نام کاربری (کد ملی یا نام):", key="log_u")
        p_log = st.text_input("رمز عبور:", type="password", key="log_p")
        if st.button("ورود به پنل مطالعه"):
            c.execute("SELECT name FROM users WHERE username=? AND password=?", (u_log, p_log))
            user = c.fetchone()
            if user:
                st.session_state['logged_in'] = True
                st.session_state['username'] = u_log
                st.session_state['name'] = user[0]
                st.rerun()
            else:
                st.error("نام کاربری یا رمز عبور اشتباه است.")

    with tab_reg:
        name_reg = st.text_input("نام و نام خانوادگی:")
        u_reg = st.text_input("نام کاربری دلخواه:")
        p_reg = st.text_input("رمز عبور دلخواه:", type="password")
        if st.button("ساخت حساب کاربری"):
            try:
                c.execute("INSERT INTO users VALUES (?, ?, ?)", (u_reg, p_reg, name_reg))
                conn.commit()
                st.success("حساب کاربری با موفقیت ساخته شد! اکنون وارد شوید.")
            except:
                st.error("این نام کاربری قبلاً ثبت شده است.")
    st.stop()

# ----------------- پنل اصلی کاربری دانش‌آموز -----------------
st.sidebar.markdown(f"### 👤 {st.session_state['name']}")
if st.sidebar.button("خروج از حساب"):
    st.session_state['logged_in'] = False
    st.rerun()

menu = st.sidebar.radio("ناوبری سامانه:", ["📝 ثبت گزارش روزانه", "📊 نمودارها و بایگانی (هفتگی / ماهانه)"])

# ----------------- صفحه ۱: ثبت گزارش -----------------
if menu == "📝 ثبت گزارش روزانه":
    st.markdown(f"""
    <div class="header-card">
        <h3>ثبت گزارش کار شبانه | آکادمی ۲۰</h3>
        <p style="color:#38bdf8;">دانش‌آموز گرامی: {st.session_state['name']}</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    rep_date = c1.date_input("تاریخ گزارش:", datetime.date.today())
    satisfaction = c2.slider("⭐️ میزان رضایت از مطالعه امروز (۱ تا ۱۰):", 1, 10, 8)

    num_slots = st.number_input("تعداد پارت‌های مطالعه امروز:", min_value=1, max_value=10, value=3)
    subjects = ["زیست‌شناسی", "شیمی", "فیزیک", "ریاضیات", "زمین‌شناسی", "ادبیات", "دینی", "عربی", "زبان", "سایر"]
    
    total_tests, total_c, total_w = 0, 0, 0
    total_minutes = 0
    parts_summary = []

    for i in range(int(num_slots)):
        with st.expander(f"📌 پارت درسی {i+1}", expanded=(i == 0)):
            col_s1, col_s2 = st.columns([2, 1])
            subj = col_s1.selectbox(f"نام درس", subjects, key=f"s_{i}")
            if subj == "سایر":
                subj = col_s1.text_input(f"نام درس دلخواه", key=f"cs_{i}")
            test_type = col_s2.radio("نوع تست", ["آموزشی", "زمان‌دار"], horizontal=True, key=f"tt_{i}")
            
            c_t1, c_t2 = st.columns(2)
            st_t = c_t1.time_input("شروع", datetime.time(8, 0), key=f"st_{i}")
            et_t = c_t2.time_input("پایان", datetime.time(9, 30), key=f"et_{i}")

            dur = (datetime.datetime.combine(datetime.date.today(), et_t) - 
                   datetime.datetime.combine(datetime.date.today(), st_t)).seconds / 60
            if dur > 0: total_minutes += dur

            c_src1, c_src2 = st.columns(2)
            src_study = c_src1.text_input("منبع درسنامه", key=f"src_s_{i}")
            src_test = c_src2.text_input("منبع تست", key=f"src_t_{i}")

            tc, tw, tu, td = st.columns(4)
            c_val = tc.number_input("صحیح", 0, key=f"c_{i}")
            w_val = tw.number_input("غلط", 0, key=f"w_{i}")
            u_val = tu.number_input("نزده", 0, key=f"u_{i}")
            d_val = td.number_input("شک‌دار", 0, key=f"d_{i}")

            notes = st.text_input("مبحث و یادداشت", key=f"nt_{i}")
            s_tests = c_val + w_val + u_val
            total_tests += s_tests; total_c += c_val; total_w += w_val
            parts_summary.append(f"{i+1}. {subj} ({st_t.strftime('%H:%M')}-{et_t.strftime('%H:%M')}) | {s_tests} تست ({c_val}ص/{w_val}غ)")

    c_sc1, c_sc2 = st.columns(2)
    screen_t = c_sc1.text_input("کل مصرف گوشی امروز:", "۲:۱۵")
    social_t = c_sc2.text_input("فضای مجازی (اینستاگرام، تلگرام):", "۴۵ دقیقه")

    study_hours = round(total_minutes / 60, 2)
    overall_perc = round(((total_c * 3 - total_w) / (total_tests * 3)) * 100, 1) if total_tests > 0 else 0.0

    if st.button("💾 ثبت نهایی در کارنامه دیتابیس"):
        c.execute('''INSERT INTO reports (username, report_date, satisfaction, study_hours, 
                    total_tests, correct_tests, wrong_tests, percentage, screen_time, social_time, details)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (st.session_state['username'], rep_date, satisfaction, study_hours,
                   total_tests, total_c, total_w, overall_perc, screen_t, social_t, "\n".join(parts_summary)))
        conn.commit()
        st.success("✅ گزارش امروز ذخیره شد و نمودارهای شما به‌روزرسانی شدند!")

    # خروجی متنی و تصویری
    st.markdown("---")
    st.subheader("🖼 دریافت کارنامه تصویری و ارسال به تلگرام")

    report_text = f"""📊 گزارش کار شبانه | آکادمی ۲۰
👤 دانش‌آموز: {st.session_state['name']}
📅 تاریخ: {rep_date} | ⭐ رضایت: {satisfaction}/10
⏳ مجموع ساعت مطالعه: {study_hours} ساعت
📝 کل تست‌ها: {total_tests} | ✅ صحیح: {total_c} | ❌ غلط: {total_w}
🎯 درصد خالص: {overall_perc}%
📱 زمان گوشی: {screen_t} (مجازی: {social_t})
━━━━━━━━━━━━━━━━━━━━
👨‍🏫 مشاور: دکتر خشایار اشکبوس | @Kh_Ashkboos"""

    col_out1, col_out2 = st.columns(2)
    with col_out1:
        st.text_area("متن تلگرام:", report_text, height=180)
        tg_url = "https://t.me/share/url?url=" + urllib.parse.quote(report_text)
        st.markdown(f'<a href="{tg_url}" target="_blank" class="tg-btn">🚀 ارسال متن به تلگرام</a>', unsafe_allow_html=True)

    with col_out2:
        img_bytes = generate_report_card(st.session_state['name'], str(rep_date), satisfaction, total_tests, overall_perc, screen_t, study_hours)
        st.image(img_bytes, caption="پیش‌نمایش کارت کارنامه گرافیکی", use_container_width=True)
        st.download_button("📥 دانلود عکس کارنامه (PNG)", img_bytes, file_name=f"report_{rep_date}.png", mime="image/png")

# ----------------- صفحه ۲: آنالیز هفتگی و ماهانه -----------------
elif menu == "📊 نمودارها و بایگانی (هفتگی / ماهانه)":
    st.markdown("### 📈 داشبورد تحلیلی عملکرد دانش‌آموز")
    
    df = pd.read_sql_query("SELECT * FROM reports WHERE username=? ORDER BY report_date ASC", 
                           conn, params=(st.session_state['username'],))
    
    if df.empty:
        st.info("هنوز گزارشی ثبت نکرده‌اید! ابتدا از منوی قبل گزارش روزانه خود را ثبت کنید.")
    else:
        df['report_date'] = pd.to_datetime(df['report_date'])
        time_frame = st.radio("بازه تحلیل:", ["۷ روز اخیر (هفتگی)", "۳۰ روز اخیر (ماهانه)"], horizontal=True)
        days = 7 if "۷" in time_frame else 30
        
        filtered_df = df[df['report_date'] >= (datetime.datetime.now() - datetime.timedelta(days=days))]

        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("مجموع ساعت مطالعه بازه", f"{filtered_df['study_hours'].sum():.1f} ساعت")
        col_m2.metric("مجموع تست‌های زده‌شده", f"{filtered_df['total_tests'].sum()} تست")
        col_m3.metric("میانگین درصد آزمون‌ها", f"{filtered_df['percentage'].mean():.1f}%")

        # نمودار میله‌ای ساعت مطالعه
        fig_hours = px.bar(filtered_df, x='report_date', y='study_hours', 
                           title="روند ساعات مطالعه روزانه", labels={'study_hours': 'ساعت مطالعه', 'report_date': 'تاریخ'},
                           color_discrete_sequence=['#38bdf8'])
        fig_hours.update_layout(template="plotly_dark")
        st.plotly_chart(fig_hours, use_container_width=True)

        # نمودار خطی تعداد تست
        fig_tests = px.line(filtered_df, x='report_date', y='total_tests', 
                            title="روند پیشرفت تست‌زنی", labels={'total_tests': 'تعداد تست', 'report_date': 'تاریخ'},
                            markers=True, color_discrete_sequence=['#4ade80'])
        fig_tests.update_layout(template="plotly_dark")
        st.plotly_chart(fig_tests, use_container_width=True)

        # اشتراک‌گذاری خلاصه تحلیل
        summary_share = f"""📊 خلاصه کارنامه {time_frame}
👤 دانش‌آموز: {st.session_state['name']}
⏳ ساعت مطالعه بازه: {filtered_df['study_hours'].sum():.1f} ساعت
📝 مجموع تست‌ها: {filtered_df['total_tests'].sum()}
🎯 میانگین درصد: {filtered_df['percentage'].mean():.1f}%
آکادمی ۲۰ | دکتر اشکبوس @Kh_Ashkboos"""
        tg_share_url = "https://t.me/share/url?url=" + urllib.parse.quote(summary_share)
        st.markdown(f'<a href="{tg_share_url}" target="_blank" class="tg-btn">📤 ارسال آمار هفتگی/ماهانه به تلگرام</a>', unsafe_allow_html=True)
