import streamlit as st
import datetime
import urllib.parse

# تنظیمات اولیه صفحه
st.set_page_config(
    page_title="داشبورد تحصیلی آکادمی ۲۰",
    page_icon="👑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# تزریق CSS فوق‌پیشرفته (Glassmorphism & Neon Dark Theme)
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');
    
    * {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl;
        text-align: right;
    }

    /* پس‌زمینه کل صفحه */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(15, 23, 42) 0%, rgb(2, 6, 23) 90%);
        color: #f8fafc;
    }

    /* هدر لوکس آکادمی */
    .header-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 10px 30px -10px rgba(2, 132, 199, 0.3);
        margin-bottom: 25px;
    }

    .badge {
        display: inline-block;
        background: linear-gradient(90deg, #0284c7, #38bdf8);
        color: #041226 !important;
        font-weight: 800;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 13px;
        margin-bottom: 10px;
    }

    /* کارت‌های شاخص زنده */
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 20px;
    }
    
    .metric-box {
        flex: 1;
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 14px;
        text-align: center;
        backdrop-filter: blur(8px);
    }

    .metric-val {
        font-size: 24px;
        font-weight: 900;
        color: #38bdf8;
    }

    .metric-label {
        font-size: 12px;
        color: #94a3b8;
    }

    /* آکاردئون پارت‌ها */
    div[data-testid="stExpander"] {
        background: rgba(30, 41, 59, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 16px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* فیلدها و اینپوت‌ها */
    .stTextInput>div>div>input, .stSelectbox>div>div, .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.6) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }

    .stTextInput>div>div>input:focus, .stTextArea textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.3) !important;
    }

    /* دکمه ارسال تلگرام مدرن */
    .tg-btn {
        display: block;
        width: 100%;
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: white !important;
        text-align: center;
        font-size: 18px;
        font-weight: 800;
        padding: 16px;
        border-radius: 16px;
        border: none;
        text-decoration: none;
        box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.5);
        transition: transform 0.2s, box-shadow 0.2s;
        margin-top: 20px;
    }

    .tg-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 30px -5px rgba(2, 132, 199, 0.7);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ۱. بنر بالایی آکادمی
st.markdown("""
<div class="header-card">
    <span class="badge">👑 سیستم هوشمند گزارش‌دهی</span>
    <h2 style="color: #f8fafc; margin: 5px 0 8px 0; font-weight: 900;">داشبورد شبانه آکادمی ۲۰</h2>
    <p style="color: #94a3b8; font-size: 14px; margin: 0;">تحت نظارت و راهبری مستقیم <b>دکتر خشایار اشکبوس</b></p>
</div>
""", unsafe_allow_html=True)

# فرم ورود نام و رضایت
c_name, c_sat = st.columns([1.5, 1])
student_name = c_name.text_input("👤 نام و نام خانوادگی دانش‌آموز:", "دانش‌آموز کوشا")
satisfaction = c_sat.slider("⭐️ میزان رضایت امروز (۱ تا ۱۰):", 1, 10, 8)

st.write("")

# ۲. پارت‌های مطالعه
st.markdown("### 📚 ثبت ریز فعالیت‌های درسی")
num_slots = st.number_input("تعداد پارت‌های مطالعه امروز:", min_value=1, max_value=12, value=3)

subjects = ["زیست‌شناسی", "شیمی", "فیزیک", "ریاضیات", "زمین‌شناسی", "ادبیات فارسی", "دین و زندگی", "عربی", "زبان انگلیسی", "سایر"]

total_tests = 0
total_c = 0
total_w = 0
parts_summary = []

