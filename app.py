import streamlit as st
import datetime
import urllib.parse
import urllib.request
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import random
import os
import re
import math

# ═══════════════════════════════════════════════════════
# ۰. زیرساخت فارسی برای PIL
# ═══════════════════════════════════════════════════════
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_RTL = True
except ImportError:
    HAS_RTL = False


def fa(text):
    """تبدیل متن فارسی برای رندر در PIL"""
    text = str(text)
    if HAS_RTL:
        try:
            return get_display(arabic_reshaper.reshape(text))
        except Exception:
            return text
    return text


def ensure_font():
    """دانلود فونت وزیرمتن در اولین اجرا"""
    font_path = "Vazirmatn-Bold.ttf"
    if os.path.exists(font_path):
        return font_path
    urls = [
        "https://github.com/rastikerdar/vazirmatn/raw/master/fonts/ttf/Vazirmatn-Bold.ttf",
        "https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/ttf/Vazirmatn-Bold.ttf",
    ]
    for u in urls:
        try:
            urllib.request.urlretrieve(u, font_path)
            return font_path
        except Exception:
            continue
    return None


FONT_PATH = ensure_font()


def load_font(size):
    if FONT_PATH and os.path.exists(FONT_PATH):
        try:
            return ImageFont.truetype(FONT_PATH, size)
        except Exception:
            pass
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()


