import streamlit as st
import streamlit.components.v1 as components
import datetime
import urllib.parse
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io, random, re, json

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
        border:1px solid rgba(250,204,21,.35); border-radius:18px; padding:18px 20px; margin-bottom:18px; }
    .xp-header { display:flex; justify-content:space-between; align-items:center; gap:12px; margin-bottom:14px; flex-wrap:wrap; }
    .level-badge { display:inline-flex; align-items:center; gap:8px;
        background:linear-gradient(90deg,rgba(250,204,21,.2),rgba(244,114,182,.2));
        border:2px solid #facc15; border-radius:12px; padding:8px 14px; font-weight:900; font-size:15px;
        color:#facc15 !important; }
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
    
    .metric-card { background:linear-gradient(145deg,rgba(17,24,39,.85),rgba(30,41,59,.75));
        backdrop-filter:blur(12px); border:1px solid rgba(56,189,248,.28); border-radius:18px;
        padding:18px 12px; text-align:center; }
    .metric-num { font-size:28px; font-weight:900;
        background:linear-gradient(90deg,#38bdf8,#4ade80); -webkit-background-clip:text;
        -webkit-text-fill-color:transparent; background-clip:text; }
    .metric-txt { font-size:12px; color:#94a3b8 !important; margin-top:6px; }
    .metric-icon { font-size:22px; display:block; margin-bottom:4px; }
    
    .badge-ach { display:block; padding:18px 10px; border-radius:14px; font-weight:800; font-size:13px;
        margin:5px 0; border:2px solid; text-align:center; }
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
    
    .ddi-panel { border-radius:16px; padding:16px; margin:12px 0; text-align:center; border:3px solid; }
    .ddi-green { border-color:#4ade80; background:linear-gradient(135deg,rgba(74,222,128,.15),rgba(56,189,248,.1)); }
    .ddi-yellow { border-color:#facc15; background:linear-gradient(135deg,rgba(250,204,21,.15),rgba(251,146,60,.1)); }
    .ddi-red { border-color:#f87171; background:linear-gradient(135deg,rgba(248,113,113,.2),rgba(220,38,38,.15)); }
    .ddi-value { font-size:42px; font-weight:900; letter-spacing:2px; }
    .ddi-label { font-size:14px; margin-top:6px; font-weight:800; }
    
    .rank-card { background:linear-gradient(145deg,rgba(17,24,39,.85),rgba(30,41,59,.75));
        border:2px solid rgba(168,85,247,.4); border-radius:18px; padding:22px; margin-bottom:16px; }
    .rank-number { font-size:56px; font-weight:900; letter-spacing:2px;
        background:linear-gradient(90deg,#38bdf8,#a78bfa,#f472b6); -webkit-background-clip:text;
        -webkit-text-fill-color:transparent; background-clip:text; line-height:1; }
    .rank-label { font-size:13px; color:#94a3b8 !important; margin-top:8px; }
    
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
    .stButton > button { background:linear-gradient(90deg,#0284c7,#7c3aed) !important; color:#fff !important;
        border:none !important; border-radius:12px !important; font-weight:800 !important;
        padding:10px 18px !important; transition:all .3s !important; }
    .stButton > button:hover { transform:translateY(-2px); }
    .tg-button { display:block; width:100%; background:linear-gradient(90deg,#0088cc,#005f8f);
        color:#fff !important; text-align:center; font-size:16px; font-weight:800;
        padding:14px; border-radius:12px; text-decoration:none; margin-top:15px; }
    .stTabs [data-baseweb="tab-list"] { gap:6px; background:rgba(17,24,39,.6);
        padding:8px; border-radius:14px; border:1px solid rgba(56,189,248,.18); flex-wrap:wrap; }
    .stTabs [data-baseweb="tab"] { border-radius:10px !important; padding:10px 14px !important; font-weight:700 !important; }
    .stTabs [aria-selected="true"] { background:linear-gradient(90deg,#0284c7,#7c3aed) !important; color:#fff !important; }
    
    .glass-card { background:rgba(17,24,39,.72); backdrop-filter:blur(12px);
        border:1px solid rgba(56,189,248,.22); border-radius:16px; padding:18px; margin-bottom:14px; }
    
    div[data-baseweb="select"] > div { background-color:#1e293b !important; color:#fff !important; }
    div[data-baseweb="popover"] *, ul[role="listbox"] *, li[role="option"] * {
        background-color:#1e293b !important; color:#fff !important; }
    ul[role="listbox"] li:hover, li[role="option"]:hover { background-color:#0284c7 !important; }
    
    .time-label { font-weight:700; color:#38bdf8 !important; font-size:14px; margin-bottom:8px; display:block; }
    .time-preview { text-align:center; background:linear-gradient(90deg,#0284c7,#7c3aed);
        color:#fff !important; font-weight:900; font-size:26px; padding:12px; border-radius:12px;
        margin:8px 0; letter-spacing:3px; font-family:'Courier New',monospace !important; }
    
    .clock-grid-label { font-size:12.5px; color:#94a3b8 !important; margin:8px 0 4px 0; display:block; font-weight:700; }
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

ERROR_TAGS = ["بی‌دقتی محاسباتی","فراموشی فرمول","دام طراح","کمبود وقت","عدم تسلط به مبحث","اشتباه در خواندن سؤال"]

# ═══════════════════════════════════════════════════════
# ۵. Helpers
# ═══════════════════════════════════════════════════════
def compute_streak(df):
    if df.empty: return 0
    dates = sorted(set(pd.to_datetime(df['report_date']).dt.date), reverse=True)
    today = datetime.date.today()
    if dates[0] != today and dates[0] != today - datetime.timedelta(days=1): return 0
    check = dates[0]; s = 0
    for d in dates:
        if d == check: s += 1; check -= datetime.timedelta(days=1)
        elif d < check: break
    return s

def calculate_xp(df):
    if df.empty: return 0
    return int(df['study_hours'].sum() * 50 + df['total_tests'].sum() * 2)

def get_level(xp):
    cur = LEVELS[0]; nxt = None; idx = 0
    for i, lvl in enumerate(LEVELS):
        if xp >= lvl[0]: cur = lvl; idx = i
    if idx + 1 < len(LEVELS): nxt = LEVELS[idx + 1]
    if nxt:
        rng = nxt[0] - cur[0]
        prog = min(100, max(0, ((xp - cur[0]) / rng) * 100))
    else: prog = 100.0
    return cur, nxt, prog

def parse_duration(text):
    text = str(text).strip()
    for i, d in enumerate("۰۱۲۳۴۵۶۷۸۹"): text = text.replace(d, str(i))
    text = text.replace('ساعت', ':').replace('دقیقه', '').replace('دق', '').replace('،', '').replace(',', '').strip()
    if ':' in text:
        try:
            h, m = text.split(':')[:2]
            return int(float(h)) * 60 + int(float(m))
        except Exception: pass
    nums = re.findall(r'[\d.]+', text)
    return int(float(nums[0])) if nums else 0

def compute_ddi(study_hours, social_time_str):
    social_min = parse_duration(social_time_str)
    study_min = study_hours * 60
    if study_min <= 0: return (100.0, "red") if social_min > 0 else (0.0, "green")
    ddi = (social_min / study_min) * 100
    return round(ddi, 1), ("green" if ddi < 10 else "yellow" if ddi < 25 else "red")

DDI_META = {
    "green": ("💎", "مغز الماسی — تمرکز فولادین!", "#4ade80", "ddi-green"),
    "yellow": ("⚠️", "خطر افت دوپامین — مواظب باش!", "#facc15", "ddi-yellow"),
    "red": ("🔥", "وضعیت بحرانی — تمرکز در حال سوختن!", "#f87171", "ddi-red"),
}

def ddi_badge_html(ddi, level):
    icon, lbl, color, cls = DDI_META[level]
    return f"""<div class="ddi-panel {cls}">
        <div class="ddi-value" style="color:{color};">{ddi}%</div>
        <div class="ddi-label" style="color:{color};">{icon} {lbl}</div>
        <div style="font-size:11px; color:#94a3b8; margin-top:4px;">
            شاخص تخلیه تمرکز (DDI) = (شبکه‌های اجتماعی ÷ مطالعه) × ۱۰۰</div>
    </div>"""

def predict_rank(avg_hours, avg_tests, avg_percent):
    h = min(max(avg_hours, 0), 14) / 14
    t = min(max(avg_tests, 0), 200) / 200
    p = min(max(avg_percent, 0), 100) / 100
    comp = h * 0.30 + t * 0.25 + p * 0.45
    traz = int(3000 + comp * 7000)
    rm = int(max(50, 250000 * ((1 - comp) ** 3.2)))
    rl = max(1, int(rm * 0.65)); rh = int(rm * 1.55)
    return traz, rl, rm, rh, comp

def rank_tier(rank_mid):
    if rank_mid < 500: return "🏆 منطقه المپیک", "#facc15"
    if rank_mid < 2000: return "🥇 منطقه طلایی", "#f472b6"
    if rank_mid < 5000: return "🥈 منطقه نقره‌ای", "#a78bfa"
    if rank_mid < 15000: return "🥉 منطقه برنزی", "#38bdf8"
    if rank_mid < 50000: return "💪 در حال رشد", "#4ade80"
    return "🌱 تازه شروع کردی", "#94a3b8"

def arena_leaderboard(code):
    mem = pd.read_sql_query("SELECT username, nickname FROM arena_members WHERE code=?", conn, params=(code,))
    if mem.empty: return pd.DataFrame()
    cutoff = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
    rows = []
    for _, m in mem.iterrows():
        df = pd.read_sql_query(
            "SELECT study_hours, total_tests FROM reports WHERE username=? AND report_date>=?",
            conn, params=(m['username'], cutoff))
        h = float(df['study_hours'].sum()) if not df.empty else 0.0
        t = int(df['total_tests'].sum()) if not df.empty else 0
        rows.append({'nickname': m['nickname'], 'hours': round(h, 1), 'tests': t,
                     'score': int(h * 50 + t * 2),
                     'is_me': m['username'] == st.session_state['username']})
    lb = pd.DataFrame(rows).sort_values('score', ascending=False).reset_index(drop=True)
    lb.index = lb.index + 1
    return lb

def ai_coach_analysis(df, today_report=None):
    tips = []
    if df.empty: return [("info", "🤖 هنوز داده‌ای برای تحلیل نیست.")]
    sh = df['study_hours'].sum(); stt = df['total_tests'].sum()
    if sh > 0:
        sp = stt / sh
        if sp >= 60: tips.append(("success", f"🚀 سرعت تست‌زنی فوق‌العاده! ({sp:.0f} تست/ساعت)"))
        elif sp >= 35: tips.append(("success", f"👍 سرعت تست‌زنی خوب ({sp:.0f} تست/ساعت)"))
        elif sp >= 15: tips.append(("warning", f"⚙️ سرعت متوسط ({sp:.0f} تست/ساعت)"))
        else: tips.append(("danger", f"⚠️ سرعت پایین ({sp:.0f} تست/ساعت)"))
    if today_report:
        ddi, dl = compute_ddi(today_report['study_hours'], today_report['social_time'])
        if dl == "red": tips.append(("danger", f"🔥 DDI {ddi}% — تمرکزت می‌سوزه!"))
        elif dl == "yellow": tips.append(("warning", f"⚠️ DDI {ddi}% — تعادل رو بهتر کن"))
        else: tips.append(("success", f"💎 DDI {ddi}% — مغز الماسی!"))
    asat = df['satisfaction'].mean()
    if asat >= 8: tips.append(("success", f"😊 رضایتت {asat:.1f}/10 عالیه"))
    elif asat < 6: tips.append(("warning", f"💙 رضایتت {asat:.1f}/10 پایینه"))
    return tips

def check_badges(username, report, parts_data):
    nb = []
    c.execute("SELECT badge_id FROM user_badges WHERE username=?", (username,))
    ex = {r[0] for r in c.fetchall()}
    dfu = pd.read_sql_query("SELECT * FROM reports WHERE username=? ORDER BY report_date ASC", conn, params=(username,))
    tr = len(dfu); streak = compute_streak(dfu)
    tt = report['total_tests']; sh = report['study_hours']; pc = report['percentage']
    bio_m = sum(p['minutes'] for p in parts_data if 'زیست' in p['subject'])
    ddi, dl = compute_ddi(sh, report['social_time'])
    _, _, rm, _, _ = predict_rank(sh, tt, pc)
    cand = set()
    if tr >= 1: cand.add("first_step")
    if tt >= 100: cand.add("hunter_100")
    if tt >= 200: cand.add("hunter_200")
    if parse_duration(report['screen_time']) <= 30: cand.add("steel_focus")
    if bio_m >= 180: cand.add("bio_marathon")
    if sh >= 8: cand.add("marathon_day")
    if streak >= 7: cand.add("streak_7")
    if streak >= 30: cand.add("streak_30")
    if pc >= 100 and tt >= 20: cand.add("perfect_day")
    if tr >= 10: cand.add("consistent")
    if ddi < 10: cand.add("ddi_diamond")
    if ddi < 5: cand.add("ddi_warrior")
    if rm < 1000 and tt >= 50: cand.add("rank_hunter")
    for p in parts_data:
        if p.get('start_hour', 99) < 6: cand.add("early_bird")
        if p.get('end_hour', 0) >= 23: cand.add("night_owl")
    for bid in cand:
        if bid not in ex:
            nb.append(bid)
            c.execute("INSERT OR IGNORE INTO user_badges VALUES (?,?,?)", (username, bid, datetime.datetime.now()))
    if nb: conn.commit()
    return nb


# ═══════════════════════════════════════════════════════
# ۶. ⏰ TIME PICKER — نسخه جدید کاملاً کاربردی
# ═══════════════════════════════════════════════════════
def _set_state(k, v):
    st.session_state[k] = v

def creative_time_picker(label, key_prefix, default_h=8, default_m=0):
    """
    انتخابگر ساعت با شبکه دکمه‌های بزرگ.
    - ۲۴ دکمه ساعت در ۶ ستون
    - ۱۲ دکمه دقیقه در ۶ ستون
    - پیش‌نمایش درشت زنده
    """
    hk = f"{key_prefix}_H"
    mk = f"{key_prefix}_M"
    
    if hk not in st.session_state: st.session_state[hk] = default_h
    if mk not in st.session_state: st.session_state[mk] = default_m
    
    cur_h = st.session_state[hk]
    cur_m = st.session_state[mk]
    
    # پیش‌نمایش اول
    st.markdown(f'<span class="time-label">🕐 {label}</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="time-preview">⏰ {cur_h:02d}:{cur_m:02d}</div>', unsafe_allow_html=True)
    
    # ساعت‌ها: 6 ستون × 4 ردیف
    st.markdown('<span class="clock-grid-label">🕐 ساعت (کلیک کن):</span>', unsafe_allow_html=True)
    for row in range(4):
        cols = st.columns(6)
        for col_idx in range(6):
            h = row * 6 + col_idx
            is_act = cur_h == h
            lbl = f"✅ {h:02d}" if is_act else f"{h:02d}"
            cols[col_idx].button(
                lbl,
                key=f"{key_prefix}_HB_{h}",
                use_container_width=True,
                on_click=_set_state,
                args=(hk, h),
                type="primary" if is_act else "secondary",
            )
    
    # دقیقه‌ها: 6 ستون × 2 ردیف
    st.markdown('<span class="clock-grid-label">⏱️ دقیقه (پله ۵):</span>', unsafe_allow_html=True)
    minutes_list = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    for row in range(2):
        cols = st.columns(6)
        for col_idx in range(6):
            m = minutes_list[row * 6 + col_idx]
            is_act = cur_m == m
            lbl = f"✅ {m:02d}" if is_act else f"{m:02d}"
            cols[col_idx].button(
                lbl,
                key=f"{key_prefix}_MB_{m}",
                use_container_width=True,
                on_click=_set_state,
                args=(mk, m),
                type="primary" if is_act else "secondary",
            )
    
    # نمایش نهایی + محاسبه مدت
    final_h = st.session_state.get(hk, default_h)
    final_m = st.session_state.get(mk, default_m)
    st.markdown(f'<div class="time-preview">⏰ {final_h:02d}:{final_m:02d}</div>', unsafe_allow_html=True)
    
    return datetime.time(final_h, final_m)


# ═══════════════════════════════════════════════════════
# ۷. 🎨 HTML CARD GENERATOR (فارسی سالم + دانلود PNG)
# ═══════════════════════════════════════════════════════
def render_html_report_card(name, date_str, satisfaction, study_hours, total_tests,
                             percentage, screen_time, ddi_val, ddi_lvl, level_name,
                             xp, streak, card_id="card1"):
    """کارت کارنامه با HTML + html2canvas → فارسی کاملاً درست"""
    ddi_color = {"green":"#4ade80","yellow":"#facc15","red":"#f87171"}[ddi_lvl]
    ddi_label = {"green":"💎 مغز الماسی","yellow":"⚠️ افت دوپامین","red":"🔥 تمرکز بحرانی"}[ddi_lvl]
    ddi_bg = {"green":"rgba(74,222,128,0.08)","yellow":"rgba(250,204,21,0.08)","red":"rgba(248,113,113,0.12)"}[ddi_lvl]
    
    html = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
        <meta charset="UTF-8">
        <link href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css" rel="stylesheet">
        <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
        <style>
            * {{ box-sizing: border-box; font-family: Vazirmatn, sans-serif; }}
            body {{ margin:0; padding:0; background: transparent; }}
            #card-{card_id} {{
                width: 520px; padding: 34px 30px;
                background: linear-gradient(145deg, #0b1220 0%, #1a2240 100%);
                border: 3px solid #38bdf8; border-radius: 24px;
                color: #fff; position: relative; overflow: hidden;
                box-shadow: 0 24px 60px rgba(56,189,248,0.35), inset 0 1px 0 rgba(255,255,255,0.08);
            }}
            #card-{card_id}::before {{
                content:''; position:absolute; inset:6px; border-radius:18px; padding:2px;
                background: linear-gradient(135deg,#38bdf8,#a78bfa,#f472b6,#facc15,#38bdf8);
                background-size: 300% 100%;
                animation: shift 8s linear infinite;
                -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
                -webkit-mask-composite: xor; mask-composite: exclude; pointer-events: none;
            }}
            @keyframes shift {{ 0%{{background-position:0% 50%}} 100%{{background-position:200% 50%}} }}
            
            .badge-20 {{
                position: absolute; top: 20px; left: 20px; width: 64px; height: 64px;
                border-radius: 50%; display:flex; align-items:center; justify-content:center;
                background: radial-gradient(circle at 30% 30%, #fef08a, #facc15 40%, #d97706 100%);
                color: #0b1220; font-weight: 900; font-size: 22px;
                box-shadow: 0 0 30px rgba(250,204,21,0.8);
            }}
            
            .head {{ text-align: center; margin-bottom: 20px; }}
            .title {{
                font-size: 30px; font-weight: 900; margin: 0;
                background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            .subtitle {{ color: #94a3b8; font-size: 13px; margin-top: 4px; }}
            .student {{ font-size: 22px; color: #38bdf8; font-weight: 800; text-align: center; margin: 12px 0 2px; }}
            .dateline {{ text-align: center; color: #cbd5e1; font-size: 13px; margin-bottom: 18px; }}
            
            .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 14px; }}
            .mcard {{
                background: rgba(15,23,42,0.85); border: 2px solid #38bdf8;
                border-radius: 14px; padding: 12px 10px; text-align: center;
            }}
            .mlabel {{ color: #94a3b8; font-size: 12px; margin-bottom: 4px; }}
            .mvalue {{ font-size: 26px; font-weight: 900; line-height: 1.1; }}
            
            .ddi {{
                background: {ddi_bg}; border: 3px solid {ddi_color};
                border-radius: 14px; padding: 12px; text-align: center; margin-bottom: 12px;
            }}
            .ddi-v {{ font-size: 32px; font-weight: 900; color: {ddi_color}; }}
            .ddi-l {{ font-size: 14px; font-weight: 800; color: {ddi_color}; margin-top: 2px; }}
            .ddi-s {{ font-size: 10.5px; color: #64748b; margin-top: 4px; }}
            
            .rpg {{
                background: rgba(30,15,45,0.6); border: 2px solid #a78bfa;
                border-radius: 14px; padding: 12px; display: flex;
                justify-content: space-around; margin-bottom: 14px;
            }}
            .rpg-item {{ text-align: center; flex: 1; }}
            .rpg-l {{ color: #94a3b8; font-size: 11px; margin-bottom: 3px; }}
            .rpg-v {{ font-size: 17px; font-weight: 900; }}
            
            .foot {{
                text-align: center; border-top: 1px solid #38bdf8;
                padding-top: 12px; color: #38bdf8; font-size: 14px; font-weight: 800;
            }}
            .tg {{ color: #facc15; font-size: 13px; margin-top: 4px; font-weight: 700; }}
            
            .dl-btn {{
                margin-top: 16px; padding: 12px 24px;
                background: linear-gradient(90deg, #0284c7, #7c3aed);
                border: none; color: #fff; font-family: Vazirmatn;
                font-weight: 800; border-radius: 12px; cursor: pointer;
                font-size: 15px; width: 520px;
                box-shadow: 0 6px 20px rgba(124,58,237,0.4);
            }}
            .dl-btn:hover {{ filter: brightness(1.15); }}
        </style>
    </head>
    <body>
        <div id="card-{card_id}">
            <div class="badge-20">20</div>
            <div class="head">
                <h1 class="title">👑 آکادمی ۲۰</h1>
                <div class="subtitle">کارنامه عملکرد روزانه</div>
            </div>
            <div class="student">{name}</div>
            <div class="dateline">📅 {date_str}</div>
            
            <div class="grid">
                <div class="mcard" style="border-color:#38bdf8;">
                    <div class="mlabel">⏳ ساعت مطالعه</div>
                    <div class="mvalue" style="color:#38bdf8;">{study_hours}</div>
                </div>
                <div class="mcard" style="border-color:#4ade80;">
                    <div class="mlabel">📝 تعداد تست</div>
                    <div class="mvalue" style="color:#4ade80;">{total_tests}</div>
                </div>
                <div class="mcard" style="border-color:#facc15;">
                    <div class="mlabel">🎯 درصد خالص</div>
                    <div class="mvalue" style="color:#facc15;">{percentage}%</div>
                </div>
                <div class="mcard" style="border-color:#f472b6;">
                    <div class="mlabel">⭐ رضایت</div>
                    <div class="mvalue" style="color:#f472b6;">{satisfaction}/10</div>
                </div>
            </div>
            
            <div class="ddi">
                <div class="ddi-v">{ddi_val}%</div>
                <div class="ddi-l">{ddi_label}</div>
                <div class="ddi-s">شاخص تخلیه تمرکز (DDI)</div>
            </div>
            
            <div class="rpg">
                <div class="rpg-item">
                    <div class="rpg-l">🎮 سطح</div>
                    <div class="rpg-v" style="color:#facc15;">{level_name}</div>
                </div>
                <div class="rpg-item">
                    <div class="rpg-l">⚡ XP</div>
                    <div class="rpg-v" style="color:#38bdf8;">{xp:,}</div>
                </div>
                <div class="rpg-item">
                    <div class="rpg-l">🔥 زنجیره</div>
                    <div class="rpg-v" style="color:#fb923c;">{streak} روز</div>
                </div>
            </div>
            
            <div class="foot">
                مشاور: دکتر خشایار اشکبوس
                <div class="tg">📱 @Kh_Ashkboos</div>
            </div>
        </div>
        
        <button class="dl-btn" onclick="dl_{card_id}()">📥 دانلود کارنامه PNG</button>
        
        <script>
            function dl_{card_id}() {{
                const card = document.getElementById('card-{card_id}');
                html2canvas(card, {{ backgroundColor: '#0b1220', scale: 2, useCORS: true, allowTaint: true }})
                .then(canvas => {{
                    const link = document.createElement('a');
                    link.download = 'academy20_{date_str}.png';
                    link.href = canvas.toDataURL('image/png');
                    link.click();
                }});
            }}
        </script>
    </body>
    </html>
    """
    return html


def render_html_story_card(name, date_str, study_hours, total_tests, percentage,
                            ddi_val, ddi_lvl, level_name, xp_today, streak,
                            badges_list, story_id="story1"):
    """کارنامه استوری 1080×1920 با html2canvas"""
    ddi_color = {"green":"#4ade80","yellow":"#facc15","red":"#f87171"}[ddi_lvl]
    ddi_label = {"green":"💎 مغز الماسی","yellow":"⚠️ افت دوپامین","red":"🔥 تمرکز بحرانی"}[ddi_lvl]
    
    badges_html = ""
    if badges_list:
        items = "".join([f'<span style="background:linear-gradient(90deg,#facc15,#f472b6); color:#0b1220; padding:6px 12px; border-radius:8px; margin:3px; font-weight:800; font-size:16px; display:inline-block;">{BADGES[b][0]} {BADGES[b][1]}</span>' for b in badges_list[:3]])
        badges_html = f'<div style="background:rgba(30,20,10,0.7); border:2px solid #facc15; border-radius:16px; padding:20px; margin-top:20px; text-align:center;">' \
                      f'<div style="color:#facc15; font-weight:900; font-size:22px; margin-bottom:10px;">🏆 مدال‌های امشب</div>{items}</div>'
    
    html = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
        <meta charset="UTF-8">
        <link href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css" rel="stylesheet">
        <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
        <style>
            * {{ box-sizing: border-box; font-family: Vazirmatn, sans-serif; }}
            body {{ margin:0; padding:20px; background:#05070f; display:flex; flex-direction:column; align-items:center; }}
            
            #story-{story_id} {{
                width: 405px; height: 720px; padding: 30px 24px;
                background: radial-gradient(circle at 30% 10%, #1e2447 0%, #0b0f19 50%, #05070f 100%);
                border: 3px solid #38bdf8; border-radius: 20px;
                color: #fff; position: relative; overflow: hidden;
                display: flex; flex-direction: column;
            }}
            #story-{story_id}::before {{
                content:''; position:absolute; inset:5px; border-radius:14px; padding:2px;
                background: linear-gradient(135deg,#38bdf8,#a78bfa,#f472b6,#facc15,#38bdf8);
                background-size: 300% 100%; animation: shift 8s linear infinite;
                -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
                -webkit-mask-composite: xor; mask-composite: exclude; pointer-events: none;
            }}
            @keyframes shift {{ 0%{{background-position:0% 50%}} 100%{{background-position:200% 50%}} }}
            
            .badge-20 {{
                position: absolute; top: 20px; left: 20px; width: 52px; height: 52px;
                border-radius: 50%; display:flex; align-items:center; justify-content:center;
                background: radial-gradient(circle at 30% 30%, #fef08a, #facc15 40%, #d97706 100%);
                color: #0b1220; font-weight: 900; font-size: 18px;
                box-shadow: 0 0 20px rgba(250,204,21,0.8);
            }}
            
            .title {{ font-size: 32px; font-weight: 900; text-align: center; margin: 10px 0 4px;
                background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
            .subtitle {{ text-align: center; color: #94a3b8; font-size: 13px; margin-bottom: 16px; }}
            .student {{ text-align: center; font-size: 22px; font-weight: 900; color: #38bdf8; margin-bottom: 2px; }}
            .date {{ text-align: center; color: #cbd5e1; font-size: 13px; margin-bottom: 18px; }}
            
            .mcard {{ background: rgba(15,23,42,0.9); border: 2px solid #38bdf8;
                border-radius: 12px; padding: 14px; margin-bottom: 8px; display:flex;
                justify-content: space-between; align-items: center; }}
            .mcard-l {{ color: #94a3b8; font-size: 14px; }}
            .mcard-v {{ font-size: 22px; font-weight: 900; }}
            
            .ddi {{ background: rgba(15,20,15,0.6); border: 3px solid {ddi_color};
                border-radius: 12px; padding: 12px; text-align: center; margin: 10px 0; }}
            .ddi-v {{ font-size: 26px; font-weight: 900; color: {ddi_color}; }}
            .ddi-l {{ font-size: 13px; font-weight: 800; color: {ddi_color}; }}
            
            .rpg {{ background: rgba(30,15,45,0.6); border: 2px solid #a78bfa;
                border-radius: 12px; padding: 10px; display: flex; justify-content: space-around; margin-top: 10px; }}
            .rpg-item {{ text-align: center; }}
            .rpg-l {{ color: #94a3b8; font-size: 11px; }}
            .rpg-v {{ font-size: 16px; font-weight: 900; }}
            
            .foot {{ margin-top: auto; text-align: center; padding-top: 14px; border-top: 1px solid #38bdf8; }}
            .foot-t {{ color: #38bdf8; font-size: 15px; font-weight: 800; }}
            .foot-tg {{ color: #facc15; font-size: 18px; font-weight: 900; margin-top: 4px; }}
            .foot-s {{ color: #64748b; font-size: 11px; margin-top: 4px; }}
            
            .dl-btn {{ margin-top: 16px; padding: 12px 24px;
                background: linear-gradient(90deg, #f09433, #dc2743, #bc1888);
                border: none; color: #fff; font-family: Vazirmatn; font-weight: 800;
                border-radius: 12px; cursor: pointer; font-size: 15px; width: 405px; }}
        </style>
    </head>
    <body>
        <div id="story-{story_id}">
            <div class="badge-20">20</div>
            <div class="title">👑 آکادمی ۲۰</div>
            <div class="subtitle">کارنامه استوری کنکوری</div>
            <div class="student">{name}</div>
            <div class="date">📅 {date_str}</div>
            
            <div class="mcard" style="border-color:#38bdf8;">
                <span class="mcard-l">⏳ ساعت مطالعه</span>
                <span class="mcard-v" style="color:#38bdf8;">{study_hours}</span>
            </div>
            <div class="mcard" style="border-color:#4ade80;">
                <span class="mcard-l">📝 تعداد تست</span>
                <span class="mcard-v" style="color:#4ade80;">{total_tests}</span>
            </div>
            <div class="mcard" style="border-color:#facc15;">
                <span class="mcard-l">🎯 درصد خالص</span>
                <span class="mcard-v" style="color:#facc15;">{percentage}%</span>
            </div>
            
            <div class="ddi">
                <div class="ddi-v">{ddi_val}%</div>
                <div class="ddi-l">{ddi_label}</div>
            </div>
            
            <div class="rpg">
                <div class="rpg-item"><div class="rpg-l">🎮 سطح</div>
                    <div class="rpg-v" style="color:#facc15;">{level_name}</div></div>
                <div class="rpg-item"><div class="rpg-l">⚡ XP</div>
                    <div class="rpg-v" style="color:#38bdf8;">+{xp_today:,}</div></div>
                <div class="rpg-item"><div class="rpg-l">🔥 زنجیره</div>
                    <div class="rpg-v" style="color:#fb923c;">{streak} روز</div></div>
            </div>
            
            {badges_html}
            
            <div class="foot">
                <div class="foot-t">مشاور: دکتر خشایار اشکبوس</div>
                <div class="foot-tg">@Kh_Ashkboos</div>
                <div class="foot-s">با آکادمی ۲۰، کنکور رو فتح کن!</div>
            </div>
        </div>
        
        <button class="dl-btn" onclick="dl_{story_id}()">📥 دانلود استوری (۱۰۸۰×۱۹۲۰)</button>
        
        <script>
            function dl_{story_id}() {{
                html2canvas(document.getElementById('story-{story_id}'), {{
                    backgroundColor: '#05070f', scale: 2.667, useCORS: true, allowTaint: true
                }}).then(canvas => {{
                    const link = document.createElement('a');
                    link.download = 'story_{date_str}.png';
                    link.href = canvas.toDataURL('image/png');
                    link.click();
                }});
            }}
        </script>
    </body>
    </html>
    """
    return html


# ═══════════════════════════════════════════════════════
# ۸. Pomodoro
# ═══════════════════════════════════════════════════════
if 'pomo' not in st.session_state:
    st.session_state.pomo = {'running': False, 'end_time': None, 'duration': 25*60, 'last_remaining': 25*60}

try:
    @st.fragment(run_every=1.0)
    def render_timer_fragment():
        p = st.session_state.pomo
        if p['running'] and p['end_time']:
            rem = int((p['end_time'] - datetime.datetime.now()).total_seconds())
            if rem <= 0:
                p['running'] = False; rem = 0; p['last_remaining'] = 0
                st.toast("⏰ زمان تمام شد!", icon="🔔")
            else: p['last_remaining'] = rem
        else: rem = p.get('last_remaining', p.get('duration', 25*60))
        m, s = divmod(max(0, rem), 60)
        status = "🔥 در حال اجرا..." if p['running'] else "⏸️ آماده شروع"
        st.markdown(f'<div class="pomodoro-box"><div class="pomo-time">{m:02d}:{s:02d}</div>'
                    f'<div class="pomo-label">{status}</div></div>', unsafe_allow_html=True)
    HAS_FRAG = True
except Exception:
    HAS_FRAG = False

def render_pomodoro():
    col1, col2 = st.columns([2, 1])
    with col1:
        mode = st.radio("حالت", ["🎯 تمرکز (۲۵ دقیقه)", "☕ استراحت (۵ دقیقه)", "⚡ تست سرعتی (۱۰ دقیقه)"],
                        key="pomo_mode", horizontal=True)
    with col2:
        cm = st.number_input("یا دقیقه دلخواه:", 1, 120, 25, key="pomo_cm")
    durs = {"🎯 تمرکز (۲۵ دقیقه)":25*60, "☕ استراحت (۵ دقیقه)":5*60, "⚡ تست سرعتی (۱۰ دقیقه)":10*60}
    sel = durs.get(mode, cm*60)
    st.session_state.pomo['duration'] = sel
    if HAS_FRAG: render_timer_fragment()
    else:
        p = st.session_state.pomo
        rem = (max(0, int((p['end_time']-datetime.datetime.now()).total_seconds()))
               if p['running'] and p['end_time'] else p.get('last_remaining', sel))
        m, s = divmod(rem, 60)
        st.markdown(f'<div class="pomodoro-box"><div class="pomo-time">{m:02d}:{s:02d}</div>'
                    f'<div class="pomo-label">{"🔥 در حال اجرا" if p["running"] else "⏸️ آماده"}</div></div>',
                    unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    if b1.button("▶️ شروع / ادامه", use_container_width=True, key="pomo_s"):
        if not st.session_state.pomo['running']:
            rem = st.session_state.pomo.get('last_remaining', sel)
            if rem <= 0: rem = sel
            st.session_state.pomo['running'] = True
            st.session_state.pomo['end_time'] = datetime.datetime.now() + datetime.timedelta(seconds=rem)
            st.rerun()
    if b2.button("⏸️ توقف", use_container_width=True, key="pomo_p"):
        if st.session_state.pomo['running'] and st.session_state.pomo['end_time']:
            rem = int((st.session_state.pomo['end_time'] - datetime.datetime.now()).total_seconds())
            st.session_state.pomo['last_remaining'] = max(0, rem)
            st.session_state.pomo['running'] = False; st.session_state.pomo['end_time'] = None
            st.rerun()
    if b3.button("🔄 ریست", use_container_width=True, key="pomo_r"):
        st.session_state.pomo = {'running':False, 'end_time':None, 'duration':sel, 'last_remaining':sel}
        st.rerun()


# ═══════════════════════════════════════════════════════
# ۹. Session & Login
# ═══════════════════════════════════════════════════════
for k, v in [('logged_in', False), ('username', ''), ('name', '')]:
    if k not in st.session_state: st.session_state[k] = v

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
            r = c.fetchone()
            if r:
                st.session_state['logged_in'] = True
                st.session_state['username'] = u; st.session_state['name'] = r[0]
                st.rerun()
            else: st.error("❌ اطلاعات اشتباه")
    with tab_r:
        nm = st.text_input("نام و نام خانوادگی:")
        un = st.text_input("نام کاربری:")
        pn = st.text_input("رمز عبور:", type="password")
        if st.button("✨ ثبت‌نام", use_container_width=True):
            if nm and un and pn:
                try:
                    c.execute("INSERT INTO users VALUES (?,?,?)", (un, pn, nm)); conn.commit()
                    st.success("🎉 ثبت شد!")
                except Exception: st.error("⚠️ تکراری")
            else: st.warning("پر کن")
    st.stop()

# ═══════════════════════════════════════════════════════
# ۱۰. Dashboard
# ═══════════════════════════════════════════════════════
df_all = pd.read_sql_query("SELECT * FROM reports WHERE username=? ORDER BY report_date ASC",
                           conn, params=(st.session_state['username'],))
streak = compute_streak(df_all)
total_xp = calculate_xp(df_all)
cur_lvl, nxt_lvl, prog = get_level(total_xp)
motiv = random.choice(MOTIVATIONS)

st.markdown(f"""
<div class="hero-header">
    <div class="hero-title">داشبورد قهرمان | آکادمی ۲۰</div>
    <p class="hero-sub">🎯 {st.session_state['name']}</p>
</div>""", unsafe_allow_html=True)

nx_hint = (f"{nxt_lvl[0]-total_xp:,} XP تا {nxt_lvl[2]} {nxt_lvl[1]}" if nxt_lvl else "🔥 بالاترین سطح!")
nx_lbl = f"{nxt_lvl[0]:,}" if nxt_lvl else "∞"
st.markdown(f"""
<div class="xp-container">
    <div class="xp-header">
        <div class="level-badge"><span>{cur_lvl[2]}</span><span>سطح {cur_lvl[1]}</span></div>
        <div class="streak-badge">🔥 {streak} روز متوالی</div>
    </div>
    <div class="xp-info-row">
        <span class="xp-amount">⚡ {total_xp:,} XP</span>
        <span class="xp-next-hint">{nx_hint}</span>
    </div>
    <div class="xp-track"><div class="xp-fill" style="--target:{prog:.1f}%; width:{prog:.1f}%;"></div></div>
    <div class="xp-labels">
        <span>{cur_lvl[0]:,} XP</span>
        <span class="xp-pct">{prog:.1f}%</span>
        <span>{nx_lbl} XP</span>
    </div>
</div>""", unsafe_allow_html=True)

st.markdown(f"""
<div class="glass-card" style="display:flex; align-items:center; gap:14px;">
    <div style="font-size:28px;">💬</div>
    <div style="font-size:14px; color:#e2e8f0;">{motiv}</div>
</div>""", unsafe_allow_html=True)

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
    satisfaction = cd2.slider("⭐️ کیفیت (۱-۱۰):", 1, 10, 8)

    st.markdown("#### 📚 ریز پارت‌ها")
    num_slots = st.number_input("تعداد پارت‌ها:", 1, 12, 3, key="numparts")

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
            with ct1: st_t = creative_time_picker("ساعت شروع", f"st_{i}", 8, 0)
            with ct2: et_t = creative_time_picker("ساعت پایان", f"et_{i}", 9, 30)

            dur = (datetime.datetime.combine(datetime.date.today(), et_t) -
                   datetime.datetime.combine(datetime.date.today(), st_t)).total_seconds() / 60
            if dur <= 0: dur += 24*60
            total_minutes += dur

            st.markdown(f"""<div style="background:rgba(74,222,128,.12); border-right:3px solid #4ade80;
                padding:8px 12px; border-radius:8px; margin:8px 0; font-size:13px;">
                ⏱️ مدت: <b style="color:#4ade80;">{int(dur//60)} س {int(dur%60)} د</b></div>""",
                unsafe_allow_html=True)

            csrc1, csrc2 = st.columns(2)
            csrc1.text_input("منبع درسنامه", key=f"src_s_{i}")
            csrc2.text_input("منبع تست", key=f"src_t_{i}")

            st.caption("آمار تست:")
            tc1, tc2, tc3, tc4 = st.columns(4)
            c_val = tc1.number_input("صحیح", 0, value=0, key=f"c_{i}")
            w_val = tc2.number_input("غلط", 0, value=0, key=f"w_{i}")
            tc3.number_input("نزده", 0, value=0, key=f"u_{i}")
            tc4.number_input("شک‌دار", 0, value=0, key=f"d_{i}")

            err_tag = None
            if w_val > 0:
                st.markdown("##### 🎯 جعبه سیاه اشتباهات")
                err_tag = st.selectbox(f"علت غلط‌های {subj}:", ERROR_TAGS + ["ترکیبی/نامشخص"], key=f"err_{i}")

            st.text_input("توضیحات", key=f"nt_{i}")

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
        for e in error_data:
            c.execute('''INSERT INTO error_vault (report_id, username, report_date, subject, error_tag, count)
                        VALUES (?,?,?,?,?,?)''',
                      (rid, st.session_state['username'], rep_date, e['subject'], e['tag'], e['count']))
        conn.commit()

        rpt = {'total_tests':total_tests, 'study_hours':study_hours,
               'percentage':overall_perc, 'screen_time':screen_t, 'social_time':social_t}
        nb = check_badges(st.session_state['username'], rpt, parts_data)
        st.balloons()
        st.success(f"✅ ذخیره شد! (+{xp_today:,} XP)")
        if nb:
            bh = "".join([f'<span class="badge-ach unlocked" style="display:inline-block;">{BADGES[b][0]} {BADGES[b][1]}</span>' for b in nb])
            st.markdown(f'<div class="glass-card" style="border-color:#facc15;">'
                        f'<h3 style="color:#facc15 !important;">🎉 مدال جدید!</h3>{bh}</div>',
                        unsafe_allow_html=True)
        st.session_state['last_report'] = {
            'date': str(rep_date), 'satisfaction': satisfaction, 'hours': study_hours,
            'tests': total_tests, 'perc': overall_perc, 'screen': screen_t,
            'ddi': ddi_val, 'ddi_lvl': ddi_lvl, 'xp_today': xp_today,
            'new_badges': nb,
        }

    st.markdown("---")
    st.markdown("#### 🖼️ کارنامه‌های تصویری (HTML — فارسی کاملاً سالم)")

    co1, co2 = st.columns(2)
    with co1:
        st.caption("📄 کارنامه عادی")
        card_html = render_html_report_card(
            st.session_state['name'], str(rep_date), satisfaction, study_hours,
            total_tests, overall_perc, screen_t, ddi_val, ddi_lvl,
            cur_lvl[1], total_xp + xp_today, streak, card_id="r1"
        )
        components.html(card_html, height=800, scrolling=False)
    with co2:
        st.caption("📱 کارنامه استوری (اینستاگرام/تلگرام)")
        story_html = render_html_story_card(
            st.session_state['name'], str(rep_date), study_hours, total_tests,
            overall_perc, ddi_val, ddi_lvl, cur_lvl[1], xp_today, streak,
            st.session_state.get('last_report', {}).get('new_badges', []),
            story_id="s1"
        )
        components.html(story_html, height=900, scrolling=True)

    # متن تلگرام
    report_text = f"""📊 گزارش کار | آکادمی ۲۰
👤 {st.session_state['name']}
🎮 سطح: {cur_lvl[1]} | ⚡ +{xp_today:,} XP
📅 {rep_date} | ⭐ {satisfaction}/10
⏳ مطالعه: {study_hours} ساعت
📝 تست: {total_tests} (✅ {total_c} | ❌ {total_w})
🎯 درصد: {overall_perc}%
📱 اسکرین: {screen_t} | 💎 DDI: {ddi_val}%
━━━━━━━━━━━━━━━━━━━━
🔥 زنجیره: {streak} روز
👨‍🏫 دکتر خشایار اشکبوس | @Kh_Ashkboos"""
    tg = "https://t.me/share/url?url=" + urllib.parse.quote(report_text)
    st.markdown(f'<a href="{tg}" target="_blank" class="tg-button">🚀 ارسال متن به تلگرام</a>',
                unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# TAB 2 — Pomodoro
# ═══════════════════════════════════════════════════════
with t2:
    st.markdown("### 🍅 تایمر پومودورو")
    render_pomodoro()

# ═══════════════════════════════════════════════════════
# TAB 3 — Rank Predictor
# ═══════════════════════════════════════════════════════
with t3:
    st.markdown("### 🔮 شبیه‌ساز تراز و تخمین رتبه زنده")
    if df_all.empty:
        st.info("⚠️ حداقل یک گزارش ثبت کن.")
    else:
        df30 = df_all[pd.to_datetime(df_all['report_date']) >=
                      pd.Timestamp(datetime.date.today() - datetime.timedelta(days=30))]
        if df30.empty: df30 = df_all
        ah = df30['study_hours'].mean(); at = df30['total_tests'].mean(); ap = df30['percentage'].mean()
        traz, rlo, rmid, rhi, comp = predict_rank(ah, at, ap)
        tier, tcol = rank_tier(rmid)
        cA, cB = st.columns(2)
        with cA:
            st.markdown(f"""<div class="rank-card" style="text-align:center;">
                <div style="font-size:13px; color:#94a3b8;">بازه احتمالی رتبه (۳۰ روز اخیر)</div>
                <div class="rank-number" style="margin:14px 0;">{rlo:,} تا {rhi:,}</div>
                <div class="rank-label">مرکز تخمین: <b style="color:#38bdf8;">{rmid:,}</b></div>
                <div style="margin-top:14px; font-size:18px; font-weight:900; color:{tcol};">{tier}</div>
            </div>""", unsafe_allow_html=True)
        with cB:
            st.markdown(f"""<div class="rank-card" style="text-align:center; border-color:rgba(56,189,248,.4);">
                <div style="font-size:13px; color:#94a3b8;">تراز تخمینی</div>
                <div class="rank-number" style="margin:14px 0;">{traz:,}</div>
                <div class="rank-label">از ۱۰,۰۰۰</div>
                <div style="margin-top:14px; font-size:13px; color:#94a3b8;">امتیاز ترکیبی: <b style="color:#facc15;">{comp*100:.1f}%</b></div>
            </div>""", unsafe_allow_html=True)

        st.markdown("#### 🎮 شبیه‌سازی «چی می‌شه اگر...»")
        scen = []
        for dh, dt, dp, lbl in [(0,0,0,"📍 فعلی"),(0.5,10,2,"📈 کمی بهتر"),(1.0,20,5,"🚀 جدی‌تر"),
                                 (1.5,35,8,"🔥 حرفه‌ای"),(2.0,50,12,"💎 المپیک")]:
            nh = min(ah+dh,14); nt = min(at+dt,250); np_ = min(ap+dp,100)
            _, rl2, rm2, rh2, _ = predict_rank(nh, nt, np_)
            scen.append({'سناریو':lbl,'ساعت':round(nh,1),'تست':int(nt),'درصد':round(np_,1),
                         'رتبه تخمینی':f"{rl2:,} - {rh2:,}",'تفاوت':f"{rmid-rm2:+,}" if rm2!=rmid else "—"})
        st.dataframe(pd.DataFrame(scen), use_container_width=True, hide_index=True)

        fig_w = go.Figure()
        for i, sc in enumerate(scen):
            _, rl2, rm2, rh2, _ = predict_rank(sc['ساعت'], sc['تست'], sc['درصد'])
            color = "#38bdf8" if i==0 else "#4ade80" if rm2 < rmid else "#f87171"
            fig_w.add_trace(go.Bar(x=[sc['سناریو']], y=[rm2], name=sc['سناریو'],
                marker_color=color, text=[f"{rm2:,}"], textposition='outside',
                error_y=dict(type='data', symmetric=False, array=[rh2-rm2], arrayminus=[rm2-rl2],
                             color=color, thickness=1.5, width=8), showlegend=False))
        fig_w.update_layout(title="تخمین رتبه در سناریوها (کمتر = بهتر)",
            template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font={'family':'Vazirmatn'}, yaxis_title="رتبه تخمینی", height=420)
        st.plotly_chart(fig_w, use_container_width=True)

        st.markdown("#### 📉 روند رتبه تخمینی روز به روز")
        dfs = df_all.sort_values('report_date').copy()
        dfs['date'] = pd.to_datetime(dfs['report_date'])
        dfs['predicted_rank'] = [predict_rank(r['study_hours'], r['total_tests'], r['percentage'])[2]
                                  for _, r in dfs.iterrows()]
        ft = px.line(dfs, x='date', y='predicted_rank', title="تغییرات رتبه در طول زمان",
                     labels={'predicted_rank':'رتبه','date':'تاریخ'}, markers=True,
                     color_discrete_sequence=['#a78bfa'])
        ft.update_traces(line=dict(width=3), marker=dict(size=10, line=dict(width=2, color='#0b0f19')))
        ft.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)',
                         paper_bgcolor='rgba(0,0,0,0)', font={'family':'Vazirmatn'},
                         yaxis_autorange="reversed")
        st.plotly_chart(ft, use_container_width=True)

# ═══════════════════════════════════════════════════════
# TAB 4 — Arena
# ═══════════════════════════════════════════════════════
with t4:
    st.markdown("### ⚔️ اتاق جنگ — دو﻿ئل دوستانه")
    my = pd.read_sql_query(
        "SELECT r.code, r.name, m.nickname FROM arena_rooms r "
        "JOIN arena_members m ON r.code=m.code WHERE m.username=?",
        conn, params=(st.session_state['username'],))
    a1, a2 = st.columns(2)
    with a1:
        st.markdown("##### 🏗️ ساخت اتاق")
        nn = st.text_input("اسم اتاق:", key="rn")
        nk = st.text_input("اسم مستعار:", key="rnk")
        if st.button("✨ ساخت", use_container_width=True):
            if nn and nk:
                code = f"{random.randint(1000,9999)}-{random.choice('ABCDEFGH')}{random.choice('ABCDEFGH')}"
                try:
                    c.execute("INSERT INTO arena_rooms VALUES (?,?,?,?)",
                              (code, nn, st.session_state['username'], datetime.datetime.now()))
                    c.execute("INSERT INTO arena_members VALUES (?,?,?,?)",
                              (code, st.session_state['username'], nk, datetime.datetime.now()))
                    conn.commit(); st.success(f"🎉 کد دعوت: `{code}`"); st.rerun()
                except Exception as e: st.error(f"خطا: {e}")
            else: st.warning("پر کن")
    with a2:
        st.markdown("##### 🎟️ پیوستن")
        jc = st.text_input("کد اتاق:", key="jc").strip()
        jn = st.text_input("اسم مستعار:", key="jn")
        if st.button("🚀 پیوستن", use_container_width=True):
            if jc and jn:
                c.execute("SELECT name FROM arena_rooms WHERE code=?", (jc,))
                r = c.fetchone()
                if not r: st.error("❌ پیدا نشد")
                else:
                    try:
                        c.execute("INSERT INTO arena_members VALUES (?,?,?,?)",
                                  (jc, st.session_state['username'], jn, datetime.datetime.now()))
                        conn.commit(); st.success(f"🎉 به «{r[0]}» پیوستی!"); st.rerun()
                    except Exception: st.info("ℹ️ قبلاً عضو بودی")

    st.markdown("---")
    if my.empty: st.info("💡 هنوز توی اتاقی نیستی")
    else:
        opts = [f"{r['name']} ({r['code']})" for _, r in my.iterrows()]
        sel = st.selectbox("🏠 اتاق‌های تو:", opts)
        sc = sel.split("(")[-1].rstrip(")")
        lb = arena_leaderboard(sc)
        if lb.empty: st.info("خالی")
        else:
            st.markdown(f"#### 🏆 لیدربورد ۷ روز — {sel}")
            icons = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
            for idx, row in lb.iterrows():
                ic = icons[idx-1] if idx <= 10 else f"{idx}."
                mc = "arena-me" if row['is_me'] else ""
                mb = " <span style='color:#38bdf8; font-size:11px;'>(تو)</span>" if row['is_me'] else ""
                st.markdown(f"""<div class="arena-card {mc}">
                    <div class="arena-rank">{ic}</div>
                    <div style="flex:1;">
                        <div style="font-weight:800; font-size:15px;">{row['nickname']}{mb}</div>
                        <div style="font-size:12px; color:#94a3b8;">⏳ {row['hours']} س &nbsp;•&nbsp; 📝 {row['tests']} تست</div>
                    </div>
                    <div style="font-size:18px; font-weight:900; color:#facc15;">
                        {row['score']:,} <span style="font-size:11px; color:#94a3b8;">XP</span>
                    </div>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# TAB 5 — Analysis
# ═══════════════════════════════════════════════════════
with t5:
    st.markdown("### 📈 داشبورد تحلیل هوشمند")
    if df_all.empty: st.info("⚠️ گزارشی نیست")
    else:
        df_all['report_date'] = pd.to_datetime(df_all['report_date'])
        cf, _ = st.columns([1, 2])
        tf_ = cf.radio("بازه:", ["۷ روز", "۳۰ روز", "همه"], horizontal=True)
        if "۷" in tf_: fdf = df_all[df_all['report_date'] >= pd.Timestamp(datetime.date.today() - datetime.timedelta(days=7))]
        elif "۳۰" in tf_: fdf = df_all[df_all['report_date'] >= pd.Timestamp(datetime.date.today() - datetime.timedelta(days=30))]
        else: fdf = df_all

        if not fdf.empty:
            sh = fdf['study_hours'].sum(); stt = fdf['total_tests'].sum()
            ap = fdf['percentage'].mean(); asat = fdf['satisfaction'].mean()
            pXP = int(sh*50 + stt*2)
            st.markdown(f"""<div style="display:grid; grid-template-columns: repeat(5, 1fr); gap:10px; margin-bottom:22px;">
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

            st.markdown("#### 🤖 تحلیلگر AI Coach")
            tips = ai_coach_analysis(fdf, df_all.iloc[-1].to_dict())
            th = "".join([f'<div class="ai-tip {cc}">{tt}</div>' for cc, tt in tips])
            st.markdown(f'<div class="ai-coach">{th}</div>', unsafe_allow_html=True)

            st.markdown("#### 🎯 جعبه سیاه اشتباهات")
            ev = pd.read_sql_query("SELECT subject, error_tag, SUM(count) as cnt FROM error_vault "
                                    "WHERE username=? GROUP BY subject, error_tag",
                                    conn, params=(st.session_state['username'],))
            if ev.empty:
                st.info("💡 تا حالا اشتباهی تگ نکردی")
            else:
                e1, e2 = st.columns(2)
                with e1:
                    fe = px.pie(ev, names='error_tag', values='cnt', hole=.5,
                                title="📊 توزیع کل علل غلط‌ها",
                                color_discrete_sequence=px.colors.qualitative.Bold)
                    fe.update_traces(textposition='inside', textinfo='percent+label')
                    fe.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)',
                                     font={'family':'Vazirmatn'}, height=420)
                    st.plotly_chart(fe, use_container_width=True)
                with e2:
                    fe2 = px.bar(ev, x='subject', y='cnt', color='error_tag',
                                 title="🎓 تفکیک بر اساس درس",
                                 color_discrete_sequence=px.colors.qualitative.Bold)
                    fe2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)',
                                      plot_bgcolor='rgba(0,0,0,0)', font={'family':'Vazirmatn'},
                                      height=420, barmode='stack')
                    st.plotly_chart(fe2, use_container_width=True)

            st.markdown("#### 💎 روند DDI")
            drows = [{'date': r['report_date'], **dict(zip(['ddi','level'], compute_ddi(r['study_hours'], r['social_time'])))}
                     for _, r in fdf.iterrows()]
            if drows:
                ddf = pd.DataFrame(drows)
                cm = {'green':'#4ade80','yellow':'#facc15','red':'#f87171'}
                fd = go.Figure()
                for lv, cc in cm.items():
                    s = ddf[ddf['level']==lv]
                    if not s.empty:
                        fd.add_trace(go.Scatter(x=s['date'], y=s['ddi'], mode='markers',
                            name=lv, marker=dict(color=cc, size=14, line=dict(width=2, color='#0b0f19'))))
                fd.add_hline(y=10, line_dash="dash", line_color="#4ade80", annotation_text="سبز (۱۰٪)")
                fd.add_hline(y=25, line_dash="dash", line_color="#f87171", annotation_text="قرمز (۲۵٪)")
                fd.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)',
                                 paper_bgcolor='rgba(0,0,0,0)', font={'family':'Vazirmatn'},
                                 title="روند DDI — پایین‌تر = بهتر", yaxis_title="DDI (%)")
                st.plotly_chart(fd, use_container_width=True)

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
                gg.update_layout(template="plotly_dark", height=280, plot_bgcolor='rgba(0,0,0,0)',
                                 paper_bgcolor='rgba(0,0,0,0)', font={'family':'Vazirmatn'})
                st.plotly_chart(gg, use_container_width=True)
            with g2:
                fh = px.bar(fdf, x='report_date', y='study_hours', title=f"⏳ ساعت مطالعه ({tf_})",
                            color='study_hours', color_continuous_scale=['#0ea5e9','#7c3aed','#f472b6'])
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
    st.markdown(f"""<div class="glass-card" style="text-align:center;">
        <div style="font-size:14px; color:#94a3b8;">پیشرفت مدال‌ها</div>
        <div style="font-size:32px; font-weight:900; color:#facc15; margin:8px 0;">{uc} / {tb}</div>
        <div class="xp-track" style="height:14px;">
            <div class="xp-fill" style="--target:{pct:.0f}%; width:{pct:.0f}%;"></div>
        </div>
    </div>""", unsafe_allow_html=True)
    cols = st.columns(4)
    for idx, (bid, (ic, nm, dsc)) in enumerate(BADGES.items()):
        unl = bid in um
        cls = "unlocked" if unl else "locked"
        du = ""
        if unl:
            try:
                dt = pd.to_datetime(um[bid])
                du = f"<div style='font-size:10px; color:#94a3b8; margin-top:6px;'>{dt.strftime('%Y/%m/%d')}</div>"
            except Exception: pass
        with cols[idx % 4]:
            st.markdown(f"""<div class="badge-ach {cls}">
                <div style="font-size:36px;">{ic}</div>
                <div style="font-size:14px; font-weight:900; margin-top:6px;">{nm}</div>
                <div style="font-size:11px; color:#94a3b8; margin-top:4px;">{dsc}</div>
                {du}</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# TAB 7 — Settings
# ═══════════════════════════════════════════════════════
with t7:
    st.markdown(f"""<div class="glass-card">
        <h3>👤 پروفایل</h3>
        <p>نام: <b style="color:#38bdf8;">{st.session_state['name']}</b></p>
        <p>نام کاربری: <code style="color:#38bdf8;">{st.session_state['username']}</code></p>
        <p>سطح: <span style="color:{cur_lvl[3]}; font-weight:900;">{cur_lvl[2]} {cur_lvl[1]}</span></p>
        <p>⚡ XP: <b style="color:#facc15;">{total_xp:,}</b></p>
        <p>🔥 زنجیره: <b style="color:#fb923c;">{streak} روز</b></p>
        <p>📊 گزارش‌ها: <b>{len(df_all)}</b></p>
    </div>""", unsafe_allow_html=True)
    if st.button("🚪 خروج", use_container_width=True):
        st.session_state['logged_in'] = False
        st.rerun()
