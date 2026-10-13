import streamlit as st
import datetime
import urllib.parse
import urllib.request
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io, os, re, random, math

# ═══════════════════════════════════════════════════════
# ۰. PIL Persian Engine
# ═══════════════════════════════════════════════════════
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_RTL = True
except ImportError:
    HAS_RTL = False

def fa(text):
    text = str(text)
    if HAS_RTL:
        try: return get_display(arabic_reshaper.reshape(text))
        except Exception: return text
    return text

def ensure_font():
    fp = "Vazirmatn-Bold.ttf"
    if os.path.exists(fp): return fp
    for u in ["https://github.com/rastikerdar/vazirmatn/raw/master/fonts/ttf/Vazirmatn-Bold.ttf",
              "https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/ttf/Vazirmatn-Bold.ttf"]:
        try:
            urllib.request.urlretrieve(u, fp); return fp
        except Exception: continue
    return None

FONT_PATH = ensure_font()

def load_font(size):
    if FONT_PATH and os.path.exists(FONT_PATH):
        try: return ImageFont.truetype(FONT_PATH, size)
        except Exception: pass
    try: return ImageFont.truetype("arial.ttf", size)
    except Exception: return ImageFont.load_default()

# ═══════════════════════════════════════════════════════
# ۱. Page Config
# ═══════════════════════════════════════════════════════
st.set_page_config(page_title="آکادمی ۲۰ | RPG کنکور", page_icon="👑", layout="wide")