for i in range(int(num_slots)):
    with st.expander(f"📖 پارت مطالعاتی {i+1}", expanded=(i == 0)):
        col_s1, col_s2 = st.columns([2, 1])
        subj = col_s1.selectbox(f"نام درس (پارت {i+1})", subjects, key=f"s_{i}")
        if subj == "سایر":
            subj = col_s1.text_input(f"نام درس انتخابی", key=f"cs_{i}")
        
        test_type = col_s2.radio(f"نوع تست", ["آموزشی", "زمان‌دار"], horizontal=True, key=f"tt_{i}")
        
        c_t1, c_t2 = st.columns(2)
        start_t = c_t1.time_input(f"ساعت شروع", datetime.time(8, 0), key=f"st_{i}")
        end_t = c_t2.time_input(f"ساعت پایان", datetime.time(9, 30), key=f"et_{i}")

        c_src1, c_src2 = st.columns(2)
        src_study = c_src1.text_input(f"منبع درسنامه", key=f"src_s_{i}")
        src_test = c_src2.text_input(f"منبع تست", key=f"src_t_{i}")

        timed_dur_str = ""
        if test_type == "زمان‌دار":
            timed_min = st.number_input(f"مدت آزمون (دقیقه)", min_value=5, max_value=250, value=30, key=f"td_{i}")
            timed_dur_str = f" [⏱ {timed_min} دقیقه]"

        st.caption("🎯 آمار تفکیکی تست‌ها:")
        tc, tw, tu, td = st.columns(4)
        c = tc.number_input("صحیح", min_value=0, value=0, key=f"c_{i}")
        w = tw.number_input("غلط", min_value=0, value=0, key=f"w_{i}")
        u = tu.number_input("نزده", min_value=0, value=0, key=f"u_{i}")
        d = td.number_input("شک‌دار", min_value=0, value=0, key=f"d_{i}")

        notes = st.text_input(f"مبحث و نکات کلیدی مطالعه", key=f"nt_{i}")

        slot_tests = c + w + u
        total_tests += slot_tests
        total_c += c
        total_w += w

        slot_perc = round(((c * 3 - w) / (slot_tests * 3)) * 100, 1) if slot_tests > 0 else 0.0

        parts_summary.append(
            f"{i+1}. {subj} | {start_t.strftime('%H:%M')} تا {end_t.strftime('%H:%M')}\n"
            f"   ▫️ نوع: {test_type}{timed_dur_str} | منابع: {src_study or '-'} / {src_test or '-'}\n"
            f"   ▫️ تست: {slot_tests} (✅ {c} | ❌ {w} | 🔘 {u} | ❓ {d}) » درصد: {slot_perc}%\n"
            f"   ▫️ توضیحات: {notes or 'ندارد'}"
        )

# ۳. اسکرین تایم
st.write("")
st.markdown("### 📱 پایش و کنترل مصرف تلفن همراه")
c_sc1, c_sc2 = st.columns(2)
screen_time = c_sc1.text_input("کل استفاده از گوشی امروز:", "۱ ساعت و ۴۵ دقیقه")
social_time = c_sc2.text_input("فضای مجازی (اینستاگرام، تلگرام):", "۳۰ دقیقه")

# محاسبه شاخص‌های کلی
overall_percent = 0.0
if total_tests > 0:
    overall_percent = round(((total_c * 3 - total_w) / (total_tests * 3)) * 100, 1)

# کارت‌های شاخص زنده گرافیکی
st.markdown(f"""
<div class="metric-container">
    <div class="metric-box">
        <div class="metric-val">{total_tests}</div>
        <div class="metric-label">مجموع تست امروز</div>
    </div>
    <div class="metric-box">
        <div class="metric-val" style="color: #4ade80;">{total_c}</div>
        <div class="metric-label">پاسخ‌های صحیح</div>
    </div>
    <div class="metric-box">
        <div class="metric-val" style="color: {'#4ade80' if overall_percent >= 60 else '#f87171'};">{overall_percent}%</div>
        <div class="metric-label">درصد خالص آزمون</div>
    </div>
</div>
""", unsafe_allow_html=True)

# تولید متن رسمی برای گزارش شبانه تلگرام
today_str = datetime.date.today().strftime("%Y/%m/%d")
report_text = f"""📊 گزارش کار شبانه | آکادمی ۲۰
👤 دانش‌آموز: {student_name}
📅 تاریخ: {today_str}
⭐️ رضایت از روز: {satisfaction} از 10

📈 کل تست‌ها: {total_tests} | ✅ صحیح: {total_c} | ❌ غلط: {total_w}
🎯 درصد کل پاسخ‌گویی: {overall_percent}%
📱 اسکرین تایم گوشی: {screen_time} (شبکه‌های اجتماعی: {social_time})
━━━━━━━━━━━━━━━━━━━━
📚 ریز فعالیت پارت‌ها:
""" + "\n".join(parts_summary) + f"""
━━━━━━━━━━━━━━━━━━━━
👨‍🏫 مشاور: دکتر خشایار اشکبوس | @Kh_Ashkboos"""

st.markdown("### 📋 متن آماده ارسال به مشاور")
st.text_area("پیش‌نمایش خروجی:", report_text, height=220)

tg_url = "https://t.me/share/url?url=" + urllib.parse.quote(report_text)
st.markdown(f'<a href="{tg_url}" target="_blank" class="tg-btn">🚀 ارسال مستقیم به تلگرام مشاور</a>', unsafe_allow_html=True)