# ═══════════════════════════════════════════════════════
# ۱. تنظیمات صفحه
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="آکادمی ۲۰ | سیستم RPG کنکور",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════
# ۲. استایل‌ها
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
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(56, 189, 248, 0.35); }
        50% { box-shadow: 0 0 45px rgba(56, 189, 248, 0.85); }
    }
    @keyframes fillBar {
        from { width: 0%; }
        to { width: var(--target, 50%); }
    }
    @keyframes floatUp {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    @keyframes popIn {
        0% { transform: scale(0.6); opacity: 0; }
        60% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(1); }
    }
    @keyframes rotateGlow {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }

    .stApp {
        background: radial-gradient(circle at 15% 5%, #1e2447 0%, #0b0f19 42%, #05070f 100%) !important;
        color: #ffffff !important;
    }
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            radial-gradient(2px 2px at 20% 30%, rgba(56,189,248,0.45), transparent),
            radial-gradient(1.5px 1.5px at 65% 70%, rgba(74,222,128,0.4), transparent),
            radial-gradient(1.5px 1.5px at 82% 22%, rgba(250,204,21,0.4), transparent),
            radial-gradient(1px 1px at 40% 82%, rgba(248,113,113,0.4), transparent);
        background-size: 550px 550px, 420px 420px, 630px 630px, 320px 320px;
        pointer-events: none;
        z-index: 0;
        opacity: 0.55;
    }

    /* هدر */
    .hero-header {
        position: relative;
        background: linear-gradient(135deg, rgba(17,24,39,0.9) 0%, rgba(30,41,59,0.85) 100%);
        backdrop-filter: blur(14px);
        border-radius: 22px;
        padding: 26px 22px;
        text-align: center;
        margin-bottom: 22px;
        overflow: hidden;
        border: 1px solid rgba(56, 189, 248, 0.25);
        box-shadow: 0 10px 40px rgba(2, 132, 199, 0.18);
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
    .hero-sub { color: #cbd5e1 !important; font-size: 14px; margin: 0; }

    /* XP Bar */
    .xp-container {
        background: rgba(17,24,39,0.78);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(250, 204, 21, 0.35);
        border-radius: 18px;
        padding: 16px 20px;
        margin-bottom: 18px;
        box-shadow: 0 8px 26px rgba(250, 204, 21, 0.15);
        position: relative;
        overflow: hidden;
    }
    .xp-container::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, transparent, rgba(250,204,21,0.06), transparent);
        animation: gradientShift 6s linear infinite;
        background-size: 200% 100%;
    }
    .xp-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
        gap: 12px;
        flex-wrap: wrap;
    }
    .level-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(90deg, rgba(250,204,21,0.2), rgba(244,114,182,0.2));
        border: 2px solid #facc15;
        border-radius: 14px;
        padding: 8px 16px;
        font-weight: 900;
        font-size: 16px;
        color: #facc15 !important;
        animation: pulseGlow 3s ease-in-out infinite;
        white-space: nowrap;
    }
    .xp-amount {
        color: #38bdf8 !important;
        font-weight: 900;
        font-size: 15px;
    }
    .xp-track {
        background: #0b0f19;
        border-radius: 999px;
        height: 22px;
        overflow: hidden;
        position: relative;
        border: 1px solid rgba(56,189,248,0.25);
    }
    .xp-fill {
        height: 100%;
        background: linear-gradient(90deg, #0284c7, #7c3aed, #f472b6, #facc15);
        background-size: 300% 100%;
        animation: fillBar 1.4s cubic-bezier(.2,.9,.3,1.1) forwards, gradientShift 4s linear infinite;
        border-radius: 999px;
        box-shadow: 0 0 20px rgba(250,204,21,0.6);
        position: relative;
    }
    .xp-fill::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: gradientShift 2s linear infinite;
        background-size: 200% 100%;
    }

    /* کارت‌های شاخص */
    .metric-card {
        position: relative;
        background: linear-gradient(145deg, rgba(17,24,39,0.85), rgba(30,41,59,0.75));
        backdrop-filter: blur(12px);
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
        box-shadow: 0 14px 36px rgba(56, 189, 248, 0.4);
    }
    .metric-num {
        font-size: 30px;
        font-weight: 900;
        background: linear-gradient(90deg, #38bdf8, #4ade80);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .metric-txt { font-size: 12.5px; color: #94a3b8 !important; margin-top: 6px; }
    .metric-icon { font-size: 22px; display: block; margin-bottom: 4px; }

    /* Streak */
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

    /* بج دستاورد */
    .badge-ach {
        display: inline-block;
        padding: 14px 12px;
        border-radius: 14px;
        font-weight: 800;
        font-size: 13px;
        margin: 5px;
        border: 2px solid;
        text-align: center;
        transition: all 0.3s;
        cursor: pointer;
        animation: popIn 0.6s ease;
    }
    .badge-ach.unlocked {
        color: #facc15;
        border-color: #facc15;
        background: linear-gradient(145deg, rgba(250,204,21,0.15), rgba(244,114,182,0.08));
        box-shadow: 0 0 18px rgba(250,204,21,0.4);
    }
    .badge-ach.unlocked:hover {
        transform: translateY(-4px) rotate(-2deg);
        box-shadow: 0 0 30px rgba(250,204,21,0.75);
    }
    .badge-ach.locked {
        color: #475569;
        border-color: #334155;
        background: rgba(15,23,42,0.6);
        opacity: 0.6;
    }

    /* AI Coach */
    .ai-coach {
        background: linear-gradient(135deg, rgba(56,189,248,0.12), rgba(168,85,247,0.12));
        border: 1px solid rgba(56,189,248,0.4);
        border-radius: 16px;
        padding: 16px;
        margin: 12px 0;
        position: relative;
        overflow: hidden;
    }
    .ai-coach::before {
        content: '🤖';
        position: absolute;
        top: 8px;
        left: 12px;
        font-size: 22px;
        opacity: 0.5;
    }
    .ai-tip {
        padding: 8px 12px;
        margin: 6px 0;
        border-radius: 10px;
        font-size: 13.5px;
        border-right: 4px solid;
    }
    .ai-tip.success { background: rgba(74,222,128,0.1); border-color: #4ade80; color: #86efac; }
    .ai-tip.warning { background: rgba(250,204,21,0.1); border-color: #facc15; color: #fde047; }
    .ai-tip.danger { background: rgba(248,113,113,0.1); border-color: #f87171; color: #fca5a5; }
    .ai-tip.info { background: rgba(56,189,248,0.1); border-color: #38bdf8; color: #7dd3fc; }

    /* Pomodoro */
    .pomodoro-box {
        background: linear-gradient(145deg, #0f172a, #1e293b);
        border: 2px solid #38bdf8;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 30px rgba(56,189,248,0.3);
    }
    .pomo-time {
        font-size: 56px;
        font-weight: 900;
        font-family: 'Courier New', monospace !important;
        background: linear-gradient(90deg, #38bdf8, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 4px;
        line-height: 1;
    }
    .pomo-label {
        font-size: 13px;
        color: #94a3b8 !important;
        margin-top: 8px;
        font-weight: 700;
    }

    label, p, span, h1, h2, h3, h4, div {
        color: #ffffff !important;
        font-weight: 600;
    }

    input, textarea, select {
        background-color: rgba(30,41,59,0.85) !important;
        color: #ffffff !important;
        border: 1px solid rgba(56,189,248,0.35) !important;
        border-radius: 12px !important;
    }
    input:focus, textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 3px rgba(56,189,248,0.18) !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #0284c7, #7c3aed) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        padding: 10px 18px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(124,58,237,0.28) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 10px 30px rgba(124,58,237,0.55) !important;
    }

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
    }
    .tg-button:hover { transform: translateY(-3px); filter: brightness(1.1); }

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(17,24,39,0.6);
        padding: 8px;
        border-radius: 14px;
        border: 1px solid rgba(56,189,248,0.18);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        padding: 10px 14px !important;
        font-weight: 700 !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #0284c7, #7c3aed) !important;
        color: #ffffff !important;
    }

    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: #0b0f19; }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #38bdf8, #7c3aed);
        border-radius: 10px;
    }

    .glass-card {
        background: rgba(17,24,39,0.72);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(56,189,248,0.22);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.28);
    }

    /* رفع مشکل Dropdown */
    div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border-color: rgba(56,189,248,0.35) !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] input {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] *,
    div[data-baseweb="menu"],
    div[data-baseweb="menu"] *,
    ul[role="listbox"],
    ul[role="listbox"] *,
    li[role="option"],
    li[role="option"] * {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }
    ul[role="listbox"] li:hover,
    li[role="option"]:hover {
        background-color: #0284c7 !important;
    }
    li[aria-selected="true"] {
        background-color: #0369a1 !important;
        color: #ffffff !important;
        font-weight: 800 !important;
    }
    button[data-testid="stNumberInputStepUp"],
    button[data-testid="stNumberInputStepDown"] {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }
    div[data-baseweb="calendar"],
    div[data-baseweb="calendar"] * {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }

    .time-label {
        font-weight: 700;
        color: #38bdf8 !important;
        font-size: 13.5px;
        margin-bottom: 4px;
    }
    .time-preview {
        text-align: center;
        background: linear-gradient(90deg, #0284c7, #7c3aed);
        color: #fff;
        font-weight: 900;
        font-size: 17px;
        padding: 8px 12px;
        border-radius: 10px;
        margin-top: 4px;
        letter-spacing: 1.5px;
        box-shadow: 0 4px 15px rgba(2,132,199,0.4);
        animation: pulseGlow 3s ease-in-out infinite;
    }
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
c.execute('''CREATE TABLE IF NOT EXISTS parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT, report_id INTEGER, username TEXT, report_date DATE,
    subject TEXT, minutes REAL, tests INT, correct INT, wrong INT
)''')
c.execute('''CREATE TABLE IF NOT EXISTS user_badges (
    username TEXT, badge_id TEXT, unlocked_at TIMESTAMP,
    PRIMARY KEY (username, badge_id)
)''')
conn.commit()

# ═══════════════════════════════════════════════════════
# ۴. ثابت‌ها — جملات، سطح‌ها، مدال‌ها
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

# سطوح RPG: (XP موردنیاز، نام، ایموجی، رنگ)
LEVELS = [
    (0,     "نوآموز",         "🌱", "#94a3b8"),
    (500,   "تازه‌کار",        "📗", "#4ade80"),
    (1500,  "کوشا",            "📘", "#38bdf8"),
    (3000,  "سخت‌کوش",         "⚔️", "#a78bfa"),
    (6000,  "حرفه‌ای",          "🥇", "#facc15"),
    (12000, "استاد",           "👑", "#fb923c"),
    (25000, "افسانه‌ای",        "🌟", "#f472b6"),
    (50000, "اسطوره تجربی",    "🔱", "#f43f5e"),
]

# مدال‌های افتخار
BADGES = {
    "first_step":   ("🎯", "اولین قدم",        "اولین گزارش ثبت شد"),
    "hunter_100":   ("🏹", "شکارچی تست",       "۱۰۰+ تست در یک روز"),
    "hunter_200":   ("⚡", "تست‌زن افسانه‌ای",  "۲۰۰+ تست در یک روز"),
    "steel_focus":  ("🛡️", "تمرکز فولادین",    "زیر ۳۰ دقیقه گوشی"),
    "bio_marathon": ("🧬", "ماراتن زیست",      "۳+ ساعت زیست در یک روز"),
    "marathon_day": ("🏃", "ماراتن روزانه",    "۸+ ساعت مطالعه در یک روز"),
    "streak_7":     ("🔥", "هفت‌روز پیوسته",   "۷ روز متوالی مطالعه"),
    "streak_30":    ("💫", "ماه کامل",         "۳۰ روز متوالی مطالعه"),
    "early_bird":   ("🐓", "سحرخیز",           "شروع مطالعه قبل از ۶ صبح"),
    "night_owl":    ("🦉", "جغد شب",           "مطالعه بعد از ساعت ۲۳"),
    "perfect_day":  ("💯", "روز بی‌نقص",       "درصد تست ۱۰۰٪"),
    "consistent":   ("📊", "استمرار طلایی",    "۱۰ گزارش متوالی"),
}

# ═══════════════════════════════════════════════════════
# ۵. توابع محاسباتی
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


def calculate_xp(df):
    """XP = ساعت مطالعه × ۵۰ + تست × ۲"""
    if df.empty:
        return 0
    return int(df['study_hours'].sum() * 50 + df['total_tests'].sum() * 2)


def get_level(xp):
    """(سطح فعلی، سطح بعدی، درصد پیشرفت به سمت بعدی)"""
    current = LEVELS[0]
    next_lvl = None
    current_idx = 0
    for i, lvl in enumerate(LEVELS):
        if xp >= lvl[0]:
            current = lvl
            current_idx = i
    if current_idx + 1 < len(LEVELS):
        next_lvl = LEVELS[current_idx + 1]

    if next_lvl:
        range_xp = next_lvl[0] - current[0]
        gained = xp - current[0]
        progress = min(100, max(0, (gained / range_xp) * 100))
    else:
        progress = 100.0
    return current, next_lvl, progress


def parse_duration(text):
    """تبدیل '۲:۱۵' یا '۴۵ دقیقه' یا '۱ ساعت' به دقیقه"""
    text = str(text).strip()
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    for i, d in enumerate(persian_digits):
        text = text.replace(d, str(i))
    text = text.replace('ساعت', ':').replace('دقیقه', '').replace('دق', '')
    text = text.replace('،', '').replace(',', '').strip()

    if ':' in text:
        try:
            h, m = text.split(':')[:2]
            return int(float(h)) * 60 + int(float(m))
        except Exception:
            pass

    nums = re.findall(r'[\d.]+', text)
    if nums:
        return int(float(nums[0]))
    return 0


def check_badges(username, report, parts_data):
    """بررسی و بازگشت مدال‌های جدید باز شده"""
    new_badges = []
    c.execute("SELECT badge_id FROM user_badges WHERE username=?", (username,))
    existing = {r[0] for r in c.fetchall()}

    df_user = pd.read_sql_query(
        "SELECT * FROM reports WHERE username=? ORDER BY report_date ASC",
        conn, params=(username,)
    )
    total_reports = len(df_user)
    streak = compute_streak(df_user)

    tests_today = report['total_tests']
    study_hours = report['study_hours']
    perc = report['percentage']
    screen_min = parse_duration(report['screen_time'])

    bio_min = sum(p['minutes'] for p in parts_data if 'زیست' in p['subject'])
    earliest_start = None
    latest_end = None

    candidates = set()

    if total_reports >= 1:
        candidates.add("first_step")
    if tests_today >= 100:
        candidates.add("hunter_100")
    if tests_today >= 200:
        candidates.add("hunter_200")
    if screen_min > 0 and screen_min <= 30:
        candidates.add("steel_focus")
    if bio_min >= 180:
        candidates.add("bio_marathon")
    if study_hours >= 8:
        candidates.add("marathon_day")
    if streak >= 7:
        candidates.add("streak_7")
    if streak >= 30:
        candidates.add("streak_30")
    if perc >= 100 and tests_today >= 20:
        candidates.add("perfect_day")
    if total_reports >= 10:
        candidates.add("consistent")

    # بررسی ساعت شروع و پایان از parts
    for p in parts_data:
        sh = p.get('start_hour', 99)
        eh = p.get('end_hour', 0)
        if sh < 6:
            candidates.add("early_bird")
        if eh >= 23 or eh <= 3:
            candidates.add("night_owl")

    for bid in candidates:
        if bid not in existing:
            new_badges.append(bid)
            c.execute("INSERT OR IGNORE INTO user_badges VALUES (?, ?, ?)",
                      (username, bid, datetime.datetime.now()))

    if new_badges:
        conn.commit()
    return new_badges


def ai_coach_analysis(df, today_report=None):
    """تحلیل هوشمند مبتنی بر قواعد"""
    tips = []

    if df.empty:
        tips.append(("info", "🤖 هنوز داده‌ای برای تحلیل نیست. اولین گزارش را ثبت کن!"))
        return tips

    # نرخ تست بر ساعت
    total_hours = df['study_hours'].sum()
    total_tests = df['total_tests'].sum()
    if total_hours > 0:
        speed = total_tests / total_hours
        if speed >= 60:
            tips.append(("success", f"🚀 سرعت تست‌زنی‌ت فوق‌العاده است! ({speed:.0f} تست در ساعت)"))
        elif speed >= 35:
            tips.append(("success", f"👍 سرعت تست‌زنی خوبه ({speed:.0f} تست در ساعت). ادامه بده!"))
        elif speed >= 15:
            tips.append(("warning", f"⚙️ سرعت تست‌زنی متوسطه ({speed:.0f} تست در ساعت). تلاش کن به ۴۰+ برسونی."))
        else:
            tips.append(("danger", f"⚠️ سرعت تست‌زنی پایین است ({speed:.0f} تست در ساعت). روی تمرکز کار کن."))

    # نسبت اسکرین‌تایم به مطالعه
    if today_report:
        screen_min = parse_duration(today_report['screen_time'])
        study_min = today_report['study_hours'] * 60
        if study_min > 0:
            ratio = screen_min / study_min
            if ratio >= 1:
                tips.append(("danger", f"📱 اسکرین‌تایم ({screen_min} دقیقه) از مطالعه بیشتره! فوراً محدود کن."))
            elif ratio >= 0.6:
                tips.append(("warning", f"⚠️ اسکرین‌تایم بالاست ({ratio*100:.0f}% از مطالعه). هدف: زیر ۴۰٪."))
            else:
                tips.append(("success", f"🎯 تعادل دیجیتال عالی! ({ratio*100:.0f}% اسکرین‌تایم/مطالعه)"))

    # رضایت
    avg_sat = df['satisfaction'].mean()
    if avg_sat >= 8:
        tips.append(("success", f"😊 میانگین رضایتت {avg_sat:.1f}/10 عالیه. روحت شاده!"))
    elif avg_sat >= 6:
        tips.append(("info", f"🙂 میانگین رضایتت {avg_sat:.1f}/10 قابل قبوله. دنبال بهبود باش."))
    else:
        tips.append(("warning", f"💙 رضایتت {avg_sat:.1f}/10 پایینه. به خودت استراحت بده و برنامه رو متعادل کن."))

    # روند تست
    if len(df) >= 3:
        recent = df.tail(3)['total_tests'].mean()
        older = df.head(max(1, len(df) - 3))['total_tests'].mean()
        if recent > older * 1.2:
            tips.append(("success", "📈 روند تست‌زنی‌ت صعودیه! این مسیر رو ادامه بده."))
        elif recent < older * 0.8:
            tips.append(("warning", "📉 افت در تعداد تست‌ها دیده می‌شه. انگیزه‌ت رو برگردون!"))

    return tips


# ═══════════════════════════════════════════════════════
# ۶. تولید پوستر گرافیکی نئونی ۳بعدی با فونت فارسی
# ═══════════════════════════════════════════════════════
def draw_neon_text(base_img, text, xy, font, color, glow_color, glow_size=8):
    """رندر متن با افکت نئون درخشان"""
    overlay = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # چند لایه برای شدت نور
    for offset in range(glow_size, 0, -1):
        alpha = int(70 * (1 - offset / glow_size))
        bbox = od.textbbox(xy, text, font=font)
        od.text((xy[0] + offset, xy[1]), text, font=font, fill=glow_color + (alpha,))
        od.text((xy[0] - offset, xy[1]), text, font=font, fill=glow_color + (alpha,))
        od.text((xy[0], xy[1] + offset), text, font=font, fill=glow_color + (alpha,))
        od.text((xy[0], xy[1] - offset), text, font=font, fill=glow_color + (alpha,))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=3))
    base_img.paste(overlay, (0, 0), overlay)
    d = ImageDraw.Draw(base_img)
    # سایه زیرین
    d.text((xy[0] + 2, xy[1] + 2), text, font=font, fill=(0, 0, 0))
    d.text(xy, text, font=font, fill=color)


def draw_academy_badge(img, cx, cy, r):
    """نشان طلایی آکادمی ۲۰"""
    d = ImageDraw.Draw(img, 'RGBA')
    # هاله بیرونی
    for i in range(20, 0, -1):
        alpha = int(80 * (1 - i / 20))
        d.ellipse([(cx - r - i, cy - r - i), (cx + r + i, cy + r + i)],
                  fill=(250, 204, 21, alpha))
    # حلقه طلایی
    d.ellipse([(cx - r, cy - r), (cx + r, cy + r)],
              fill=(30, 25, 10), outline=(250, 204, 21), width=4)
    d.ellipse([(cx - r + 6, cy - r + 6), (cx + r - 6, cy + r - 6)],
              outline=(255, 220, 90), width=2)
    # متن ۲۰
    f = load_font(34)
    txt = "20"
    bbox = d.textbbox((0, 0), txt, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text((cx - tw // 2, cy - th // 2 - 6), txt, font=f, fill=(250, 204, 21))


def generate_report_card(name, date_str, satisfaction, study_hours, total_tests,
                          percentage, screen_time, level_name, xp, streak):
    W, H = 1000, 700
    img = Image.new('RGB', (W, H), '#05080f')
    draw = ImageDraw.Draw(img)

    # پس‌زمینه گرادیانی تیره
    for y in range(H):
        ratio = y / H
        r = int(8 + 25 * ratio)
        g = int(11 + 30 * ratio)
        b = int(22 + 55 * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # شبکه نقطه‌ای
    for x in range(0, W, 40):
        for y in range(0, H, 40):
            if (x + y) % 120 == 0:
                draw.ellipse([(x - 1, y - 1), (x + 1, y + 1)], fill=(56, 189, 248, 40))

    # قاب نئونی سه‌لایه
    for i, col in enumerate([(56, 189, 248), (124, 58, 237), (244, 114, 182)]):
        draw.rectangle([(15 + i * 3, 15 + i * 3), (W - 15 - i * 3, H - 15 - i * 3)],
                       outline=col, width=2)

    # گوشه‌های تزئینی
    corner_size = 40
    for cx, cy in [(20, 20), (W - 20, 20), (20, H - 20), (W - 20, H - 20)]:
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                draw.line([(cx, cy), (cx + dx * corner_size, cy)], fill=(250, 204, 21), width=3)
                draw.line([(cx, cy), (cx, cy + dy * corner_size)], fill=(250, 204, 21), width=3)

    # هدر
    header_text = fa("آکادمی ۲۰ • کارنامه عملکرد روزانه")
    f_header = load_font(28)
    bbox = draw.textbbox((0, 0), header_text, font=f_header)
    tw = bbox[2] - bbox[0]
    draw_neon_text(img, header_text, ((W - tw) // 2, 40), f_header,
                   (255, 255, 255), (56, 189, 248), glow_size=10)

    # نام دانش‌آموز
    name_txt = fa(f"دانش‌آموز: {name}")
    f_name = load_font(22)
    bbox = draw.textbbox((0, 0), name_txt, font=f_name)
    tw = bbox[2] - bbox[0]
    draw_neon_text(img, name_txt, ((W - tw) // 2, 85), f_name,
                   (200, 220, 255), (124, 58, 237), glow_size=6)

    # تاریخ
    date_txt = fa(f"تاریخ: {date_str}")
    f_date = load_font(16)
    bbox = draw.textbbox((0, 0), date_txt, font=f_date)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 118), date_txt, font=f_date, fill=(148, 163, 184))

    # خط جداکننده
    draw.line([(60, 150), (W - 60, 150)], fill=(56, 189, 248), width=2)

    # ═══ نشان طلایی آکادمی (وسط راست)
    draw_academy_badge(img, W - 110, 220, 50)

    # ═══ کارت‌های داده با نئون
    def draw_data_card(x, y, w, h, label, value, color):
        # سایه
        draw.rectangle([(x + 3, y + 3), (x + w + 3, y + h + 3)], fill=(0, 0, 0, 100))
        # بدنه
        draw.rectangle([(x, y), (x + w, y + h)], fill=(15, 23, 42), outline=color, width=2)
        # گوشه روشن
        draw.line([(x, y), (x + 25, y)], fill=(255, 255, 255), width=3)
        draw.line([(x, y), (x, y + 25)], fill=(255, 255, 255), width=3)
        # لیبل
        f_lbl = load_font(16)
        draw.text((x + 20, y + 15), fa(label), font=f_lbl, fill=(148, 163, 184))
        # مقدار
        f_val = load_font(32)
        draw.text((x + 20, y + h // 2 - 8), fa(str(value)), font=f_val, fill=color)

    # چیدمان ۲×۲ کارت‌ها
    card_w, card_h = 400, 110
    draw_data_card(50, 180, card_w, card_h,
                   "⏳ ساعت مطالعه", f"{study_hours} ساعت", (56, 189, 248))
    draw_data_card(480, 180, card_w, card_h,
                   "📝 تعداد تست", f"{total_tests} تست", (74, 222, 128))
    draw_data_card(50, 305, card_w, card_h,
                   "🎯 درصد خالص", f"{percentage}%", (250, 204, 21))
    draw_data_card(480, 305, card_w, card_h,
                   "⭐ رضایت روز", f"{satisfaction}/10", (244, 114, 182))

    # ═══ نوار اسکرین‌تایم
    draw.rectangle([(50, 435), (W - 50, 490)], fill=(20, 15, 15), outline=(248, 113, 113), width=2)
    f_s = load_font(18)
    draw.text((70, 450), fa(f"📱 اسکرین‌تایم امروز: {screen_time}"), font=f_s, fill=(248, 113, 113))

    # ═══ اطلاعات RPG
    draw.rectangle([(50, 505), (W - 50, 590)], fill=(15, 20, 40),
                   outline=(168, 85, 247), width=2)
    f_rpg = load_font(20)
    draw.text((70, 520), fa(f"🎮 سطح: {level_name}"), font=f_rpg, fill=(250, 204, 21))
    draw.text((70, 555), fa(f"⚡ XP کل: {xp:,}"), font=f_rpg, fill=(56, 189, 248))
    draw.text((550, 520), fa(f"🔥 زنجیره: {streak} روز"), font=f_rpg, fill=(251, 146, 60))

    # ═══ فوتر
    draw.line([(60, 610), (W - 60, 610)], fill=(56, 189, 248), width=1)
    f_foot = load_font(16)
    foot1 = fa("مشاور: دکتر خشایار اشکبوس")
    bbox = draw.textbbox((0, 0), foot1, font=f_foot)
    draw.text(((W - (bbox[2] - bbox[0])) // 2, 625), foot1, font=f_foot, fill=(56, 189, 248))
    foot2 = "Telegram: @Kh_Ashkboos"
    bbox = draw.textbbox((0, 0), foot2, font=f_foot)
    draw.text(((W - (bbox[2] - bbox[0])) // 2, 655), foot2, font=f_foot, fill=(148, 163, 184))

    buf = io.BytesIO()
    img.save(buf, format='PNG', quality=95)
    return buf.getvalue()


# ═══════════════════════════════════════════════════════
# ۷. انتخابگر ساعت خلاقانه
# ═══════════════════════════════════════════════════════
def creative_time_picker(label, key_prefix, default_h=8, default_m=0):
    st.markdown(f'<div class="time-label">🕐 {label}</div>', unsafe_allow_html=True)
    col_h, col_m = st.columns([3, 2])
    h = col_h.slider("ساعت", 0, 23, default_h, key=f"{key_prefix}_h", label_visibility="collapsed")
    m = col_m.slider("دقیقه", 0, 55, default_m, step=5, key=f"{key_prefix}_m", label_visibility="collapsed")
    st.markdown(f'<div class="time-preview">⏰ {h:02d}:{m:02d}</div>', unsafe_allow_html=True)
    return datetime.time(h, m)


# ═══════════════════════════════════════════════════════
# ۸. تایمر پومودورو
# ═══════════════════════════════════════════════════════
if 'pomo' not in st.session_state:
    st.session_state.pomo = {
        'running': False,
        'end_time': None,
        'mode': 'focus',
        'duration': 25 * 60,
    }


def render_pomodoro():
    pomo = st.session_state.pomo

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        mode = st.radio("حالت", ["🎯 تمرکز (۲۵ دقیقه)", "☕ استراحت (۵ دقیقه)", "⚡ تست سرعتی (۱۰ دقیقه)"],
                        key="pomo_mode_radio", horizontal=False)
    with col2:
        custom_min = st.number_input("دقیقه دلخواه", 1, 120, 25, key="pomo_custom")

    durations = {"🎯 تمرکز (۲۵ دقیقه)": 25 * 60,
                 "☕ استراحت (۵ دقیقه)": 5 * 60,
                 "⚡ تست سرعتی (۱۰ دقیقه)": 10 * 60}
    selected_dur = durations.get(mode, custom_min * 60)

    # نمایش
    placeholder = st.empty()

    def show_timer():
        pomo = st.session_state.pomo
        if pomo['running'] and pomo['end_time']:
            remaining = int((pomo['end_time'] - datetime.datetime.now()).total_seconds())
            if remaining <= 0:
                pomo['running'] = False
                remaining = 0
                st.toast("⏰ زمان تمام شد!", icon="🔔")
            mins, secs = divmod(max(0, remaining), 60)
        else:
            mins, secs = divmod(selected_dur, 60)

        placeholder.markdown(f"""
        <div class="pomodoro-box">
            <div class="pomo-time">{mins:02d}:{secs:02d}</div>
            <div class="pomo-label">{"در حال اجرا..." if pomo['running'] else "آماده شروع"}</div>
        </div>
        """, unsafe_allow_html=True)

    show_timer()

    btn1, btn2, btn3 = st.columns(3)
    if btn1.button("▶️ شروع", use_container_width=True, key="pomo_start"):
        st.session_state.pomo['running'] = True
        st.session_state.pomo['end_time'] = datetime.datetime.now() + datetime.timedelta(seconds=selected_dur)
        st.rerun()

    if btn2.button("⏸️ توقف", use_container_width=True, key="pomo_pause"):
        if st.session_state.pomo['running'] and st.session_state.pomo['end_time']:
            remaining = int((st.session_state.pomo['end_time'] - datetime.datetime.now()).total_seconds())
            st.session_state.pomo['running'] = False
            st.session_state.pomo['end_time'] = None
            st.info(f"⏸️ متوقف شد. باقی‌مانده: {remaining//60}:{remaining%60:02d}")
        st.rerun()

    if btn3.button("🔄 ریست", use_container_width=True, key="pomo_reset"):
        st.session_state.pomo = {'running': False, 'end_time': None, 'mode': 'focus', 'duration': 25 * 60}
        st.rerun()

    # اگر در حال اجرا، رفرش خودکار هر ثانیه
    if st.session_state.pomo['running']:
        st.markdown(
            '<meta http-equiv="refresh" content="1">',
            unsafe_allow_html=True
        )


# ═══════════════════════════════════════════════════════
# ۹. نشست
# ═══════════════════════════════════════════════════════
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['name'] = ''

# ═══════════════════════════════════════════════════════
# ۱۰. ورود / ثبت‌نام
# ═══════════════════════════════════════════════════════
if not st.session_state['logged_in']:
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">🎮 آکادمی ۲۰ — سیستم RPG کنکور</div>
        <p class="hero-sub">XP بگیر، لول‌آپ شو، مدال باز کن، فتح کن! | <b>دکتر خشایار اشکبوس</b></p>
    </div>
    """, unsafe_allow_html=True)

    tab_login, tab_reg = st.tabs(["🔑 ورود", "📝 ثبت‌نام جدید"])

    with tab_login:
        col_u, col_p = st.columns(2)
        u_in = col_u.text_input("نام کاربری:", key="l_user")
        p_in = col_p.text_input("رمز عبور:", type="password", key="l_pass")
        if st.button("🚀 ورود به ماجراجویی", use_container_width=True):
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
        u_new = st.text_input("نام کاربری دلخواه:")
        p_new = st.text_input("رمز عبور دلخواه:", type="password")
        if st.button("✨ آغاز سفر قهرمانی", use_container_width=True):
            if name_in and u_new and p_new:
                try:
                    c.execute("INSERT INTO users VALUES (?, ?, ?)", (u_new, p_new, name_in))
                    conn.commit()
                    st.success("🎉 حساب ساخته شد! وارد شو و سفرت رو شروع کن.")
                except Exception:
                    st.error("⚠️ این نام کاربری قبلاً گرفته شده.")
            else:
                st.warning("لطفاً همه فیلدها را پر کنید.")
    st.stop()

# ═══════════════════════════════════════════════════════
# ۱۱. داشبورد اصلی
# ═══════════════════════════════════════════════════════
df_all = pd.read_sql_query("SELECT * FROM reports WHERE username=? ORDER BY report_date ASC",
                           conn, params=(st.session_state['username'],))
streak = compute_streak(df_all)
total_xp = calculate_xp(df_all)
current_lvl, next_lvl, progress = get_level(total_xp)
motivation = random.choice(MOTIVATIONS)

# هدر
st.markdown(f"""
<div class="hero-header">
    <div class="hero-title">داشبورد قهرمان | آکادمی ۲۰</div>
    <p class="hero-sub">🎯 {st.session_state['name']} — سطح {current_lvl[1]}</p>
</div>
""", unsafe_allow_html=True)

# XP Bar
xp_next_txt = ""
if next_lvl:
    remaining_xp = next_lvl[0] - total_xp
    xp_next_txt = f"<span style='color:#94a3b8; font-size:12px;'>({remaining_xp:,} XP تا {next_lvl[1]})</span>"
else:
    xp_next_txt = "<span style='color:#facc15; font-size:12px;'>🔥 به بالاترین سطح رسیدی!</span>"

st.markdown(f"""
<div class="xp-container">
    <div class="xp-row">
        <div class="level-badge">
            <span>{current_lvl[2]}</span>
            <span>سطح {current_lvl[1]}</span>
        </div>
        <div style="text-align:left;">
            <div class="xp-amount">⚡ {total_xp:,} XP</div>
            <div style="font-size:11px; color:#94a3b8;">{xp_next_txt}</div>
        </div>
        <div class="streak-badge">🔥 {streak} روز متوالی</div>
    </div>
    <div class="xp-track">
        <div class="xp-fill" style="--target: {progress:.1f}%; width: {progress:.1f}%;"></div>
    </div>
    <div style="display:flex; justify-content:space-between; margin-top:6px; font-size:11px; color:#94a3b8;">
        <span>{current_lvl[0]:,} XP</span>
        <span style="color:#facc15; font-weight:800;">{progress:.1f}%</span>
        <span>{"{:,.0f}".format(next_lvl[0]) if next_lvl else "∞"} XP</span>
    </div>
</div>
""", unsafe_allow_html=True)

# نوار انگیزشی
st.markdown(f"""
<div class="glass-card" style="display:flex; align-items:center; gap:14px;">
    <div style="font-size:28px;">💬</div>
    <div style="font-size:14px; color:#e2e8f0;">{motivation}</div>
</div>
""", unsafe_allow_html=True)

# تب‌ها
main_tab1, main_tab2, main_tab3, main_tab4, main_tab5 = st.tabs([
    "📝 ثبت گزارش",
    "🍅 پومودورو",
    "📈 تحلیل‌ها",
    "🏆 دستاوردها",
    "⚙️ تنظیمات"
])

# ═══════════════════════════════════════════════════════
# تب ۱: ثبت گزارش
# ═══════════════════════════════════════════════════════
with main_tab1:
    c_d1, c_d2 = st.columns(2)
    rep_date = c_d1.date_input("📅 تاریخ ثبت گزارش:", datetime.date.today())
    satisfaction = c_d2.slider("⭐️ کیفیت مطالعه (۱ تا ۱۰):", 1, 10, 8)

    st.markdown("#### 📚 ریز پارت‌های درسی")
    num_slots = st.number_input("تعداد پارت‌ها:", min_value=1, max_value=12, value=3)

    subjects = ["زیست‌شناسی", "شیمی", "فیزیک", "ریاضیات", "زمین‌شناسی",
                "فارسی", "دینی", "عربی", "زبان", "سایر"]

    total_tests, total_c, total_w = 0, 0, 0
    total_minutes = 0
    parts_summary = []
    parts_data = []

    for i in range(int(num_slots)):
        with st.expander(f"📌 پارت {i+1}", expanded=(i == 0)):
            col_s1, col_s2 = st.columns([2, 1])
            subj = col_s1.selectbox(f"درس (پارت {i+1})", subjects, key=f"s_{i}")
            if subj == "سایر":
                subj = col_s1.text_input("نام درس", key=f"cs_{i}")
            test_type = col_s2.radio("نوع تست", ["آموزشی", "زمان‌دار"],
                                     horizontal=True, key=f"tt_{i}")

            c_t1, c_t2 = st.columns(2)
            with c_t1:
                st_t = creative_time_picker("ساعت شروع", f"st_{i}", 8, 0)
            with c_t2:
                et_t = creative_time_picker("ساعت پایان", f"et_{i}", 9, 30)

            start_dt = datetime.datetime.combine(datetime.date.today(), st_t)
            end_dt = datetime.datetime.combine(datetime.date.today(), et_t)
            dur = (end_dt - start_dt).total_seconds() / 60
            if dur <= 0:
                dur += 24 * 60
            total_minutes += dur

            hrs, mins = int(dur // 60), int(dur % 60)
            st.markdown(
                f"""<div style="background:rgba(74,222,128,0.12); border-right:3px solid #4ade80;
                padding:8px 12px; border-radius:8px; margin:8px 0; font-size:13px;">
                ⏱️ مدت پارت: <b style="color:#4ade80;">{hrs} ساعت و {mins} دقیقه</b>
                </div>""", unsafe_allow_html=True)

            c_src1, c_src2 = st.columns(2)
            c_src1.text_input("منبع درسنامه", key=f"src_s_{i}")
            c_src2.text_input("منبع تست", key=f"src_t_{i}")

            st.caption("آمار تست‌ها:")
            tc, tw, tu, td = st.columns(4)
            c_val = tc.number_input("صحیح", min_value=0, value=0, key=f"c_{i}")
            w_val = tw.number_input("غلط", min_value=0, value=0, key=f"w_{i}")
            tu.number_input("نزده", min_value=0, value=0, key=f"u_{i}")
            td.number_input("شک‌دار", min_value=0, value=0, key=f"d_{i}")

            st.text_input("مبحث و توضیحات", key=f"nt_{i}")

            s_tests = c_val + w_val
            total_tests += s_tests
            total_c += c_val
            total_w += w_val
            parts_summary.append(
                f"{i+1}. {subj} ({st_t.strftime('%H:%M')} تا {et_t.strftime('%H:%M')}) | "
                f"{s_tests} تست ({c_val}ص/{w_val}غ)"
            )
            parts_data.append({
                'subject': subj,
                'minutes': dur,
                'tests': s_tests,
                'correct': c_val,
                'wrong': w_val,
                'start_hour': st_t.hour,
                'end_hour': et_t.hour,
            })

    st.markdown("#### 📱 کنترل اسکرین‌تایم")
    c_sc1, c_sc2 = st.columns(2)
    screen_t = c_sc1.text_input("کل مصرف گوشی امروز:", "۲:۱۵")
    social_t = c_sc2.text_input("شبکه‌های اجتماعی:", "۴۵ دقیقه")

    study_hours = round(total_minutes / 60, 2)
    overall_perc = round(((total_c * 3 - total_w) / (total_tests * 3)) * 100, 1) if total_tests > 0 else 0.0

    # XP پیش‌بینی
    xp_today = int(study_hours * 50 + total_tests * 2)
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:13px; color:#94a3b8;">پیش‌بینی امروز</div>
        <div style="font-size:20px; font-weight:900; color:#38bdf8; margin-top:6px;">
            ⏳ {study_hours} ساعت &nbsp;|&nbsp; 📝 {total_tests} تست &nbsp;|&nbsp; 🎯 {overall_perc}%
        </div>
        <div style="margin-top:8px; font-size:15px; font-weight:800; color:#facc15;">
            ⚡ +{xp_today:,} XP کسب خواهی کرد
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ═══ نمودار دونات زنده
    if parts_data:
        st.markdown("#### 🍩 نمودار زنده سبد مطالعاتی امروز")
        live_df = pd.DataFrame(parts_data)
        live_df = live_df[live_df['minutes'] > 0]

        if not live_df.empty:
            d1, d2 = st.columns(2)
            with d1:
                fig_donut = px.pie(
                    live_df, names='subject', values='minutes', hole=0.55,
                    title="⏱️ سهم دروس بر اساس زمان (دقیقه)",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_donut.update_traces(textposition='inside', textinfo='percent+label')
                fig_donut.update_layout(
                    template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)', font={'family': 'Vazirmatn'},
                    showlegend=False, height=340
                )
                st.plotly_chart(fig_donut, use_container_width=True)

            with d2:
                radar_df = live_df.groupby('subject')['tests'].sum().reset_index()
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=radar_df['tests'],
                    theta=radar_df['subject'],
                    fill='toself',
                    fillcolor='rgba(56,189,248,0.25)',
                    line=dict(color='#38bdf8', width=2),
                    name='تعداد تست'
                ))
                fig_radar.update_layout(
                    polar=dict(
                        bgcolor='rgba(15,23,42,0.5)',
                        radialaxis=dict(visible=True, gridcolor='rgba(56,189,248,0.2)', color='#94a3b8'),
                        angularaxis=dict(gridcolor='rgba(56,189,248,0.2)', color='#e2e8f0')
                    ),
                    template="plotly_dark", showlegend=False, height=340,
                    paper_bgcolor='rgba(0,0,0,0)', font={'family': 'Vazirmatn'}
                )
                st.plotly_chart(fig_radar, use_container_width=True)

    # ═══ ثبت نهایی
    if st.button("💾 ثبت نهایی گزارش", use_container_width=True):
        c.execute('''INSERT INTO reports (username, report_date, satisfaction, study_hours,
                    total_tests, correct_tests, wrong_tests, percentage, screen_time, social_time, details)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (st.session_state['username'], rep_date, satisfaction, study_hours,
                   total_tests, total_c, total_w, overall_perc, screen_t, social_t, "\n".join(parts_summary)))
        report_id = c.lastrowid

        for p in parts_data:
            c.execute('''INSERT INTO parts (report_id, username, report_date, subject, minutes, tests, correct, wrong)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (report_id, st.session_state['username'], rep_date,
                       p['subject'], p['minutes'], p['tests'], p['correct'], p['wrong']))
        conn.commit()

        # بررسی مدال‌ها
        report_obj = {
            'total_tests': total_tests, 'study_hours': study_hours,
            'percentage': overall_perc, 'screen_time': screen_t,
        }
        new_badges = check_badges(st.session_state['username'], report_obj, parts_data)

        st.balloons()
        st.success(f"✅ گزارش ذخیره شد! (+{xp_today:,} XP)")

        if new_badges:
            badge_html = "".join([
                f'<span class="badge-ach unlocked">{BADGES[b][0]} {BADGES[b][1]}</span>'
                for b in new_badges
            ])
            st.markdown(f"""
            <div class="glass-card" style="border-color:#facc15; animation: popIn 0.8s ease;">
                <h3 style="color:#facc15 !important; margin:0 0 10px 0;">🎉 مدال‌های جدید باز شد!</h3>
                {badge_html}
            </div>
            """, unsafe_allow_html=True)

    # ═══ کارنامه تصویری
    st.markdown("---")
    st.markdown("#### 🖼️ کارنامه تصویری نئونی (با فونت فارسی)")

    col_out1, col_out2 = st.columns(2)

    report_text = f"""📊 گزارش کار شبانه | آکادمی ۲۰
👤 دانش‌آموز: {st.session_state['name']}
🎮 سطح: {current_lvl[1]} | ⚡ XP امروز: +{xp_today:,}
📅 تاریخ: {rep_date} | ⭐ رضایت: {satisfaction}/10
⏳ مطالعه: {study_hours} ساعت
📝 کل تست‌ها: {total_tests} (✅ {total_c} | ❌ {total_w})
🎯 درصد خالص: {overall_perc}%
📱 اسکرین‌تایم: {screen_t} (فضای مجازی: {social_t})
━━━━━━━━━━━━━━━━━━━━
📚 ریز پارت‌ها:
""" + "\n".join(parts_summary) + f"""
━━━━━━━━━━━━━━━━━━━━
🔥 زنجیره: {streak} روز
👨‍🏫 مشاور: دکتر خشایار اشکبوس | @Kh_Ashkboos"""

    with col_out1:
        st.text_area("متن آماده کپی:", report_text, height=200)
        tg_url = "https://t.me/share/url?url=" + urllib.parse.quote(report_text)
        st.markdown(f'<a href="{tg_url}" target="_blank" class="tg-button">🚀 ارسال به تلگرام مشاور</a>',
                    unsafe_allow_html=True)

    with col_out2:
        try:
            img_bytes = generate_report_card(
                st.session_state['name'], str(rep_date), satisfaction, study_hours,
                total_tests, overall_perc, screen_t, current_lvl[1], total_xp + xp_today, streak
            )
            st.image(img_bytes, caption="کارنامه نئونی اختصاصی شما", use_container_width=True)
            st.download_button("📥 دانلود کارت PNG", img_bytes,
                               file_name=f"academy20_{rep_date}.png",
                               mime="image/png", use_container_width=True)
        except Exception as e:
            st.error(f"خطا در تولید تصویر: {e}")

# ═══════════════════════════════════════════════════════
# تب ۲: پومودورو
# ═══════════════════════════════════════════════════════
with main_tab2:
    st.markdown("### 🍅 تایمر پومودورو / استاپ‌واچ کنکوری")
    st.markdown("""
    <div class="glass-card" style="font-size:13.5px; color:#cbd5e1;">
    🎯 <b>روش پومودورو:</b> ۲۵ دقیقه تمرکز کامل + ۵ دقیقه استراحت.
    برای تست‌زنی سرعتی از حالت ⚡ استفاده کن. برای مرور از حالت ☕.
    </div>
    """, unsafe_allow_html=True)
    render_pomodoro()

# ═══════════════════════════════════════════════════════
# تب ۳: تحلیل‌ها + AI Coach
# ═══════════════════════════════════════════════════════
with main_tab3:
    st.markdown("### 📈 داشبورد تحلیل هوشمند")

    if df_all.empty:
        st.info("⚠️ هنوز گزارشی ثبت نکرده‌ای! اول یک گزارش بفرست.")
    else:
        df_all['report_date'] = pd.to_datetime(df_all['report_date'])

        c_filter, _ = st.columns([1, 2])
        time_frame = c_filter.radio("بازه:", ["۷ روز اخیر", "۳۰ روز اخیر", "همه"],
                                    horizontal=True)
        if "۷" in time_frame:
            filtered_df = df_all[df_all['report_date'] >= pd.Timestamp(datetime.date.today() - datetime.timedelta(days=7))]
        elif "۳۰" in time_frame:
            filtered_df = df_all[df_all['report_date'] >= pd.Timestamp(datetime.date.today() - datetime.timedelta(days=30))]
        else:
            filtered_df = df_all

        if filtered_df.empty:
            st.warning("در این بازه داده‌ای نیست.")
        else:
            sum_hours = filtered_df['study_hours'].sum()
            sum_tests = filtered_df['total_tests'].sum()
            avg_perc = filtered_df['percentage'].mean()
            avg_sat = filtered_df['satisfaction'].mean()
            period_xp = int(sum_hours * 50 + sum_tests * 2)

            st.markdown(f"""
            <div style="display:grid; grid-template-columns: repeat(5, 1fr); gap:10px; margin-bottom:22px;">
                <div class="metric-card">
                    <span class="metric-icon">⚡</span>
                    <div class="metric-num">{period_xp:,}</div>
                    <div class="metric-txt">XP بازه</div>
                </div>
                <div class="metric-card">
                    <span class="metric-icon">⏳</span>
                    <div class="metric-num">{sum_hours:.1f}</div>
                    <div class="metric-txt">ساعت مطالعه</div>
                </div>
                <div class="metric-card">
                    <span class="metric-icon">📝</span>
                    <div class="metric-num">{sum_tests}</div>
                    <div class="metric-txt">تعداد تست</div>
                </div>
                <div class="metric-card">
                    <span class="metric-icon">🎯</span>
                    <div class="metric-num">{avg_perc:.1f}%</div>
                    <div class="metric-txt">میانگین درصد</div>
                </div>
                <div class="metric-card">
                    <span class="metric-icon">⭐</span>
                    <div class="metric-num">{avg_sat:.1f}</div>
                    <div class="metric-txt">میانگین رضایت</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ═══ AI Coach
            st.markdown("#### 🤖 تحلیلگر هوش مصنوعی (AI Coach)")
            last_report = df_all.iloc[-1].to_dict() if not df_all.empty else None
            tips = ai_coach_analysis(filtered_df, last_report)

            tips_html = "".join([
                f'<div class="ai-tip {cls}">{txt}</div>' for cls, txt in tips
            ])
            st.markdown(f'<div class="ai-coach">{tips_html}</div>', unsafe_allow_html=True)

            # ═══ Sunburst (سهم دروس)
            st.markdown("#### 🌞 تحلیل سبد مطالعاتی (Sunburst)")
            parts_df = pd.read_sql_query(
                "SELECT subject, minutes, tests FROM parts WHERE username=? AND report_date >= ?",
                conn, params=(st.session_state['username'],
                              (datetime.date.today() - datetime.timedelta(days=30)).isoformat())
            )

            if not parts_df.empty:
                sc1, sc2 = st.columns(2)
                with sc1:
                    fig_sun = px.sunburst(
                        parts_df, path=['subject'], values='minutes',
                        color='minutes', color_continuous_scale=['#0ea5e9', '#7c3aed', '#f472b6'],
                        title="⏱️ توزیع زمان بین دروس"
                    )
                    fig_sun.update_layout(
                        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)',
                        font={'family': 'Vazirmatn'}, height=400
                    )
                    st.plotly_chart(fig_sun, use_container_width=True)

                with sc2:
                    subj_grouped = parts_df.groupby('subject').agg(
                        {'minutes': 'sum', 'tests': 'sum'}
                    ).reset_index().sort_values('minutes', ascending=False)
                    fig_bar = px.bar(
                        subj_grouped, x='subject', y='minutes', color='tests',
                        title="📊 رتبه‌بندی دروس بر اساس زمان",
                        color_continuous_scale=['#38bdf8', '#f472b6']
                    )
                    fig_bar.update_layout(
                        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)', font={'family': 'Vazirmatn'},
                        height=400
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("💡 برای مشاهده تحلیل سبد دروس، حداقل یک گزارش ثبت کن.")

            # ═══ روندها
            st.markdown("#### 📈 روندهای عملکرد")
            g1, g2 = st.columns([1, 2])
            with g1:
                gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=float(avg_perc),
                    number={'suffix': "%", 'font': {'color': '#38bdf8', 'size': 34}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickcolor': '#94a3b8'},
                        'bar': {'color': "#4ade80"},
                        'bgcolor': "#1e293b",
                        'steps': [
                            {'range': [0, 40], 'color': 'rgba(248,113,113,0.18)'},
                            {'range': [40, 70], 'color': 'rgba(250,204,21,0.18)'},
                            {'range': [70, 100], 'color': 'rgba(74,222,128,0.18)'},
                        ],
                    },
                    title={'text': "درصد خالص", 'font': {'color': '#cbd5e1', 'size': 14}}
                ))
                gauge.update_layout(template="plotly_dark", height=280,
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    font={'family': 'Vazirmatn'})
                st.plotly_chart(gauge, use_container_width=True)

            with g2:
                fig_hours = px.bar(
                    filtered_df, x='report_date', y='study_hours',
                    title=f"⏳ ساعت مطالعه ({time_frame})",
                    color='study_hours',
                    color_continuous_scale=['#0ea5e9', '#7c3aed', '#f472b6']
                )
                fig_hours.update_layout(
                    template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)', font={'family': 'Vazirmatn'},
                    coloraxis_showscale=False, height=280
                )
                st.plotly_chart(fig_hours, use_container_width=True)

            fig_tests = px.area(
                filtered_df, x='report_date', y='total_tests',
                title=f"📝 روند تست‌زنی ({time_frame})",
                color_discrete_sequence=['#4ade80']
            )
            fig_tests.update_traces(line=dict(width=3), fillcolor='rgba(74,222,128,0.15)')
            fig_tests.update_layout(
                template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)', font={'family': 'Vazirmatn'}
            )
            st.plotly_chart(fig_tests, use_container_width=True)

# ═══════════════════════════════════════════════════════
# تب ۴: دستاوردها
# ═══════════════════════════════════════════════════════
with main_tab4:
    st.markdown("### 🏆 تالار افتخارات و مدال‌ها")

    c.execute("SELECT badge_id, unlocked_at FROM user_badges WHERE username=?",
              (st.session_state['username'],))
    unlocked_rows = c.fetchall()
    unlocked_map = {r[0]: r[1] for r in unlocked_rows}

    # خلاصه
    total_badges = len(BADGES)
    unlocked_count = len(unlocked_map)
    pct = (unlocked_count / total_badges) * 100

    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:14px; color:#94a3b8;">پیشرفت مدال‌ها</div>
        <div style="font-size:32px; font-weight:900; color:#facc15; margin:8px 0;">
            {unlocked_count} / {total_badges}
        </div>
        <div class="xp-track" style="height:14px;">
            <div class="xp-fill" style="--target: {pct:.0f}%; width: {pct:.0f}%;
                 background: linear-gradient(90deg, #facc15, #f472b6, #38bdf8);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # گرید مدال‌ها
    st.markdown("#### 🎖️ گالری مدال‌ها")
    cols = st.columns(4)
    for idx, (bid, (icon, name, desc)) in enumerate(BADGES.items()):
        is_unlocked = bid in unlocked_map
        cls = "unlocked" if is_unlocked else "locked"
        date_unlocked = ""
        if is_unlocked:
            try:
                dt = pd.to_datetime(unlocked_map[bid])
                date_unlocked = f"<div style='font-size:10px; color:#94a3b8; margin-top:6px;'>{dt.strftime('%Y/%m/%d')}</div>"
            except Exception:
                pass
        with cols[idx % 4]:
            st.markdown(f"""
            <div class="badge-ach {cls}" style="display:block; padding:18px 10px;">
                <div style="font-size:36px;">{icon}</div>
                <div style="font-size:14px; font-weight:900; margin-top:6px;">{name}</div>
                <div style="font-size:11px; color:#94a3b8; margin-top:4px;">{desc}</div>
                {date_unlocked}
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# تب ۵: تنظیمات
# ═══════════════════════════════════════════════════════
with main_tab5:
    st.markdown(f"""
    <div class="glass-card">
        <h3 style="margin:0 0 14px 0;">👤 پروفایل قهرمان</h3>
        <p>نام: <b style="color:#38bdf8;">{st.session_state['name']}</b></p>
        <p>نام کاربری: <code style="color:#38bdf8;">{st.session_state['username']}</code></p>
        <p>سطح: <span style="color:{current_lvl[3]}; font-weight:900;">{current_lvl[2]} {current_lvl[1]}</span></p>
        <p>⚡ XP کل: <b style="color:#facc15;">{total_xp:,}</b></p>
        <p>🔥 زنجیره: <b style="color:#fb923c;">{streak} روز</b></p>
        <p>📊 تعداد گزارش‌ها: <b>{len(df_all)}</b></p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 خروج از حساب", use_container_width=True):
        st.session_state['logged_in'] = False
        st.rerun()