# ═══════════════════════════════════════════════════════
# ۲. Styles
# ═══════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');
    * { font-family: 'Vazirmatn', sans-serif !important; direction: rtl; text-align: right; }

    @keyframes gradientShift { 0%{background-position:0% 50%} 100%{background-position:200% 50%} }
    @keyframes pulseGlow { 0%,100%{box-shadow:0 0 20px rgba(56,189,248,0.35)} 50%{box-shadow:0 0 45px rgba(56,189,248,0.85)} }
    @keyframes fillBar { from{width:0%} to{width:var(--target,50%)} }
    @keyframes popIn { 0%{transform:scale(0.6);opacity:0} 60%{transform:scale(1.1);opacity:1} 100%{transform:scale(1)} }

    .stApp { background: radial-gradient(circle at 15% 5%, #1e2447 0%, #0b0f19 42%, #05070f 100%) !important; color:#fff !important; }
    .stApp::before { content:''; position:fixed; inset:0;
        background-image: radial-gradient(2px 2px at 20% 30%,rgba(56,189,248,.45),transparent),
            radial-gradient(1.5px 1.5px at 65% 70%,rgba(74,222,128,.4),transparent),
            radial-gradient(1.5px 1.5px at 82% 22%,rgba(250,204,21,.4),transparent);
        background-size:550px 550px,420px 420px,630px 630px; pointer-events:none; z-index:0; opacity:.5; }

    .hero-header { position:relative; background:linear-gradient(135deg,rgba(17,24,39,.9),rgba(30,41,59,.85));
        backdrop-filter:blur(14px); border-radius:22px; padding:24px; text-align:center; margin-bottom:22px;
        border:1px solid rgba(56,189,248,.25); box-shadow:0 10px 40px rgba(2,132,199,.18); }
    .hero-header::before { content:''; position:absolute; inset:-2px; border-radius:22px; padding:2px;
        background:linear-gradient(90deg,#38bdf8,#4ade80,#facc15,#f472b6,#38bdf8); background-size:300% 100%;
        animation:gradientShift 8s linear infinite;
        -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
        -webkit-mask-composite:xor; mask-composite:exclude; pointer-events:none; }
    .hero-title { font-size:26px; font-weight:900;
        background:linear-gradient(90deg,#38bdf8,#a78bfa,#f472b6); -webkit-background-clip:text;
        -webkit-text-fill-color:transparent; background-clip:text; margin:0 0 6px 0; }
    .hero-sub { color:#cbd5e1 !important; font-size:14px; margin:0; }

    .xp-container { background:rgba(17,24,39,.82); backdrop-filter:blur(12px);
        border:1px solid rgba(250,204,21,.35); border-radius:18px; padding:18px 20px; margin-bottom:18px;
        box-shadow:0 8px 26px rgba(250,204,21,.15); }
    .xp-header { display:flex; justify-content:space-between; align-items:center; gap:12px; margin-bottom:14px; flex-wrap:wrap; }
    .level-badge { display:inline-flex; align-items:center; gap:8px;
        background:linear-gradient(90deg,rgba(250,204,21,.2),rgba(244,114,182,.2));
        border:2px solid #facc15; border-radius:12px; padding:8px 14px; font-weight:900; font-size:15px;
        color:#facc15 !important; animation:pulseGlow 3s ease-in-out infinite; }
    .streak-badge { display:inline-flex; align-items:center; gap:6px;
        background:linear-gradient(90deg,rgba(251,146,60,.18),rgba(248,113,113,.18));
        border:1.5px solid rgba(251,146,60,.6); padding:8px 14px; border-radius:12px;
        font-weight:800; font-size:14px; color:#fb923c !important; }
    .xp-info-row { display:flex; justify-content:space-between; align-items:baseline; gap:12px; margin-bottom:10px; flex-wrap:wrap; font-size:13px; }
    .xp-amount { color:#38bdf8 !important; font-weight:900; font-size:16px; }
    .xp-next-hint { color:#94a3b8 !important; font-size:12px; }
    .xp-track { background:#0b0f19; border-radius:999px; height:20px; overflow:hidden; position:relative;
        border:1px solid rgba(56,189,248,.25); margin-bottom:8px; }
    .xp-fill { height:100%; background:linear-gradient(90deg,#0284c7,#7c3aed,#f472b6,#facc15);
        background-size:300% 100%; animation:fillBar 1.4s cubic-bezier(.2,.9,.3,1.1) forwards,gradientShift 4s linear infinite;
        border-radius:999px; box-shadow:0 0 20px rgba(250,204,21,.55); }
    .xp-labels { display:flex; justify-content:space-between; align-items:center; font-size:11px; color:#64748b !important; }
    .xp-labels .xp-pct { color:#facc15 !important; font-weight:900; font-size:13px; }

    .metric-card { position:relative; background:linear-gradient(145deg,rgba(17,24,39,.85),rgba(30,41,59,.75));
        backdrop-filter:blur(12px); border:1px solid rgba(56,189,248,.28); border-radius:18px;
        padding:18px 12px; text-align:center; transition:all .35s cubic-bezier(.2,.9,.3,1.3);
        overflow:hidden; box-shadow:0 8px 26px rgba(0,0,0,.35); }
    .metric-card:hover { transform:translateY(-6px) scale(1.02); border-color:rgba(56,189,248,.7);
        box-shadow:0 14px 36px rgba(56,189,248,.4); }
    .metric-num { font-size:28px; font-weight:900;
        background:linear-gradient(90deg,#38bdf8,#4ade80); -webkit-background-clip:text;
        -webkit-text-fill-color:transparent; background-clip:text; }
    .metric-txt { font-size:12px; color:#94a3b8 !important; margin-top:6px; }
    .metric-icon { font-size:22px; display:block; margin-bottom:4px; }

    .badge-ach { display:block; padding:18px 10px; border-radius:14px; font-weight:800; font-size:13px;
        margin:5px 0; border:2px solid; text-align:center; transition:all .3s; animation:popIn .6s ease; }
    .badge-ach.unlocked { color:#facc15; border-color:#facc15;
        background:linear-gradient(145deg,rgba(250,204,21,.15),rgba(244,114,182,.08)); box-shadow:0 0 18px rgba(250,204,21,.35); }
    .badge-ach.locked { color:#475569; border-color:#334155; background:rgba(15,23,42,.6); opacity:.55; }

    .ai-coach { background:linear-gradient(135deg,rgba(56,189,248,.12),rgba(168,85,247,.12));
        border:1px solid rgba(56,189,248,.4); border-radius:16px; padding:16px; margin:12px 0; }
    .ai-tip { padding:8px 12px; margin:6px 0; border-radius:10px; font-size:13.5px; border-right:4px solid; }
    .ai-tip.success { background:rgba(74,222,128,.1); border-color:#4ade80; color:#86efac; }
    .ai-tip.warning { background:rgba(250,204,21,.1); border-color:#facc15; color:#fde047; }
    .ai-tip.danger { background:rgba(248,113,113,.1); border-color:#f87171; color:#fca5a5; }
    .ai-tip.info { background:rgba(56,189,248,.1); border-color:#38bdf8; color:#7dd3fc; }

    .pomodoro-box { background:linear-gradient(145deg,#0f172a,#1e293b); border:2px solid #38bdf8;
        border-radius:20px; padding:24px; text-align:center; box-shadow:0 0 30px rgba(56,189,248,.3); margin:16px 0; }
    .pomo-time { font-size:64px; font-weight:900; font-family:'Courier New',monospace !important;
        background:linear-gradient(90deg,#38bdf8,#f472b6); -webkit-background-clip:text;
        -webkit-text-fill-color:transparent; background-clip:text; letter-spacing:4px; line-height:1; }
    .pomo-label { font-size:13px; color:#94a3b8 !important; margin-top:8px; font-weight:700; }

    /* DDI */
    .ddi-panel { border-radius:16px; padding:16px; margin:12px 0; text-align:center; border:3px solid; }
    .ddi-green { border-color:#4ade80; background:linear-gradient(135deg,rgba(74,222,128,.15),rgba(56,189,248,.1)); }
    .ddi-yellow { border-color:#facc15; background:linear-gradient(135deg,rgba(250,204,21,.15),rgba(251,146,60,.1)); }
    .ddi-red { border-color:#f87171; background:linear-gradient(135deg,rgba(248,113,113,.2),rgba(220,38,38,.15)); animation:pulseGlow 2s infinite; }
    .ddi-value { font-size:42px; font-weight:900; letter-spacing:2px; }
    .ddi-label { font-size:14px; margin-top:6px; font-weight:800; }

    /* Rank Predictor */
    .rank-card { background:linear-gradient(145deg,rgba(17,24,39,.85),rgba(30,41,59,.75));
        border:2px solid rgba(168,85,247,.4); border-radius:18px; padding:22px; margin-bottom:16px;
        box-shadow:0 10px 30px rgba(168,85,247,.2); }
    .rank-number { font-size:56px; font-weight:900; letter-spacing:2px;
        background:linear-gradient(90deg,#38bdf8,#a78bfa,#f472b6); -webkit-background-clip:text;
        -webkit-text-fill-color:transparent; background-clip:text; line-height:1; }
    .rank-label { font-size:13px; color:#94a3b8 !important; margin-top:8px; }

    /* Arena */
    .arena-card { background:linear-gradient(145deg,rgba(17,24,39,.85),rgba(30,41,59,.75));
        border:1px solid rgba(250,204,21,.35); border-radius:16px; padding:14px;
        display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; gap:10px; }
    .arena-rank { font-size:22px; font-weight:900; min-width:44px; text-align:center;
        background:linear-gradient(90deg,#facc15,#f472b6); -webkit-background-clip:text;
        -webkit-text-fill-color:transparent; background-clip:text; }
    .arena-me { border:2px solid #38bdf8; box-shadow:0 0 20px rgba(56,189,248,.35); }

    label,p,span,h1,h2,h3,h4,div { color:#fff !important; font-weight:600; }
    input,textarea,select { background-color:rgba(30,41,59,.85) !important; color:#fff !important;
        border:1px solid rgba(56,189,248,.35) !important; border-radius:12px !important; }
    input:focus,textarea:focus { border-color:#38bdf8 !important; box-shadow:0 0 0 3px rgba(56,189,248,.18) !important; }
    .stButton > button { background:linear-gradient(90deg,#0284c7,#7c3aed) !important; color:#fff !important;
        border:none !important; border-radius:12px !important; font-weight:800 !important;
        padding:10px 18px !important; transition:all .3s !important; box-shadow:0 6px 20px rgba(124,58,237,.28) !important; }
    .stButton > button:hover { transform:translateY(-2px) scale(1.01);
        box-shadow:0 10px 30px rgba(124,58,237,.55) !important; }
    .tg-button { display:block; width:100%; background:linear-gradient(90deg,#0088cc,#005f8f);
        color:#fff !important; text-align:center; font-size:16px; font-weight:800;
        padding:14px; border-radius:12px; text-decoration:none;
        box-shadow:0 6px 18px rgba(2,132,199,.45); margin-top:15px; transition:all .3s; }
    .tg-button:hover { transform:translateY(-3px); filter:brightness(1.1); }
    .insta-button { display:block; width:100%;
        background:linear-gradient(90deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888);
        color:#fff !important; text-align:center; font-size:16px; font-weight:800;
        padding:14px; border-radius:12px; text-decoration:none;
        box-shadow:0 6px 18px rgba(220,39,67,.5); margin-top:10px; transition:all .3s; }
    .insta-button:hover { transform:translateY(-3px); filter:brightness(1.15); }
    .stTabs [data-baseweb="tab-list"] { gap:6px; background:rgba(17,24,39,.6);
        padding:8px; border-radius:14px; border:1px solid rgba(56,189,248,.18); flex-wrap:wrap; }
    .stTabs [data-baseweb="tab"] { border-radius:10px !important; padding:10px 14px !important; font-weight:700 !important; }
    .stTabs [aria-selected="true"] { background:linear-gradient(90deg,#0284c7,#7c3aed) !important; color:#fff !important; }
    ::-webkit-scrollbar { width:10px; height:10px; }
    ::-webkit-scrollbar-track { background:#0b0f19; }
    ::-webkit-scrollbar-thumb { background:linear-gradient(180deg,#38bdf8,#7c3aed); border-radius:10px; }
    .glass-card { background:rgba(17,24,39,.72); backdrop-filter:blur(12px);
        border:1px solid rgba(56,189,248,.22); border-radius:16px; padding:18px; margin-bottom:14px;
        box-shadow:0 8px 24px rgba(0,0,0,.28); }

    div[data-baseweb="select"] > div { background-color:#1e293b !important; color:#fff !important; border-color:rgba(56,189,248,.35) !important; }
    div[data-baseweb="select"] span,div[data-baseweb="select"] div,div[data-baseweb="select"] input {
        color:#fff !important; background-color:transparent !important; }
    div[data-baseweb="popover"],div[data-baseweb="popover"] *,div[data-baseweb="menu"],div[data-baseweb="menu"] *,
    ul[role="listbox"],ul[role="listbox"] *,li[role="option"],li[role="option"] * {
        background-color:#1e293b !important; color:#fff !important; }
    ul[role="listbox"] li:hover,li[role="option"]:hover { background-color:#0284c7 !important; }
    li[aria-selected="true"] { background-color:#0369a1 !important; color:#fff !important; font-weight:800 !important; }
    div[data-baseweb="calendar"],div[data-baseweb="calendar"] * { background-color:#1e293b !important; color:#fff !important; }

    .time-label { font-weight:700; color:#38bdf8 !important; font-size:13.5px; margin-bottom:6px; display:block; }
    .time-preview { text-align:center; background:linear-gradient(90deg,#0284c7,#7c3aed);
        color:#fff !important; font-weight:900; font-size:22px; padding:10px 12px; border-radius:12px;
        margin-top:8px; letter-spacing:3px; box-shadow:0 4px 15px rgba(2,132,199,.5);
        font-family:'Courier New',monospace !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# ۳. Database
# ═══════════════════════════════════════════════════════
conn = sqlite3.connect("konkur_academy.db", check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, name TEXT)')
c.execute('''CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, report_date DATE,
    satisfaction INT, study_hours REAL, total_tests INT, correct_tests INT,
    wrong_tests INT, percentage REAL, screen_time TEXT, social_time TEXT, details TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT, report_id INTEGER, username TEXT, report_date DATE,
    subject TEXT, minutes REAL, tests INT, correct INT, wrong INT)''')
c.execute('''CREATE TABLE IF NOT EXISTS user_badges (
    username TEXT, badge_id TEXT, unlocked_at TIMESTAMP, PRIMARY KEY (username, badge_id))''')
c.execute('''CREATE TABLE IF NOT EXISTS error_vault (
    id INTEGER PRIMARY KEY AUTOINCREMENT, report_id INTEGER, username TEXT, report_date DATE,
    subject TEXT, error_tag TEXT, count INT)''')
c.execute('''CREATE TABLE IF NOT EXISTS arena_rooms (
    code TEXT PRIMARY KEY, name TEXT, created_by TEXT, created_at TIMESTAMP)''')
c.execute('''CREATE TABLE IF NOT EXISTS arena_members (
    code TEXT, username TEXT, nickname TEXT, joined_at TIMESTAMP,
    PRIMARY KEY (code, username))''')
conn.commit()

# ═══════════════════════════════════════════════════════
# ۴. Constants
# ═══════════════════════════════════════════════════════
MOTIVATIONS = [
    "🌟 هر تستی که می‌زنی، یک قدم به رویاهات نزدیک‌تر می‌شی.",
    "🔥 موفقیت حاصل تکرارهای کوچک روزانه است.",
    "🚀 امروزت رو بساز، چون فردا از همین امروزها ساخته می‌شه.",
    "💎 فشارِ امروز، الماسِ فردا رو می‌سازه.",
    "🎯 تمرکز روی پیشرفت، نه کمال.",
    "⚡ تو از دیروز خودت قوی‌تری؛ همین کافیه.",
    "🌈 سختی‌های امروز، پله‌های افتخار فردا هستن.",
    "👑 کسی که هر روز تلاش می‌کنه، شکست نمی‌خوره.",
]

LEVELS = [
    (0,"نوآموز","🌱","#94a3b8"), (500,"تازه‌کار","📗","#4ade80"),
    (1500,"کوشا","📘","#38bdf8"), (3000,"سخت‌کوش","⚔️","#a78bfa"),
    (6000,"حرفه‌ای","🥇","#facc15"), (12000,"استاد","👑","#fb923c"),
    (25000,"افسانه‌ای","🌟","#f472b6"), (50000,"اسطوره تجربی","🔱","#f43f5e"),
]

BADGES = {
    "first_step":("🎯","اولین قدم","اولین گزارش ثبت شد"),
    "hunter_100":("🏹","شکارچی تست","۱۰۰+ تست در روز"),
    "hunter_200":("⚡","تست‌زن افسانه‌ای","۲۰۰+ تست در روز"),
    "steel_focus":("🛡️","تمرکز فولادین","زیر ۳۰ دقیقه گوشی"),
    "bio_marathon":("🧬","ماراتن زیست","۳+ ساعت زیست در روز"),
    "marathon_day":("🏃","ماراتن روزانه","۸+ ساعت مطالعه"),
    "streak_7":("🔥","هفت‌روز پیوسته","۷ روز متوالی"),
    "streak_30":("💫","ماه کامل","۳۰ روز متوالی"),
    "early_bird":("🐓","سحرخیز","شروع قبل از ۶ صبح"),
    "night_owl":("🦉","جغد شب","مطالعه بعد از ۲۳"),
    "perfect_day":("💯","روز بی‌نقص","درصد تست ۱۰۰٪"),
    "consistent":("📊","استمرار طلایی","۱۰ گزارش متوالی"),
    "ddi_diamond":("💎","مغز الماسی","DDI زیر ۱۰٪"),
    "ddi_warrior":("🧠","جنگجوی تمرکز","DDI زیر ۵٪"),
    "rank_hunter":("🎖️","شکارچی رتبه","پیش‌بینی زیر ۱۰۰۰"),
}

ERROR_TAGS = [
    "بی‌دقتی محاسباتی",
    "فراموشی فرمول",
    "دام طراح",
    "کمبود وقت",
    "عدم تسلط به مبحث",
    "اشتباه در خواندن سؤال",
]

# ═══════════════════════════════════════════════════════
# ۵. Helpers
# ═══════════════════════════════════════════════════════
def compute_streak(df):
    if df.empty: return 0
    dates = sorted(set(pd.to_datetime(df['report_date']).dt.date), reverse=True)
    today = datetime.date.today()
    if dates[0] != today and dates[0] != today - datetime.timedelta(days=1): return 0
    check = dates[0]; streak = 0
    for d in dates:
        if d == check: streak += 1; check -= datetime.timedelta(days=1)
        elif d < check: break
    return streak


def calculate_xp(df):
    if df.empty: return 0
    return int(df['study_hours'].sum() * 50 + df['total_tests'].sum() * 2)


def get_level(xp):
    current = LEVELS[0]; next_lvl = None; idx = 0
    for i, lvl in enumerate(LEVELS):
        if xp >= lvl[0]: current = lvl; idx = i
    if idx + 1 < len(LEVELS): next_lvl = LEVELS[idx + 1]
    if next_lvl:
        rng = next_lvl[0] - current[0]
        prog = min(100, max(0, ((xp - current[0]) / rng) * 100))
    else: prog = 100.0
    return current, next_lvl, prog


def parse_duration(text):
    text = str(text).strip()
    for i, d in enumerate("۰۱۲۳۴۵۶۷۸۹"): text = text.replace(d, str(i))
    text = text.replace('ساعت', ':').replace('دقیقه', '').replace('دق', '')
    text = text.replace('،', '').replace(',', '').strip()
    if ':' in text:
        try:
            h, m = text.split(':')[:2]
            return int(float(h)) * 60 + int(float(m))
        except Exception: pass
    nums = re.findall(r'[\d.]+', text)
    if nums: return int(float(nums[0]))
    return 0


# ═══════════════════════════════════════════════════════
# 6. 🆕 DDI — Dopamine Drain Index
# ═══════════════════════════════════════════════════════
def compute_ddi(study_hours, social_time_str):
    social_min = parse_duration(social_time_str)
    study_min = study_hours * 60
    if study_min <= 0:
        return (100.0, "red") if social_min > 0 else (0.0, "green")
    ddi = (social_min / study_min) * 100
    return round(ddi, 1), ("green" if ddi < 10 else "yellow" if ddi < 25 else "red")


DDI_META = {
    "green":  ("💎", "مغز الماسی — تمرکز فولادین!",  "#4ade80", "ddi-green"),
    "yellow": ("⚠️", "خطر افت دوپامین — مواظب باش!", "#facc15", "ddi-yellow"),
    "red":    ("🔥", "وضعیت بحرانی — تمرکز در حال سوختن!", "#f87171", "ddi-red"),
}


def ddi_badge_html(ddi, level):
    icon, label, color, cls = DDI_META[level]
    return f"""
    <div class="ddi-panel {cls}">
        <div class="ddi-value" style="color:{color};">{ddi}%</div>
        <div class="ddi-label" style="color:{color};">{icon} {label}</div>
        <div style="font-size:11px; color:#94a3b8; margin-top:4px;">
            شاخص تخلیه تمرکز (DDI) = (شبکه‌های اجتماعی ÷ مطالعه) × ۱۰۰
        </div>
    </div>"""


# ═══════════════════════════════════════════════════════
# 7. 🆕 Predictive Rank Engine
# ═══════════════════════════════════════════════════════
def predict_rank(avg_hours, avg_tests, avg_percent):
    """
    مدل هیوریستیک سبک بر اساس نرمال‌سازی داده‌های کنکور.
    برمی‌گرداند: traz (تراز تخمینی), rank_low, rank_mid, rank_high, composite
    """
    h = min(max(avg_hours, 0), 14) / 14
    t = min(max(avg_tests, 0), 200) / 200
    p = min(max(avg_percent, 0), 100) / 100

    # وزن‌ها: درصد مهم‌ترینه، بعد ساعت، بعد حجم
    composite = h * 0.30 + t * 0.25 + p * 0.45  # 0..1

    # تراز فرضی روی ۱۰۰۰۰
    traz = int(3000 + composite * 7000)

    # رتبه: تابع نمایی
    rank_mid = int(max(50, 250000 * ((1 - composite) ** 3.2)))
    rank_low = max(1, int(rank_mid * 0.65))
    rank_high = int(rank_mid * 1.55)
    return traz, rank_low, rank_mid, rank_high, composite


def rank_tier(rank_mid):
    if rank_mid < 500: return "🏆 منطقه المپیک", "#facc15"
    if rank_mid < 2000: return "🥇 منطقه طلایی", "#f472b6"
    if rank_mid < 5000: return "🥈 منطقه نقره‌ای", "#a78bfa"
    if rank_mid < 15000: return "🥉 منطقه برنزی", "#38bdf8"
    if rank_mid < 50000: return "💪 در حال رشد", "#4ade80"
    return "🌱 تازه شروع کردی", "#94a3b8"


# ═══════════════════════════════════════════════════════
# 8. 🆕 Arena Leaderboard
# ═══════════════════════════════════════════════════════
def arena_leaderboard(code):
    members = pd.read_sql_query(
        "SELECT username, nickname FROM arena_members WHERE code=?",
        conn, params=(code,))
    if members.empty: return pd.DataFrame()
    cutoff = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
    rows = []
    for _, m in members.iterrows():
        df = pd.read_sql_query(
            "SELECT study_hours, total_tests FROM reports WHERE username=? AND report_date>=?",
            conn, params=(m['username'], cutoff))
        h = float(df['study_hours'].sum()) if not df.empty else 0.0
        t = int(df['total_tests'].sum()) if not df.empty else 0
        rows.append({
            'nickname': m['nickname'],
            'hours': round(h, 1),
            'tests': t,
            'score': int(h * 50 + t * 2),
            'is_me': m['username'] == st.session_state['username'],
        })
    lb = pd.DataFrame(rows).sort_values('score', ascending=False).reset_index(drop=True)
    lb.index = lb.index + 1
    return lb


# ═══════════════════════════════════════════════════════
# 9. AI Coach
# ═══════════════════════════════════════════════════════
def ai_coach_analysis(df, today_report=None):
    tips = []
    if df.empty:
        return [("info", "🤖 هنوز داده‌ای برای تحلیل نیست. اولین گزارش را ثبت کن!")]
    total_hours = df['study_hours'].sum()
    total_tests = df['total_tests'].sum()
    if total_hours > 0:
        speed = total_tests / total_hours
        if speed >= 60: tips.append(("success", f"🚀 سرعت تست‌زنی فوق‌العاده! ({speed:.0f} تست/ساعت)"))
        elif speed >= 35: tips.append(("success", f"👍 سرعت تست‌زنی خوب ({speed:.0f} تست/ساعت)"))
        elif speed >= 15: tips.append(("warning", f"⚙️ سرعت متوسط ({speed:.0f} تست/ساعت). ۴۰+ هدف بذار"))
        else: tips.append(("danger", f"⚠️ سرعت پایین ({speed:.0f} تست/ساعت). روی تمرکز کار کن"))

    if today_report:
        ddi, ddi_lvl = compute_ddi(today_report['study_hours'], today_report['social_time'])
        if ddi_lvl == "red": tips.append(("danger", f"🔥 DDI {ddi}% — اسکرین‌تایم داری تمرکزت رو می‌خوره!"))
        elif ddi_lvl == "yellow": tips.append(("warning", f"⚠️ DDI {ddi}% — تعادل دیجیتال رو بهتر کن"))
        else: tips.append(("success", f"💎 DDI {ddi}% — مغز الماسی!"))

    avg_sat = df['satisfaction'].mean()
    if avg_sat >= 8: tips.append(("success", f"😊 رضایتت {avg_sat:.1f}/10 عالیه"))
    elif avg_sat < 6: tips.append(("warning", f"💙 رضایتت {avg_sat:.1f}/10 پایینه. استراحت لازمه"))

    if len(df) >= 3:
        recent = df.tail(3)['total_tests'].mean()
        older = df.head(max(1, len(df) - 3))['total_tests'].mean()
        if recent > older * 1.2: tips.append(("success", "📈 روند صعودی تست‌زنی"))
        elif recent < older * 0.8: tips.append(("warning", "📉 افت در تعداد تست‌ها"))
    return tips


def check_badges(username, report, parts_data):
    new_badges = []
    c.execute("SELECT badge_id FROM user_badges WHERE username=?", (username,))
    existing = {r[0] for r in c.fetchall()}
    df_user = pd.read_sql_query("SELECT * FROM reports WHERE username=? ORDER BY report_date ASC",
                                conn, params=(username,))
    total_reports = len(df_user); streak = compute_streak(df_user)
    tests_today = report['total_tests']; study_hours = report['study_hours']
    perc = report['percentage']
    bio_min = sum(p['minutes'] for p in parts_data if 'زیست' in p['subject'])
    ddi, ddi_lvl = compute_ddi(study_hours, report['social_time'])
    _, _, rank_mid, _, _ = predict_rank(study_hours, tests_today, perc)

    candidates = set()
    if total_reports >= 1: candidates.add("first_step")
    if tests_today >= 100: candidates.add("hunter_100")
    if tests_today >= 200: candidates.add("hunter_200")
    if parse_duration(report['screen_time']) <= 30: candidates.add("steel_focus")
    if bio_min >= 180: candidates.add("bio_marathon")
    if study_hours >= 8: candidates.add("marathon_day")
    if streak >= 7: candidates.add("streak_7")
    if streak >= 30: candidates.add("streak_30")
    if perc >= 100 and tests_today >= 20: candidates.add("perfect_day")
    if total_reports >= 10: candidates.add("consistent")
    if ddi < 10: candidates.add("ddi_diamond")
    if ddi < 5: candidates.add("ddi_warrior")
    if rank_mid < 1000 and tests_today >= 50: candidates.add("rank_hunter")
    for p in parts_data:
        if p.get('start_hour', 99) < 6: candidates.add("early_bird")
        if p.get('end_hour', 0) >= 23: candidates.add("night_owl")

    for bid in candidates:
        if bid not in existing:
            new_badges.append(bid)
            c.execute("INSERT OR IGNORE INTO user_badges VALUES (?,?,?)",
                      (username, bid, datetime.datetime.now()))
    if new_badges: conn.commit()
    return new_badges


# ═══════════════════════════════════════════════════════
# 10. Poster & Story Card Generators
# ═══════════════════════════════════════════════════════
def draw_neon_text(base, text, xy, font, color, glow, gsize=8):
    ov = Image.new('RGBA', base.size, (0,0,0,0))
    od = ImageDraw.Draw(ov)
    for o in range(gsize, 0, -1):
        a = int(70 * (1 - o / gsize))
        for dx, dy in [(o,0),(-o,0),(0,o),(0,-o)]:
            od.text((xy[0]+dx, xy[1]+dy), text, font=font, fill=glow + (a,))
    ov = ov.filter(ImageFilter.GaussianBlur(radius=3))
    base.paste(ov, (0,0), ov)
    d = ImageDraw.Draw(base)
    d.text((xy[0]+2, xy[1]+2), text, font=font, fill=(0,0,0))
    d.text(xy, text, font=font, fill=color)


def draw_gold_badge(img, cx, cy, r):
    d = ImageDraw.Draw(img, 'RGBA')
    for i in range(20, 0, -1):
        d.ellipse([(cx-r-i, cy-r-i), (cx+r+i, cy+r+i)], fill=(250,204,21, int(80*(1-i/20))))
    d.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=(30,25,10), outline=(250,204,21), width=4)
    d.ellipse([(cx-r+6, cy-r+6), (cx+r-6, cy+r-6)], outline=(255,220,90), width=2)
    f = load_font(34)
    bbox = d.textbbox((0,0), "20", font=f)
    d.text((cx-(bbox[2]-bbox[0])//2, cy-(bbox[3]-bbox[1])//2 - 6), "20", font=f, fill=(250,204,21))


def generate_report_card(name, date_str, satisfaction, study_hours, total_tests,
                          percentage, screen_time, level_name, xp, streak, ddi_val, ddi_lvl):
    W, H = 1000, 720
    img = Image.new('RGB', (W, H), '#05080f'); draw = ImageDraw.Draw(img)
    for y in range(H):
        r = int(8 + 25*y/H); g = int(11 + 30*y/H); b = int(22 + 55*y/H)
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    for i, col in enumerate([(56,189,248),(124,58,237),(244,114,182)]):
        draw.rectangle([(15+i*3,15+i*3),(W-15-i*3,H-15-i*3)], outline=col, width=2)
    for cx, cy in [(20,20),(W-20,20),(20,H-20),(W-20,H-20)]:
        for dx in (-1,1):
            for dy in (-1,1):
                draw.line([(cx,cy),(cx+dx*40,cy)], fill=(250,204,21), width=3)
                draw.line([(cx,cy),(cx,cy+dy*40)], fill=(250,204,21), width=3)

    t = fa("آکادمی ۲۰ • کارنامه عملکرد"); f = load_font(28)
    bbox = draw.textbbox((0,0), t, font=f); tw = bbox[2]-bbox[0]
    draw_neon_text(img, t, ((W-tw)//2, 40), f, (255,255,255), (56,189,248), 10)
    nm = fa(f"دانش‌آموز: {name}"); fn = load_font(22)
    bbox = draw.textbbox((0,0), nm, font=fn); tw = bbox[2]-bbox[0]
    draw_neon_text(img, nm, ((W-tw)//2, 85), fn, (200,220,255), (124,58,237), 6)
    dt = fa(f"تاریخ: {date_str}"); fd = load_font(16)
    bbox = draw.textbbox((0,0), dt, font=fd); tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, 118), dt, font=fd, fill=(148,163,184))
    draw.line([(60,150),(W-60,150)], fill=(56,189,248), width=2)
    draw_gold_badge(img, W-110, 220, 50)

    def card(x, y, w, h, lbl, val, color):
        draw.rectangle([(x+3,y+3),(x+w+3,y+h+3)], fill=(0,0,0,100))
        draw.rectangle([(x,y),(x+w,y+h)], fill=(15,23,42), outline=color, width=2)
        draw.line([(x,y),(x+25,y)], fill=(255,255,255), width=3)
        draw.line([(x,y),(x,y+25)], fill=(255,255,255), width=3)
        draw.text((x+20, y+15), fa(lbl), font=load_font(16), fill=(148,163,184))
        draw.text((x+20, y+h//2-8), fa(str(val)), font=load_font(30), fill=color)

    cw, ch = 400, 110
    card(50, 180, cw, ch, "⏳ ساعت مطالعه", f"{study_hours} ساعت", (56,189,248))
    card(480, 180, cw, ch, "📝 تعداد تست", f"{total_tests}", (74,222,128))
    card(50, 305, cw, ch, "🎯 درصد خالص", f"{percentage}%", (250,204,21))
    card(480, 305, cw, ch, "⭐ رضایت", f"{satisfaction}/10", (244,114,182))

    draw.rectangle([(50, 435), (W-50, 490)], fill=(20,15,15), outline=(248,113,113), width=2)
    draw.text((70, 450), fa(f"📱 اسکرین‌تایم: {screen_time}"), font=load_font(18), fill=(248,113,113))

    ddi_color = {"green": (74,222,128), "yellow": (250,204,21), "red": (248,113,113)}[ddi_lvl]
    draw.rectangle([(50, 500), (W-50, 560)], fill=(15,25,15) if ddi_lvl=="green" else (25,20,10) if ddi_lvl=="yellow" else (30,10,10),
                   outline=ddi_color, width=2)
    draw.text((70, 518), fa(f"DDI: {ddi_val}%"), font=load_font(22), fill=ddi_color)
    ddi_lbl = {"green":"مغز الماسی 💎","yellow":"افت دوپامین ⚠️","red":"تمرکز بحرانی 🔥"}[ddi_lvl]
    draw.text((450, 522), fa(ddi_lbl), font=load_font(18), fill=ddi_color)

    draw.rectangle([(50, 570), (W-50, 640)], fill=(15,20,40), outline=(168,85,247), width=2)
    draw.text((70, 585), fa(f"🎮 سطح: {level_name}"), font=load_font(20), fill=(250,204,21))
    draw.text((70, 615), fa(f"⚡ XP: {xp:,}"), font=load_font(18), fill=(56,189,248))
    draw.text((600, 590), fa(f"🔥 زنجیره: {streak} روز"), font=load_font(18), fill=(251,146,60))

    draw.text((60, 665), fa("دکتر خشایار اشکبوس"), font=load_font(16), fill=(56,189,248))
    draw.text((60, 692), "Telegram: @Kh_Ashkboos", font=load_font(16), fill=(148,163,184))
    buf = io.BytesIO(); img.save(buf, format='PNG', quality=95)
    return buf.getvalue()


# ═══ Story Card (1080×1920) ═══
def generate_story_card(name, date_str, study_hours, total_tests, percentage,
                         ddi_val, ddi_lvl, level_name, xp_today, streak, badges_list):
    W, H = 1080, 1920
    img = Image.new('RGB', (W, H), '#05070f')
    draw = ImageDraw.Draw(img)
    for y in range(H):
        r = int(8 + 30*y/H); g = int(11 + 35*y/H); b = int(25 + 70*y/H)
        draw.line([(0,y),(W,y)], fill=(r,g,b))

    # Decorative
    for i, col in enumerate([(56,189,248),(124,58,237),(244,114,182)]):
        draw.rectangle([(20+i*4,20+i*4),(W-20-i*4,H-20-i*4)], outline=col, width=3)
    for cx, cy in [(40,40),(W-40,40),(40,H-40),(W-40,H-40)]:
        for dx in (-1,1):
            for dy in (-1,1):
                draw.line([(cx,cy),(cx+dx*70,cy)], fill=(250,204,21), width=4)
                draw.line([(cx,cy),(cx,cy+dy*70)], fill=(250,204,21), width=4)

    # ═══ Brand
    f_brand = load_font(72)
    b = fa("👑 آکادمی ۲۰"); bbox = draw.textbbox((0,0), b, font=f_brand); tw = bbox[2]-bbox[0]
    draw_neon_text(img, b, ((W-tw)//2, 130), f_brand, (255,255,255), (56,189,248), 14)

    f_sub = load_font(32)
    s = fa("کارنامه استوری کنکوری"); bbox = draw.textbbox((0,0), s, font=f_sub); tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, 230), s, font=f_sub, fill=(148,163,184))

    # ═══ Name
    f_name = load_font(52)
    nm = fa(name); bbox = draw.textbbox((0,0), nm, font=f_name); tw = bbox[2]-bbox[0]
    draw_neon_text(img, nm, ((W-tw)//2, 300), f_name, (56,189,248), (168,85,247), 8)

    f_date = load_font(30)
    dt = fa(date_str); bbox = draw.textbbox((0,0), dt, font=f_date); tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, 375), dt, font=f_date, fill=(203,213,225))

    # ═══ Big Metrics
    y = 470
    for lbl, val, col in [
        ("⏳ ساعت مطالعه", f"{study_hours}", (56,189,248)),
        ("📝 تعداد تست", f"{total_tests}", (74,222,128)),
        ("🎯 درصد خالص", f"{percentage}%", (250,204,21)),
    ]:
        draw.rectangle([(90,y),(W-90,y+150)], fill=(15,23,42), outline=col, width=3)
        # Corner highlight
        draw.line([(90,y),(90+50,y)], fill=(255,255,255), width=3)
        draw.line([(90,y),(90,y+50)], fill=(255,255,255), width=3)
        f_l = load_font(32)
        draw.text((130, y+22), fa(lbl), font=f_l, fill=(148,163,184))
        f_v = load_font(66)
        bbox = draw.textbbox((0,0), fa(val), font=f_v)
        draw.text((130, y+70), fa(val), font=f_v, fill=col)
        y += 170

    # ═══ DDI
    ddi_col = {"green":(74,222,128), "yellow":(250,204,21), "red":(248,113,113)}[ddi_lvl]
    ddi_txt = {"green":"💎 مغز الماسی", "yellow":"⚠️ افت دوپامین", "red":"🔥 تمرکز بحرانی"}[ddi_lvl]
    draw.rectangle([(90,y),(W-90,y+140)], fill=(15,20,15), outline=ddi_col, width=4)
    draw.text((130, y+20), fa("شاخص DDI"), font=load_font(28), fill=(148,163,184))
    draw.text((130, y+58), fa(f"{ddi_val}%"), font=load_font(52), fill=ddi_col)
    draw.text((W-500, y+80), fa(ddi_txt), font=load_font(30), fill=ddi_col)
    y += 160

    # ═══ Level + XP
    draw.rectangle([(90,y),(W-90,y+130)], fill=(20,15,40), outline=(168,85,247), width=3)
    draw.text((130, y+25), fa(f"🎮 {level_name}"), font=load_font(36), fill=(250,204,21))
    draw.text((130, y+75), fa(f"⚡ +{xp_today:,} XP امشب  •  🔥 {streak} روز"), font=load_font(26), fill=(56,189,248))
    y += 150

    # ═══ Badges
    if badges_list:
        draw.rectangle([(90,y),(W-90,y+140)], fill=(20,15,20), outline=(250,204,21), width=3)
        draw.text((130, y+18), fa("🏆 مدال‌های امشب:"), font=load_font(28), fill=(250,204,21))
        bs = "  •  ".join([f"{BADGES[bid][0]} {BADGES[bid][1]}" for bid in badges_list[:3]])
        draw.text((130, y+65), fa(bs), font=load_font(24), fill=(255,255,255))
        y += 160

    # ═══ Watermark & Footer
    draw_gold_badge(img, W-140, H-260, 60)
    f_ft = load_font(32)
    f1 = fa("مشاور: دکتر خشایار اشکبوس")
    bbox = draw.textbbox((0,0), f1, font=f_ft); tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, H-200), f1, font=f_ft, fill=(56,189,248))
    f2 = load_font(38)
    f2t = "@Kh_Ashkboos"
    bbox = draw.textbbox((0,0), f2t, font=f2); tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, H-140), f2t, font=f2, fill=(250,204,21))
    f3 = load_font(22)
    f3t = fa("با آکادمی ۲۰، کنکور رو فتح کن!")
    bbox = draw.textbbox((0,0), f3t, font=f3); tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, H-80), f3t, font=f3, fill=(148,163,184))

    buf = io.BytesIO(); img.save(buf, format='PNG', quality=95)
    return buf.getvalue()


# ═══════════════════════════════════════════════════════
# 11. Time Picker
# ═══════════════════════════════════════════════════════
HOURS = list(range(24))
MINUTES = [0,5,10,15,20,25,30,35,40,45,50,55]
QUICK_HOURS = [6,7,8,9,10,12,14,16,18,20,22]

def _set_kv(k, v): st.session_state[k] = v

def creative_time_picker(label, key_prefix, default_h=8, default_m=0):
    st.markdown(f'<span class="time-label">🕐 {label}</span>', unsafe_allow_html=True)
    st.caption("⚡ انتخاب سریع ساعت:")
    qcols = st.columns(len(QUICK_HOURS))
    cur_h = st.session_state.get(f"{key_prefix}_h", default_h)
    for idx, qh in enumerate(QUICK_HOURS):
        label_btn = f"✓ {qh:02d}" if cur_h == qh else f"{qh:02d}"
        qcols[idx].button(label_btn, key=f"{key_prefix}_qh_{qh}",
                          on_click=_set_kv, args=(f"{key_prefix}_h", qh),
                          use_container_width=True)
    c1, c2 = st.columns(2)
    hour = c1.selectbox("ساعت", HOURS, index=st.session_state.get(f"{key_prefix}_h", default_h),
                        format_func=lambda x: f"{x:02d}", key=f"{key_prefix}_h")
    minute = c2.selectbox("دقیقه", MINUTES,
                          index=MINUTES.index(default_m) if default_m in MINUTES else 0,
                          format_func=lambda x: f"{x:02d}", key=f"{key_prefix}_m")
    st.markdown(f'<div class="time-preview">⏰ {hour:02d}:{minute:02d}</div>', unsafe_allow_html=True)
    return datetime.time(hour, minute)


# ═══════════════════════════════════════════════════════
# 12. Pomodoro
# ═══════════════════════════════════════════════════════
if 'pomo' not in st.session_state:
    st.session_state.pomo = {'running': False, 'end_time': None, 'duration': 25*60, 'last_remaining': 25*60}

try:
    @st.fragment(run_every=1.0)
    def render_timer_fragment():
        pomo = st.session_state.pomo
        if pomo['running'] and pomo['end_time']:
            rem = int((pomo['end_time'] - datetime.datetime.now()).total_seconds())
            if rem <= 0:
                pomo['running'] = False; rem = 0; pomo['last_remaining'] = 0
                st.toast("⏰ زمان تمام شد!", icon="🔔")
            else: pomo['last_remaining'] = rem
        else: rem = pomo.get('last_remaining', pomo.get('duration', 25*60))
        m, s = divmod(max(0, rem), 60)
        status = "🔥 در حال اجرا..." if pomo['running'] else "⏸️ آماده شروع"
        st.markdown(f'<div class="pomodoro-box"><div class="pomo-time">{m:02d}:{s:02d}</div>'
                    f'<div class="pomo-label">{status}</div></div>', unsafe_allow_html=True)
    HAS_FRAGMENT = True
except Exception:
    HAS_FRAGMENT = False


def render_pomodoro():
    col1, col2 = st.columns([2, 1])
    with col1:
        mode = st.radio("حالت", ["🎯 تمرکز (۲۵ دقیقه)", "☕ استراحت (۵ دقیقه)", "⚡ تست سرعتی (۱۰ دقیقه)"],
                        key="pomo_mode_radio", horizontal=True)
    with col2:
        custom_min = st.number_input("یا دقیقه دلخواه:", 1, 120, 25, key="pomo_custom")
    durs = {"🎯 تمرکز (۲۵ دقیقه)":25*60, "☕ استراحت (۵ دقیقه)":5*60, "⚡ تست سرعتی (۱۰ دقیقه)":10*60}
    selected = durs.get(mode, custom_min*60)
    st.session_state.pomo['duration'] = selected
    if HAS_FRAGMENT: render_timer_fragment()
    else:
        pomo = st.session_state.pomo
        rem = (max(0, int((pomo['end_time']-datetime.datetime.now()).total_seconds()))
               if pomo['running'] and pomo['end_time'] else pomo.get('last_remaining', selected))
        m, s = divmod(rem, 60)
        st.markdown(f'<div class="pomodoro-box"><div class="pomo-time">{m:02d}:{s:02d}</div>'
                    f'<div class="pomo-label">{"🔥 در حال اجرا" if pomo["running"] else "⏸️ آماده"}</div></div>',
                    unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    if b1.button("▶️ شروع / ادامه", use_container_width=True, key="pomo_start"):
        if not st.session_state.pomo['running']:
            rem = st.session_state.pomo.get('last_remaining', selected)
            if rem <= 0: rem = selected
            st.session_state.pomo['running'] = True
            st.session_state.pomo['end_time'] = datetime.datetime.now() + datetime.timedelta(seconds=rem)
            st.rerun()
    if b2.button("⏸️ توقف موقت", use_container_width=True, key="pomo_pause"):
        if st.session_state.pomo['running'] and st.session_state.pomo['end_time']:
            rem = int((st.session_state.pomo['end_time'] - datetime.datetime.now()).total_seconds())
            st.session_state.pomo['last_remaining'] = max(0, rem)
            st.session_state.pomo['running'] = False; st.session_state.pomo['end_time'] = None
            st.rerun()
    if b3.button("🔄 ریست کامل", use_container_width=True, key="pomo_reset"):
        st.session_state.pomo = {'running':False, 'end_time':None, 'duration':selected, 'last_remaining':selected}
        st.rerun()


# ═══════════════════════════════════════════════════════
# 13. Session
# ═══════════════════════════════════════════════════════
for k in ['logged_in']:
    if k not in st.session_state: st.session_state[k] = False
if 'username' not in st.session_state: st.session_state['username'] = ''
if 'name' not in st.session_state: st.session_state['name'] = ''

# ═══════════════════════════════════════════════════════
# 14. Login
# ═══════════════════════════════════════════════════════
if not st.session_state['logged_in']:
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">🎮 آکادمی ۲۰ — RPG کنکور</div>
        <p class="hero-sub">XP بگیر، لول‌آپ شو، رتبه رو شکار کن! | <b>دکتر خشایار اشکبوس</b></p>
    </div>""", unsafe_allow_html=True)
    tab_l, tab_r = st.tabs(["🔑 ورود", "📝 ثبت‌نام"])
    with tab_l:
        cu, cp = st.columns(2)
        u = cu.text_input("نام کاربری:", key="l_u")
        p = cp.text_input("رمز عبور:", type="password", key="l_p")
        if st.button("🚀 ورود", use_container_width=True):
            c.execute("SELECT name FROM users WHERE username=? AND password=?", (u, p))
            res = c.fetchone()
            if res:
                st.session_state['logged_in'] = True
                st.session_state['username'] = u; st.session_state['name'] = res[0]
                st.rerun()
            else: st.error("❌ اطلاعات اشتباه")
    with tab_r:
        nm = st.text_input("نام و نام خانوادگی:")
        un = st.text_input("نام کاربری دلخواه:")
        pn = st.text_input("رمز عبور:", type="password")
        if st.button("✨ ثبت‌نام", use_container_width=True):
            if nm and un and pn:
                try:
                    c.execute("INSERT INTO users VALUES (?,?,?)", (un, pn, nm)); conn.commit()
                    st.success("🎉 ثبت شد!")
                except Exception: st.error("⚠️ نام کاربری تکراریه")
            else: st.warning("همه فیلدها را پر کن")
    st.stop()

# ═══════════════════════════════════════════════════════
# 15. Dashboard
# ═══════════════════════════════════════════════════════
df_all = pd.read_sql_query("SELECT * FROM reports WHERE username=? ORDER BY report_date ASC",
                           conn, params=(st.session_state['username'],))
streak = compute_streak(df_all)
total_xp = calculate_xp(df_all)
current_lvl, next_lvl, progress = get_level(total_xp)
motivation = random.choice(MOTIVATIONS)

st.markdown(f"""
<div class="hero-header">
    <div class="hero-title">داشبورد قهرمان | آکادمی ۲۰</div>
    <p class="hero-sub">🎯 {st.session_state['name']}</p>
</div>""", unsafe_allow_html=True)

next_hint = (f"{next_lvl[0]-total_xp:,} XP تا {next_lvl[2]} {next_lvl[1]}"
             if next_lvl else "🔥 بالاترین سطح!")
next_label = f"{next_lvl[0]:,}" if next_lvl else "∞"
st.markdown(f"""
<div class="xp-container">
    <div class="xp-header">
        <div class="level-badge"><span>{current_lvl[2]}</span><span>سطح {current_lvl[1]}</span></div>
        <div class="streak-badge">🔥 {streak} روز متوالی</div>
    </div>
    <div class="xp-info-row">
        <span class="xp-amount">⚡ {total_xp:,} XP</span>
        <span class="xp-next-hint">{next_hint}</span>
    </div>
    <div class="xp-track"><div class="xp-fill" style="--target:{progress:.1f}%; width:{progress:.1f}%;"></div></div>
    <div class="xp-labels">
        <span>{current_lvl[0]:,} XP</span>
        <span class="xp-pct">{progress:.1f}%</span>
        <span>{next_label} XP</span>
    </div>
</div>""", unsafe_allow_html=True)

st.markdown(f"""
<div class="glass-card" style="display:flex; align-items:center; gap:14px;">
    <div style="font-size:28px;">💬</div>
    <div style="font-size:14px; color:#e2e8f0;">{motivation}</div>
</div>""", unsafe_allow_html=True)

# Tabs (7 tabs)
t1, t2, t3, t4, t5, t6, t7 = st.tabs([
    "📝 ثبت گزارش", "🍅 پومودورو", "🔮 پیش‌بینی رتبه",
    "⚔️ اتاق جنگ", "📈 تحلیل‌ها", "🏆 دستاوردها", "⚙️ تنظیمات"
])

# ═══════════════════════════════════════════════════════
# TAB 1 — Report
# ═══════════════════════════════════════════════════════
with t1:
    cd1, cd2 = st.columns(2)
    rep_date = cd1.date_input("📅 تاریخ:", datetime.date.today())
    satisfaction = cd2.slider("⭐️ کیفیت مطالعه (۱-۱۰):", 1, 10, 8)

    st.markdown("#### 📚 ریز پارت‌ها")
    num_slots = st.number_input("تعداد پارت‌ها:", 1, 12, 3)

    subjects = ["زیست‌شناسی","شیمی","فیزیک","ریاضیات","زمین‌شناسی","فارسی","دینی","عربی","زبان","سایر"]
    total_tests = total_c = total_w = 0
    total_minutes = 0
    parts_summary, parts_data, error_data = [], [], []

    for i in range(int(num_slots)):
        with st.expander(f"📌 پارت {i+1}", expanded=(i == 0)):
            cs1, cs2 = st.columns([2, 1])
            subj = cs1.selectbox(f"درس (پارت {i+1})", subjects, key=f"s_{i}")
            if subj == "سایر": subj = cs1.text_input("نام درس", key=f"cs_{i}")
            cs2.radio("نوع تست", ["آموزشی","زمان‌دار"], horizontal=True, key=f"tt_{i}")

            ct1, ct2 = st.columns(2)
            with ct1: st_t = creative_time_picker("شروع", f"st_{i}", 8, 0)
            with ct2: et_t = creative_time_picker("پایان", f"et_{i}", 9, 30)

            dur = (datetime.datetime.combine(datetime.date.today(), et_t) -
                   datetime.datetime.combine(datetime.date.today(), st_t)).total_seconds()/60
            if dur <= 0: dur += 24*60
            total_minutes += dur

            st.markdown(f"""<div style="background:rgba(74,222,128,.12); border-right:3px solid #4ade80;
                padding:8px 12px; border-radius:8px; margin:8px 0; font-size:13px;">
                ⏱️ <b style="color:#4ade80;">{int(dur//60)} س {int(dur%60)} د</b></div>""", unsafe_allow_html=True)

            csrc1, csrc2 = st.columns(2)
            csrc1.text_input("منبع درسنامه", key=f"src_s_{i}")
            csrc2.text_input("منبع تست", key=f"src_t_{i}")

            st.caption("آمار تست:")
            tc1, tc2, tc3, tc4 = st.columns(4)
            c_val = tc1.number_input("صحیح", 0, value=0, key=f"c_{i}")
            w_val = tc2.number_input("غلط", 0, value=0, key=f"w_{i}")
            tc3.number_input("نزده", 0, value=0, key=f"u_{i}")
            tc4.number_input("شک‌دار", 0, value=0, key=f"d_{i}")

            # 🆕 Error Vault — tag if wrong > 0
            err_tag = None
            if w_val > 0:
                st.markdown("##### 🎯 جعبه سیاه اشتباهات (Smart Error Vault)")
                err_tag = st.selectbox(
                    f"علت اصلی غلط‌های {subj}:",
                    ERROR_TAGS + ["ترکیبی / نامشخص"],
                    key=f"err_{i}",
                    help="با تگ کردن دقیق، AI Coach الگوی اشتباهاتت رو کشف می‌کنه"
                )

            st.text_input("مبحث و توضیحات", key=f"nt_{i}")

            s_tests = c_val + w_val
            total_tests += s_tests; total_c += c_val; total_w += w_val
            parts_summary.append(f"{i+1}. {subj} ({st_t.strftime('%H:%M')}-{et_t.strftime('%H:%M')}) | {s_tests} تست ({c_val}ص/{w_val}غ)")
            parts_data.append({'subject':subj, 'minutes':dur, 'tests':s_tests, 'correct':c_val, 'wrong':w_val,
                               'start_hour':st_t.hour, 'end_hour':et_t.hour})
            if err_tag and w_val > 0:
                error_data.append({'subject':subj, 'tag':err_tag, 'count':w_val})

    st.markdown("#### 📱 کنترل اسکرین‌تایم")
    sc1, sc2 = st.columns(2)
    screen_t = sc1.text_input("کل مصرف گوشی:", "۲:۱۵")
    social_t = sc2.text_input("شبکه‌های اجتماعی:", "۴۵ دقیقه")

    study_hours = round(total_minutes/60, 2)
    overall_perc = round(((total_c*3 - total_w) / (total_tests*3))*100, 1) if total_tests > 0 else 0.0

    # 🆕 DDI نمایش زنده
    ddi_val, ddi_lvl = compute_ddi(study_hours, social_t)
    st.markdown(ddi_badge_html(ddi_val, ddi_lvl), unsafe_allow_html=True)

    xp_today = int(study_hours*50 + total_tests*2)
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:13px; color:#94a3b8;">پیش‌بینی امروز</div>
        <div style="font-size:20px; font-weight:900; color:#38bdf8; margin-top:6px;">
            ⏳ {study_hours} ساعت &nbsp;|&nbsp; 📝 {total_tests} تست &nbsp;|&nbsp; 🎯 {overall_perc}%
        </div>
        <div style="margin-top:8px; font-size:15px; font-weight:800; color:#facc15;">
            ⚡ +{xp_today:,} XP
        </div>
    </div>""", unsafe_allow_html=True)

    # Live donut
    if parts_data:
        live_df = pd.DataFrame(parts_data)
        live_df = live_df[live_df['minutes'] > 0]
        if not live_df.empty:
            st.markdown("#### 🍩 سبد مطالعاتی امروز")
            dd1, dd2 = st.columns(2)
            with dd1:
                fig_d = px.pie(live_df, names='subject', values='minutes', hole=.55,
                               title="⏱️ سهم دروس (دقیقه)",
                               color_discrete_sequence=px.colors.qualitative.Set3)
                fig_d.update_traces(textposition='inside', textinfo='percent+label')
                fig_d.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)', font={'family':'Vazirmatn'},
                                    showlegend=False, height=340)
                st.plotly_chart(fig_d, use_container_width=True)
            with dd2:
                rd = live_df.groupby('subject')['tests'].sum().reset_index()
                fr = go.Figure()
                fr.add_trace(go.Scatterpolar(r=rd['tests'], theta=rd['subject'], fill='toself',
                                             fillcolor='rgba(56,189,248,.25)',
                                             line=dict(color='#38bdf8', width=2), name='تست'))
                fr.update_layout(polar=dict(bgcolor='rgba(15,23,42,.5)',
                                            radialaxis=dict(visible=True, gridcolor='rgba(56,189,248,.2)', color='#94a3b8'),
                                            angularaxis=dict(gridcolor='rgba(56,189,248,.2)', color='#e2e8f0')),
                                 template="plotly_dark", showlegend=False, height=340,
                                 paper_bgcolor='rgba(0,0,0,0)', font={'family':'Vazirmatn'})
                st.plotly_chart(fr, use_container_width=True)

    if st.button("💾 ثبت نهایی گزارش", use_container_width=True):
        c.execute('''INSERT INTO reports (username, report_date, satisfaction, study_hours,
                    total_tests, correct_tests, wrong_tests, percentage, screen_time, social_time, details)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
                  (st.session_state['username'], rep_date, satisfaction, study_hours,
                   total_tests, total_c, total_w, overall_perc, screen_t, social_t, "\n".join(parts_summary)))
        rid = c.lastrowid
        for p in parts_data:
            c.execute('''INSERT INTO parts (report_id, username, report_date, subject, minutes, tests, correct, wrong)
                        VALUES (?,?,?,?,?,?,?,?)''',
                      (rid, st.session_state['username'], rep_date, p['subject'], p['minutes'],
                       p['tests'], p['correct'], p['wrong']))
        # 🆕 Save errors
        for e in error_data:
            c.execute('''INSERT INTO error_vault (report_id, username, report_date, subject, error_tag, count)
                        VALUES (?,?,?,?,?,?)''',
                      (rid, st.session_state['username'], rep_date, e['subject'], e['tag'], e['count']))
        conn.commit()

        rpt = {'total_tests':total_tests, 'study_hours':study_hours,
               'percentage':overall_perc, 'screen_time':screen_t, 'social_time':social_t}
        new_b = check_badges(st.session_state['username'], rpt, parts_data)
        st.balloons()
        st.success(f"✅ ذخیره شد! (+{xp_today:,} XP)")
        if new_b:
            bh = "".join([f'<span class="badge-ach unlocked" style="display:inline-block;">{BADGES[b][0]} {BADGES[b][1]}</span>' for b in new_b])
            st.markdown(f'<div class="glass-card" style="border-color:#facc15;">'
                        f'<h3 style="color:#facc15 !important;">🎉 مدال جدید!</h3>{bh}</div>',
                        unsafe_allow_html=True)

    # Work sheets
    st.markdown("---")
    st.markdown("#### 🖼️ کارنامه‌های تصویری")

    report_text = f"""📊 گزارش کار | آکادمی ۲۰
👤 {st.session_state['name']}
🎮 سطح: {current_lvl[1]} | ⚡ +{xp_today:,} XP
📅 {rep_date} | ⭐ {satisfaction}/10
⏳ مطالعه: {study_hours} ساعت
📝 تست: {total_tests} (✅ {total_c} | ❌ {total_w})
🎯 درصد: {overall_perc}%
📱 اسکرین: {screen_t} | 💎 DDI: {ddi_val}%
━━━━━━━━━━━━━━━━━━━━
📚 ریز پارت‌ها:
""" + "\n".join(parts_summary) + f"""
━━━━━━━━━━━━━━━━━━━━
🔥 زنجیره: {streak} روز
👨‍🏫 دکتر خشایار اشکبوس | @Kh_Ashkboos"""

    co1, co2 = st.columns(2)
    with co1:
        st.text_area("متن کپی:", report_text, height=180)
        tg_url = "https://t.me/share/url?url=" + urllib.parse.quote(report_text)
        st.markdown(f'<a href="{tg_url}" target="_blank" class="tg-button">🚀 ارسال به تلگرام</a>',
                    unsafe_allow_html=True)
        try:
            card_bytes = generate_report_card(st.session_state['name'], str(rep_date), satisfaction,
                                              study_hours, total_tests, overall_perc, screen_t,
                                              current_lvl[1], total_xp+xp_today, streak, ddi_val, ddi_lvl)
            st.download_button("📥 دانلود کارنامه (۱۰۰۰×۷۲۰)", card_bytes,
                               file_name=f"report_{rep_date}.png", mime="image/png",
                               use_container_width=True)
        except Exception as e:
            st.error(f"خطای کارنامه: {e}")

    with co2:
        try:
            story_bytes = generate_story_card(
                st.session_state['name'], str(rep_date), study_hours, total_tests,
                overall_perc, ddi_val, ddi_lvl, current_lvl[1], xp_today, streak,
                list(BADGES.keys())[:0]  # placeholder
            )
            st.image(story_bytes, caption="📱 کارنامه استوری (۱۰۸۰×۱۹۲۰)", use_container_width=True)
            st.download_button("📥 دانلود استوری اینستاگرام/تلگرام", story_bytes,
                               file_name=f"story_{rep_date}.png", mime="image/png",
                               use_container_width=True)
        except Exception as e:
            st.error(f"خطای استوری: {e}")

# ═══════════════════════════════════════════════════════
# TAB 2 — Pomodoro
# ═══════════════════════════════════════════════════════
with t2:
    st.markdown("### 🍅 تایمر پومودورو کنکوری")
    st.markdown("""
    <div class="glass-card" style="font-size:13.5px; color:#cbd5e1;">
    🎯 <b>پومودورو:</b> ۲۵ دقیقه تمرکز + ۵ دقیقه استراحت.
    ⚡ حالت سرعتی برای تست. ☕ برای استراحت.
    </div>""", unsafe_allow_html=True)
    render_pomodoro()

# ═══════════════════════════════════════════════════════
# TAB 3 — 🔮 Rank Predictor
# ═══════════════════════════════════════════════════════
with t3:
    st.markdown("### 🔮 شبیه‌ساز تراز و تخمین رتبه زنده")
    st.markdown("""
    <div class="glass-card" style="font-size:13.5px; color:#cbd5e1;">
    🤖 بر اساس میانگین ۳۰ روز اخیر (ساعت مطالعه + حجم تست + درصد خالص)، یک بازه احتمالی رتبه کنکور با مدل هیوریستیک تخمین زده می‌شود.
    <b style="color:#facc15;">توجه:</b> این تخمین آموزشی است و جایگزین آزمون واقعی نیست.
    </div>""", unsafe_allow_html=True)

    if df_all.empty:
        st.info("⚠️ برای فعال شدن پیش‌بینی، حداقل ۱ گزارش ثبت کن.")
    else:
        df30 = df_all[pd.to_datetime(df_all['report_date']) >=
                      pd.Timestamp(datetime.date.today() - datetime.timedelta(days=30))]
        if df30.empty:
            st.warning("⚠️ در ۳۰ روز اخیر گزارشی نداری. بازه «همه» استفاده می‌شود.")
            df30 = df_all

        avg_h = df30['study_hours'].mean()
        avg_t = df30['total_tests'].mean()
        avg_p = df30['percentage'].mean()

        traz, rlo, rmid, rhi, comp = predict_rank(avg_h, avg_t, avg_p)
        tier, tcol = rank_tier(rmid)

        cA, cB = st.columns([1, 1])
        with cA:
            st.markdown(f"""
            <div class="rank-card" style="text-align:center;">
                <div style="font-size:13px; color:#94a3b8;">بازه احتمالی رتبه (۳۰ روز اخیر)</div>
                <div class="rank-number" style="margin:14px 0;">{rlo:,} تا {rhi:,}</div>
                <div class="rank-label">مرکز تخمین: <b style="color:#38bdf8;">{rmid:,}</b></div>
                <div style="margin-top:14px; font-size:18px; font-weight:900; color:{tcol};">
                    {tier}
                </div>
            </div>""", unsafe_allow_html=True)
        with cB:
            st.markdown(f"""
            <div class="rank-card" style="text-align:center; border-color:rgba(56,189,248,.4);">
                <div style="font-size:13px; color:#94a3b8;">تراز تخمینی</div>
                <div class="rank-number" style="margin:14px 0; background:linear-gradient(90deg,#4ade80,#38bdf8,#a78bfa); -webkit-background-clip:text;">{traz:,}</div>
                <div class="rank-label">از ۱۰,۰۰۰</div>
                <div style="margin-top:14px; font-size:13px; color:#94a3b8;">امتیاز ترکیبی: <b style="color:#facc15;">{comp*100:.1f}%</b></div>
            </div>""", unsafe_allow_html=True)

        # میانگین‌های پایه
        st.markdown(f"""
        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:12px; margin:18px 0;">
            <div class="metric-card"><span class="metric-icon">⏳</span>
                <div class="metric-num">{avg_h:.1f}</div>
                <div class="metric-txt">میانگین ساعت</div></div>
            <div class="metric-card"><span class="metric-icon">📝</span>
                <div class="metric-num">{avg_t:.0f}</div>
                <div class="metric-txt">میانگین تست</div></div>
            <div class="metric-card"><span class="metric-icon">🎯</span>
                <div class="metric-num">{avg_p:.1f}%</div>
                <div class="metric-txt">میانگین درصد</div></div>
        </div>""", unsafe_allow_html=True)

        # 🎮 What-If Scenarios
        st.markdown("#### 🎮 شبیه‌سازی «چی می‌شه اگر...»")
        scenarios = []
        for dh, dt, dp, lbl in [
            (0, 0, 0, "📍 وضعیت فعلی"),
            (0.5, 10, 2, "📈 کمی بهتر"),
            (1.0, 20, 5, "🚀 جدی‌تر"),
            (1.5, 35, 8, "🔥 حالت حرفه‌ای"),
            (2.0, 50, 12, "💎 منطقه المپیک"),
        ]:
            nh = min(avg_h + dh, 14); nt = min(avg_t + dt, 250); np_ = min(avg_p + dp, 100)
            _, rl2, rm2, rh2, _ = predict_rank(nh, nt, np_)
            scenarios.append({
                'سناریو': lbl,
                'ساعت': round(nh, 1),
                'تست': int(nt),
                'درصد': round(np_, 1),
                'رتبه تخمینی': f"{rl2:,} - {rh2:,}",
                'تفاوت': f"{rmid - rm2:+,}" if rm2 != rmid else "—",
            })
        sdf = pd.DataFrame(scenarios)
        st.dataframe(sdf, use_container_width=True, hide_index=True)

        # Chart
        fig_what = go.Figure()
        for i, sc in enumerate(scenarios):
            _, rl2, rm2, rh2, _ = predict_rank(sc['ساعت'], sc['تست'], sc['درصد'])
            color = "#38bdf8" if i == 0 else "#4ade80" if rm2 < rmid else "#f87171"
            fig_what.add_trace(go.Bar(
                x=[sc['سناریو']], y=[rm2], name=sc['سناریو'],
                marker_color=color, text=[f"{rm2:,}"], textposition='outside',
                error_y=dict(type='data', symmetric=False,
                             array=[rh2-rm2], arrayminus=[rm2-rl2], color=color, thickness=1.5, width=8),
                showlegend=False,
            ))
        fig_what.update_layout(
            title="تخمین رتبه در سناریوهای مختلف (کمتر = بهتر)",
            template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)', font={'family':'Vazirmatn'},
            yaxis_title="رتبه تخمینی", height=420,
        )
        st.plotly_chart(fig_what, use_container_width=True)

        # Trend
        st.markdown("#### 📉 روند رتبه تخمینی شما (روز به روز)")
        df_sorted = df_all.sort_values('report_date').copy()
        df_sorted['date'] = pd.to_datetime(df_sorted['report_date'])
        ranks = []
        for _, row in df_sorted.iterrows():
            _, _, rm, _, _ = predict_rank(row['study_hours'], row['total_tests'], row['percentage'])
            ranks.append(rm)
        df_sorted['predicted_rank'] = ranks

        fig_tr = px.line(df_sorted, x='date', y='predicted_rank',
                         title="تغییرات رتبه تخمینی در طول زمان",
                         labels={'predicted_rank':'رتبه تخمینی', 'date':'تاریخ'},
                         markers=True, color_discrete_sequence=['#a78bfa'])
        fig_tr.update_traces(line=dict(width=3), marker=dict(size=10,
                             line=dict(width=2, color='#0b0f19')))
        fig_tr.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)',
                             paper_bgcolor='rgba(0,0,0,0)', font={'family':'Vazirmatn'},
                             yaxis_autorange="reversed")
        st.plotly_chart(fig_tr, use_container_width=True)

# ═══════════════════════════════════════════════════════
# TAB 4 — ⚔️ Arena
# ═══════════════════════════════════════════════════════
with t4:
    st.markdown("### ⚔️ اتاق جنگ — دو﻿ئل دوستانه")
    st.markdown("""
    <div class="glass-card" style="font-size:13.5px; color:#cbd5e1;">
    🔥 با دوستات <b>اتاق مطالعه گروهی</b> بساز، اسم مستعار بذار و در <b>لیدربورد هفتگی</b> با هم رقابت کن!
    رتبه‌بندی بر اساس ساعت مطالعه × ۵۰ + تعداد تست × ۲.
    </div>""", unsafe_allow_html=True)

    my_rooms = pd.read_sql_query(
        "SELECT r.code, r.name, m.nickname FROM arena_rooms r "
        "JOIN arena_members m ON r.code=m.code WHERE m.username=?",
        conn, params=(st.session_state['username'],))

    a1, a2 = st.columns(2)
    with a1:
        st.markdown("##### 🏗️ ساخت اتاق جدید")
        new_name = st.text_input("اسم اتاق:", placeholder="مثلاً: جنگجویان پزشکی ۱۴۰۵", key="new_room_name")
        new_nick = st.text_input("اسم مستعار خودت:", placeholder="مثلاً: دکتر X", key="new_nick")
        if st.button("✨ ساخت اتاق", use_container_width=True):
            if new_name and new_nick:
                code = f"{random.randint(1000,9999)}-{random.choice('ABCDEFGHJK')}{random.choice('ABCDEFGHJK')}"
                try:
                    c.execute("INSERT INTO arena_rooms VALUES (?,?,?,?)",
                              (code, new_name, st.session_state['username'], datetime.datetime.now()))
                    c.execute("INSERT INTO arena_members VALUES (?,?,?,?)",
                              (code, st.session_state['username'], new_nick, datetime.datetime.now()))
                    conn.commit()
                    st.success(f"🎉 اتاق ساخته شد! کد دعوت: `{code}`")
                    st.rerun()
                except Exception as e:
                    st.error(f"خطا: {e}")
            else:
                st.warning("همه فیلدها پر کن")

    with a2:
        st.markdown("##### 🎟️ پیوستن به اتاق")
        join_code = st.text_input("کد اتاق:", key="join_code").strip()
        join_nick = st.text_input("اسم مستعار:", key="join_nick")
        if st.button("🚀 پیوستن", use_container_width=True):
            if join_code and join_nick:
                c.execute("SELECT name FROM arena_rooms WHERE code=?", (join_code,))
                r = c.fetchone()
                if not r:
                    st.error("❌ اتاق پیدا نشد")
                else:
                    try:
                        c.execute("INSERT INTO arena_members VALUES (?,?,?,?)",
                                  (join_code, st.session_state['username'], join_nick, datetime.datetime.now()))
                        conn.commit()
                        st.success(f"🎉 به «{r[0]}» پیوستی!")
                        st.rerun()
                    except Exception:
                        st.info("ℹ️ قبلاً عضو بودی")

    st.markdown("---")
    if my_rooms.empty:
        st.info("💡 هنوز توی هیچ اتاقی نیستی. یکی بساز یا به دوستت بپیوند!")
    else:
        room_options = [f"{r['name']} ({r['code']})" for _, r in my_rooms.iterrows()]
        selected = st.selectbox("🏠 اتاق‌های تو:", room_options)
        sel_code = selected.split("(")[-1].rstrip(")")
        lb = arena_leaderboard(sel_code)

        if lb.empty:
            st.info("اتاق خالیه")
        else:
            st.markdown(f"#### 🏆 لیدربورد ۷ روز اخیر — {selected}")
            rank_icons = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
            for idx, row in lb.iterrows():
                icon = rank_icons[idx-1] if idx <= 10 else f"{idx}."
                me_cls = "arena-me" if row['is_me'] else ""
                me_badge = " <span style='color:#38bdf8; font-size:11px;'>(تو)</span>" if row['is_me'] else ""
                st.markdown(f"""
                <div class="arena-card {me_cls}">
                    <div class="arena-rank">{icon}</div>
                    <div style="flex:1;">
                        <div style="font-weight:800; font-size:15px;">{row['nickname']}{me_badge}</div>
                        <div style="font-size:12px; color:#94a3b8;">
                            ⏳ {row['hours']} ساعت &nbsp;•&nbsp; 📝 {row['tests']} تست
                        </div>
                    </div>
                    <div style="font-size:18px; font-weight:900; color:#facc15;">
                        {row['score']:,} <span style="font-size:11px; color:#94a3b8;">XP</span>
                    </div>
                </div>""", unsafe_allow_html=True)

            # Bar chart
            fig_lb = px.bar(lb, x='nickname', y='score',
                            title="مقایسه امتیاز اعضا",
                            color='score',
                            color_continuous_scale=['#0ea5e9','#7c3aed','#f472b6','#facc15'])
            fig_lb.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)',
                                 paper_bgcolor='rgba(0,0,0,0)', font={'family':'Vazirmatn'},
                                 coloraxis_showscale=False, showlegend=False)
            st.plotly_chart(fig_lb, use_container_width=True)

# ═══════════════════════════════════════════════════════
# TAB 5 — Analysis + AI Coach + Error Vault
# ═══════════════════════════════════════════════════════
with t5:
    st.markdown("### 📈 داشبورد تحلیل هوشمند")
    if df_all.empty:
        st.info("⚠️ هنوز گزارشی ثبت نکرده‌ای!")
    else:
        df_all['report_date'] = pd.to_datetime(df_all['report_date'])
        cf1, _ = st.columns([1, 2])
        tf = cf1.radio("بازه:", ["۷ روز", "۳۰ روز", "همه"], horizontal=True)
        if "۷" in tf:
            fdf = df_all[df_all['report_date'] >= pd.Timestamp(datetime.date.today() - datetime.timedelta(days=7))]
        elif "۳۰" in tf:
            fdf = df_all[df_all['report_date'] >= pd.Timestamp(datetime.date.today() - datetime.timedelta(days=30))]
        else: fdf = df_all

        if fdf.empty:
            st.warning("داده‌ای در این بازه نیست.")
        else:
            sh = fdf['study_hours'].sum(); stt = fdf['total_tests'].sum()
            ap = fdf['percentage'].mean(); asat = fdf['satisfaction'].mean()
            pXP = int(sh*50 + stt*2)

            st.markdown(f"""
            <div style="display:grid; grid-template-columns: repeat(5, 1fr); gap:10px; margin-bottom:22px;">
                <div class="metric-card"><span class="metric-icon">⚡</span>
                    <div class="metric-num">{pXP:,}</div><div class="metric-txt">XP بازه</div></div>
                <div class="metric-card"><span class="metric-icon">⏳</span>
                    <div class="metric-num">{sh:.1f}</div><div class="metric-txt">ساعت</div></div>
                <div class="metric-card"><span class="metric-icon">📝</span>
                    <div class="metric-num">{stt}</div><div class="metric-txt">تست</div></div>
                <div class="metric-card"><span class="metric-icon">🎯</span>
                    <div class="metric-num">{ap:.1f}%</div><div class="metric-txt">درصد</div></div>
                <div class="metric-card"><span class="metric-icon">⭐</span>
                    <div class="metric-num">{asat:.1f}</div><div class="metric-txt">رضایت</div></div>
            </div>""", unsafe_allow_html=True)

            # AI Coach
            st.markdown("#### 🤖 تحلیلگر AI Coach")
            last_r = df_all.iloc[-1].to_dict()
            tips = ai_coach_analysis(fdf, last_r)
            th = "".join([f'<div class="ai-tip {c}">{t}</div>' for c, t in tips])
            st.markdown(f'<div class="ai-coach">{th}</div>', unsafe_allow_html=True)

            # 🆕 Error Vault Chart
            st.markdown("#### 🎯 جعبه سیاه اشتباهات (Smart Error Vault)")
            ev = pd.read_sql_query(
                "SELECT subject, error_tag, SUM(count) as cnt FROM error_vault "
                "WHERE username=? GROUP BY subject, error_tag",
                conn, params=(st.session_state['username'],))
            if ev.empty:
                st.info("💡 تا حالا اشتباهی تگ نکرده‌ای. دفعه بعد که غلط زدی، علتش رو تگ کن!")
            else:
                ec1, ec2 = st.columns(2)
                with ec1:
                    fig_et = px.pie(ev, names='error_tag', values='cnt', hole=.5,
                                    title="📊 توزیع کل علل غلط‌ها",
                                    color_discrete_sequence=px.colors.qualitative.Bold)
                    fig_et.update_traces(textposition='inside', textinfo='percent+label')
                    fig_et.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)',
                                         paper_bgcolor='rgba(0,0,0,0)', font={'family':'Vazirmatn'},
                                         showlegend=True, height=420)
                    st.plotly_chart(fig_et, use_container_width=True)
                with ec2:
                    fig_es = px.bar(ev, x='subject', y='cnt', color='error_tag',
                                    title="🎓 تفکیک علل غلط بر اساس درس",
                                    color_discrete_sequence=px.colors.qualitative.Bold)
                    fig_es.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)',
                                         paper_bgcolor='rgba(0,0,0,0)', font={'family':'Vazirmatn'},
                                         height=420, barmode='stack')
                    st.plotly_chart(fig_es, use_container_width=True)

                # Coach insight
                top_err = ev.groupby('error_tag')['cnt'].sum().sort_values(ascending=False)
                if len(top_err) >= 1:
                    top_name = top_err.index[0]
                    top_pct = (top_err.iloc[0] / top_err.sum()) * 100
                    st.markdown(f"""
                    <div class="ai-coach">
                        <div class="ai-tip info">
                        🧠 <b>تحلیل مشاور:</b> بیشترین علت غلط‌های تو <b style="color:#facc15;">{top_name}</b> است
                        ({top_pct:.0f}٪ از کل غلط‌ها).
                        {"این یعنی مشکل تو «دانش» نیست، بلکه «اجرا»ست — تمرین تمرکز و مدیریت زمان." if 'دقت' in top_name or 'وقت' in top_name or 'خواندن' in top_name else "روی مرور و تثبیت مباحث تمرکز کن."}
                        </div>
                    </div>""", unsafe_allow_html=True)

            # DDI Chart
            st.markdown("#### 💎 شاخص تخلیه تمرکز (DDI) در طول زمان")
            ddi_rows = []
            for _, row in fdf.iterrows():
                dv, dl = compute_ddi(row['study_hours'], row['social_time'])
                ddi_rows.append({'date': row['report_date'], 'ddi': dv, 'level': dl})
            if ddi_rows:
                ddf = pd.DataFrame(ddi_rows)
                cmap = {'green':'#4ade80', 'yellow':'#facc15', 'red':'#f87171'}
                fig_ddi = go.Figure()
                for lvl, col in cmap.items():
                    sub = ddf[ddf['level'] == lvl]
                    if not sub.empty:
                        fig_ddi.add_trace(go.Scatter(
                            x=sub['date'], y=sub['ddi'], mode='markers',
                            name=lvl, marker=dict(color=col, size=14,
                            line=dict(width=2, color='#0b0f19'))))
                fig_ddi.add_hline(y=10, line_dash="dash", line_color="#4ade80",
                                  annotation_text="مرز سبز (۱۰٪)")
                fig_ddi.add_hline(y=25, line_dash="dash", line_color="#f87171",
                                  annotation_text="مرز قرمز (۲۵٪)")
                fig_ddi.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)',
                                      paper_bgcolor='rgba(0,0,0,0)', font={'family':'Vazirmatn'},
                                      title="روند DDI روزانه — پایین‌تر = بهتر",
                                      yaxis_title="DDI (%)")
                st.plotly_chart(fig_ddi, use_container_width=True)

            # Sunburst
            st.markdown("#### 🌞 سبد مطالعاتی ۳۰ روزه")
            pd30 = pd.read_sql_query(
                "SELECT subject, minutes, tests FROM parts WHERE username=? AND report_date >= ?",
                conn, params=(st.session_state['username'],
                              (datetime.date.today() - datetime.timedelta(days=30)).isoformat()))
            if not pd30.empty:
                sc1, sc2 = st.columns(2)
                with sc1:
                    fs = px.sunburst(pd30, path=['subject'], values='minutes', color='minutes',
                                     color_continuous_scale=['#0ea5e9','#7c3aed','#f472b6'],
                                     title="⏱️ توزیع زمان")
                    fs.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)',
                                     font={'family':'Vazirmatn'}, height=400)
                    st.plotly_chart(fs, use_container_width=True)
                with sc2:
                    sg = pd30.groupby('subject').agg({'minutes':'sum','tests':'sum'}).reset_index().sort_values('minutes', ascending=False)
                    fb = px.bar(sg, x='subject', y='minutes', color='tests',
                                title="📊 رتبه‌بندی دروس",
                                color_continuous_scale=['#38bdf8','#f472b6'])
                    fb.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)',
                                     plot_bgcolor='rgba(0,0,0,0)', font={'family':'Vazirmatn'}, height=400)
                    st.plotly_chart(fb, use_container_width=True)

            # Trends
            st.markdown("#### 📈 روندها")
            g1, g2 = st.columns([1, 2])
            with g1:
                gg = go.Figure(go.Indicator(mode="gauge+number", value=float(ap),
                    number={'suffix':'%','font':{'color':'#38bdf8','size':34}},
                    gauge={'axis':{'range':[0,100]}, 'bar':{'color':'#4ade80'}, 'bgcolor':'#1e293b',
                           'steps':[{'range':[0,40],'color':'rgba(248,113,113,.18)'},
                                    {'range':[40,70],'color':'rgba(250,204,21,.18)'},
                                    {'range':[70,100],'color':'rgba(74,222,128,.18)'}]},
                    title={'text':"درصد خالص",'font':{'color':'#cbd5e1','size':14}}))
                gg.update_layout(template="plotly_dark", height=280,
                                 plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                 font={'family':'Vazirmatn'})
                st.plotly_chart(gg, use_container_width=True)
            with g2:
                fh = px.bar(fdf, x='report_date', y='study_hours',
                            title=f"⏳ ساعت مطالعه ({tf})", color='study_hours',
                            color_continuous_scale=['#0ea5e9','#7c3aed','#f472b6'])
                fh.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)',
                                 paper_bgcolor='rgba(0,0,0,0)', font={'family':'Vazirmatn'},
                                 coloraxis_showscale=False, height=280)
                st.plotly_chart(fh, use_container_width=True)

# ═══════════════════════════════════════════════════════
# TAB 6 — Badges
# ═══════════════════════════════════════════════════════
with t6:
    st.markdown("### 🏆 تالار افتخارات")
    c.execute("SELECT badge_id, unlocked_at FROM user_badges WHERE username=?",
              (st.session_state['username'],))
    um = {r[0]: r[1] for r in c.fetchall()}
    tb = len(BADGES); uc = len(um); pct = (uc/tb)*100

    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:14px; color:#94a3b8;">پیشرفت مدال‌ها</div>
        <div style="font-size:32px; font-weight:900; color:#facc15; margin:8px 0;">{uc} / {tb}</div>
        <div class="xp-track" style="height:14px;">
            <div class="xp-fill" style="--target:{pct:.0f}%; width:{pct:.0f}%;"></div>
        </div>
    </div>""", unsafe_allow_html=True)

    cols = st.columns(4)
    for idx, (bid, (icon, name, desc)) in enumerate(BADGES.items()):
        unl = bid in um
        cls = "unlocked" if unl else "locked"
        date_u = ""
        if unl:
            try:
                dt = pd.to_datetime(um[bid])
                date_u = f"<div style='font-size:10px; color:#94a3b8; margin-top:6px;'>{dt.strftime('%Y/%m/%d')}</div>"
            except Exception: pass
        with cols[idx % 4]:
            st.markdown(f"""<div class="badge-ach {cls}">
                <div style="font-size:36px;">{icon}</div>
                <div style="font-size:14px; font-weight:900; margin-top:6px;">{name}</div>
                <div style="font-size:11px; color:#94a3b8; margin-top:4px;">{desc}</div>
                {date_u}</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# TAB 7 — Settings
# ═══════════════════════════════════════════════════════
with t7:
    st.markdown(f"""
    <div class="glass-card">
        <h3>👤 پروفایل قهرمان</h3>
        <p>نام: <b style="color:#38bdf8;">{st.session_state['name']}</b></p>
        <p>نام کاربری: <code style="color:#38bdf8;">{st.session_state['username']}</code></p>
        <p>سطح: <span style="color:{current_lvl[3]}; font-weight:900;">{current_lvl[2]} {current_lvl[1]}</span></p>
        <p>⚡ XP: <b style="color:#facc15;">{total_xp:,}</b></p>
        <p>🔥 زنجیره: <b style="color:#fb923c;">{streak} روز</b></p>
        <p>📊 گزارش‌ها: <b>{len(df_all)}</b></p>
    </div>""", unsafe_allow_html=True)

    if st.button("🚪 خروج از حساب", use_container_width=True):
        st.session_state['logged_in'] = False
        st.rerun()
