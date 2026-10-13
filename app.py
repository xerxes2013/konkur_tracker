import streamlit as st
import datetime
import urllib.parse

st.set_page_config(page_title="گزارش کار آکادمی ۲۰", page_icon="📊", layout="centered")

# طراحی دارک و استایل راست‌به‌چپ
st.markdown("""
<style>
    body { direction: rtl; text-align: right; font-family: Tahoma, sans-serif; }
    .stTextInput, .stSelectbox, .stSlider, .stTextArea { direction: rtl; text-align: right; }
    div[data-testid="stExpander"] { background-color: #1e293b; border-radius: 10px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("📊 ثبت گزارش کار شبانه")
st.caption("آکادمی ۲۰ | دکتر خشایار اشکبوس (@Kh_Ashkboos)")

# ۱. اسلایدر رضایت
st.subheader("⭐ رضایت از مطالعه امروز")
satisfaction = st.slider("از ۱ تا ۱۰ به کیفیت مطالعه امروزت نمره بده:", 1, 10, 8)

# ۲. پارت‌های مطالعه
st.subheader("📚 پارت‌های مطالعاتی")
subjects = ["زیست‌شناسی", "شیمی", "فیزیک", "ریاضیات", "زمین‌شناسی", "ادبیات فارسی", "دین و زندگی", "عربی", "زبان انگلیسی", "سایر"]

num_slots = st.number_input("تعداد پارت‌های مطالعه امروز:", min_value=1, max_value=12, value=3)

total_tests = 0
total_c = 0
total_w = 0
parts_summary = []

for i in range(int(num_slots)):
    with st.expander(f"📌 پارت مطالعاتی {i+1}", expanded=True):
        subj = st.selectbox(f"نام درس", subjects, key=f"s_{i}")
        if subj == "سایر":
            subj = st.text_input(f"نام درس دلخواه را بنویسید", key=f"cs_{i}")
        
        c1, c2 = st.columns(2)
        start_t = c1.time_input(f"ساعت شروع", datetime.time(8, 0), key=f"st_{i}")
        end_t = c2.time_input(f"ساعت پایان", datetime.time(9, 30), key=f"et_{i}")
        
        c_src1, c_src2 = st.columns(2)
        src_study = c_src1.text_input(f"منبع درسنامه", key=f"src_s_{i}")
        src_test = c_src2.text_input(f"منبع تست", key=f"src_t_{i}")
        
        test_type = st.radio(f"نوع تست‌زنی", ["آموزشی", "زمان‌دار"], horizontal=True, key=f"tt_{i}")
        timed_dur = ""
        if test_type == "زمان‌دار":
            timed_dur = f" (تایم: {st.number_input('زمان آزمون (دقیقه)', min_value=5, max_value=200, value=30, key=f'td_{i}')} دقیقه)"
        
        tc, tw, tu, td = st.columns(4)
        c = tc.number_input("صحیح", min_value=0, value=0, key=f"c_{i}")
        w = tw.number_input("غلط", min_value=0, value=0, key=f"w_{i}")
        u = tu.number_input("نزده", min_value=0, value=0, key=f"u_{i}")
        d = td.number_input("شک‌دار", min_value=0, value=0, key=f"d_{i}")
        
        notes = st.text_input(f"مبحث / توضیحات این پارت", key=f"nt_{i}")
        
        slot_tests = c + w + u
        total_tests += slot_tests
        total_c += c
        total_w += w
        
        parts_summary.append(f"{i+1}. {subj} | {start_t.strftime('%H:%M')} تا {end_t.strftime('%H:%M')} | {test_type}{timed_dur}\n   ▫️ تست: {slot_tests} ({c} ص / {w} غ) | مبحث: {notes}")

# ۳. اسکرین تایم گوشی
st.subheader("📱 اسکرین تایم و مصرف گوشی")
c_sc1, c_sc2 = st.columns(2)
screen_time = c_sc1.text_input("کل زمان استفاده از گوشی امروز:", "۲:۱۵")
social_time = c_sc2.text_input("مدت فضای مجازی (اینستاگرام، تلگرام):", "۴۵ دقیقه")

# محاسبه درصد نهایی کنکور
overall_percent = 0.0
if total_tests > 0:
    overall_percent = round(((total_c * 3 - total_w) / (total_tests * 3)) * 100, 1)

# تولید متن نهایی برای کپی و تلگرام
report_text = f"""📊 گزارش کار شبانه | آکادمی ۲۰
👤 دانش‌آموز تحت نظر دکتر اشکبوس
⭐️ رضایت از روز: {satisfaction} از 10

📝 کل تست‌ها: {total_tests} | ✅ صحیح: {total_c} | ❌ غلط: {total_w}
🎯 درصد پاسخ‌گویی: {overall_percent}%
📱 زمان گوشی: {screen_time} (فضای مجازی: {social_time})
━━━━━━━━━━━━━━━━━━━━
📚 ریز پارت‌های مطالعه:
""" + "\n".join(parts_summary) + f"""
━━━━━━━━━━━━━━━━━━━━
👨‍🏫 مشاور: دکتر خشایار اشکبوس | @Kh_Ashkboos"""

st.markdown("---")
st.subheader("📋 متن آماده ارسال به مشاور")
st.text_area("متن گزارش کار:", report_text, height=220)

tg_url = "https://t.me/share/url?url=" + urllib.parse.quote(report_text)
st.markdown(f'<a href="{tg_url}" target="_blank"><button style="background-color:#0284c7;color:white;padding:14px;border-radius:12px;border:none;font-weight:bold;cursor:pointer;width:100%;font-size:16px;">🚀 ارسال مستقیم به تلگرام</button></a>', unsafe_allow_html=True)
