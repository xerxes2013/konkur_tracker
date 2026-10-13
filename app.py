# ═══════════════════════════════════════════════════════════════════
# 👑 آکادمی ۲۰ — سیستم کامل RPG کنکور
# نسخه نهایی | دکتر خشایار اشکبوس
# ═══════════════════════════════════════════════════════════════════

import streamlit as st
import streamlit.components.v1 as components
import datetime
import urllib.parse
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import re
import html as html_lib

# ═══════════════════════════════════════════════════════════════════
# ۱. تنظیمات صفحه
# ═══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="آکادمی ۲۰ | RPG کنکور",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════════
# ۲. استایل‌های پیشرفته
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');

* {
    font-family: 'Vazirmatn', sans-serif !important;
    direction: rtl;
    text-align: right;
}

/* ═══ انیمیشن‌ها ═══ */
@keyframes gradientShift { 0%{background-position:0% 50%} 100%{background-position:200% 50%} }
@keyframes pulseGlow {
    0%,100% { box-shadow: 0 0 20px rgba(56,189,248,0.35), 0 0 40px rgba(168,85,247,0.15); }
    50% { box-shadow: 0 0 45px rgba(56,189,248,0.85), 0 0 80px rgba(168,85,247,0.35); }
}
@keyframes fillBar { from{width:0%} to{width:var(--target,50%)} }
@keyframes popIn {
    0% { transform: scale(0.6) rotate(-5deg); opacity: 0; }
    60% { transform: scale(1.1) rotate(3deg); opacity: 1; }
    100% { transform: scale(1) rotate(0); }
}
@keyframes floatY {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(-6px); }
}
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
@keyframes rotate360 { to { transform: rotate(360deg); } }

/* ═══ پس‌زمینه ═══ */
.stApp {
    background:
        radial-gradient(circle at 10% 0%, #1e2447 0%, transparent 45%),
        radial-gradient(circle at 90% 100%, #2a1345 0%, transparent 50%),
        radial-gradient(circle at 50% 50%, #0d1424 0%, #05070f 100%) !important;
    color: #fff !important;
}
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background-image:
        radial-gradient(1.5px 1.5px at 20% 30%, rgba(56,189,248,0.5), transparent),
        radial-gradient(1.2px 1.2px at 65% 70%, rgba(74,222,128,0.4), transparent),
        radial-gradient(1.3px 1.3px at 82% 22%, rgba(250,204,21,0.4), transparent),
        radial-gradient(1px 1px at 15% 80%, rgba(244,114,182,0.4), transparent),
        radial-gradient(1.2px 1.2px at 88% 55%, rgba(168,85,247,0.4), transparent);
    background-size: 620px 620px, 480px 480px, 700px 700px, 350px 350px, 550px 550px;
    pointer-events: none; z-index: 0; opacity: 0.55;
    animation: floatY 12s ease-in-out infinite;
}

/* ═══ هدر ═══ */
.hero-header {
    position: relative;
    background: linear-gradient(135deg, rgba(17,24,39,0.85) 0%, rgba(30,41,59,0.75) 100%);
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border-radius: 24px;
    padding: 28px 24px;
    text-align: center;
    margin-bottom: 24px;
    border: 1px solid rgba(56,189,248,0.28);
    box-shadow: 0 20px 60px rgba(2,132,199,0.18), inset 0 1px 0 rgba(255,255,255,0.08);
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute; inset: -2px; border-radius: 24px; padding: 2px;
    background: linear-gradient(90deg, #38bdf8, #4ade80, #facc15, #f472b6, #a78bfa, #38bdf8);
    background-size: 400% 100%;
    animation: gradientShift 10s linear infinite;
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor; mask-composite: exclude;
    pointer-events: none;
}
.hero-title {
    font-size: 30px; font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6, #facc15);
    background-size: 300% 100%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0 0 8px 0;
    animation: gradientShift 6s linear infinite;
}
.hero-sub { color: #cbd5e1 !important; font-size: 14px; margin: 0; }

/* ═══ XP Panel ═══ */
.xp-container {
    background: linear-gradient(135deg, rgba(17,24,39,0.85), rgba(30,41,59,0.78));
    backdrop-filter: blur(16px);
    border: 1px solid rgba(250,204,21,0.35);
    border-radius: 20px;
    padding: 20px 24px;
    margin-bottom: 20px;
    box-shadow: 0 12px 40px rgba(250,204,21,0.12), inset 0 1px 0 rgba(255,255,255,0.05);
}
.xp-header {
    display: flex; justify-content: space-between; align-items: center;
    gap: 12px; margin-bottom: 14px; flex-wrap: wrap;
}
.level-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: linear-gradient(90deg, rgba(250,204,21,0.22), rgba(244,114,182,0.22));
    border: 2px solid #facc15; border-radius: 14px;
    padding: 9px 16px; font-weight: 900; font-size: 15px;
    color: #facc15 !important;
    animation: pulseGlow 3s ease-in-out infinite;
    white-space: nowrap;
}
.streak-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: linear-gradient(90deg, rgba(251,146,60,0.2), rgba(248,113,113,0.2));
    border: 1.5px solid rgba(251,146,60,0.65);
    padding: 9px 16px; border-radius: 14px;
    font-weight: 800; font-size: 14px;
    color: #fb923c !important;
    white-space: nowrap;
}
.xp-info-row {
    display: flex; justify-content: space-between; align-items: baseline;
    gap: 12px; margin-bottom: 10px; flex-wrap: wrap;
    font-size: 13px;
}
.xp-amount { color: #38bdf8 !important; font-weight: 900; font-size: 17px; }
.xp-next-hint { color: #94a3b8 !important; font-size: 12px; }
.xp-track {
    background: #05070f; border-radius: 999px; height: 22px;
    overflow: hidden; position: relative;
    border: 1px solid rgba(56,189,248,0.3);
    margin-bottom: 8px;
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.5);
}
.xp-fill {
    height: 100%;
    background: linear-gradient(90deg, #0284c7, #7c3aed, #f472b6, #facc15);
    background-size: 300% 100%;
    animation: fillBar 1.4s cubic-bezier(.2,.9,.3,1.1) forwards,
               gradientShift 4s linear infinite;
    border-radius: 999px;
    box-shadow: 0 0 24px rgba(250,204,21,0.6);
    position: relative;
}
.xp-fill::after {
    content: '';
    position: absolute; inset: 0; border-radius: 999px;
    background: linear-gradient(90deg, transparent 30%, rgba(255,255,255,0.35), transparent 70%);
    background-size: 200% 100%;
    animation: gradientShift 2.5s linear infinite;
}
.xp-labels {
    display: flex; justify-content: space-between; align-items: center;
    font-size: 11px; color: #64748b !important;
}
.xp-labels .xp-pct { color: #facc15 !important; font-weight: 900; font-size: 13px; }

/* ═══ کارت‌های متریک ═══ */
.metric-card {
    position: relative;
    background: linear-gradient(145deg, rgba(17,24,39,0.88), rgba(30,41,59,0.72));
    backdrop-filter: blur(12px);
    border: 1px solid rgba(56,189,248,0.28);
    border-radius: 18px;
    padding: 18px 12px;
    text-align: center;
    transition: all 0.35s cubic-bezier(.2,.9,.3,1.3);
    overflow: hidden;
    box-shadow: 0 8px 26px rgba(0,0,0,0.35);
}
.metric-card:hover {
    transform: translateY(-6px) scale(1.02);
    border-color: rgba(56,189,248,0.75);
    box-shadow: 0 16px 40px rgba(56,189,248,0.4);
}
.metric-card::after {
    content: ''; position: absolute;
    top: 0; left: -60%; width: 60%; height: 100%;
    background: linear-gradient(120deg, transparent, rgba(255,255,255,0.1), transparent);
    transition: 0.7s;
}
.metric-card:hover::after { left: 120%; }
.metric-num {
    font-size: 28px; font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #4ade80);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.metric-txt { font-size: 12px; color: #94a3b8 !important; margin-top: 6px; }
.metric-icon { font-size: 22px; display: block; margin-bottom: 4px; }

/* ═══ مدال‌ها ═══ */
.badge-ach {
    display: block; padding: 18px 12px; border-radius: 16px;
    font-weight: 800; font-size: 13px; margin: 5px 0;
    border: 2px solid; text-align: center;
    transition: all 0.35s cubic-bezier(.2,.9,.3,1.3);
    animation: popIn 0.6s ease;
}
.badge-ach.unlocked {
    color: #facc15; border-color: #facc15;
    background: linear-gradient(145deg, rgba(250,204,21,0.15), rgba(244,114,182,0.1));
    box-shadow: 0 0 24px rgba(250,204,21,0.4);
}
.badge-ach.unlocked:hover {
    transform: translateY(-6px) rotate(-3deg);
    box-shadow: 0 0 40px rgba(250,204,21,0.75);
}
.badge-ach.locked {
    color: #475569; border-color: #334155;
    background: rgba(15,23,42,0.65); opacity: 0.55;
}

/* ═══ AI Coach ═══ */
.ai-coach {
    background: linear-gradient(135deg, rgba(56,189,248,0.1), rgba(168,85,247,0.1));
    border: 1px solid rgba(56,189,248,0.4);
    border-radius: 18px; padding: 16px; margin: 12px 0;
    box-shadow: 0 8px 30px rgba(56,189,248,0.15);
}
.ai-tip {
    padding: 10px 14px; margin: 6px 0; border-radius: 12px;
    font-size: 13.5px; border-right: 4px solid;
    background: rgba(15,23,42,0.4);
}
.ai-tip.success { border-color: #4ade80; color: #86efac; }
.ai-tip.warning { border-color: #facc15; color: #fde047; }
.ai-tip.danger { border-color: #f87171; color: #fca5a5; }
.ai-tip.info { border-color: #38bdf8; color: #7dd3fc; }

/* ═══ پومودورو ═══ */
.pomodoro-box {
    background: linear-gradient(145deg, #0f172a, #1e293b);
    border: 2px solid #38bdf8; border-radius: 22px;
    padding: 28px; text-align: center;
    box-shadow: 0 0 40px rgba(56,189,248,0.35), inset 0 1px 0 rgba(255,255,255,0.05);
    margin: 16px 0;
}
.pomo-time {
    font-size: 72px; font-weight: 900;
    font-family: 'Courier New', monospace !important;
    background: linear-gradient(90deg, #38bdf8, #f472b6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 6px; line-height: 1;
}
.pomo-label { font-size: 13px; color: #94a3b8 !important; margin-top: 10px; font-weight: 700; }

/* ═══ DDI Panel ═══ */
.ddi-panel {
    border-radius: 18px; padding: 18px; margin: 12px 0;
    text-align: center; border: 3px solid;
}
.ddi-green { border-color: #4ade80; background: linear-gradient(135deg, rgba(74,222,128,0.15), rgba(56,189,248,0.08)); }
.ddi-yellow { border-color: #facc15; background: linear-gradient(135deg, rgba(250,204,21,0.15), rgba(251,146,60,0.08)); }
.ddi-red { border-color: #f87171; background: linear-gradient(135deg, rgba(248,113,113,0.2), rgba(220,38,38,0.15)); animation: pulseGlow 2s infinite; }
.ddi-value { font-size: 44px; font-weight: 900; letter-spacing: 3px; }
.ddi-label { font-size: 14px; margin-top: 6px; font-weight: 800; }

/* ═══ Rank Card ═══ */
.rank-card {
    background: linear-gradient(145deg, rgba(17,24,39,0.88), rgba(30,41,59,0.72));
    border: 2px solid rgba(168,85,247,0.4);
    border-radius: 20px; padding: 24px; margin-bottom: 16px;
    box-shadow: 0 12px 40px rgba(168,85,247,0.2);
}
.rank-number {
    font-size: 58px; font-weight: 900; letter-spacing: 3px;
    background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1;
}
.rank-label { font-size: 13px; color: #94a3b8 !important; margin-top: 8px; }

/* ═══ Arena Card ═══ */
.arena-card {
    background: linear-gradient(145deg, rgba(17,24,39,0.88), rgba(30,41,59,0.72));
    border: 1px solid rgba(250,204,21,0.35);
    border-radius: 16px; padding: 14px 18px;
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 10px; gap: 14px;
    transition: all 0.3s;
}
.arena-card:hover { transform: translateX(-4px); border-color: rgba(250,204,21,0.7); }
.arena-rank {
    font-size: 24px; font-weight: 900; min-width: 48px; text-align: center;
    background: linear-gradient(90deg, #facc15, #f472b6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.arena-me { border: 2px solid #38bdf8; box-shadow: 0 0 24px rgba(56,189,248,0.4); }

/* ═══ عمومی ═══ */
label, p, span, h1, h2, h3, h4, div {
    color: #fff !important; font-weight: 600;
}
input, textarea, select {
    background-color: rgba(30,41,59,0.85) !important;
    color: #fff !important;
    border: 1px solid rgba(56,189,248,0.35) !important;
    border-radius: 12px !important;
}
input:focus, textarea:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.18) !important;
}

.stButton > button {
    background: linear-gradient(90deg, #0284c7, #7c3aed) !important;
    color: #fff !important;
    border: none !important; border-radius: 12px !important;
    font-weight: 800 !important;
    padding: 10px 18px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.28) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.01);
    box-shadow: 0 12px 32px rgba(124,58,237,0.55) !important;
    filter: brightness(1.1);
}

.tg-button {
    display: block; width: 100%;
    background: linear-gradient(90deg, #0088cc, #005f8f);
    color: #fff !important; text-align: center;
    font-size: 16px; font-weight: 800;
    padding: 14px; border-radius: 12px;
    text-decoration: none; margin-top: 15px;
    box-shadow: 0 6px 18px rgba(2,132,199,0.45);
    transition: all 0.3s;
}
.tg-button:hover { transform: translateY(-3px); filter: brightness(1.1); }

.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: rgba(17,24,39,0.65);
    padding: 10px; border-radius: 16px;
    border: 1px solid rgba(56,189,248,0.2);
    flex-wrap: wrap;
    backdrop-filter: blur(12px);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 12px !important;
    padding: 11px 16px !important;
    font-weight: 700 !important;
    transition: 0.25s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #0284c7, #7c3aed) !important;
    color: #fff !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.4);
}

::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: #0b0f19; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #38bdf8, #7c3aed);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #38bdf8, #f472b6); }

.glass-card {
    background: rgba(17,24,39,0.72);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(56,189,248,0.22);
    border-radius: 18px; padding: 18px; margin-bottom: 14px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.28);
}

/* ═══ Dropdown Fix ═══ */
div[data-baseweb="select"] > div {
    background-color: #1e293b !important;
    color: #fff !important;
    border-color: rgba(56,189,248,0.35) !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] div,
div[data-baseweb="select"] input {
    color: #fff !important;
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
    color: #fff !important;
}
ul[role="listbox"] li:hover,
li[role="option"]:hover {
    background-color: #0284c7 !important;
}
li[aria-selected="true"] {
    background-color: #0369a1 !important;
    color: #fff !important;
    font-weight: 800 !important;
}
div[data-baseweb="calendar"],
div[data-baseweb="calendar"] * {
    background-color: #1e293b !important;
    color: #fff !important;
}

/* ═══ Time Picker Trigger ═══ */
.time-label {
    font-weight: 800; color: #38bdf8 !important;
    font-size: 14px; margin-bottom: 6px; display: block;
}
.time-preview {
    text-align: center;
    background: linear-gradient(90deg, #0284c7, #7c3aed);
    color: #fff !important; font-weight: 900; font-size: 24px;
    padding: 12px; border-radius: 12px; margin-top: 8px;
    letter-spacing: 3px;
    font-family: 'Courier New', monospace !important;
    box-shadow: 0 4px 20px rgba(2,132,199,0.5);
}

/* ═══ Dialog Modal (Time Picker) ═══ */
div[role="dialog"] {
    background: linear-gradient(145deg, #0f172a, #1a2340) !important;
    border: 2px solid #38bdf8 !important;
    border-radius: 20px !important;
    box-shadow: 0 0 60px rgba(56,189,248,0.4) !important;
}

/* ═══ Modal Clock Scroll ═══ */
.clock-scroll {
    max-height: 240px;
    overflow-y: auto;
    padding: 4px;
    border-radius: 12px;
    background: rgba(15,23,42,0.6);
    border: 1px solid rgba(56,189,248,0.25);
}

/* ═══ Hide Streamlit Menu ═══ */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# ۳. دیتابیس
# ═══════════════════════════════════════════════════════════════════
conn = sqlite3.connect("konkur_academy.db", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY, password TEXT, name TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, report_date DATE,
    satisfaction INT, study_hours REAL, total_tests INT, correct_tests INT,
    wrong_tests INT, percentage REAL, screen_time TEXT, social_time TEXT, details TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT, report_id INTEGER, username TEXT,
    report_date DATE, subject TEXT, minutes REAL, tests INT, correct INT, wrong INT)''')

c.execute('''CREATE TABLE IF NOT EXISTS user_badges (
    username TEXT, badge_id TEXT, unlocked_at TIMESTAMP,
    PRIMARY KEY (username, badge_id))''')

c.execute('''CREATE TABLE IF NOT EXISTS error_vault (
    id INTEGER PRIMARY KEY AUTOINCREMENT, report_id INTEGER, username TEXT,
    report_date DATE, subject TEXT, error_tag TEXT, count INT)''')

c.execute('''CREATE TABLE IF NOT EXISTS arena_rooms (
    code TEXT PRIMARY KEY, name TEXT, created_by TEXT, created_at TIMESTAMP)''')

c.execute('''CREATE TABLE IF NOT EXISTS arena_members (
    code TEXT, username TEXT, nickname TEXT, joined_at TIMESTAMP,
    PRIMARY KEY (code, username))''')

conn.commit()

# ═══════════════════════════════════════════════════════════════════
# ۴. ثابت‌ها
# ═══════════════════════════════════════════════════════════════════
MOTIVATIONS = [
    "🌟 هر تستی که می‌زنی، یک قدم به رویاهات نزدیک‌تر می‌شی.",
    "🔥 موفقیت حاصل تکرارهای کوچک روزانه است، نه یک‌شبه معجزه.",
    "🚀 امروزت رو بساز، چون فردا از همین امروزها ساخته می‌شه.",
    "💎 فشارِ امروز، الماسِ فردا رو می‌سازه.",
    "🎯 تمرکز روی پیشرفت، نه کمال. همین کافیه.",
    "⚡ تو از دیروز خودت قوی‌تری؛ همین کافیه برای ادامه.",
    "🌈 سختی‌های امروز، پله‌های افتخار فردا هستن.",
    "👑 کسی که هر روز تلاش می‌کنه، شکست نمی‌خوره؛ فقط یاد می‌گیره.",
    "🏆 رتبه‌های برتر، آدم‌های خاصی نیستن؛ عادت‌های خاص دارن.",
    "🔱 هر روزی که بی‌گزارش بگذره، یک روز از رقیبات عقب می‌افتی.",
]

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

BADGES = {
    "first_step":   ("🎯", "اولین قدم",        "اولین گزارش ثبت شد"),
    "hunter_100":   ("🏹", "شکارچی تست",       "۱۰۰+ تست در یک روز"),
    "hunter_200":   ("⚡", "تست‌زن افسانه‌ای",  "۲۰۰+ تست در یک روز"),
    "steel_focus":  ("🛡️", "تمرکز فولادین",    "زیر ۳۰ دقیقه گوشی"),
    "bio_marathon": ("🧬", "ماراتن زیست",      "۳+ ساعت زیست در یک روز"),
    "marathon_day": ("🏃", "ماراتن روزانه",    "۸+ ساعت مطالعه در یک روز"),
    "streak_7":     ("🔥", "هفت‌روز پیوسته",   "۷ روز متوالی"),
    "streak_30":    ("💫", "ماه کامل",         "۳۰ روز متوالی"),
    "early_bird":   ("🐓", "سحرخیز",           "شروع مطالعه قبل از ۶ صبح"),
    "night_owl":    ("🦉", "جغد شب",           "مطالعه بعد از ساعت ۲۳"),
    "perfect_day":  ("💯", "روز بی‌نقص",       "درصد تست ۱۰۰٪"),
    "consistent":   ("📊", "استمرار طلایی",    "۱۰ گزارش متوالی"),
    "ddi_diamond":  ("💎", "مغز الماسی",       "DDI زیر ۱۰٪"),
    "ddi_warrior":  ("🧠", "جنگجوی تمرکز",     "DDI زیر ۵٪"),
    "rank_hunter":  ("🎖️", "شکارچی رتبه",      "پیش‌بینی زیر ۱۰۰۰"),
    "night_king":   ("🌌", "پادشاه شب",        "۳ روز متوالی مطالعه بعد از نیمه‌شب"),
}

ERROR_TAGS = [
    "بی‌دقتی محاسباتی",
    "فراموشی فرمول",
    "دام طراح",
    "کمبود وقت",
    "عدم تسلط به مبحث",
    "اشتباه در خواندن سؤال",
]

# ═══════════════════════════════════════════════════════════════════
# ۵. توابع محاسباتی
# ═══════════════════════════════════════════════════════════════════
def compute_streak(df):
    if df.empty:
        return 0
    dates = sorted(set(pd.to_datetime(df['report_date']).dt.date), reverse=True)
    today = datetime.date.today()
    if dates[0] != today and dates[0] != today - datetime.timedelta(days=1):
        return 0
    check = dates[0]
    streak = 0
    for d in dates:
        if d == check:
            streak += 1
            check -= datetime.timedelta(days=1)
        elif d < check:
            break
    return streak


def calculate_xp(df):
    if df.empty:
        return 0
    return int(df['study_hours'].sum() * 50 + df['total_tests'].sum() * 2)


def get_level(xp):
    current = LEVELS[0]
    next_lvl = None
    idx = 0
    for i, lvl in enumerate(LEVELS):
        if xp >= lvl[0]:
            current = lvl
            idx = i
    if idx + 1 < len(LEVELS):
        next_lvl = LEVELS[idx + 1]
    if next_lvl:
        rng = next_lvl[0] - current[0]
        prog = min(100, max(0, ((xp - current[0]) / rng) * 100))
    else:
        prog = 100.0
    return current, next_lvl, prog


def parse_duration(text):
    text = str(text).strip()
    for i, d in enumerate("۰۱۲۳۴۵۶۷۸۹"):
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
    return int(float(nums[0])) if nums else 0


def compute_ddi(study_hours, social_time_str):
    social_min = parse_duration(social_time_str)
    study_min = study_hours * 60
    if study_min <= 0:
        return (100.0, "red") if social_min > 0 else (0.0, "green")
    ddi = (social_min / study_min) * 100
    return round(ddi, 1), ("green" if ddi < 10 else "yellow" if ddi < 25 else "red")


DDI_META = {
    "green":  ("💎", "مغز الماسی — تمرکز فولادین!", "#4ade80", "ddi-green"),
    "yellow": ("⚠️", "خطر افت دوپامین — مواظب باش!", "#facc15", "ddi-yellow"),
    "red":    ("🔥", "وضعیت بحرانی — تمرکز در حال سوختن!", "#f87171", "ddi-red"),
}


def ddi_badge_html(ddi, level):
    icon, lbl, color, cls = DDI_META[level]
    return f"""
    <div class="ddi-panel {cls}">
        <div class="ddi-value" style="color:{color};">{ddi}%</div>
        <div class="ddi-label" style="color:{color};">{icon} {lbl}</div>
        <div style="font-size:11px; color:#94a3b8; margin-top:6px;">
            شاخص تخلیه تمرکز (DDI) = (شبکه‌های اجتماعی ÷ مطالعه) × ۱۰۰
        </div>
    </div>"""


def predict_rank(avg_hours, avg_tests, avg_percent):
    h = min(max(avg_hours, 0), 14) / 14
    t = min(max(avg_tests, 0), 200) / 200
    p = min(max(avg_percent, 0), 100) / 100
    comp = h * 0.30 + t * 0.25 + p * 0.45
    traz = int(3000 + comp * 7000)
    rm = int(max(50, 250000 * ((1 - comp) ** 3.2)))
    rl = max(1, int(rm * 0.65))
    rh = int(rm * 1.55)
    return traz, rl, rm, rh, comp


def rank_tier(rank_mid):
    if rank_mid < 500:  return "🏆 منطقه المپیک", "#facc15"
    if rank_mid < 2000: return "🥇 منطقه طلایی", "#f472b6"
    if rank_mid < 5000: return "🥈 منطقه نقره‌ای", "#a78bfa"
    if rank_mid < 15000: return "🥉 منطقه برنزی", "#38bdf8"
    if rank_mid < 50000: return "💪 در حال رشد", "#4ade80"
    return "🌱 تازه شروع کردی", "#94a3b8"


def arena_leaderboard(code):
    mem = pd.read_sql_query(
        "SELECT username, nickname FROM arena_members WHERE code=?",
        conn, params=(code,))
    if mem.empty:
        return pd.DataFrame()
    cutoff = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
    rows = []
    for _, m in mem.iterrows():
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


def ai_coach_analysis(df, today_report=None):
    tips = []
    if df.empty:
        return [("info", "🤖 هنوز داده‌ای برای تحلیل نیست. اولین گزارش را ثبت کن!")]
    sh = df['study_hours'].sum()
    stt = df['total_tests'].sum()
    if sh > 0:
        sp = stt / sh
        if sp >= 60:
            tips.append(("success", f"🚀 سرعت تست‌زنی فوق‌العاده! ({sp:.0f} تست/ساعت)"))
        elif sp >= 35:
            tips.append(("success", f"👍 سرعت تست‌زنی خوب ({sp:.0f} تست/ساعت)"))
        elif sp >= 15:
            tips.append(("warning", f"⚙️ سرعت متوسط ({sp:.0f} تست/ساعت). تلاش کن ۴۰+ بشه"))
        else:
            tips.append(("danger", f"⚠️ سرعت پایین ({sp:.0f} تست/ساعت). روی تمرکز کار کن"))
    if today_report:
        ddi, dl = compute_ddi(today_report['study_hours'], today_report['social_time'])
        if dl == "red":
            tips.append(("danger", f"🔥 DDI {ddi}% — اسکرین‌تایم داری تمرکزت رو می‌خوره!"))
        elif dl == "yellow":
            tips.append(("warning", f"⚠️ DDI {ddi}% — تعادل دیجیتال رو بهتر کن"))
        else:
            tips.append(("success", f"💎 DDI {ddi}% — مغز الماسی!"))
    asat = df['satisfaction'].mean()
    if asat >= 8:
        tips.append(("success", f"😊 رضایتت {asat:.1f}/10 عالیه"))
    elif asat < 6:
        tips.append(("warning", f"💙 رضایتت {asat:.1f}/10 پایینه. به خودت استراحت بده"))
    if len(df) >= 3:
        recent = df.tail(3)['total_tests'].mean()
        older = df.head(max(1, len(df) - 3))['total_tests'].mean()
        if recent > older * 1.2:
            tips.append(("success", "📈 روند صعودی تست‌زنی"))
        elif recent < older * 0.8:
            tips.append(("warning", "📉 افت در تعداد تست‌ها"))
    return tips


def check_badges(username, report, parts_data):
    new_badges = []
    c.execute("SELECT badge_id FROM user_badges WHERE username=?", (username,))
    existing = {r[0] for r in c.fetchall()}
    dfu = pd.read_sql_query(
        "SELECT * FROM reports WHERE username=? ORDER BY report_date ASC",
        conn, params=(username,))
    total_reports = len(dfu)
    streak = compute_streak(dfu)
    tt = report['total_tests']
    sh = report['study_hours']
    pc = report['percentage']
    bio_m = sum(p['minutes'] for p in parts_data if 'زیست' in p['subject'])
    ddi, dl = compute_ddi(sh, report['social_time'])
    _, _, rm, _, _ = predict_rank(sh, tt, pc)

    cand = set()
    if total_reports >= 1: cand.add("first_step")
    if tt >= 100: cand.add("hunter_100")
    if tt >= 200: cand.add("hunter_200")
    if parse_duration(report['screen_time']) <= 30: cand.add("steel_focus")
    if bio_m >= 180: cand.add("bio_marathon")
    if sh >= 8: cand.add("marathon_day")
    if streak >= 7: cand.add("streak_7")
    if streak >= 30: cand.add("streak_30")
    if pc >= 100 and tt >= 20: cand.add("perfect_day")
    if total_reports >= 10: cand.add("consistent")
    if ddi < 10: cand.add("ddi_diamond")
    if ddi < 5: cand.add("ddi_warrior")
    if rm < 1000 and tt >= 50: cand.add("rank_hunter")
    for p in parts_data:
        if p.get('start_hour', 99) < 6: cand.add("early_bird")
        if p.get('end_hour', 0) >= 23: cand.add("night_owl")

    for bid in cand:
        if bid not in existing:
            new_badges.append(bid)
            c.execute(
                "INSERT OR IGNORE INTO user_badges VALUES (?,?,?)",
                (username, bid, datetime.datetime.now()))

    if new_badges:
        conn.commit()
    return new_badges


# ═══════════════════════════════════════════════════════════════════
# ۶. 🕐 TIME PICKER MODAL — به سبک آلارم گوشی
# ═══════════════════════════════════════════════════════════════════

HAS_DIALOG = hasattr(st, "dialog")


if HAS_DIALOG:

    @st.dialog("⏰ انتخاب ساعت", width="small")
    def _time_picker_modal(key_prefix, label):
        """مودال آلارم‌مانند با دو ستون اسکرول‌دار"""
        hk = f"{key_prefix}_H"
        mk = f"{key_prefix}_M"

        h = st.session_state.get(hk, 8)
        m = st.session_state.get(mk, 0)

        # نمایش درشت ساعت
        st.markdown(f"""
        <div style="text-align:center; padding:10px 0 16px 0;">
            <div style="font-family:'Courier New',monospace;
                        font-size:60px; font-weight:900; letter-spacing:8px;
                        background:linear-gradient(90deg,#38bdf8,#a78bfa,#f472b6);
                        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                        background-clip:text; line-height:1;">
                {h:02d}:{m:02d}
            </div>
            <div style="color:#94a3b8; font-size:13px; margin-top:8px; font-weight:700;">
                🕐 {label}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        # ستون ساعت (0-23) — اسکرول‌دار
        with col1:
            st.markdown(
                "<div style='text-align:center; color:#38bdf8; font-weight:800; "
                "font-size:14px; margin-bottom:8px;'>ساعت</div>",
                unsafe_allow_html=True)
            with st.container(height=260, border=False):
                for hh in range(24):
                    is_sel = (hh == h)
                    label_btn = f"✅  {hh:02d}" if is_sel else f"   {hh:02d}"
                    if st.button(
                        label_btn,
                        key=f"{key_prefix}_mh_{hh}",
                        use_container_width=True,
                        type="primary" if is_sel else "secondary",
                    ):
                        st.session_state[hk] = hh
                        st.rerun()

        # ستون دقیقه (0-55، پله 5) — اسکرول‌دار
        with col2:
            st.markdown(
                "<div style='text-align:center; color:#38bdf8; font-weight:800; "
                "font-size:14px; margin-bottom:8px;'>دقیقه</div>",
                unsafe_allow_html=True)
            with st.container(height=260, border=False):
                for mm in range(0, 60, 5):
                    is_sel = (mm == m)
                    label_btn = f"✅  {mm:02d}" if is_sel else f"   {mm:02d}"
                    if st.button(
                        label_btn,
                        key=f"{key_prefix}_mm_{mm}",
                        use_container_width=True,
                        type="primary" if is_sel else "secondary",
                    ):
                        st.session_state[mk] = mm
                        st.rerun()

        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

        # دکمه‌های میانبر سریع
        st.markdown(
            "<div style='text-align:center; color:#64748b; font-size:11.5px; "
            "margin:4px 0 8px 0; font-weight:700;'>⚡ میانبرهای پرکاربرد:</div>",
            unsafe_allow_html=True)

        quick_cols = st.columns(4)
        quick_items = [
            (6, 30, "🌅 06:30"),
            (8, 0, "☀️ 08:00"),
            (16, 0, "🌤️ 16:00"),
            (22, 0, "🌙 22:00"),
        ]
        for idx, (qh, qm, qlbl) in enumerate(quick_items):
            if quick_cols[idx].button(
                qlbl,
                key=f"{key_prefix}_quick_{idx}",
                use_container_width=True,
            ):
                st.session_state[hk] = qh
                st.session_state[mk] = qm
                st.rerun()

        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

        # دکمه تایید
        if st.button("✅ تایید و بستن", use_container_width=True,
                     type="primary", key=f"{key_prefix}_ok"):
            st.session_state.pop(f"modal_open_{key_prefix}", None)
            st.rerun()


def time_picker_trigger(label, key_prefix, default_h=8, default_m=0):
    """دکمه بازکننده مودال + نمایش ساعت انتخاب‌شده"""
    hk = f"{key_prefix}_H"
    mk = f"{key_prefix}_M"

    if hk not in st.session_state:
        st.session_state[hk] = default_h
    if mk not in st.session_state:
        st.session_state[mk] = default_m

    h = st.session_state[hk]
    m = st.session_state[mk]

    st.markdown(f'<div class="time-label">🕐 {label}</div>', unsafe_allow_html=True)

    if HAS_DIALOG:
        if st.button(
            f"⏰  {h:02d}:{m:02d}   —   کلیک کن",
            key=f"{key_prefix}_open",
            use_container_width=True,
        ):
            st.session_state[f"modal_open_{key_prefix}"] = True
            st.rerun()

        if st.session_state.get(f"modal_open_{key_prefix}"):
            _time_picker_modal(key_prefix, label)
    else:
        st.warning("⚠️ برای مودال ساعت، Streamlit را آپدیت کن: `pip install -U streamlit`")
        opts_h = list(range(24))
        opts_m = list(range(0, 60, 5))
        h = st.selectbox("ساعت", opts_h, index=h,
                         format_func=lambda x: f"{x:02d}",
                         key=f"{key_prefix}_fbh")
        m = st.selectbox("دقیقه", opts_m,
                         index=opts_m.index(m) if m in opts_m else 0,
                         format_func=lambda x: f"{x:02d}",
                         key=f"{key_prefix}_fbm")
        st.session_state[hk] = h
        st.session_state[mk] = m

    st.markdown(f'<div class="time-preview">⏰ {h:02d}:{m:02d}</div>',
                unsafe_allow_html=True)
    return datetime.time(h, m)


# ═══════════════════════════════════════════════════════════════════
# ۷. کارنامه HTML (فارسی ۱۰۰٪ سالم)
# ═══════════════════════════════════════════════════════════════════

def render_html_report_card(name, date_str, satisfaction, study_hours, total_tests,
                             percentage, screen_time, ddi_val, ddi_lvl, level_name,
                             xp, streak, card_id="card1"):
    ddi_color = {"green": "#4ade80", "yellow": "#facc15", "red": "#f87171"}[ddi_lvl]
    ddi_label = {
        "green": "💎 مغز الماسی",
        "yellow": "⚠️ افت دوپامین",
        "red": "🔥 تمرکز بحرانی"
    }[ddi_lvl]
    ddi_bg = {
        "green": "rgba(74,222,128,0.08)",
        "yellow": "rgba(250,204,21,0.08)",
        "red": "rgba(248,113,113,0.12)"
    }[ddi_lvl]

    safe_name = html_lib.escape(str(name))

    return f"""<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
<meta charset="UTF-8">
<link href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css" rel="stylesheet">
<script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
<style>
* {{ box-sizing: border-box; font-family: Vazirmatn, sans-serif; }}
body {{ margin:0; padding:0; background: transparent; }}
#card-{card_id} {{
    width: 520px; padding: 36px 30px 28px;
    background: linear-gradient(145deg, #0b1220 0%, #1a2240 100%);
    border: 3px solid #38bdf8; border-radius: 26px;
    color: #fff; position: relative; overflow: hidden;
    box-shadow: 0 24px 60px rgba(56,189,248,0.35);
    margin: 0 auto;
}}
#card-{card_id}::before {{
    content:''; position:absolute; inset:6px; border-radius:20px; padding:2px;
    background: linear-gradient(135deg,#38bdf8,#a78bfa,#f472b6,#facc15,#38bdf8);
    background-size: 300% 100%; animation: shift 8s linear infinite;
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor; mask-composite: exclude;
    pointer-events: none;
}}
@keyframes shift {{ 0%{{background-position:0% 50%}} 100%{{background-position:200% 50%}} }}
.badge-20 {{
    position: absolute; top: 22px; left: 22px; width: 70px; height: 70px;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    background: radial-gradient(circle at 30% 30%, #fef08a, #facc15 40%, #d97706 100%);
    color: #0b1220; font-weight: 900; font-size: 24px;
    box-shadow: 0 0 34px rgba(250,204,21,0.85);
}}
.head {{ text-align: center; margin-bottom: 22px; }}
.title {{
    font-size: 32px; font-weight: 900; margin: 0;
    background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}}
.subtitle {{ color: #94a3b8; font-size: 13px; margin-top: 6px; }}
.student {{ font-size: 22px; color: #38bdf8; font-weight: 900; text-align: center; margin: 14px 0 4px; }}
.dateline {{ text-align: center; color: #cbd5e1; font-size: 13px; margin-bottom: 20px; }}
.grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px; }}
.mcard {{
    background: rgba(15,23,42,0.85); border: 2px solid #38bdf8;
    border-radius: 16px; padding: 14px 10px; text-align: center;
}}
.mlabel {{ color: #94a3b8; font-size: 12px; margin-bottom: 6px; }}
.mvalue {{ font-size: 28px; font-weight: 900; line-height: 1.1; }}
.ddi {{
    background: {ddi_bg}; border: 3px solid {ddi_color};
    border-radius: 16px; padding: 14px; text-align: center; margin-bottom: 14px;
}}
.ddi-v {{ font-size: 34px; font-weight: 900; color: {ddi_color}; }}
.ddi-l {{ font-size: 14px; font-weight: 800; color: {ddi_color}; margin-top: 4px; }}
.ddi-s {{ font-size: 10.5px; color: #64748b; margin-top: 6px; }}
.rpg {{
    background: rgba(30,15,45,0.6); border: 2px solid #a78bfa;
    border-radius: 16px; padding: 14px; display: flex;
    justify-content: space-around; margin-bottom: 16px;
}}
.rpg-item {{ text-align: center; flex: 1; }}
.rpg-l {{ color: #94a3b8; font-size: 11px; margin-bottom: 4px; }}
.rpg-v {{ font-size: 18px; font-weight: 900; }}
.foot {{
    text-align: center; border-top: 1px solid #38bdf8;
    padding-top: 14px; color: #38bdf8; font-size: 15px; font-weight: 800;
}}
.tg {{ color: #facc15; font-size: 13px; margin-top: 6px; font-weight: 700; }}
.dl-btn {{
    margin: 18px auto 0; padding: 12px 24px; display: block;
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
    <div class="student">{safe_name}</div>
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
    html2canvas(card, {{
        backgroundColor: '#0b1220', scale: 2,
        useCORS: true, allowTaint: true
    }}).then(canvas => {{
        const link = document.createElement('a');
        link.download = 'academy20_{date_str}.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
    }});
}}
</script>
</body>
</html>"""


def render_html_story_card(name, date_str, study_hours, total_tests, percentage,
                            ddi_val, ddi_lvl, level_name, xp_today, streak,
                            badges_list, story_id="story1"):
    ddi_color = {"green": "#4ade80", "yellow": "#facc15", "red": "#f87171"}[ddi_lvl]
    ddi_label = {
        "green": "💎 مغز الماسی",
        "yellow": "⚠️ افت دوپامین",
        "red": "🔥 تمرکز بحرانی"
    }[ddi_lvl]

    safe_name = html_lib.escape(str(name))

    badges_html = ""
    if badges_list:
        items = "".join([
            f'<span style="background:linear-gradient(90deg,#facc15,#f472b6); '
            f'color:#0b1220; padding:6px 12px; border-radius:8px; margin:3px; '
            f'font-weight:900; font-size:15px; display:inline-block;">'
            f'{BADGES[b][0]} {BADGES[b][1]}</span>'
            for b in badges_list[:3]
        ])
        badges_html = (
            '<div style="background:rgba(30,20,10,0.7); border:2px solid #facc15; '
            'border-radius:14px; padding:14px; margin-top:14px; text-align:center;">'
            '<div style="color:#facc15; font-weight:900; font-size:16px; margin-bottom:8px;">'
            '🏆 مدال‌های امشب</div>' + items + '</div>'
        )

    return f"""<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
<meta charset="UTF-8">
<link href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css" rel="stylesheet">
<script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
<style>
* {{ box-sizing: border-box; font-family: Vazirmatn, sans-serif; }}
body {{ margin:0; padding:16px; background:#05070f; display:flex; flex-direction:column; align-items:center; }}
#story-{story_id} {{
    width: 405px; height: 720px; padding: 28px 22px;
    background: radial-gradient(circle at 30% 10%, #1e2447 0%, #0b0f19 50%, #05070f 100%);
    border: 3px solid #38bdf8; border-radius: 22px;
    color: #fff; position: relative; overflow: hidden;
    display: flex; flex-direction: column;
}}
#story-{story_id}::before {{
    content:''; position:absolute; inset:5px; border-radius:16px; padding:2px;
    background: linear-gradient(135deg,#38bdf8,#a78bfa,#f472b6,#facc15,#38bdf8);
    background-size: 300% 100%; animation: shift 8s linear infinite;
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor; mask-composite: exclude;
    pointer-events: none;
}}
@keyframes shift {{ 0%{{background-position:0% 50%}} 100%{{background-position:200% 50%}} }}
.badge-20 {{
    position: absolute; top: 18px; left: 18px; width: 54px; height: 54px;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    background: radial-gradient(circle at 30% 30%, #fef08a, #facc15 40%, #d97706 100%);
    color: #0b1220; font-weight: 900; font-size: 18px;
    box-shadow: 0 0 22px rgba(250,204,21,0.8);
}}
.title {{ font-size: 30px; font-weight: 900; text-align: center; margin: 12px 0 4px;
    background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
.subtitle {{ text-align: center; color: #94a3b8; font-size: 12.5px; margin-bottom: 14px; }}
.student {{ text-align: center; font-size: 20px; font-weight: 900; color: #38bdf8; margin-bottom: 3px; }}
.date {{ text-align: center; color: #cbd5e1; font-size: 12.5px; margin-bottom: 14px; }}
.mcard {{ background: rgba(15,23,42,0.9); border: 2px solid #38bdf8;
    border-radius: 12px; padding: 12px 14px; margin-bottom: 8px; display: flex;
    justify-content: space-between; align-items: center; }}
.mcard-l {{ color: #94a3b8; font-size: 13px; }}
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
.foot {{ margin-top: auto; text-align: center; padding-top: 12px; border-top: 1px solid #38bdf8; }}
.foot-t {{ color: #38bdf8; font-size: 14px; font-weight: 800; }}
.foot-tg {{ color: #facc15; font-size: 17px; font-weight: 900; margin-top: 4px; }}
.foot-s {{ color: #64748b; font-size: 11px; margin-top: 4px; }}
.dl-btn {{ margin: 16px auto 0; padding: 12px 24px; display: block;
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
    <div class="student">{safe_name}</div>
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
        backgroundColor: '#05070f', scale: 2.667,
        useCORS: true, allowTaint: true
    }}).then(canvas => {{
        const link = document.createElement('a');
        link.download = 'story_{date_str}.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
    }});
}}
</script>
</body>
</html>"""


# ═══════════════════════════════════════════════════════════════════
# ۸. پومودورو
# ═══════════════════════════════════════════════════════════════════
if 'pomo' not in st.session_state:
    st.session_state.pomo = {
        'running': False, 'end_time': None,
        'duration': 25 * 60, 'last_remaining': 25 * 60,
    }

try:
    @st.fragment(run_every=1.0)
    def render_timer_fragment():
        p = st.session_state.pomo
        if p['running'] and p['end_time']:
            rem = int((p['end_time'] - datetime.datetime.now()).total_seconds())
            if rem <= 0:
                p['running'] = False
                rem = 0
                p['last_remaining'] = 0
                st.toast("⏰ زمان تمام شد!", icon="🔔")
            else:
                p['last_remaining'] = rem
        else:
            rem = p.get('last_remaining', p.get('duration', 25 * 60))
        m, s = divmod(max(0, rem), 60)
        status = "🔥 در حال اجرا..." if p['running'] else "⏸️ آماده شروع"
        st.markdown(
            f'<div class="pomodoro-box">'
            f'<div class="pomo-time">{m:02d}:{s:02d}</div>'
            f'<div class="pomo-label">{status}</div></div>',
            unsafe_allow_html=True)
    HAS_FRAG = True
except Exception:
    HAS_FRAG = False


def render_pomodoro():
    col1, col2 = st.columns([2, 1])
    with col1:
        mode = st.radio(
            "حالت",
            ["🎯 تمرکز (۲۵ دقیقه)", "☕ استراحت (۵ دقیقه)", "⚡ تست سرعتی (۱۰ دقیقه)"],
            key="pomo_mode", horizontal=True)
    with col2:
        cm = st.number_input("یا دقیقه دلخواه:", 1, 120, 25, key="pomo_cm")

    durs = {
        "🎯 تمرکز (۲۵ دقیقه)": 25 * 60,
        "☕ استراحت (۵ دقیقه)": 5 * 60,
        "⚡ تست سرعتی (۱۰ دقیقه)": 10 * 60,
    }
    sel = durs.get(mode, cm * 60)
    st.session_state.pomo['duration'] = sel

    if HAS_FRAG:
        render_timer_fragment()
    else:
        p = st.session_state.pomo
        rem = (max(0, int((p['end_time'] - datetime.datetime.now()).total_seconds()))
               if p['running'] and p['end_time']
               else p.get('last_remaining', sel))
        m, s = divmod(rem, 60)
        st.markdown(
            f'<div class="pomodoro-box">'
            f'<div class="pomo-time">{m:02d}:{s:02d}</div>'
            f'<div class="pomo-label">'
            f'{"🔥 در حال اجرا" if p["running"] else "⏸️ آماده"}</div></div>',
            unsafe_allow_html=True)

    b1, b2, b3 = st.columns(3)
    if b1.button("▶️ شروع / ادامه", use_container_width=True, key="pomo_s"):
        if not st.session_state.pomo['running']:
            rem = st.session_state.pomo.get('last_remaining', sel)
            if rem <= 0:
                rem = sel
            st.session_state.pomo['running'] = True
            st.session_state.pomo['end_time'] = datetime.datetime.now() + datetime.timedelta(seconds=rem)
            st.rerun()

    if b2.button("⏸️ توقف", use_container_width=True, key="pomo_p"):
        if st.session_state.pomo['running'] and st.session_state.pomo['end_time']:
            rem = int((st.session_state.pomo['end_time'] - datetime.datetime.now()).total_seconds())
            st.session_state.pomo['last_remaining'] = max(0, rem)
            st.session_state.pomo['running'] = False
            st.session_state.pomo['end_time'] = None
            st.rerun()

    if b3.button("🔄 ریست", use_container_width=True, key="pomo_r"):
        st.session_state.pomo = {
            'running': False, 'end_time': None,
            'duration': sel, 'last_remaining': sel,
        }
        st.rerun()


# ═══════════════════════════════════════════════════════════════════
# ۹. Session & Login
# ═══════════════════════════════════════════════════════════════════
for k, v in [('logged_in', False), ('username', ''), ('name', '')]:
    if k not in st.session_state:
        st.session_state[k] = v

if not st.session_state['logged_in']:
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">🎮 آکادمی ۲۰ — RPG کنکور</div>
        <p class="hero-sub">XP بگیر، لول‌آپ شو، رتبه رو شکار کن! | <b>دکتر خشایار اشکبوس</b></p>
    </div>
    """, unsafe_allow_html=True)

    tab_l, tab_r = st.tabs(["🔑 ورود", "📝 ثبت‌نام جدید"])
    with tab_l:
        cu, cp = st.columns(2)
        u = cu.text_input("نام کاربری:", key="l_u")
        p = cp.text_input("رمز عبور:", type="password", key="l_p")
        if st.button("🚀 ورود به داشبورد", use_container_width=True):
            c.execute("SELECT name FROM users WHERE username=? AND password=?", (u, p))
            r = c.fetchone()
            if r:
                st.session_state['logged_in'] = True
                st.session_state['username'] = u
                st.session_state['name'] = r[0]
                st.rerun()
            else:
                st.error("❌ نام کاربری یا رمز عبور اشتباه است.")

    with tab_r:
        nm = st.text_input("نام و نام خانوادگی:")
        un = st.text_input("نام کاربری دلخواه:")
        pn = st.text_input("رمز عبور دلخواه:", type="password")
        if st.button("✨ ساخت حساب جدید", use_container_width=True):
            if nm and un and pn:
                try:
                    c.execute("INSERT INTO users VALUES (?,?,?)", (un, pn, nm))
                    conn.commit()
                    st.success("🎉 حساب ساخته شد! وارد شو.")
                except Exception:
                    st.error("⚠️ این نام کاربری قبلاً گرفته شده.")
            else:
                st.warning("همه فیلدها را پر کن.")
    st.stop()

# ═══════════════════════════════════════════════════════════════════
# ۱۰. داشبورد
# ═══════════════════════════════════════════════════════════════════
df_all = pd.read_sql_query(
    "SELECT * FROM reports WHERE username=? ORDER BY report_date ASC",
    conn, params=(st.session_state['username'],))

streak = compute_streak(df_all)
total_xp = calculate_xp(df_all)
cur_lvl, nxt_lvl, prog = get_level(total_xp)
motiv = random.choice(MOTIVATIONS)

st.markdown(f"""
<div class="hero-header">
    <div class="hero-title">داشبورد قهرمان | آکادمی ۲۰</div>
    <p class="hero-sub">🎯 {st.session_state['name']}</p>
</div>
""", unsafe_allow_html=True)

nx_hint = (f"{nxt_lvl[0] - total_xp:,} XP تا {nxt_lvl[2]} {nxt_lvl[1]}"
           if nxt_lvl else "🔥 به بالاترین سطح رسیدی!")
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
    <div class="xp-track">
        <div class="xp-fill" style="--target:{prog:.1f}%; width:{prog:.1f}%;"></div>
    </div>
    <div class="xp-labels">
        <span>{cur_lvl[0]:,} XP</span>
        <span class="xp-pct">{prog:.1f}%</span>
        <span>{nx_lbl} XP</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="glass-card" style="display:flex; align-items:center; gap:14px;">
    <div style="font-size:30px;">💬</div>
    <div style="font-size:14px; color:#e2e8f0;">{motiv}</div>
</div>
""", unsafe_allow_html=True)

t1, t2, t3, t4, t5, t6, t7 = st.tabs([
    "📝 ثبت گزارش",
    "🍅 پومودورو",
    "🔮 پیش‌بینی رتبه",
    "⚔️ اتاق جنگ",
    "📈 تحلیل‌ها",
    "🏆 دستاوردها",
    "⚙️ تنظیمات",
])

# ═══════════════════════════════════════════════════════════════════
# TAB 1 — Report
# ═══════════════════════════════════════════════════════════════════
with t1:
    cd1, cd2 = st.columns(2)
    rep_date = cd1.date_input("📅 تاریخ:", datetime.date.today())
    satisfaction = cd2.slider("⭐️ کیفیت مطالعه (۱ تا ۱۰):", 1, 10, 8)

    st.markdown("#### 📚 ریز پارت‌های درسی")
    num_slots = st.number_input("تعداد پارت‌ها:", 1, 12, 3, key="numparts")

    subjects = ["زیست‌شناسی", "شیمی", "فیزیک", "ریاضیات", "زمین‌شناسی",
                "فارسی", "دینی", "عربی", "زبان", "سایر"]

    total_tests = total_c = total_w = 0
    total_minutes = 0
    parts_summary, parts_data, error_data = [], [], []

    for i in range(int(num_slots)):
        with st.expander(f"📌 پارت درسی {i+1}", expanded=(i == 0)):
            cs1, cs2 = st.columns([2, 1])
            subj = cs1.selectbox(f"درس (پارت {i+1})", subjects, key=f"s_{i}")
            if subj == "سایر":
                subj = cs1.text_input("نام درس انتخابی", key=f"cs_{i}")
            cs2.radio("نوع تست", ["آموزشی", "زمان‌دار"], horizontal=True, key=f"tt_{i}")

            ct1, ct2 = st.columns(2)
            with ct1:
                st_t = time_picker_trigger("ساعت شروع", f"st_{i}", 8, 0)
            with ct2:
                et_t = time_picker_trigger("ساعت پایان", f"et_{i}", 9, 30)

            dur = (datetime.datetime.combine(datetime.date.today(), et_t) -
                   datetime.datetime.combine(datetime.date.today(), st_t)).total_seconds() / 60
            if dur <= 0:
                dur += 24 * 60
            total_minutes += dur

            st.markdown(
                f"""<div style="background:rgba(74,222,128,.12); border-right:3px solid #4ade80;
                padding:10px 14px; border-radius:10px; margin:10px 0; font-size:13.5px;">
                ⏱️ مدت این پارت: <b style="color:#4ade80;">{int(dur//60)} ساعت و {int(dur%60)} دقیقه</b>
                </div>""", unsafe_allow_html=True)

            csrc1, csrc2 = st.columns(2)
            csrc1.text_input("منبع درسنامه", key=f"src_s_{i}")
            csrc2.text_input("منبع تست", key=f"src_t_{i}")

            st.caption("آمار تست‌ها:")
            tc1, tc2, tc3, tc4 = st.columns(4)
            c_val = tc1.number_input("صحیح", 0, value=0, key=f"c_{i}")
            w_val = tc2.number_input("غلط", 0, value=0, key=f"w_{i}")
            tc3.number_input("نزده", 0, value=0, key=f"u_{i}")
            tc4.number_input("شک‌دار", 0, value=0, key=f"d_{i}")

            err_tag = None
            if w_val > 0:
                st.markdown("##### 🎯 جعبه سیاه اشتباهات (Smart Error Vault)")
                err_tag = st.selectbox(
                    f"علت اصلی غلط‌های {subj}:",
                    ERROR_TAGS + ["ترکیبی / نامشخص"],
                    key=f"err_{i}",
                    help="با تگ دقیق، AI Coach الگوی اشتباهاتت رو کشف می‌کنه")

            st.text_input("مبحث و توضیحات", key=f"nt_{i}")

            s_tests = c_val + w_val
            total_tests += s_tests
            total_c += c_val
            total_w += w_val
            parts_summary.append(
                f"{i+1}. {subj} ({st_t.strftime('%H:%M')}-{et_t.strftime('%H:%M')}) | "
                f"{s_tests} تست ({c_val}ص/{w_val}غ)")
            parts_data.append({
                'subject': subj, 'minutes': dur, 'tests': s_tests,
                'correct': c_val, 'wrong': w_val,
                'start_hour': st_t.hour, 'end_hour': et_t.hour,
            })
            if err_tag and w_val > 0:
                error_data.append({'subject': subj, 'tag': err_tag, 'count': w_val})

    st.markdown("#### 📱 کنترل اسکرین‌تایم")
    sc1, sc2 = st.columns(2)
    screen_t = sc1.text_input("کل مصرف گوشی امروز:", "۲:۱۵")
    social_t = sc2.text_input("شبکه‌های اجتماعی:", "۴۵ دقیقه")

    study_hours = round(total_minutes / 60, 2)
    overall_perc = round(((total_c * 3 - total_w) / (total_tests * 3)) * 100, 1) if total_tests > 0 else 0.0
    ddi_val, ddi_lvl = compute_ddi(study_hours, social_t)
    st.markdown(ddi_badge_html(ddi_val, ddi_lvl), unsafe_allow_html=True)

    xp_today = int(study_hours * 50 + total_tests * 2)
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:13px; color:#94a3b8;">پیش‌بینی امروز</div>
        <div style="font-size:22px; font-weight:900; color:#38bdf8; margin-top:8px;">
            ⏳ {study_hours} ساعت &nbsp;•&nbsp; 📝 {total_tests} تست &nbsp;•&nbsp; 🎯 {overall_perc}%
        </div>
        <div style="margin-top:10px; font-size:16px; font-weight:800; color:#facc15;">
            ⚡ +{xp_today:,} XP
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💾 ثبت نهایی گزارش", use_container_width=True):
        c.execute('''INSERT INTO reports (username, report_date, satisfaction, study_hours,
                    total_tests, correct_tests, wrong_tests, percentage, screen_time, social_time, details)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
                  (st.session_state['username'], rep_date, satisfaction, study_hours,
                   total_tests, total_c, total_w, overall_perc, screen_t, social_t,
                   "\n".join(parts_summary)))
        rid = c.lastrowid
        for p in parts_data:
            c.execute('''INSERT INTO parts (report_id, username, report_date, subject, minutes, tests, correct, wrong)
                        VALUES (?,?,?,?,?,?,?,?)''',
                      (rid, st.session_state['username'], rep_date, p['subject'],
                       p['minutes'], p['tests'], p['correct'], p['wrong']))
        for e in error_data:
            c.execute('''INSERT INTO error_vault (report_id, username, report_date, subject, error_tag, count)
                        VALUES (?,?,?,?,?,?)''',
                      (rid, st.session_state['username'], rep_date, e['subject'], e['tag'], e['count']))
        conn.commit()

        rpt = {
            'total_tests': total_tests, 'study_hours': study_hours,
            'percentage': overall_perc, 'screen_time': screen_t,
            'social_time': social_t,
        }
        nb = check_badges(st.session_state['username'], rpt, parts_data)
        st.balloons()
        st.success(f"✅ گزارش ذخیره شد! (+{xp_today:,} XP)")

        if nb:
            bh = "".join([
                f'<span class="badge-ach unlocked" style="display:inline-block;">'
                f'{BADGES[b][0]} {BADGES[b][1]}</span>' for b in nb])
            st.markdown(
                f'<div class="glass-card" style="border-color:#facc15;">'
                f'<h3 style="color:#facc15 !important;">🎉 مدال جدید باز شد!</h3>{bh}</div>',
                unsafe_allow_html=True)

        st.session_state['last_report'] = {
            'date': str(rep_date), 'satisfaction': satisfaction, 'hours': study_hours,
            'tests': total_tests, 'perc': overall_perc, 'screen': screen_t,
            'ddi': ddi_val, 'ddi_lvl': ddi_lvl, 'xp_today': xp_today,
            'new_badges': nb,
        }

    st.markdown("---")
    st.markdown("#### 🖼️ کارنامه‌های تصویری (HTML — فارسی سالم)")

    co1, co2 = st.columns(2)
    with co1:
        st.caption("📄 کارنامه عادی")
        card_html = render_html_report_card(
            st.session_state['name'], str(rep_date), satisfaction, study_hours,
            total_tests, overall_perc, screen_t, ddi_val, ddi_lvl,
            cur_lvl[1], total_xp + xp_today, streak, card_id="r1")
        components.html(card_html, height=830, scrolling=False)

    with co2:
        st.caption("📱 کارنامه استوری (اینستاگرام/تلگرام)")
        story_html = render_html_story_card(
            st.session_state['name'], str(rep_date), study_hours, total_tests,
            overall_perc, ddi_val, ddi_lvl, cur_lvl[1], xp_today, streak,
            st.session_state.get('last_report', {}).get('new_badges', []),
            story_id="s1")
        components.html(story_html, height=880, scrolling=True)

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
    st.markdown(f'<a href="{tg}" target="_blank" class="tg-button">🚀 ارسال متن به تلگرام مشاور</a>',
                unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# TAB 2 — Pomodoro
# ═══════════════════════════════════════════════════════════════════
with t2:
    st.markdown("### 🍅 تایمر پومودورو کنکوری")
    st.markdown("""
    <div class="glass-card" style="font-size:13.5px; color:#cbd5e1;">
    🎯 <b>پومودورو:</b> ۲۵ دقیقه تمرکز + ۵ دقیقه استراحت.
    حالت ⚡ برای تست سرعتی. حالت ☕ برای مرور.
    </div>""", unsafe_allow_html=True)
    render_pomodoro()

# ═══════════════════════════════════════════════════════════════════
# TAB 3 — Rank Predictor
# ═══════════════════════════════════════════════════════════════════
with t3:
    st.markdown("### 🔮 شبیه‌ساز تراز و تخمین رتبه زنده")
    st.markdown("""
    <div class="glass-card" style="font-size:13.5px; color:#cbd5e1;">
    🤖 بر اساس میانگین ۳۰ روز اخیر (ساعت + تست + درصد)، یک بازه احتمالی رتبه تخمین زده می‌شود.
    <b style="color:#facc15;">توجه:</b> این تخمین آموزشی است.
    </div>""", unsafe_allow_html=True)

    if df_all.empty:
        st.info("⚠️ برای فعال شدن، حداقل یک گزارش ثبت کن.")
    else:
        df30 = df_all[pd.to_datetime(df_all['report_date']) >=
                      pd.Timestamp(datetime.date.today() - datetime.timedelta(days=30))]
        if df30.empty:
            df30 = df_all

        ah = df30['study_hours'].mean()
        at = df30['total_tests'].mean()
        ap = df30['percentage'].mean()

        traz, rlo, rmid, rhi, comp = predict_rank(ah, at, ap)
        tier, tcol = rank_tier(rmid)

        cA, cB = st.columns(2)
        with cA:
            st.markdown(f"""
            <div class="rank-card" style="text-align:center;">
                <div style="font-size:13px; color:#94a3b8;">بازه احتمالی رتبه (۳۰ روز اخیر)</div>
                <div class="rank-number" style="margin:16px 0;">{rlo:,} تا {rhi:,}</div>
                <div class="rank-label">مرکز تخمین: <b style="color:#38bdf8;">{rmid:,}</b></div>
                <div style="margin-top:16px; font-size:19px; font-weight:900; color:{tcol};">{tier}</div>
            </div>""", unsafe_allow_html=True)
        with cB:
            st.markdown(f"""
            <div class="rank-card" style="text-align:center; border-color:rgba(56,189,248,.4);">
                <div style="font-size:13px; color:#94a3b8;">تراز تخمینی</div>
                <div class="rank-number" style="margin:16px 0;">{traz:,}</div>
                <div class="rank-label">از ۱۰,۰۰۰</div>
                <div style="margin-top:16px; font-size:13px; color:#94a3b8;">
                    امتیاز ترکیبی: <b style="color:#facc15;">{comp*100:.1f}%</b>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("#### 🎮 شبیه‌سازی «چی می‌شه اگر...»")
        scen = []
        for dh, dt, dp, lbl in [
            (0, 0, 0, "📍 فعلی"),
            (0.5, 10, 2, "📈 کمی بهتر"),
            (1.0, 20, 5, "🚀 جدی‌تر"),
            (1.5, 35, 8, "🔥 حرفه‌ای"),
            (2.0, 50, 12, "💎 المپیک"),
        ]:
            nh = min(ah + dh, 14)
            nt = min(at + dt, 250)
            np_ = min(ap + dp, 100)
            _, rl2, rm2, rh2, _ = predict_rank(nh, nt, np_)
            scen.append({
                'سناریو': lbl, 'ساعت': round(nh, 1),
                'تست': int(nt), 'درصد': round(np_, 1),
                'رتبه تخمینی': f"{rl2:,} - {rh2:,}",
                'تفاوت': f"{rmid - rm2:+,}" if rm2 != rmid else "—",
            })
        st.dataframe(pd.DataFrame(scen), use_container_width=True, hide_index=True)

        fig_w = go.Figure()
        for i, sc in enumerate(scen):
            _, rl2, rm2, rh2, _ = predict_rank(sc['ساعت'], sc['تست'], sc['درصد'])
            color = "#38bdf8" if i == 0 else "#4ade80" if rm2 < rmid else "#f87171"
            fig_w.add_trace(go.Bar(
                x=[sc['سناریو']], y=[rm2], name=sc['سناریو'],
                marker_color=color, text=[f"{rm2:,}"], textposition='outside',
                error_y=dict(
                    type='data', symmetric=False,
                    array=[rh2 - rm2], arrayminus=[rm2 - rl2],
                    color=color, thickness=1.5, width=8),
                showlegend=False,
            ))
        fig_w.update_layout(
            title="تخمین رتبه در سناریوها (کمتر = بهتر)",
            template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)', font={'family': 'Vazirmatn'},
            yaxis_title="رتبه تخمینی", height=420)
        st.plotly_chart(fig_w, use_container_width=True)

        st.markdown("#### 📉 روند رتبه تخمینی روز به روز")
        dfs = df_all.sort_values('report_date').copy()
        dfs['date'] = pd.to_datetime(dfs['report_date'])
        dfs['predicted_rank'] = [
            predict_rank(r['study_hours'], r['total_tests'], r['percentage'])[2]
            for _, r in dfs.iterrows()]
        ft = px.line(
            dfs, x='date', y='predicted_rank',
            title="تغییرات رتبه در طول زمان",
            labels={'predicted_rank': 'رتبه تخمینی', 'date': 'تاریخ'},
            markers=True, color_discrete_sequence=['#a78bfa'])
        ft.update_traces(line=dict(width=3),
                         marker=dict(size=10, line=dict(width=2, color='#0b0f19')))
        ft.update_layout(
            template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)', font={'family': 'Vazirmatn'},
            yaxis_autorange="reversed")
        st.plotly_chart(ft, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════
# TAB 4 — Arena
# ═══════════════════════════════════════════════════════════════════
with t4:
    st.markdown("### ⚔️ اتاق جنگ — دو﻿ئل دوستانه")
    st.markdown("""
    <div class="glass-card" style="font-size:13.5px; color:#cbd5e1;">
    🔥 با دوستات <b>اتاق مطالعه گروهی</b> بساز، اسم مستعار بذار و در
    <b>لیدربورد هفتگی</b> رقابت کن!
    </div>""", unsafe_allow_html=True)

    my = pd.read_sql_query(
        "SELECT r.code, r.name, m.nickname FROM arena_rooms r "
        "JOIN arena_members m ON r.code=m.code WHERE m.username=?",
        conn, params=(st.session_state['username'],))

    a1, a2 = st.columns(2)
    with a1:
        st.markdown("##### 🏗️ ساخت اتاق جدید")
        nn = st.text_input("اسم اتاق:", placeholder="جنگجویان پزشکی ۱۴۰۵", key="rn")
        nk = st.text_input("اسم مستعار خودت:", placeholder="دکتر X", key="rnk")
        if st.button("✨ ساخت اتاق", use_container_width=True):
            if nn and nk:
                code = f"{random.randint(1000,9999)}-{random.choice('ABCDEFGH')}{random.choice('ABCDEFGH')}"
                try:
                    c.execute("INSERT INTO arena_rooms VALUES (?,?,?,?)",
                              (code, nn, st.session_state['username'], datetime.datetime.now()))
                    c.execute("INSERT INTO arena_members VALUES (?,?,?,?)",
                              (code, st.session_state['username'], nk, datetime.datetime.now()))
                    conn.commit()
                    st.success(f"🎉 اتاق ساخته شد! کد دعوت: `{code}`")
                    st.rerun()
                except Exception as e:
                    st.error(f"خطا: {e}")
            else:
                st.warning("همه فیلدها را پر کن")

    with a2:
        st.markdown("##### 🎟️ پیوستن به اتاق")
        jc = st.text_input("کد اتاق:", key="jc").strip()
        jn = st.text_input("اسم مستعار:", key="jn")
        if st.button("🚀 پیوستن", use_container_width=True):
            if jc and jn:
                c.execute("SELECT name FROM arena_rooms WHERE code=?", (jc,))
                r = c.fetchone()
                if not r:
                    st.error("❌ اتاق پیدا نشد")
                else:
                    try:
                        c.execute("INSERT INTO arena_members VALUES (?,?,?,?)",
                                  (jc, st.session_state['username'], jn, datetime.datetime.now()))
                        conn.commit()
                        st.success(f"🎉 به «{r[0]}» پیوستی!")
                        st.rerun()
                    except Exception:
                        st.info("ℹ️ قبلاً عضو بودی")

    st.markdown("---")
    if my.empty:
        st.info("💡 هنوز توی هیچ اتاقی نیستی. یکی بساز یا به دوستت بپیوند!")
    else:
        opts = [f"{r['name']} ({r['code']})" for _, r in my.iterrows()]
        sel = st.selectbox("🏠 اتاق‌های تو:", opts)
        sc = sel.split("(")[-1].rstrip(")")
        lb = arena_leaderboard(sc)

        if lb.empty:
            st.info("اتاق خالیه")
        else:
            st.markdown(f"#### 🏆 لیدربورد ۷ روز اخیر — {sel}")
            icons = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
            for idx, row in lb.iterrows():
                ic = icons[idx - 1] if idx <= 10 else f"{idx}."
                mc = "arena-me" if row['is_me'] else ""
                mb = (" <span style='color:#38bdf8; font-size:11px;'>(تو)</span>"
                      if row['is_me'] else "")
                st.markdown(f"""
                <div class="arena-card {mc}">
                    <div class="arena-rank">{ic}</div>
                    <div style="flex:1;">
                        <div style="font-weight:800; font-size:15px;">{row['nickname']}{mb}</div>
                        <div style="font-size:12px; color:#94a3b8;">
                            ⏳ {row['hours']} ساعت &nbsp;•&nbsp; 📝 {row['tests']} تست
                        </div>
                    </div>
                    <div style="font-size:18px; font-weight:900; color:#facc15;">
                        {row['score']:,} <span style="font-size:11px; color:#94a3b8;">XP</span>
                    </div>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# TAB 5 — Analysis
# ═══════════════════════════════════════════════════════════════════
with t5:
    st.markdown("### 📈 داشبورد تحلیل هوشمند")
    if df_all.empty:
        st.info("⚠️ هنوز گزارشی ثبت نکرده‌ای!")
    else:
        df_all['report_date'] = pd.to_datetime(df_all['report_date'])
        cf, _ = st.columns([1, 2])
        tf_ = cf.radio("بازه:", ["۷ روز اخیر", "۳۰ روز اخیر", "همه"], horizontal=True)
        if "۷" in tf_:
            fdf = df_all[df_all['report_date'] >=
                         pd.Timestamp(datetime.date.today() - datetime.timedelta(days=7))]
        elif "۳۰" in tf_:
            fdf = df_all[df_all['report_date'] >=
                         pd.Timestamp(datetime.date.today() - datetime.timedelta(days=30))]
        else:
            fdf = df_all

        if not fdf.empty:
            sh = fdf['study_hours'].sum()
            stt = fdf['total_tests'].sum()
            ap = fdf['percentage'].mean()
            asat = fdf['satisfaction'].mean()
            pXP = int(sh * 50 + stt * 2)

            st.markdown(f"""
            <div style="display:grid; grid-template-columns: repeat(5, 1fr);
                        gap:12px; margin-bottom:22px;">
                <div class="metric-card"><span class="metric-icon">⚡</span>
                    <div class="metric-num">{pXP:,}</div>
                    <div class="metric-txt">XP بازه</div></div>
                <div class="metric-card"><span class="metric-icon">⏳</span>
                    <div class="metric-num">{sh:.1f}</div>
                    <div class="metric-txt">ساعت مطالعه</div></div>
                <div class="metric-card"><span class="metric-icon">📝</span>
                    <div class="metric-num">{stt}</div>
                    <div class="metric-txt">تعداد تست</div></div>
                <div class="metric-card"><span class="metric-icon">🎯</span>
                    <div class="metric-num">{ap:.1f}%</div>
                    <div class="metric-txt">میانگین درصد</div></div>
                <div class="metric-card"><span class="metric-icon">⭐</span>
                    <div class="metric-num">{asat:.1f}</div>
                    <div class="metric-txt">میانگین رضایت</div></div>
            </div>""", unsafe_allow_html=True)

            st.markdown("#### 🤖 تحلیلگر AI Coach")
            tips = ai_coach_analysis(fdf, df_all.iloc[-1].to_dict())
            th = "".join([f'<div class="ai-tip {cc}">{tt}</div>' for cc, tt in tips])
            st.markdown(f'<div class="ai-coach">{th}</div>', unsafe_allow_html=True)

            st.markdown("#### 🎯 جعبه سیاه اشتباهات")
            ev = pd.read_sql_query(
                "SELECT subject, error_tag, SUM(count) as cnt FROM error_vault "
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
                    fe.update_layout(template="plotly_dark",
                                     paper_bgcolor='rgba(0,0,0,0)',
                                     font={'family': 'Vazirmatn'}, height=420)
                    st.plotly_chart(fe, use_container_width=True)
                with e2:
                    fe2 = px.bar(ev, x='subject', y='cnt', color='error_tag',
                                 title="🎓 تفکیک علل غلط بر اساس درس",
                                 color_discrete_sequence=px.colors.qualitative.Bold)
                    fe2.update_layout(template="plotly_dark",
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      plot_bgcolor='rgba(0,0,0,0)',
                                      font={'family': 'Vazirmatn'},
                                      height=420, barmode='stack')
                    st.plotly_chart(fe2, use_container_width=True)

            st.markdown("#### 💎 روند DDI")
            drows = []
            for _, r in fdf.iterrows():
                dv, dl = compute_ddi(r['study_hours'], r['social_time'])
                drows.append({'date': r['report_date'], 'ddi': dv, 'level': dl})
            if drows:
                ddf = pd.DataFrame(drows)
                cm = {'green': '#4ade80', 'yellow': '#facc15', 'red': '#f87171'}
                fd = go.Figure()
                for lv, cc in cm.items():
                    s = ddf[ddf['level'] == lv]
                    if not s.empty:
                        fd.add_trace(go.Scatter(
                            x=s['date'], y=s['ddi'], mode='markers',
                            name=lv,
                            marker=dict(color=cc, size=14,
                                        line=dict(width=2, color='#0b0f19'))))
                fd.add_hline(y=10, line_dash="dash", line_color="#4ade80",
                             annotation_text="سبز (۱۰٪)")
                fd.add_hline(y=25, line_dash="dash", line_color="#f87171",
                             annotation_text="قرمز (۲۵٪)")
                fd.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)',
                                 paper_bgcolor='rgba(0,0,0,0)',
                                 font={'family': 'Vazirmatn'},
                                 title="روند DDI — پایین‌تر = بهتر",
                                 yaxis_title="DDI (%)")
                st.plotly_chart(fd, use_container_width=True)

            st.markdown("#### 📈 روندها")
            g1, g2 = st.columns([1, 2])
            with g1:
                gg = go.Figure(go.Indicator(
                    mode="gauge+number", value=float(ap),
                    number={'suffix': '%', 'font': {'color': '#38bdf8', 'size': 34}},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': '#4ade80'},
                        'bgcolor': '#1e293b',
                        'steps': [
                            {'range': [0, 40], 'color': 'rgba(248,113,113,.18)'},
                            {'range': [40, 70], 'color': 'rgba(250,204,21,.18)'},
                            {'range': [70, 100], 'color': 'rgba(74,222,128,.18)'},
                        ]},
                    title={'text': "درصد خالص",
                           'font': {'color': '#cbd5e1', 'size': 14}}))
                gg.update_layout(template="plotly_dark", height=280,
                                 plot_bgcolor='rgba(0,0,0,0)',
                                 paper_bgcolor='rgba(0,0,0,0)',
                                 font={'family': 'Vazirmatn'})
                st.plotly_chart(gg, use_container_width=True)
            with g2:
                fh = px.bar(fdf, x='report_date', y='study_hours',
                            title=f"⏳ ساعت مطالعه ({tf_})",
                            color='study_hours',
                            color_continuous_scale=['#0ea5e9', '#7c3aed', '#f472b6'])
                fh.update_layout(template="plotly_dark",
                                 plot_bgcolor='rgba(0,0,0,0)',
                                 paper_bgcolor='rgba(0,0,0,0)',
                                 font={'family': 'Vazirmatn'},
                                 coloraxis_showscale=False, height=280)
                st.plotly_chart(fh, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════
# TAB 6 — Badges
# ═══════════════════════════════════════════════════════════════════
with t6:
    st.markdown("### 🏆 تالار افتخارات")
    c.execute("SELECT badge_id, unlocked_at FROM user_badges WHERE username=?",
              (st.session_state['username'],))
    um = {r[0]: r[1] for r in c.fetchall()}
    tb = len(BADGES)
    uc = len(um)
    pct = (uc / tb) * 100

    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:14px; color:#94a3b8;">پیشرفت مدال‌ها</div>
        <div style="font-size:36px; font-weight:900; color:#facc15; margin:10px 0;">
            {uc} / {tb}
        </div>
        <div class="xp-track" style="height:16px;">
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
                du = (f"<div style='font-size:10px; color:#94a3b8; "
                      f"margin-top:8px;'>{dt.strftime('%Y/%m/%d')}</div>")
            except Exception:
                pass
        with cols[idx % 4]:
            st.markdown(f"""
            <div class="badge-ach {cls}">
                <div style="font-size:38px;">{ic}</div>
                <div style="font-size:14px; font-weight:900; margin-top:8px;">{nm}</div>
                <div style="font-size:11px; color:#94a3b8; margin-top:6px;">{dsc}</div>
                {du}
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# TAB 7 — Settings
# ═══════════════════════════════════════════════════════════════════
with t7:
    st.markdown(f"""
    <div class="glass-card">
        <h3 style="margin:0 0 14px 0;">👤 پروفایل قهرمان</h3>
        <p>نام: <b style="color:#38bdf8;">{st.session_state['name']}</b></p>
        <p>نام کاربری: <code style="color:#38bdf8;">{st.session_state['username']}</code></p>
        <p>سطح: <span style="color:{cur_lvl[3]}; font-weight:900;">{cur_lvl[2]} {cur_lvl[1]}</span></p>
        <p>⚡ XP کل: <b style="color:#facc15;">{total_xp:,}</b></p>
        <p>🔥 زنجیره: <b style="color:#fb923c;">{streak} روز</b></p>
        <p>📊 تعداد گزارش‌ها: <b>{len(df_all)}</b></p>
    </div>""", unsafe_allow_html=True)

    if st.button("🚪 خروج از حساب", use_container_width=True):
        st.session_state['logged_in'] = False
        st.rerun()
