# ═══════════════════════════════════════════════════════════════════════════
#                                                                           ═
#   👑  آکادمی ۲۰ — سیستم جامع هوشمند کنکور                                ═
#   ─────────────────────────────────────────────────────────────────────  ═
#   نسخه: 5.0 Ultimate Edition                                              ═
#   توسعه‌دهنده: تیم فنی آکادمی ۲۰                                          ═
#   مشاور علمی: دکتر خشایار اشکبوس | @Kh_Ashkboos                           ═
#                                                                           ═
#   بخش اول از دو بخش — زیرساخت، استایل، توابع پایه، کارت‌ساز              ═
#                                                                           ═
# ═══════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۰. واردسازی کتابخانه‌ها و وابستگی‌ها
# ═══════════════════════════════════════════════════════════════════════════

import streamlit as st
import streamlit.components.v1 as components

import datetime
import urllib.parse
import urllib.request
import sqlite3
import json
import random
import re
import math
import os
import io
import base64
import html as html_lib

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۱. تلاش برای واردسازی کتابخانه‌های PIL و پشتیبانی فارسی
# ═══════════════════════════════════════════════════════════════════════════

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_RTL = True
except ImportError:
    HAS_RTL = False


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۲. تنظیمات ابتدایی صفحه و ثابت‌های سراسری
# ═══════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="آکادمی ۲۰ | سیستم جامع کنکور",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": "https://t.me/Kh_Ashkboos",
        "Report a bug": "https://t.me/Kh_Ashkboos",
        "About": "# 👑 آکادمی ۲۰\nسیستم جامع هوشمند کنکور — نسخه ۵.۰",
    }
)

# ثابت‌های سراسری برنامه
APP_VERSION = "5.0.0"
DB_FILE = "konkur_academy.db"
FONT_FILE = "Vazirmatn-Bold.ttf"
FONT_URLS = [
    "https://github.com/rastikerdar/vazirmatn/raw/master/fonts/ttf/Vazirmatn-Bold.ttf",
    "https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/ttf/Vazirmatn-Bold.ttf",
]

# آستانه‌های سیستم RPG
XP_PER_HOUR = 50
XP_PER_TEST = 2
XP_PER_CORRECT_BONUS = 1  # پاداش تست صحیح

# آستانه‌های DDI
DDI_GREEN_MAX = 10
DDI_YELLOW_MAX = 25

# آستانه‌های Streak
STREAK_BADGE_7 = 7
STREAK_BADGE_30 = 30

# محدودیت‌های ورودی
MAX_PARTS = 15
MAX_STUDY_HOURS = 20
MAX_TESTS_PER_DAY = 500


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۳. استایل‌های سراسری — طراحی Dark Neon Glassmorphism
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
/* ═════════════════════════════════════════════════════════════════════════
   فونت اصلی
   ═════════════════════════════════════════════════════════════════════════ */
@import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');

/* ═════════════════════════════════════════════════════════════════════════
   ریست پایه
   ═════════════════════════════════════════════════════════════════════════ */
* {
    font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, sans-serif !important;
    direction: rtl;
    text-align: right;
    box-sizing: border-box;
}

/* ═════════════════════════════════════════════════════════════════════════
   انیمیشن‌های سراسری
   ═════════════════════════════════════════════════════════════════════════ */
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}

@keyframes pulseGlow {
    0%, 100% {
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.35),
                    0 0 40px rgba(168, 85, 247, 0.15);
    }
    50% {
        box-shadow: 0 0 45px rgba(56, 189, 248, 0.85),
                    0 0 80px rgba(168, 85, 247, 0.35);
    }
}

@keyframes fillBar {
    from { width: 0%; }
    to   { width: var(--target, 50%); }
}

@keyframes popIn {
    0%   { transform: scale(0.6) rotate(-5deg); opacity: 0; }
    60%  { transform: scale(1.1) rotate(3deg); opacity: 1; }
    100% { transform: scale(1) rotate(0); }
}

@keyframes floatY {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-6px); }
}

@keyframes shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

@keyframes rotate360 {
    to { transform: rotate(360deg); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes heartbeat {
    0%, 100% { transform: scale(1); }
    14%      { transform: scale(1.15); }
    28%      { transform: scale(1); }
    42%      { transform: scale(1.15); }
    70%      { transform: scale(1); }
}

@keyframes neonPulse {
    0%, 100% { filter: drop-shadow(0 0 4px currentColor); }
    50%      { filter: drop-shadow(0 0 12px currentColor); }
}

/* ═════════════════════════════════════════════════════════════════════════
   پس‌زمینه اصلی — کهکشانی سه‌لایه
   ═════════════════════════════════════════════════════════════════════════ */
.stApp {
    background:
        radial-gradient(circle at 10% 0%,   #1e2447 0%, transparent 45%),
        radial-gradient(circle at 90% 100%, #2a1345 0%, transparent 50%),
        radial-gradient(circle at 50% 50%,  #0d1424 0%, #05070f 100%) !important;
    color: #ffffff !important;
    min-height: 100vh;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(1.5px 1.5px at 20% 30%, rgba(56,189,248,0.5), transparent),
        radial-gradient(1.2px 1.2px at 65% 70%, rgba(74,222,128,0.4), transparent),
        radial-gradient(1.3px 1.3px at 82% 22%, rgba(250,204,21,0.4), transparent),
        radial-gradient(1px   1px   at 15% 80%, rgba(244,114,182,0.4), transparent),
        radial-gradient(1.2px 1.2px at 88% 55%, rgba(168,85,247,0.4), transparent),
        radial-gradient(1px   1px   at 55% 15%, rgba(56,189,248,0.35), transparent),
        radial-gradient(1.4px 1.4px at 5%  50%, rgba(250,204,21,0.3), transparent);
    background-size: 620px 620px, 480px 480px, 700px 700px, 350px 350px,
                     550px 550px, 400px 400px, 500px 500px;
    pointer-events: none;
    z-index: 0;
    opacity: 0.55;
    animation: floatY 12s ease-in-out infinite;
}

/* ═════════════════════════════════════════════════════════════════════════
   هدر قهرمانی
   ═════════════════════════════════════════════════════════════════════════ */
.hero-header {
    position: relative;
    background: linear-gradient(135deg, rgba(17,24,39,0.85) 0%,
                                       rgba(30,41,59,0.75) 100%);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 24px;
    padding: 28px 24px;
    text-align: center;
    margin-bottom: 24px;
    border: 1px solid rgba(56,189,248,0.28);
    box-shadow: 0 20px 60px rgba(2,132,199,0.18),
                inset 0 1px 0 rgba(255,255,255,0.08);
    overflow: hidden;
    animation: fadeInUp 0.6s ease;
}

.hero-header::before {
    content: '';
    position: absolute;
    inset: -2px;
    border-radius: 24px;
    padding: 2px;
    background: linear-gradient(90deg,
        #38bdf8, #4ade80, #facc15, #f472b6, #a78bfa, #38bdf8);
    background-size: 400% 100%;
    animation: gradientShift 10s linear infinite;
    -webkit-mask: linear-gradient(#fff 0 0) content-box,
                  linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    pointer-events: none;
}

.hero-title {
    font-size: 30px;
    font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6, #facc15);
    background-size: 300% 100%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 8px 0;
    animation: gradientShift 6s linear infinite;
    letter-spacing: 0.5px;
}

.hero-sub {
    color: #cbd5e1 !important;
    font-size: 14px;
    margin: 0;
    font-weight: 500;
}

/* ═════════════════════════════════════════════════════════════════════════
   پنل XP اصلی
   ═════════════════════════════════════════════════════════════════════════ */
.xp-container {
    background: linear-gradient(135deg,
        rgba(17,24,39,0.85), rgba(30,41,59,0.78));
    backdrop-filter: blur(16px);
    border: 1px solid rgba(250,204,21,0.35);
    border-radius: 20px;
    padding: 20px 24px;
    margin-bottom: 20px;
    box-shadow: 0 12px 40px rgba(250,204,21,0.12),
                inset 0 1px 0 rgba(255,255,255,0.05);
    animation: fadeInUp 0.7s ease;
}

.xp-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin-bottom: 14px;
    flex-wrap: wrap;
}

.level-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(90deg,
        rgba(250,204,21,0.22), rgba(244,114,182,0.22));
    border: 2px solid #facc15;
    border-radius: 14px;
    padding: 9px 16px;
    font-weight: 900;
    font-size: 15px;
    color: #facc15 !important;
    animation: pulseGlow 3s ease-in-out infinite;
    white-space: nowrap;
}

.streak-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(90deg,
        rgba(251,146,60,0.2), rgba(248,113,113,0.2));
    border: 1.5px solid rgba(251,146,60,0.65);
    padding: 9px 16px;
    border-radius: 14px;
    font-weight: 800;
    font-size: 14px;
    color: #fb923c !important;
    white-space: nowrap;
}

.xp-info-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 12px;
    margin-bottom: 10px;
    flex-wrap: wrap;
    font-size: 13px;
}

.xp-amount {
    color: #38bdf8 !important;
    font-weight: 900;
    font-size: 17px;
}

.xp-next-hint {
    color: #94a3b8 !important;
    font-size: 12px;
}

.xp-track {
    background: #05070f;
    border-radius: 999px;
    height: 22px;
    overflow: hidden;
    position: relative;
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
    position: absolute;
    inset: 0;
    border-radius: 999px;
    background: linear-gradient(90deg,
        transparent 30%, rgba(255,255,255,0.35), transparent 70%);
    background-size: 200% 100%;
    animation: gradientShift 2.5s linear infinite;
}

.xp-labels {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
    color: #64748b !important;
}

.xp-labels .xp-pct {
    color: #facc15 !important;
    font-weight: 900;
    font-size: 13px;
}

/* ═════════════════════════════════════════════════════════════════════════
   کارت‌های متریک
   ═════════════════════════════════════════════════════════════════════════ */
.metric-card {
    position: relative;
    background: linear-gradient(145deg,
        rgba(17,24,39,0.88), rgba(30,41,59,0.72));
    backdrop-filter: blur(12px);
    border: 1px solid rgba(56,189,248,0.28);
    border-radius: 18px;
    padding: 18px 12px;
    text-align: center;
    transition: all 0.35s cubic-bezier(.2,.9,.3,1.3);
    overflow: hidden;
    box-shadow: 0 8px 26px rgba(0,0,0,0.35);
    animation: fadeInUp 0.5s ease;
}

.metric-card:hover {
    transform: translateY(-6px) scale(1.02);
    border-color: rgba(56,189,248,0.75);
    box-shadow: 0 16px 40px rgba(56,189,248,0.4);
}

.metric-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: -60%;
    width: 60%;
    height: 100%;
    background: linear-gradient(120deg,
        transparent, rgba(255,255,255,0.1), transparent);
    transition: 0.7s;
}

.metric-card:hover::after {
    left: 120%;
}

.metric-num {
    font-size: 28px;
    font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #4ade80);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}

.metric-txt {
    font-size: 12px;
    color: #94a3b8 !important;
    margin-top: 6px;
    font-weight: 600;
}

.metric-icon {
    font-size: 22px;
    display: block;
    margin-bottom: 6px;
}

/* ═════════════════════════════════════════════════════════════════════════
   مدال‌های دستاورد
   ═════════════════════════════════════════════════════════════════════════ */
.badge-ach {
    display: block;
    padding: 18px 12px;
    border-radius: 16px;
    font-weight: 800;
    font-size: 13px;
    margin: 5px 0;
    border: 2px solid;
    text-align: center;
    transition: all 0.35s cubic-bezier(.2,.9,.3,1.3);
    animation: popIn 0.6s ease;
    position: relative;
    overflow: hidden;
}

.badge-ach.unlocked {
    color: #facc15;
    border-color: #facc15;
    background: linear-gradient(145deg,
        rgba(250,204,21,0.15), rgba(244,114,182,0.1));
    box-shadow: 0 0 24px rgba(250,204,21,0.4);
}

.badge-ach.unlocked::after {
    content: '✨';
    position: absolute;
    top: 6px;
    left: 8px;
    font-size: 14px;
    animation: floatY 2s ease-in-out infinite;
}

.badge-ach.unlocked:hover {
    transform: translateY(-6px) rotate(-3deg);
    box-shadow: 0 0 40px rgba(250,204,21,0.75);
}

.badge-ach.locked {
    color: #475569;
    border-color: #334155;
    background: rgba(15,23,42,0.65);
    opacity: 0.55;
    filter: grayscale(0.6);
}

/* ═════════════════════════════════════════════════════════════════════════
   تحلیلگر AI Coach
   ═════════════════════════════════════════════════════════════════════════ */
.ai-coach {
    background: linear-gradient(135deg,
        rgba(56,189,248,0.1), rgba(168,85,247,0.1));
    border: 1px solid rgba(56,189,248,0.4);
    border-radius: 18px;
    padding: 16px;
    margin: 12px 0;
    box-shadow: 0 8px 30px rgba(56,189,248,0.15);
}

.ai-tip {
    padding: 10px 14px;
    margin: 6px 0;
    border-radius: 12px;
    font-size: 13.5px;
    border-right: 4px solid;
    background: rgba(15,23,42,0.4);
    transition: all 0.25s;
}

.ai-tip:hover {
    transform: translateX(-4px);
    background: rgba(15,23,42,0.6);
}

.ai-tip.success { border-color: #4ade80; color: #86efac; }
.ai-tip.warning { border-color: #facc15; color: #fde047; }
.ai-tip.danger  { border-color: #f87171; color: #fca5a5; }
.ai-tip.info    { border-color: #38bdf8; color: #7dd3fc; }

/* ═════════════════════════════════════════════════════════════════════════
   تایمر پومودورو
   ═════════════════════════════════════════════════════════════════════════ */
.pomodoro-box {
    background: linear-gradient(145deg, #0f172a, #1e293b);
    border: 2px solid #38bdf8;
    border-radius: 22px;
    padding: 28px;
    text-align: center;
    box-shadow: 0 0 40px rgba(56,189,248,0.35),
                inset 0 1px 0 rgba(255,255,255,0.05);
    margin: 16px 0;
    transition: border-color 0.4s;
}

.pomo-time {
    font-size: 72px;
    font-weight: 900;
    font-family: 'Courier New', monospace !important;
    background: linear-gradient(90deg, #38bdf8, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 6px;
    line-height: 1;
}

.pomo-label {
    font-size: 13px;
    color: #94a3b8 !important;
    margin-top: 10px;
    font-weight: 700;
}

/* ═════════════════════════════════════════════════════════════════════════
   پنل DDI
   ═════════════════════════════════════════════════════════════════════════ */
.ddi-panel {
    border-radius: 18px;
    padding: 18px;
    margin: 12px 0;
    text-align: center;
    border: 3px solid;
    transition: all 0.3s;
    animation: fadeInUp 0.5s ease;
}

.ddi-green {
    border-color: #4ade80;
    background: linear-gradient(135deg,
        rgba(74,222,128,0.15), rgba(56,189,248,0.08));
}

.ddi-yellow {
    border-color: #facc15;
    background: linear-gradient(135deg,
        rgba(250,204,21,0.15), rgba(251,146,60,0.08));
}

.ddi-red {
    border-color: #f87171;
    background: linear-gradient(135deg,
        rgba(248,113,113,0.2), rgba(220,38,38,0.15));
    animation: pulseGlow 2s infinite;
}

.ddi-value {
    font-size: 44px;
    font-weight: 900;
    letter-spacing: 3px;
    line-height: 1;
}

.ddi-label {
    font-size: 14px;
    margin-top: 8px;
    font-weight: 800;
}

/* ═════════════════════════════════════════════════════════════════════════
   کارت پیش‌بینی رتبه
   ═════════════════════════════════════════════════════════════════════════ */
.rank-card {
    background: linear-gradient(145deg,
        rgba(17,24,39,0.88), rgba(30,41,59,0.72));
    border: 2px solid rgba(168,85,247,0.4);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: 0 12px 40px rgba(168,85,247,0.2);
}

.rank-number {
    font-size: 58px;
    font-weight: 900;
    letter-spacing: 3px;
    background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}

.rank-label {
    font-size: 13px;
    color: #94a3b8 !important;
    margin-top: 8px;
}

/* ═════════════════════════════════════════════════════════════════════════
   کارت‌های آرنا
   ═════════════════════════════════════════════════════════════════════════ */
.arena-card {
    background: linear-gradient(145deg,
        rgba(17,24,39,0.88), rgba(30,41,59,0.72));
    border: 1px solid rgba(250,204,21,0.35);
    border-radius: 16px;
    padding: 14px 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    gap: 14px;
    transition: all 0.3s;
}

.arena-card:hover {
    transform: translateX(-4px);
    border-color: rgba(250,204,21,0.7);
    box-shadow: 0 8px 24px rgba(250,204,21,0.2);
}

.arena-rank {
    font-size: 24px;
    font-weight: 900;
    min-width: 48px;
    text-align: center;
    background: linear-gradient(90deg, #facc15, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.arena-me {
    border: 2px solid #38bdf8;
    box-shadow: 0 0 24px rgba(56,189,248,0.4);
}

/* ═════════════════════════════════════════════════════════════════════════
   فرم‌ها و ورودی‌ها
   ═════════════════════════════════════════════════════════════════════════ */
label, p, span, h1, h2, h3, h4, h5, h6, div {
    color: #ffffff !important;
    font-weight: 600;
}

input, textarea, select {
    background-color: rgba(30,41,59,0.85) !important;
    color: #ffffff !important;
    border: 1px solid rgba(56,189,248,0.35) !important;
    border-radius: 12px !important;
    transition: all 0.25s;
}

input:focus, textarea:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.18) !important;
}

/* ═════════════════════════════════════════════════════════════════════════
   دکمه‌های اصلی
   ═════════════════════════════════════════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(90deg, #0284c7, #7c3aed) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    padding: 10px 18px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.28) !important;
    letter-spacing: 0.3px;
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.01);
    box-shadow: 0 12px 32px rgba(124,58,237,0.55) !important;
    filter: brightness(1.1);
}

.stButton > button:active {
    transform: translateY(0) scale(0.99);
}

/* ═════════════════════════════════════════════════════════════════════════
   دکمه تلگرام
   ═════════════════════════════════════════════════════════════════════════ */
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
    margin-top: 15px;
    box-shadow: 0 6px 18px rgba(2,132,199,0.45);
    transition: all 0.3s;
}

.tg-button:hover {
    transform: translateY(-3px);
    filter: brightness(1.1);
    box-shadow: 0 12px 30px rgba(2,132,199,0.75);
}

/* ═════════════════════════════════════════════════════════════════════════
   تب‌ها
   ═════════════════════════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: rgba(17,24,39,0.65);
    padding: 10px;
    border-radius: 16px;
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

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(56,189,248,0.12);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #0284c7, #7c3aed) !important;
    color: #ffffff !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.4);
}

/* ═════════════════════════════════════════════════════════════════════════
   اسکرول‌بار سفارشی
   ═════════════════════════════════════════════════════════════════════════ */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #0b0f19;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #38bdf8, #7c3aed);
    border-radius: 10px;
    transition: 0.3s;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #38bdf8, #f472b6);
}

/* ═════════════════════════════════════════════════════════════════════════
   کارت شیشه‌ای عمومی
   ═════════════════════════════════════════════════════════════════════════ */
.glass-card {
    background: rgba(17,24,39,0.72);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(56,189,248,0.22);
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.28);
    animation: fadeInUp 0.4s ease;
}

/* ═════════════════════════════════════════════════════════════════════════
   رفع مشکل Dropdown
   ═════════════════════════════════════════════════════════════════════════ */
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

div[data-baseweb="calendar"],
div[data-baseweb="calendar"] * {
    background-color: #1e293b !important;
    color: #ffffff !important;
}

/* ═════════════════════════════════════════════════════════════════════════
   انتخابگر ساعت
   ═════════════════════════════════════════════════════════════════════════ */
.time-label {
    font-weight: 800;
    color: #38bdf8 !important;
    font-size: 14px;
    margin-bottom: 6px;
    display: block;
}

.time-preview {
    text-align: center;
    background: linear-gradient(90deg, #0284c7, #7c3aed);
    color: #ffffff !important;
    font-weight: 900;
    font-size: 24px;
    padding: 12px;
    border-radius: 12px;
    margin-top: 8px;
    letter-spacing: 3px;
    font-family: 'Courier New', monospace !important;
    box-shadow: 0 4px 20px rgba(2,132,199,0.5);
    transition: all 0.3s;
}

/* ═════════════════════════════════════════════════════════════════════════
   مودال ساعت — استایل آلارم
   ═════════════════════════════════════════════════════════════════════════ */
div[role="dialog"] {
    background: linear-gradient(145deg, #0f172a, #1a2340) !important;
    border: 2px solid #38bdf8 !important;
    border-radius: 20px !important;
    box-shadow: 0 0 60px rgba(56,189,248,0.4) !important;
}

/* ═════════════════════════════════════════════════════════════════════════
   مخفی کردن منوی Streamlit
   ═════════════════════════════════════════════════════════════════════════ */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* ═════════════════════════════════════════════════════════════════════════
   کارت‌های ویژه — انیمیشن اضافه
   ═════════════════════════════════════════════════════════════════════════ */
.glow-card {
    position: relative;
    border-radius: 18px;
    padding: 18px;
    background: linear-gradient(135deg,
        rgba(56,189,248,0.08), rgba(168,85,247,0.08));
    border: 1px solid rgba(56,189,248,0.4);
    animation: neonPulse 3s ease-in-out infinite;
}

/* ═════════════════════════════════════════════════════════════════════════
   Toast شخصی‌سازی‌شده
   ═════════════════════════════════════════════════════════════════════════ */
div[data-testid="stToast"] {
    background: linear-gradient(135deg, #1e293b, #0f172a) !important;
    border: 2px solid #38bdf8 !important;
    color: #ffffff !important;
    border-radius: 14px !important;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۴. زیرساخت دیتابیس — با مهاجرت خودکار
# ═══════════════════════════════════════════════════════════════════════════

def get_db_connection():
    """ایجاد اتصال به دیتابیس SQLite با تنظیمات بهینه"""
    conn = sqlite3.connect(
        DB_FILE,
        check_same_thread=False,
        timeout=10.0,
        isolation_level=None,
    )
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA cache_size=-8000")
    return conn


@st.cache_resource
def init_database():
    """
    راه‌اندازی اولیه دیتابیس با تمام جداول مورد نیاز.
    این تابع با کش Streamlit فقط یکبار اجرا می‌شود.
    """
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = conn.cursor()

    # ─── جدول کاربران ───
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            avatar_emoji TEXT DEFAULT '👤',
            bio TEXT DEFAULT '',
            target_major TEXT DEFAULT 'پزشکی',
            target_rank INT DEFAULT 1000
        )
    ''')

    # ─── جدول گزارشات روزانه ───
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            report_date DATE NOT NULL,
            satisfaction INT NOT NULL,
            study_hours REAL NOT NULL,
            total_tests INT DEFAULT 0,
            correct_tests INT DEFAULT 0,
            wrong_tests INT DEFAULT 0,
            percentage REAL DEFAULT 0,
            screen_time TEXT DEFAULT '0:00',
            social_time TEXT DEFAULT '0',
            details TEXT DEFAULT '',
            xp_earned INT DEFAULT 0,
            ddi REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(username, report_date)
        )
    ''')

    # ─── جدول پارت‌های مطالعاتی ───
    c.execute('''
        CREATE TABLE IF NOT EXISTS parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            report_date DATE NOT NULL,
            subject TEXT NOT NULL,
            minutes REAL NOT NULL,
            tests INT DEFAULT 0,
            correct INT DEFAULT 0,
            wrong INT DEFAULT 0,
            start_hour INT DEFAULT 0,
            end_hour INT DEFAULT 0,
            study_source TEXT DEFAULT '',
            test_source TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
        )
    ''')

    # ─── جدول مدال‌های افتخار ───
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            badge_id TEXT NOT NULL,
            unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(username, badge_id)
        )
    ''')

    # ─── جدول جعبه سیاه اشتباهات ───
    c.execute('''
        CREATE TABLE IF NOT EXISTS error_vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER,
            username TEXT NOT NULL,
            report_date DATE NOT NULL,
            subject TEXT NOT NULL,
            error_tag TEXT NOT NULL,
            count INT DEFAULT 1,
            notes TEXT DEFAULT ''
        )
    ''')

    # ─── جدول اتاق‌های آرنا ───
    c.execute('''
        CREATE TABLE IF NOT EXISTS arena_rooms (
            code TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            created_by TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_private INTEGER DEFAULT 0,
            max_members INT DEFAULT 20
        )
    ''')

    # ─── جدول اعضای آرنا ───
    c.execute('''
        CREATE TABLE IF NOT EXISTS arena_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            username TEXT NOT NULL,
            nickname TEXT NOT NULL,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(code, username),
            FOREIGN KEY (code) REFERENCES arena_rooms(code) ON DELETE CASCADE
        )
    ''')

    # ─── جدول جلسات پومودورو ───
    c.execute('''
        CREATE TABLE IF NOT EXISTS pomodoro_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            session_date DATE NOT NULL,
            duration_minutes INT NOT NULL,
            mode TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ─── جدول لاگ رویدادها ───
    c.execute('''
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            event_type TEXT NOT NULL,
            event_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ─── ایندکس‌ها برای سرعت ───
    c.execute('CREATE INDEX IF NOT EXISTS idx_reports_user_date ON reports(username, report_date)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_parts_user ON parts(username)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_parts_report ON parts(report_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_badges_user ON user_badges(username)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_error_user ON error_vault(username)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_arena_members ON arena_members(code, username)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_pomodoro_user ON pomodoro_sessions(username)')

    conn.commit()
    return conn


# راه‌اندازی دیتابیس در شروع برنامه
DB_CONN = init_database()


def db_cursor():
    """گرفتن cursor از دیتابیس سراسری"""
    return DB_CONN.cursor()


def db_commit():
    """ثبت تغییرات در دیتابیس"""
    DB_CONN.commit()


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۵. ثابت‌های دامنه — جملات، سطوح، مدال‌ها، دستاوردها
# ═══════════════════════════════════════════════════════════════════════════

# ─── جملات انگیزشی (۵۰+ جمله) ───
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
    "💪 خستگی امروزت، قدرت فرداته.",
    "🌙 شب‌های بیداری، صبح‌های افتخار می‌سازن.",
    "⭐ رقیبات در حال تلاشن، یا با اونا بدو یا عقب بمون.",
    "🎖️ پشت هر موفقیت، هزار ساعت تلاش پنهانه.",
    "📚 کتاب‌های خسته، رتبه‌های درخشان می‌سازن.",
    "🌊 موج‌ها رو بشکن، تا ساحل موفقیت رو ببینی.",
    "🦁 شیرها از گله جدا می‌مونن، تا پادشاه شن.",
    "🎪 هر تست، یک تمرین برای اجرای بزرگ کنکوره.",
    "🏔️ قله رو کسی فتح می‌کنه که از شیب نترسه.",
    "💡 لحظه‌های شک، شروع لحظه‌های پیشرفتن.",
    "🌅 فردا صبح، از امروز شروع می‌شه.",
    "⏰ هر ثانیه‌ای که بگذره، یک فرصت کمتره.",
    "🎨 ذهنت رو مثل هنر ببین، هر روز بهترش کن.",
    "🚁 بلند پرواز کن، آسمون محدودیت نداره.",
    "💊 پزشک شدن، از همین امروز شروع می‌شه.",
    "🎓 مدرک، نتیجه‌ی هزار شب تلاشه.",
    "🕯️ چراغ دانش، تاریکی جهل رو می‌شکنه.",
    "⚔️ شمشیرِ تست، بهترین سلاح کنکوره.",
    "🏹 هدف رو بزن، بدون تعلل.",
    "🎯 خودت رو با دیروزت مقایسه کن، نه با دیگران.",
    "📖 دانش، زیباترین میراثه.",
    "🔬 هر آزمایش، یک کشف جدید میاره.",
    "🎭 نقش قهرمان رو خودت بازی کن.",
    "🌟 ستاره شدن، از زمین شروع می‌شه.",
    "🌺 گل‌ها از خاکستر رشد می‌کنن.",
    "🦅 عقاب‌ها تنها پرواز می‌کنن، اما بلند.",
    "🎯 هر غلط، یک درس جدید.",
    "🔥 اگه داری می‌سوزی، یعنی داری می‌درخشی.",
    "💪 عادت‌ها، سرنوشتت رو می‌سازن.",
    "🌊 دریا از قطره‌ها ساخته شده.",
    "⛰️ کوه رو می‌شه فتح کرد، با گام‌های کوچک.",
    "🏅 مدال‌ها نصیب کسانی می‌شه که خسته نشدن.",
    "🎪 زندگی صحنه‌ست، تو بازیگر اصلی‌شی.",
    "🌙 ماه کامل، از هلال شروع شد.",
    "🦋 پروانه شدن، نیاز به تحمل پیله داره.",
    "🌈 بعد از هر بارون، رنگین‌کمونه.",
    "🎨 هر رنگ، یک درس از زندگیه.",
    "⚡ انرژی مثبت، معجزه می‌کنه.",
    "🎯 روی هدفت قفل شو.",
    "🚀 موشک‌ها از زمین پرتاب می‌شن، نه از آسمون.",
]

# ─── سطوح RPG ───
LEVELS = [
    (0,      "نوآموز",         "🌱", "#94a3b8"),
    (500,    "تازه‌کار",        "📗", "#4ade80"),
    (1500,   "کوشا",            "📘", "#38bdf8"),
    (3000,   "سخت‌کوش",         "⚔️", "#a78bfa"),
    (6000,   "حرفه‌ای",          "🥇", "#facc15"),
    (12000,  "استاد",           "👑", "#fb923c"),
    (25000,  "افسانه‌ای",        "🌟", "#f472b6"),
    (50000,  "اسطوره تجربی",    "🔱", "#f43f5e"),
    (100000, "افسانه کنکور",    "💠", "#22d3ee"),
]

# ─── مدال‌های افتخار (۲۰+ مدال) ───
BADGES = {
    "first_step":   ("🎯", "اولین قدم",        "اولین گزارش ثبت شد"),
    "hunter_50":    ("🏹", "تیرانداز",          "۵۰+ تست در یک روز"),
    "hunter_100":   ("⚔️", "شکارچی تست",       "۱۰۰+ تست در یک روز"),
    "hunter_200":   ("⚡", "تست‌زن افسانه‌ای",  "۲۰۰+ تست در یک روز"),
    "hunter_300":   ("🗡️", "قهرمان تست",        "۳۰۰+ تست در یک روز"),
    "steel_focus":  ("🛡️", "تمرکز فولادین",    "زیر ۳۰ دقیقه گوشی"),
    "iron_will":    ("🧠", "اراده آهنین",        "زیر ۱۵ دقیقه گوشی"),
    "bio_marathon": ("🧬", "ماراتن زیست",      "۳+ ساعت زیست در یک روز"),
    "math_master":  ("📐", "استاد ریاضی",       "۲+ ساعت ریاضی در یک روز"),
    "marathon_day": ("🏃", "ماراتن روزانه",    "۸+ ساعت مطالعه در یک روز"),
    "mega_marathon":("🚴", "فرا ماراتن",        "۱۲+ ساعت مطالعه در یک روز"),
    "streak_3":     ("🔥", "سه‌گانه",           "۳ روز متوالی"),
    "streak_7":     ("🌟", "هفت‌روز پیوسته",   "۷ روز متوالی"),
    "streak_30":    ("💫", "ماه کامل",         "۳۰ روز متوالی"),
    "early_bird":   ("🐓", "سحرخیز",           "شروع قبل از ۶ صبح"),
    "night_owl":    ("🦉", "جغد شب",           "مطالعه بعد از ۲۳"),
    "night_king":   ("🌌", "پادشاه شب",        "۳ روز متوالی مطالعه بعد از نیمه‌شب"),
    "perfect_day":  ("💯", "روز بی‌نقص",       "درصد تست ۱۰۰٪"),
    "consistent":   ("📊", "استمرار طلایی",    "۱۰ گزارش متوالی"),
    "ddi_diamond":  ("💎", "مغز الماسی",       "DDI زیر ۱۰٪"),
    "ddi_warrior":  ("🧿", "جنگجوی تمرکز",     "DDI زیر ۵٪"),
    "rank_hunter":  ("🎖️", "شکارچی رتبه",      "پیش‌بینی زیر ۱۰۰۰"),
    "rank_master":  ("🏅", "استاد رتبه",        "پیش‌بینی زیر ۵۰۰"),
    "perfect_week": ("🎪", "هفته بی‌نقص",       "۷ روز با رضایت ۹+"),
    "centurion":    ("🏛️", "صدگانه",            "۱۰۰ ساعت مطالعه کل"),
    "thousand":     ("🌌", "هزارگانه",          "۱۰۰۰ ساعت مطالعه کل"),
}

# ─── دسته‌بندی علل غلط ───
ERROR_TAGS = [
    "بی‌دقتی محاسباتی",
    "فراموشی فرمول",
    "دام طراح",
    "کمبود وقت",
    "عدم تسلط به مبحث",
    "اشتباه در خواندن سؤال",
    "ترکیبی / نامشخص",
]

# ─── دروس ───
SUBJECTS = [
    "زیست‌شناسی",
    "شیمی",
    "فیزیک",
    "ریاضیات",
    "زمین‌شناسی",
    "فارسی",
    "دینی",
    "عربی",
    "زبان انگلیسی",
    "سایر",
]

# ─── رنگ‌های دروس ───
SUBJECT_COLORS = {
    "زیست‌شناسی": "#4ade80",
    "شیمی": "#f472b6",
    "فیزیک": "#38bdf8",
    "ریاضیات": "#a78bfa",
    "زمین‌شناسی": "#d97706",
    "فارسی": "#facc15",
    "دینی": "#22d3ee",
    "عربی": "#f87171",
    "زبان انگلیسی": "#c084fc",
    "سایر": "#94a3b8",
}

# ─── حالت‌های پومودورو ───
POMO_MODES = {
    "🎯 تمرکز عمیق": 25 * 60,
    "☕ استراحت کوتاه": 5 * 60,
    "⚡ تست سرعتی": 10 * 60,
    "🧘 تمرکز طولانی": 50 * 60,
    "🌙 مطالعه شبانه": 45 * 60,
}


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۶. توابع کمکی پایه
# ═══════════════════════════════════════════════════════════════════════════

def fa(text):
    """
    تبدیل متن فارسی برای رندر در PIL.
    اگر کتابخانه‌های لازم نصب باشن، به درستی تبدیل می‌کنه.
    """
    text = str(text)
    if HAS_RTL:
        try:
            return get_display(arabic_reshaper.reshape(text))
        except Exception:
            return text
    return text


def escape_html(text):
    """escape کردن HTML برای جلوگیری از XSS"""
    return html_lib.escape(str(text))


def ensure_font():
    """دانلود فونت وزیرمتن در اولین اجرا"""
    if os.path.exists(FONT_FILE):
        return FONT_FILE
    for url in FONT_URLS:
        try:
            urllib.request.urlretrieve(url, FONT_FILE)
            return FONT_FILE
        except Exception:
            continue
    return None


FONT_PATH = ensure_font()


def load_font(size):
    """بارگذاری فونت با سایز مشخص"""
    if FONT_PATH and os.path.exists(FONT_PATH):
        try:
            return ImageFont.truetype(FONT_PATH, size)
        except Exception:
            pass
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()


def safe_div(a, b, default=0):
    """تقسیم ایمن با مدیریت تقسیم بر صفر"""
    try:
        if b == 0:
            return default
        return a / b
    except Exception:
        return default


def clamp(value, min_val, max_val):
    """محدود کردن مقدار در بازه"""
    return max(min_val, min(value, max_val))


def format_number(num):
    """قالب‌بندی عدد با جداکننده هزارگان"""
    try:
        return f"{int(num):,}"
    except Exception:
        return str(num)


def format_hours(hours):
    """نمایش ساعت به صورت ۳.۵ ساعت"""
    try:
        return f"{float(hours):.1f}"
    except Exception:
        return "0.0"


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۷. توابع محاسباتی اصلی
# ═══════════════════════════════════════════════════════════════════════════

def compute_streak(df):
    """
    محاسبه تعداد روزهای متوالی مطالعه.
    اگر امروز یا دیروز گزارش داشته باشه، شمارش از اون شروع می‌شه.
    """
    if df.empty:
        return 0

    try:
        dates = sorted(
            set(pd.to_datetime(df['report_date']).dt.date),
            reverse=True
        )
        if not dates:
            return 0

        today = datetime.date.today()
        first = dates[0]

        # اگه آخرین گزارش نه امروزه نه دیروز، streak صفره
        if first != today and first != today - datetime.timedelta(days=1):
            return 0

        check = first
        streak = 0
        for d in dates:
            if d == check:
                streak += 1
                check -= datetime.timedelta(days=1)
            elif d < check:
                break
        return streak
    except Exception:
        return 0


def calculate_xp(df):
    """
    محاسبه XP کل:
    - ۵۰ XP برای هر ساعت مطالعه
    - ۲ XP برای هر تست
    - ۱ XP پاداش برای هر تست صحیح
    """
    if df.empty:
        return 0
    try:
        hours = df['study_hours'].sum()
        tests = df['total_tests'].sum()
        correct = df['correct_tests'].sum()
        return int(hours * XP_PER_HOUR +
                   tests * XP_PER_TEST +
                   correct * XP_PER_CORRECT_BONUS)
    except Exception:
        return 0


def calculate_session_xp(hours, tests, correct=0):
    """محاسبه XP یک جلسه واحد"""
    return int(hours * XP_PER_HOUR +
               tests * XP_PER_TEST +
               correct * XP_PER_CORRECT_BONUS)


def get_level(xp):
    """
    محاسبه سطح فعلی، سطح بعدی و درصد پیشرفت.
    خروجی: (current_level, next_level, progress_percent)
    """
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
        prog = clamp(safe_div(xp - current[0], rng) * 100, 0, 100)
    else:
        prog = 100.0

    return current, next_lvl, prog


def parse_duration(text):
    """
    تبدیل فرمت‌های مختلف به دقیقه:
    - "۲:۱۵" → 135 دقیقه
    - "۴۵ دقیقه" → 45 دقیقه
    - "1.5 ساعت" → 90 دقیقه
    """
    text = str(text).strip()

    # تبدیل اعداد فارسی به انگلیسی
    for i, d in enumerate("۰۱۲۳۴۵۶۷۸۹"):
        text = text.replace(d, str(i))

    # حذف کلمات غیر عددی
    text = text.replace('ساعت', ':').replace('دقیقه', '')
    text = text.replace('دق', '').replace('،', '')
    text = text.replace(',', '').strip()

    # حالت HH:MM
    if ':' in text:
        try:
            parts = text.split(':')
            h = int(float(parts[0]))
            m = int(float(parts[1])) if len(parts) > 1 else 0
            return h * 60 + m
        except Exception:
            pass

    # حالت عدد ساده
    nums = re.findall(r'[\d.]+', text)
    if nums:
        try:
            return int(float(nums[0]))
        except Exception:
            return 0

    return 0


def compute_ddi(study_hours, social_time_str):
    """
    محاسبه شاخص تخلیه دوپامین (DDI):
    DDI = (زمان شبکه اجتماعی ÷ زمان مطالعه) × 100
    """
    social_min = parse_duration(social_time_str)
    study_min = study_hours * 60

    if study_min <= 0:
        if social_min > 0:
            return 100.0, "red"
        return 0.0, "green"

    ddi = safe_div(social_min, study_min) * 100
    ddi = round(ddi, 1)

    if ddi < DDI_GREEN_MAX:
        level = "green"
    elif ddi < DDI_YELLOW_MAX:
        level = "yellow"
    else:
        level = "red"

    return ddi, level


# ─── اطلاعات نمایشی DDI ───
DDI_META = {
    "green":  ("💎", "مغز الماسی — تمرکز فولادین!", "#4ade80", "ddi-green"),
    "yellow": ("⚠️", "خطر افت دوپامین — مواظب باش!", "#facc15", "ddi-yellow"),
    "red":    ("🔥", "وضعیت بحرانی — تمرکز در حال سوختن!", "#f87171", "ddi-red"),
}


def ddi_badge_html(ddi, level):
    """تولید HTML پنل DDI"""
    icon, lbl, color, cls = DDI_META[level]
    return f"""
    <div class="ddi-panel {cls}">
        <div class="ddi-value" style="color:{color};">{ddi}%</div>
        <div class="ddi-label" style="color:{color};">{icon} {lbl}</div>
        <div style="font-size:11px; color:#94a3b8; margin-top:6px;">
            شاخص تخلیه تمرکز = (شبکه اجتماعی ÷ مطالعه) × ۱۰۰
        </div>
    </div>"""


def predict_rank(avg_hours, avg_tests, avg_percent):
    """
    پیش‌بینی رتبه کنکور بر اساس مدل هیوریستیک.
    خروجی: (traz, rank_low, rank_mid, rank_high, composite_score)
    """
    # نرمال‌سازی ورودی‌ها به بازه ۰-۱
    h = clamp(avg_hours, 0, 14) / 14
    t = clamp(avg_tests, 0, 200) / 200
    p = clamp(avg_percent, 0, 100) / 100

    # محاسبه امتیاز ترکیبی با وزن‌های تعیین‌شده
    comp = h * 0.30 + t * 0.25 + p * 0.45

    # تراز تخمینی از ۳۰۰۰ تا ۱۰۰۰۰
    traz = int(3000 + comp * 7000)

    # رتبه تخمینی (تابع نمایی معکوس)
    rank_mid = int(max(50, 250000 * ((1 - comp) ** 3.2)))
    rank_low = max(1, int(rank_mid * 0.65))
    rank_high = int(rank_mid * 1.55)

    return traz, rank_low, rank_mid, rank_high, comp


def rank_tier(rank_mid):
    """دسته‌بندی رتبه به مناطق"""
    if rank_mid < 500:
        return "🏆 منطقه المپیک", "#facc15"
    if rank_mid < 2000:
        return "🥇 منطقه طلایی", "#f472b6"
    if rank_mid < 5000:
        return "🥈 منطقه نقره‌ای", "#a78bfa"
    if rank_mid < 15000:
        return "🥉 منطقه برنزی", "#38bdf8"
    if rank_mid < 50000:
        return "💪 در حال رشد", "#4ade80"
    return "🌱 تازه شروع کردی", "#94a3b8"


def calculate_percentage(correct, wrong, blank=0):
    """
    محاسبه درصد خالص با فرمول کنکور:
    درصد = (۳×صحیح - غلط) ÷ (۳×کل) × ۱۰۰
    """
    total = correct + wrong + blank
    if total <= 0:
        return 0.0
    raw = (correct * 3 - wrong) / (total * 3)
    return round(clamp(raw * 100, -33.3, 100), 1)


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۸. سیستم تحلیل AI Coach
# ═══════════════════════════════════════════════════════════════════════════

def ai_coach_analysis(df, today_report=None):
    """
    تحلیل هوشمند عملکرد بر اساس قواعد آماری.
    خروجی: لیستی از (نوع, متن) برای نمایش.
    """
    tips = []

    if df.empty:
        return [("info", "🤖 هنوز داده‌ای برای تحلیل نیست. اولین گزارش را ثبت کن!")]

    # ─── تحلیل سرعت تست‌زنی ───
    sh = df['study_hours'].sum()
    stt = df['total_tests'].sum()

    if sh > 0:
        speed = safe_div(stt, sh)
        if speed >= 60:
            tips.append(("success", f"🚀 سرعت تست‌زنی فوق‌العاده! ({speed:.0f} تست/ساعت)"))
        elif speed >= 35:
            tips.append(("success", f"👍 سرعت تست‌زنی خوب ({speed:.0f} تست/ساعت)"))
        elif speed >= 15:
            tips.append(("warning", f"⚙️ سرعت متوسط ({speed:.0f} تست/ساعت). هدف ۴۰+ بذار"))
        else:
            tips.append(("danger", f"⚠️ سرعت پایین ({speed:.0f} تست/ساعت). روی تمرکز کار کن"))

    # ─── تحلیل DDI ───
    if today_report:
        ddi, dl = compute_ddi(
            today_report.get('study_hours', 0),
            today_report.get('social_time', '0')
        )
        if dl == "red":
            tips.append(("danger", f"🔥 DDI {ddi}% — اسکرین‌تایم داره تمرکزت رو می‌خوره!"))
        elif dl == "yellow":
            tips.append(("warning", f"⚠️ DDI {ddi}% — تعادل دیجیتال رو بهتر کن"))
        else:
            tips.append(("success", f"💎 DDI {ddi}% — مغز الماسی!"))

    # ─── تحلیل رضایت ───
    asat = df['satisfaction'].mean()
    if asat >= 8:
        tips.append(("success", f"😊 میانگین رضایتت {asat:.1f}/10 عالیه"))
    elif asat >= 6:
        tips.append(("info", f"🙂 میانگین رضایتت {asat:.1f}/10 قابل قبوله"))
    else:
        tips.append(("warning", f"💙 میانگین رضایتت {asat:.1f}/10 پایین. به خودت استراحت بده"))

    # ─── تحلیل روند تست‌ها ───
    if len(df) >= 3:
        recent = df.tail(3)['total_tests'].mean()
        older = df.head(max(1, len(df) - 3))['total_tests'].mean()
        if older > 0:
            change = safe_div(recent - older, older) * 100
            if change > 20:
                tips.append(("success", f"📈 روند صعودی تست‌زنی ({change:+.0f}%)"))
            elif change < -20:
                tips.append(("warning", f"📉 افت در تعداد تست‌ها ({change:+.0f}%)"))

    # ─── تحلیل درصد ───
    avg_p = df['percentage'].mean()
    if avg_p >= 70:
        tips.append(("success", f"🎯 میانگین درصدت {avg_p:.1f}% عالیه"))
    elif avg_p >= 50:
        tips.append(("info", f"📊 میانگین درصدت {avg_p:.1f}% خوبه"))
    elif avg_p >= 30:
        tips.append(("warning", f"⚙️ میانگین درصدت {avg_p:.1f}% نیاز به بهبود داره"))
    else:
        tips.append(("danger", f"⚠️ میانگین درصدت {avg_p:.1f}% پایینه"))

    return tips


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۹. سیستم مدال و دستاورد
# ═══════════════════════════════════════════════════════════════════════════

def get_unlocked_badges(username):
    """دریافت مدال‌های باز شده کاربر"""
    c = db_cursor()
    c.execute(
        "SELECT badge_id, unlocked_at FROM user_badges WHERE username=?",
        (username,)
    )
    return {row[0]: row[1] for row in c.fetchall()}


def check_and_unlock_badges(username, report, parts_data):
    """
    بررسی و باز کردن مدال‌های جدید.
    خروجی: لیست مدال‌های جدید
    """
    new_badges = []
    existing = set(get_unlocked_badges(username).keys())

    # دریافت اطلاعات کاربر
    dfu = pd.read_sql_query(
        "SELECT * FROM reports WHERE username=? ORDER BY report_date ASC",
        DB_CONN, params=(username,)
    )
    total_reports = len(dfu)
    streak = compute_streak(dfu)
    total_hours_all = dfu['study_hours'].sum() if not dfu.empty else 0

    tt = report.get('total_tests', 0)
    sh = report.get('study_hours', 0)
    pc = report.get('percentage', 0)
    screen_min = parse_duration(report.get('screen_time', '0'))
    ddi, dl = compute_ddi(sh, report.get('social_time', '0'))
    _, _, rm, _, _ = predict_rank(sh, tt, pc)

    # بررسی زیست و ریاضی
    bio_min = sum(p['minutes'] for p in parts_data if 'زیست' in p['subject'])
    math_min = sum(p['minutes'] for p in parts_data if 'ریاضی' in p['subject'])

    # بررسی شب‌کاری
    night_parts = sum(1 for p in parts_data if p.get('end_hour', 0) >= 23)
    has_night = night_parts > 0

    # ─── بررسی هر مدال ───
    candidates = set()

    if total_reports >= 1: candidates.add("first_step")
    if tt >= 50: candidates.add("hunter_50")
    if tt >= 100: candidates.add("hunter_100")
    if tt >= 200: candidates.add("hunter_200")
    if tt >= 300: candidates.add("hunter_300")
    if screen_min <= 30 and screen_min > 0: candidates.add("steel_focus")
    if screen_min <= 15 and screen_min > 0: candidates.add("iron_will")
    if bio_min >= 180: candidates.add("bio_marathon")
    if math_min >= 120: candidates.add("math_master")
    if sh >= 8: candidates.add("marathon_day")
    if sh >= 12: candidates.add("mega_marathon")
    if streak >= 3: candidates.add("streak_3")
    if streak >= 7: candidates.add("streak_7")
    if streak >= 30: candidates.add("streak_30")
    if pc >= 100 and tt >= 20: candidates.add("perfect_day")
    if total_reports >= 10: candidates.add("consistent")
    if ddi < 10: candidates.add("ddi_diamond")
    if ddi < 5: candidates.add("ddi_warrior")
    if rm < 1000 and tt >= 50: candidates.add("rank_hunter")
    if rm < 500 and tt >= 100: candidates.add("rank_master")
    if total_hours_all >= 100: candidates.add("centurion")
    if total_hours_all >= 1000: candidates.add("thousand")

    for p in parts_data:
        if p.get('start_hour', 99) < 6:
            candidates.add("early_bird")
        if p.get('end_hour', 0) >= 23:
            candidates.add("night_owl")

    # بررسی هفته بی‌نقص (۷ روز با رضایت ۹+)
    if len(dfu) >= 7:
        last7 = dfu.tail(7)
        if (last7['satisfaction'] >= 9).all():
            candidates.add("perfect_week")

    # بررسی ۳ روز شب‌کاری متوالی
    if has_night and len(dfu) >= 3:
        recent_nights = dfu.tail(3)
        night_count = 0
        for _, row in recent_nights.iterrows():
            rpt_id = row['id']
            c = db_cursor()
            c.execute(
                "SELECT COUNT(*) FROM parts WHERE report_id=? AND end_hour>=23",
                (rpt_id,)
            )
            if c.fetchone()[0] > 0:
                night_count += 1
        if night_count >= 3:
            candidates.add("night_king")

    # ثبت مدال‌های جدید
    c = db_cursor()
    for bid in candidates:
        if bid not in existing:
            new_badges.append(bid)
            try:
                c.execute(
                    "INSERT OR IGNORE INTO user_badges (username, badge_id) VALUES (?,?)",
                    (username, bid)
                )
            except Exception:
                pass

    if new_badges:
        db_commit()

    return new_badges


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۱۰. سیستم آرنا (اتاق جنگ)
# ═══════════════════════════════════════════════════════════════════════════

def arena_leaderboard(code, days=7):
    """
    ساخت لیدربورد اتاق بر اساس ۷ روز اخیر.
    خروجی: DataFrame مرتب‌شده
    """
    mem = pd.read_sql_query(
        "SELECT username, nickname FROM arena_members WHERE code=?",
        DB_CONN, params=(code,)
    )
    if mem.empty:
        return pd.DataFrame()

    cutoff = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    rows = []

    for _, m in mem.iterrows():
        df = pd.read_sql_query(
            "SELECT study_hours, total_tests, correct_tests "
            "FROM reports WHERE username=? AND report_date>=?",
            DB_CONN, params=(m['username'], cutoff)
        )
        h = float(df['study_hours'].sum()) if not df.empty else 0.0
        t = int(df['total_tests'].sum()) if not df.empty else 0
        cc = int(df['correct_tests'].sum()) if not df.empty else 0

        score = int(h * XP_PER_HOUR + t * XP_PER_TEST + cc * XP_PER_CORRECT_BONUS)

        rows.append({
            'nickname': m['nickname'],
            'hours': round(h, 1),
            'tests': t,
            'score': score,
            'is_me': m['username'] == st.session_state.get('username', ''),
        })

    lb = pd.DataFrame(rows).sort_values('score', ascending=False).reset_index(drop=True)
    lb.index = lb.index + 1
    return lb


def get_user_rooms(username):
    """دریافت اتاق‌های کاربر"""
    return pd.read_sql_query(
        "SELECT r.code, r.name, m.nickname "
        "FROM arena_rooms r "
        "JOIN arena_members m ON r.code=m.code "
        "WHERE m.username=?",
        DB_CONN, params=(username,)
    )


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۱۱. سیستم PIL فارسی — تولید پوستر (اختیاری)
# ═══════════════════════════════════════════════════════════════════════════

def draw_neon_text(base_img, text, xy, font, color, glow, gsize=8):
    """
    رسم متن با افکت نئون در PIL.
    فقط در صورتی که PIL نصب باشه کار می‌کنه.
    """
    if not HAS_PIL:
        return

    overlay = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    for offset in range(gsize, 0, -1):
        alpha = int(70 * (1 - offset / gsize))
        for dx, dy in [(offset, 0), (-offset, 0), (0, offset), (0, -offset)]:
            od.text((xy[0] + dx, xy[1] + dy), text, font=font, fill=glow + (alpha,))

    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=3))
    base_img.paste(overlay, (0, 0), overlay)

    d = ImageDraw.Draw(base_img)
    d.text((xy[0] + 2, xy[1] + 2), text, font=font, fill=(0, 0, 0))
    d.text(xy, text, font=font, fill=color)


def draw_gold_badge(img, cx, cy, r):
    """رسم نشان طلایی ۲۰ در PIL"""
    if not HAS_PIL:
        return

    d = ImageDraw.Draw(img, 'RGBA')

    # هاله درخشان
    for i in range(20, 0, -1):
        d.ellipse(
            [(cx - r - i, cy - r - i), (cx + r + i, cy + r + i)],
            fill=(250, 204, 21, int(80 * (1 - i / 20)))
        )

    # بدنه
    d.ellipse(
        [(cx - r, cy - r), (cx + r, cy + r)],
        fill=(30, 25, 10),
        outline=(250, 204, 21),
        width=4
    )

    # حلقه داخلی
    d.ellipse(
        [(cx - r + 6, cy - r + 6), (cx + r - 6, cy + r - 6)],
        outline=(255, 220, 90),
        width=2
    )

    # متن ۲۰
    f = load_font(34)
    bbox = d.textbbox((0, 0), "20", font=f)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    d.text((cx - w // 2, cy - h // 2 - 6), "20", font=f, fill=(250, 204, 21))


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۱۲. مودال انتخاب ساعت — به سبک آلارم گوشی
# ═══════════════════════════════════════════════════════════════════════════

HAS_DIALOG = hasattr(st, "dialog")


if HAS_DIALOG:

    @st.dialog("⏰ انتخاب ساعت", width="small")
    def _time_picker_modal(key_prefix, label):
        """
        مودال آلارم‌مانند با دو ستون اسکرول‌دار.
        کاربر ساعت و دقیقه رو با کلیک انتخاب می‌کنه.
        """
        hk = f"{key_prefix}_H"
        mk = f"{key_prefix}_M"

        h = st.session_state.get(hk, 8)
        m = st.session_state.get(mk, 0)

        # نمایش درشت ساعت
        st.markdown(f"""
        <div style="text-align:center; padding:10px 0 16px 0;">
            <div style="font-family:'Courier New',monospace;
                        font-size:60px; font-weight:900;
                        letter-spacing:8px;
                        background:linear-gradient(90deg,#38bdf8,#a78bfa,#f472b6);
                        -webkit-background-clip:text;
                        -webkit-text-fill-color:transparent;
                        background-clip:text; line-height:1;">
                {h:02d}:{m:02d}
            </div>
            <div style="color:#94a3b8; font-size:13px;
                        margin-top:8px; font-weight:700;">
                🕐 {label}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        # ─── ستون ساعت ───
        with col1:
            st.markdown(
                "<div style='text-align:center; color:#38bdf8; font-weight:800; "
                "font-size:14px; margin-bottom:8px;'>ساعت</div>",
                unsafe_allow_html=True
            )
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

        # ─── ستون دقیقه ───
        with col2:
            st.markdown(
                "<div style='text-align:center; color:#38bdf8; font-weight:800; "
                "font-size:14px; margin-bottom:8px;'>دقیقه</div>",
                unsafe_allow_html=True
            )
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

        # ─── میانبرهای سریع ───
        st.markdown(
            "<div style='text-align:center; color:#64748b; font-size:11.5px; "
            "margin:4px 0 8px 0; font-weight:700;'>"
            "⚡ میانبرهای پرکاربرد:</div>",
            unsafe_allow_html=True
        )

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

        # ─── دکمه تایید ───
        if st.button("✅ تایید و بستن", use_container_width=True,
                     type="primary", key=f"{key_prefix}_ok"):
            st.session_state.pop(f"modal_open_{key_prefix}", None)
            st.rerun()


def time_picker_trigger(label, key_prefix, default_h=8, default_m=0):
    """
    دکمه بازکننده مودال ساعت + نمایش ساعت انتخاب‌شده.
    خروجی: datetime.time
    """
    hk = f"{key_prefix}_H"
    mk = f"{key_prefix}_M"

    if hk not in st.session_state:
        st.session_state[hk] = default_h
    if mk not in st.session_state:
        st.session_state[mk] = default_m

    h = st.session_state[hk]
    m = st.session_state[mk]

    st.markdown(f'<div class="time-label">🕐 {label}</div>',
                unsafe_allow_html=True)

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
        # فالبک برای Streamlit قدیمی
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


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۱۳. تولیدکننده کارت HTML — کارنامه عادی
# ═══════════════════════════════════════════════════════════════════════════

def render_html_report_card(
    name, date_str, satisfaction, study_hours, total_tests,
    percentage, screen_time, ddi_val, ddi_lvl, level_name,
    xp, streak, card_id="card1"
):
    """
    تولید کارنامه HTML که با html2canvas به PNG تبدیل می‌شه.
    فارسی به‌طور کامل توسط مرورگر رندر می‌شه.
    """
    ddi_color = {"green": "#4ade80", "yellow": "#facc15", "red": "#f87171"}[ddi_lvl]
    ddi_label = {
        "green": "💎 مغز الماسی",
        "yellow": "⚠️ افت دوپامین",
        "red": "🔥 تمرکز بحرانی",
    }[ddi_lvl]
    ddi_bg = {
        "green": "rgba(74,222,128,0.08)",
        "yellow": "rgba(250,204,21,0.08)",
        "red": "rgba(248,113,113,0.12)",
    }[ddi_lvl]

    safe_name = escape_html(name)

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
    content:''; position:absolute; inset:6px;
    border-radius:20px; padding:2px;
    background: linear-gradient(135deg,
        #38bdf8,#a78bfa,#f472b6,#facc15,#38bdf8);
    background-size: 300% 100%;
    animation: shift 8s linear infinite;
    -webkit-mask: linear-gradient(#fff 0 0) content-box,
                  linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor; mask-composite: exclude;
    pointer-events: none;
}}
@keyframes shift {{
    0% {{background-position:0% 50%}}
    100% {{background-position:200% 50%}}
}}
.badge-20 {{
    position: absolute; top: 22px; left: 22px;
    width: 70px; height: 70px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    background: radial-gradient(circle at 30% 30%,
        #fef08a, #facc15 40%, #d97706 100%);
    color: #0b1220; font-weight: 900; font-size: 24px;
    box-shadow: 0 0 34px rgba(250,204,21,0.85);
}}
.head {{ text-align: center; margin-bottom: 22px; }}
.title {{
    font-size: 32px; font-weight: 900; margin: 0;
    background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}
.subtitle {{ color: #94a3b8; font-size: 13px; margin-top: 6px; }}
.student {{
    font-size: 22px; color: #38bdf8; font-weight: 900;
    text-align: center; margin: 14px 0 4px;
}}
.dateline {{
    text-align: center; color: #cbd5e1;
    font-size: 13px; margin-bottom: 20px;
}}
.grid {{
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 12px; margin-bottom: 16px;
}}
.mcard {{
    background: rgba(15,23,42,0.85);
    border: 2px solid #38bdf8;
    border-radius: 16px; padding: 14px 10px;
    text-align: center;
}}
.mlabel {{ color: #94a3b8; font-size: 12px; margin-bottom: 6px; }}
.mvalue {{ font-size: 28px; font-weight: 900; line-height: 1.1; }}
.ddi {{
    background: {ddi_bg}; border: 3px solid {ddi_color};
    border-radius: 16px; padding: 14px;
    text-align: center; margin-bottom: 14px;
}}
.ddi-v {{ font-size: 34px; font-weight: 900; color: {ddi_color}; }}
.ddi-l {{ font-size: 14px; font-weight: 800; color: {ddi_color}; margin-top: 4px; }}
.ddi-s {{ font-size: 10.5px; color: #64748b; margin-top: 6px; }}
.rpg {{
    background: rgba(30,15,45,0.6);
    border: 2px solid #a78bfa;
    border-radius: 16px; padding: 14px;
    display: flex; justify-content: space-around;
    margin-bottom: 16px;
}}
.rpg-item {{ text-align: center; flex: 1; }}
.rpg-l {{ color: #94a3b8; font-size: 11px; margin-bottom: 4px; }}
.rpg-v {{ font-size: 18px; font-weight: 900; }}
.foot {{
    text-align: center; border-top: 1px solid #38bdf8;
    padding-top: 14px; color: #38bdf8;
    font-size: 15px; font-weight: 800;
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


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۱۴. تولیدکننده کارت استوری اینستاگرام/تلگرام
# ═══════════════════════════════════════════════════════════════════════════

def render_html_story_card(
    name, date_str, study_hours, total_tests, percentage,
    ddi_val, ddi_lvl, level_name, xp_today, streak,
    badges_list, story_id="story1"
):
    """تولید کارنامه استوری ۹:۱۶ با html2canvas"""
    ddi_color = {"green": "#4ade80", "yellow": "#facc15", "red": "#f87171"}[ddi_lvl]
    ddi_label = {
        "green": "💎 مغز الماسی",
        "yellow": "⚠️ افت دوپامین",
        "red": "🔥 تمرکز بحرانی",
    }[ddi_lvl]

    safe_name = escape_html(name)

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
            '<div style="color:#facc15; font-weight:900; font-size:16px; '
            'margin-bottom:8px;">🏆 مدال‌های امشب</div>' + items + '</div>'
        )

    return f"""<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
<meta charset="UTF-8">
<link href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css" rel="stylesheet">
<script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
<style>
* {{ box-sizing: border-box; font-family: Vazirmatn, sans-serif; }}
body {{ margin:0; padding:16px; background:#05070f;
        display:flex; flex-direction:column; align-items:center; }}
#story-{story_id} {{
    width: 405px; height: 720px;
    padding: 28px 22px;
    background: radial-gradient(circle at 30% 10%,
        #1e2447 0%, #0b0f19 50%, #05070f 100%);
    border: 3px solid #38bdf8; border-radius: 22px;
    color: #fff; position: relative; overflow: hidden;
    display: flex; flex-direction: column;
}}
#story-{story_id}::before {{
    content:''; position:absolute; inset:5px;
    border-radius:16px; padding:2px;
    background: linear-gradient(135deg,
        #38bdf8,#a78bfa,#f472b6,#facc15,#38bdf8);
    background-size: 300% 100%;
    animation: shift 8s linear infinite;
    -webkit-mask: linear-gradient(#fff 0 0) content-box,
                  linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor; mask-composite: exclude;
    pointer-events: none;
}}
@keyframes shift {{
    0% {{background-position:0% 50%}}
    100% {{background-position:200% 50%}}
}}
.badge-20 {{
    position: absolute; top: 18px; left: 18px;
    width: 54px; height: 54px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    background: radial-gradient(circle at 30% 30%,
        #fef08a, #facc15 40%, #d97706 100%);
    color: #0b1220; font-weight: 900; font-size: 18px;
    box-shadow: 0 0 22px rgba(250,204,21,0.8);
}}
.title {{
    font-size: 30px; font-weight: 900;
    text-align: center; margin: 12px 0 4px;
    background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.subtitle {{
    text-align: center; color: #94a3b8;
    font-size: 12.5px; margin-bottom: 14px;
}}
.student {{
    text-align: center; font-size: 20px;
    font-weight: 900; color: #38bdf8; margin-bottom: 3px;
}}
.date {{
    text-align: center; color: #cbd5e1;
    font-size: 12.5px; margin-bottom: 14px;
}}
.mcard {{
    background: rgba(15,23,42,0.9);
    border: 2px solid #38bdf8;
    border-radius: 12px; padding: 12px 14px;
    margin-bottom: 8px;
    display: flex; justify-content: space-between; align-items: center;
}}
.mcard-l {{ color: #94a3b8; font-size: 13px; }}
.mcard-v {{ font-size: 22px; font-weight: 900; }}
.ddi {{
    background: rgba(15,20,15,0.6);
    border: 3px solid {ddi_color};
    border-radius: 12px; padding: 12px;
    text-align: center; margin: 10px 0;
}}
.ddi-v {{ font-size: 26px; font-weight: 900; color: {ddi_color}; }}
.ddi-l {{ font-size: 13px; font-weight: 800; color: {ddi_color}; }}
.rpg {{
    background: rgba(30,15,45,0.6);
    border: 2px solid #a78bfa;
    border-radius: 12px; padding: 10px;
    display: flex; justify-content: space-around;
    margin-top: 10px;
}}
.rpg-item {{ text-align: center; }}
.rpg-l {{ color: #94a3b8; font-size: 11px; }}
.rpg-v {{ font-size: 16px; font-weight: 900; }}
.foot {{
    margin-top: auto; text-align: center;
    padding-top: 12px; border-top: 1px solid #38bdf8;
}}
.foot-t {{ color: #38bdf8; font-size: 14px; font-weight: 800; }}
.foot-tg {{ color: #facc15; font-size: 17px; font-weight: 900; margin-top: 4px; }}
.foot-s {{ color: #64748b; font-size: 11px; margin-top: 4px; }}
.dl-btn {{
    margin: 16px auto 0; padding: 12px 24px; display: block;
    background: linear-gradient(90deg, #f09433, #dc2743, #bc1888);
    border: none; color: #fff; font-family: Vazirmatn;
    font-weight: 800; border-radius: 12px; cursor: pointer;
    font-size: 15px; width: 405px;
}}
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
        <div class="rpg-item">
            <div class="rpg-l">🎮 سطح</div>
            <div class="rpg-v" style="color:#facc15;">{level_name}</div>
        </div>
        <div class="rpg-item">
            <div class="rpg-l">⚡ XP</div>
            <div class="rpg-v" style="color:#38bdf8;">+{xp_today:,}</div>
        </div>
        <div class="rpg-item">
            <div class="rpg-l">🔥 زنجیره</div>
            <div class="rpg-v" style="color:#fb923c;">{streak} روز</div>
        </div>
    </div>
    {badges_html}
    <div class="foot">
        <div class="foot-t">مشاور: دکتر خشایار اشکبوس</div>
        <div class="foot-tg">@Kh_Ashkboos</div>
        <div class="foot-s">با آکادمی ۲۰، کنکور رو فتح کن!</div>
    </div>
</div>
<button class="dl-btn" onclick="dl_{story_id}()">📥 دانلود استوری</button>
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


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۱۵. موتور پومودورو با ذخیره جلسات
# ═══════════════════════════════════════════════════════════════════════════

if 'pomo' not in st.session_state:
    st.session_state.pomo = {
        'running': False,
        'end_time': None,
        'duration': 25 * 60,
        'last_remaining': 25 * 60,
        'mode': '🎯 تمرکز عمیق',
    }

try:
    @st.fragment(run_every=1.0)
    def render_timer_fragment():
        """نمایش زنده تایمر — فقط این بخش رفرش می‌شه"""
        p = st.session_state.pomo

        if p['running'] and p['end_time']:
            rem = int((p['end_time'] - datetime.datetime.now()).total_seconds())
            if rem <= 0:
                p['running'] = False
                rem = 0
                p['last_remaining'] = 0
                st.toast("⏰ زمان تمام شد!", icon="🔔")

                # ثبت جلسه پومودورو در دیتابیس
                try:
                    c = db_cursor()
                    c.execute(
                        "INSERT INTO pomodoro_sessions "
                        "(username, session_date, duration_minutes, mode, completed) "
                        "VALUES (?, ?, ?, ?, 1)",
                        (st.session_state.get('username', ''),
                         datetime.date.today(),
                         p['duration'] // 60,
                         p.get('mode', 'focus'))
                    )
                    db_commit()
                except Exception:
                    pass
            else:
                p['last_remaining'] = rem
        else:
            rem = p.get('last_remaining', p.get('duration', 25 * 60))

        m, s = divmod(max(0, rem), 60)

        if p['running']:
            status = "🔥 در حال اجرا..."
            border_color = "#4ade80"
        else:
            status = "⏸️ آماده شروع"
            border_color = "#38bdf8"

        st.markdown(
            f'<div class="pomodoro-box" style="border-color:{border_color};">'
            f'<div class="pomo-time">{m:02d}:{s:02d}</div>'
            f'<div class="pomo-label">{status}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    HAS_FRAG = True
except Exception:
    HAS_FRAG = False


def render_pomodoro_controls():
    """دکمه‌های کنترل پومودورو"""
    b1, b2, b3 = st.columns(3)

    if b1.button("▶️ شروع / ادامه", use_container_width=True, key="pomo_s"):
        if not st.session_state.pomo['running']:
            sel = st.session_state.pomo.get('duration', 25 * 60)
            rem = st.session_state.pomo.get('last_remaining', sel)
            if rem <= 0:
                rem = sel
            st.session_state.pomo['running'] = True
            st.session_state.pomo['end_time'] = (
                datetime.datetime.now() + datetime.timedelta(seconds=rem)
            )
            st.rerun()

    if b2.button("⏸️ توقف", use_container_width=True, key="pomo_p"):
        if st.session_state.pomo['running'] and st.session_state.pomo['end_time']:
            rem = int(
                (st.session_state.pomo['end_time'] - datetime.datetime.now())
                .total_seconds()
            )
            st.session_state.pomo['last_remaining'] = max(0, rem)
            st.session_state.pomo['running'] = False
            st.session_state.pomo['end_time'] = None
            st.rerun()

    if b3.button("🔄 ریست", use_container_width=True, key="pomo_r"):
        sel = st.session_state.pomo.get('duration', 25 * 60)
        st.session_state.pomo = {
            'running': False,
            'end_time': None,
            'duration': sel,
            'last_remaining': sel,
            'mode': st.session_state.pomo.get('mode', '🎯 تمرکز عمیق'),
        }
        st.rerun()


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۱۶. Session State و احراز هویت
# ═══════════════════════════════════════════════════════════════════════════

# مقادیر پیش‌فرض session
DEFAULT_SESSION = {
    'logged_in': False,
    'username': '',
    'name': '',
    'last_report': None,
    'show_story_modal': False,
}

for k, v in DEFAULT_SESSION.items():
    if k not in st.session_state:
        st.session_state[k] = v


def login_page():
    """نمایش صفحه ورود / ثبت‌نام"""
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">🎮 آکادمی ۲۰ — RPG کنکور</div>
        <p class="hero-sub">
            XP بگیر، لول‌آپ شو، رتبه رو شکار کن! | <b>دکتر خشایار اشکبوس</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_l, tab_r = st.tabs(["🔑 ورود", "📝 ثبت‌نام جدید"])

    with tab_l:
        cu, cp = st.columns(2)
        u = cu.text_input("نام کاربری:", key="l_u")
        p = cp.text_input("رمز عبور:", type="password", key="l_p")

        if st.button("🚀 ورود به داشبورد", use_container_width=True):
            if not u or not p:
                st.error("❌ نام کاربری و رمز عبور را وارد کن")
            else:
                c = db_cursor()
                c.execute(
                    "SELECT name FROM users WHERE username=? AND password=?",
                    (u, p)
                )
                r = c.fetchone()
                if r:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = u
                    st.session_state['name'] = r[0]

                    # بروزرسانی آخرین ورود
                    try:
                        c.execute(
                            "UPDATE users SET last_login=? WHERE username=?",
                            (datetime.datetime.now(), u)
                        )
                        db_commit()
                    except Exception:
                        pass

                    st.rerun()
                else:
                    st.error("❌ نام کاربری یا رمز عبور اشتباه است.")

    with tab_r:
        nm = st.text_input("نام و نام خانوادگی:")
        un = st.text_input("نام کاربری دلخواه:")
        pn = st.text_input("رمز عبور دلخواه:", type="password")
        pn2 = st.text_input("تکرار رمز عبور:", type="password")

        if st.button("✨ ساخت حساب کاربری", use_container_width=True):
            if not nm or not un or not pn:
                st.warning("همه فیلدها را پر کن.")
            elif pn != pn2:
                st.error("❌ رمز عبور و تکرارش یکسان نیست.")
            elif len(pn) < 4:
                st.warning("⚠️ رمز عبور حداقل ۴ کاراکتر باشد.")
            else:
                try:
                    c = db_cursor()
                    c.execute(
                        "INSERT INTO users (username, password, name) VALUES (?,?,?)",
                        (un, pn, nm)
                    )
                    db_commit()
                    st.success("🎉 حساب ساخته شد! حالا وارد شو.")
                    st.balloons()
                except sqlite3.IntegrityError:
                    st.error("⚠️ این نام کاربری قبلاً گرفته شده.")
                except Exception as e:
                    st.error(f"خطا: {e}")


# ─── بررسی وضعیت ورود ───
if not st.session_state['logged_in']:
    login_page()
    st.stop()


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۱۷. بارگذاری داده‌های کاربر
# ═══════════════════════════════════════════════════════════════════════════

USERNAME = st.session_state['username']
USER_NAME = st.session_state['name']

df_all = pd.read_sql_query(
    "SELECT * FROM reports WHERE username=? ORDER BY report_date ASC",
    DB_CONN, params=(USERNAME,)
)

streak = compute_streak(df_all)
total_xp = calculate_xp(df_all)
cur_lvl, nxt_lvl, prog = get_level(total_xp)
motiv = random.choice(MOTIVATIONS)


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۱۸. هدر داشبورد و پنل XP
# ═══════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<div class="hero-header">
    <div class="hero-title">داشبورد قهرمان | آکادمی ۲۰</div>
    <p class="hero-sub">🎯 {escape_html(USER_NAME)}</p>
</div>
""", unsafe_allow_html=True)

nx_hint = (
    f"{nxt_lvl[0] - total_xp:,} XP تا {nxt_lvl[2]} {nxt_lvl[1]}"
    if nxt_lvl else "🔥 به بالاترین سطح رسیدی!"
)
nx_lbl = f"{nxt_lvl[0]:,}" if nxt_lvl else "∞"

st.markdown(f"""
<div class="xp-container">
    <div class="xp-header">
        <div class="level-badge">
            <span>{cur_lvl[2]}</span>
            <span>سطح {cur_lvl[1]}</span>
        </div>
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


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۱۹. تعریف تب‌های اصلی
# ═══════════════════════════════════════════════════════════════════════════

t1, t2, t3, t4, t5, t6, t7 = st.tabs([
    "📝 ثبت گزارش",
    "🍅 پومودورو",
    "🔮 پیش‌بینی رتبه",
    "⚔️ اتاق جنگ",
    "📈 تحلیل‌ها",
    "🏆 دستاوردها",
    "⚙️ تنظیمات",
])


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۲۰. شروع تب اول — فرم ثبت گزارش
# (ادامه در پرامپت بعدی)
# ═══════════════════════════════════════════════════════════════════════════

with t1:
    st.markdown("### 📝 ثبت گزارش کار روزانه")
    st.markdown("""
    <div class="glass-card" style="font-size:13.5px; color:#cbd5e1;">
    🎯 پارت‌های مطالعه امروزت رو با جزئیات ثبت کن. سیستم XP، DDI و مدال‌ها رو
    به‌صورت خودکار محاسبه می‌کنه.
    </div>
    """, unsafe_allow_html=True)

    # ─── تاریخ و رضایت ───
    cd1, cd2 = st.columns(2)
    rep_date = cd1.date_input("📅 تاریخ:", datetime.date.today())
    satisfaction = cd2.slider("⭐️ کیفیت مطالعه (۱ تا ۱۰):", 1, 10, 8)

    st.markdown("#### 📚 ریز پارت‌های درسی")
    num_slots = st.number_input(
        "تعداد پارت‌های مطالعه:",
        min_value=1, max_value=MAX_PARTS, value=3,
        key="numparts",
    )

    # ═══════════════════════════════════════════════════════════
    # ادامه این بخش (حلقه پارت‌ها، ذخیره دیتابیس، کارت‌ها)
    # در پرامپت بعدی نوشته می‌شود.
    # ═══════════════════════════════════════════════════════════

    st.info("📌 **نیمه دوم کد در پرامپت بعدی** شامل: حلقه ثبت پارت‌ها، ذخیره در دیتابیس، کارت‌های HTML، پومودورو کامل، پیش‌بینی رتبه، اتاق جنگ، تحلیل‌ها، دستاوردها و تنظیمات.")

# ═══════════════════════════════════════════════════════════════════════════
# پایان نیمه اول
# ═══════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۲۰. تکمیل تب اول — حلقه پارت‌های درسی
# ═══════════════════════════════════════════════════════════════════════════

with t1:
    # (بخش بالای تب قبلاً نوشته شد)

    # ─── متغیرهای تجمعی ───
    total_tests = 0
    total_correct = 0
    total_wrong = 0
    total_minutes = 0
    parts_summary = []
    parts_data = []
    error_data = []

    # ─── حلقه پارت‌ها ───
    for i in range(int(num_slots)):
        with st.expander(
            f"📌 پارت درسی {i+1}",
            expanded=(i == 0),
        ):
            # ─── انتخاب درس و نوع تست ───
            cs1, cs2 = st.columns([2, 1])
            subj = cs1.selectbox(
                f"درس (پارت {i+1})",
                SUBJECTS,
                key=f"s_{i}"
            )
            if subj == "سایر":
                subj = cs1.text_input("نام درس انتخابی:", key=f"cs_{i}")

            test_type = cs2.radio(
                "نوع تست",
                ["آموزشی", "زمان‌دار"],
                horizontal=True,
                key=f"tt_{i}"
            )

            # ─── انتخاب ساعت شروع و پایان با مودال ───
            ct1, ct2 = st.columns(2)
            with ct1:
                st_t = time_picker_trigger(
                    "ساعت شروع",
                    f"st_{i}",
                    default_h=8, default_m=0
                )
            with ct2:
                et_t = time_picker_trigger(
                    "ساعت پایان",
                    f"et_{i}",
                    default_h=9, default_m=30
                )

            # ─── محاسبه مدت ───
            start_dt = datetime.datetime.combine(datetime.date.today(), st_t)
            end_dt = datetime.datetime.combine(datetime.date.today(), et_t)
            dur = (end_dt - start_dt).total_seconds() / 60
            if dur <= 0:
                dur += 24 * 60
            total_minutes += dur

            hrs = int(dur // 60)
            mins = int(dur % 60)

            st.markdown(
                f"""<div style="background:rgba(74,222,128,.12);
                border-right:3px solid #4ade80;
                padding:10px 14px; border-radius:10px;
                margin:10px 0; font-size:13.5px;">
                ⏱️ مدت این پارت:
                <b style="color:#4ade80;">{hrs} ساعت و {mins} دقیقه</b>
                </div>""",
                unsafe_allow_html=True
            )

            # ─── منابع مطالعه ───
            csrc1, csrc2 = st.columns(2)
            src_study = csrc1.text_input(
                "📖 منبع درسنامه",
                key=f"src_s_{i}",
                placeholder="مثلاً: خیلی سبز، الگو"
            )
            src_test = csrc2.text_input(
                "📝 منبع تست",
                key=f"src_t_{i}",
                placeholder="مثلاً: آزمون گاج"
            )

            # ─── آمار تست ───
            st.caption("آمار تست‌ها:")
            tc1, tc2, tc3, tc4 = st.columns(4)
            c_val = tc1.number_input(
                "✅ صحیح",
                min_value=0, value=0,
                key=f"c_{i}"
            )
            w_val = tc2.number_input(
                "❌ غلط",
                min_value=0, value=0,
                key=f"w_{i}"
            )
            b_val = tc3.number_input(
                "⭕ نزده",
                min_value=0, value=0,
                key=f"u_{i}"
            )
            d_val = tc4.number_input(
                "❔ شک‌دار",
                min_value=0, value=0,
                key=f"d_{i}"
            )

            # ─── جعبه سیاه اشتباهات ───
            err_tag = None
            if w_val > 0:
                st.markdown("##### 🎯 جعبه سیاه اشتباهات (Smart Error Vault)")
                st.caption(
                    "علت اصلی غلط‌ها رو تگ کن تا AI Coach الگوی اشتباهاتت رو کشف کنه"
                )
                err_tag = st.selectbox(
                    f"علت اصلی غلط‌های {subj}:",
                    ERROR_TAGS,
                    key=f"err_{i}"
                )

            # ─── توضیحات ───
            notes = st.text_input(
                "📝 مبحث و توضیحات این پارت:",
                key=f"nt_{i}",
                placeholder="مثلاً: فصل ۳ - تنظیم عصبی"
            )

            # ─── محاسبات این پارت ───
            s_tests = c_val + w_val + b_val
            total_tests += s_tests
            total_correct += c_val
            total_wrong += w_val

            parts_summary.append(
                f"{i+1}. {subj} "
                f"({st_t.strftime('%H:%M')}-{et_t.strftime('%H:%M')}) | "
                f"{s_tests} تست ({c_val}✅/{w_val}❌)"
            )

            parts_data.append({
                'subject': subj,
                'minutes': dur,
                'tests': s_tests,
                'correct': c_val,
                'wrong': w_val,
                'blank': b_val,
                'doubt': d_val,
                'start_hour': st_t.hour,
                'end_hour': et_t.hour,
                'study_source': src_study,
                'test_source': src_test,
                'notes': notes,
            })

            if err_tag and w_val > 0:
                error_data.append({
                    'subject': subj,
                    'tag': err_tag,
                    'count': w_val,
                })

    # ═══════════════════════════════════════════════════════════
    # ▌ بخش اسکرین‌تایم و DDI
    # ═══════════════════════════════════════════════════════════

    st.markdown("---")
    st.markdown("#### 📱 کنترل مصرف تلفن همراه")

    sc1, sc2 = st.columns(2)
    screen_t = sc1.text_input(
        "کل مصرف گوشی امروز:",
        "۲:۱۵",
        help="مثلاً: ۲:۱۵ (۲ ساعت و ۱۵ دقیقه)"
    )
    social_t = sc2.text_input(
        "شبکه‌های اجتماعی:",
        "۴۵ دقیقه",
        help="مثلاً: ۴۵ دقیقه یا ۱:۳۰"
    )

    # ─── محاسبات نهایی ───
    study_hours = round(total_minutes / 60, 2)
    overall_perc = calculate_percentage(
        total_correct, total_wrong, total_tests - total_correct - total_wrong
    )
    ddi_val, ddi_lvl = compute_ddi(study_hours, social_t)

    # ─── نمایش DDI زنده ───
    st.markdown(ddi_badge_html(ddi_val, ddi_lvl), unsafe_allow_html=True)

    # ─── پیش‌بینی XP ───
    xp_today = calculate_session_xp(
        study_hours, total_tests, total_correct
    )

    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:13px; color:#94a3b8;">
            📊 پیش‌بینی امروز
        </div>
        <div style="font-size:22px; font-weight:900;
                    color:#38bdf8; margin-top:10px;">
            ⏳ {study_hours} ساعت &nbsp;•&nbsp;
            📝 {total_tests} تست &nbsp;•&nbsp;
            🎯 {overall_perc}%
        </div>
        <div style="margin-top:12px; font-size:17px;
                    font-weight:800; color:#facc15;">
            ⚡ +{xp_today:,} XP کسب خواهی کرد
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─── نمودار زنده سبد مطالعاتی ───
    if parts_data:
        live_df = pd.DataFrame(parts_data)
        live_df = live_df[live_df['minutes'] > 0]

        if not live_df.empty:
            st.markdown("#### 🍩 سبد مطالعاتی امروز")
            d1, d2 = st.columns(2)

            with d1:
                fig_donut = px.pie(
                    live_df,
                    names='subject',
                    values='minutes',
                    hole=0.55,
                    title="⏱️ سهم دروس بر اساس زمان",
                    color='subject',
                    color_discrete_map=SUBJECT_COLORS,
                )
                fig_donut.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                )
                fig_donut.update_layout(
                    template="plotly_dark",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font={'family': 'Vazirmatn'},
                    showlegend=False,
                    height=340,
                )
                st.plotly_chart(fig_donut, use_container_width=True)

            with d2:
                radar_df = live_df.groupby('subject')['tests'].sum().reset_index()
                if not radar_df.empty and radar_df['tests'].sum() > 0:
                    fig_radar = go.Figure()
                    fig_radar.add_trace(go.Scatterpolar(
                        r=radar_df['tests'],
                        theta=radar_df['subject'],
                        fill='toself',
                        fillcolor='rgba(56,189,248,0.25)',
                        line=dict(color='#38bdf8', width=2),
                        name='تست',
                    ))
                    fig_radar.update_layout(
                        polar=dict(
                            bgcolor='rgba(15,23,42,0.5)',
                            radialaxis=dict(
                                visible=True,
                                gridcolor='rgba(56,189,248,0.2)',
                                color='#94a3b8',
                            ),
                            angularaxis=dict(
                                gridcolor='rgba(56,189,248,0.2)',
                                color='#e2e8f0',
                            ),
                        ),
                        template="plotly_dark",
                        showlegend=False,
                        height=340,
                        paper_bgcolor='rgba(0,0,0,0)',
                        font={'family': 'Vazirmatn'},
                    )
                    st.plotly_chart(fig_radar, use_container_width=True)
                else:
                    st.info("📊 برای نمایش رادار، باید تست ثبت کنی")

    # ═══════════════════════════════════════════════════════════
    # ▌ ثبت نهایی گزارش
    # ═══════════════════════════════════════════════════════════

    st.markdown("---")

    col_save, col_info = st.columns([2, 1])
    with col_info:
        st.caption(
            f"📊 {len(parts_data)} پارت • "
            f"{study_hours} ساعت • "
            f"{total_tests} تست"
        )

    with col_save:
        if st.button(
            "💾 ثبت نهایی گزارش در دیتابیس",
            use_container_width=True,
            type="primary",
        ):
            if study_hours <= 0 and total_tests == 0:
                st.warning("⚠️ باید حداقل یک پارت با زمان یا تست ثبت کنی")
            else:
                try:
                    c = db_cursor()

                    # ─── بررسی تکراری نبودن ───
                    c.execute(
                        "SELECT id FROM reports WHERE username=? AND report_date=?",
                        (USERNAME, rep_date)
                    )
                    existing = c.fetchone()

                    if existing:
                        # بروزرسانی گزارش موجود
                        report_id = existing[0]
                        c.execute('''
                            UPDATE reports SET
                                satisfaction=?, study_hours=?, total_tests=?,
                                correct_tests=?, wrong_tests=?, percentage=?,
                                screen_time=?, social_time=?, details=?,
                                xp_earned=?, ddi=?
                            WHERE id=?
                        ''', (
                            satisfaction, study_hours, total_tests,
                            total_correct, total_wrong, overall_perc,
                            screen_t, social_t, "\n".join(parts_summary),
                            xp_today, ddi_val, report_id
                        ))
                        # پاک کردن پارت‌های قدیمی
                        c.execute("DELETE FROM parts WHERE report_id=?", (report_id,))
                        c.execute("DELETE FROM error_vault WHERE report_id=?", (report_id,))
                        st.info("ℹ️ گزارش امروز بروزرسانی شد")
                    else:
                        # ثبت گزارش جدید
                        c.execute('''
                            INSERT INTO reports (
                                username, report_date, satisfaction, study_hours,
                                total_tests, correct_tests, wrong_tests, percentage,
                                screen_time, social_time, details, xp_earned, ddi
                            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                        ''', (
                            USERNAME, rep_date, satisfaction, study_hours,
                            total_tests, total_correct, total_wrong, overall_perc,
                            screen_t, social_t, "\n".join(parts_summary),
                            xp_today, ddi_val
                        ))
                        report_id = c.lastrowid
                        st.success(f"✅ گزارش ذخیره شد! (+{xp_today:,} XP)")

                    # ─── ذخیره پارت‌ها ───
                    for p in parts_data:
                        c.execute('''
                            INSERT INTO parts (
                                report_id, username, report_date, subject,
                                minutes, tests, correct, wrong,
                                start_hour, end_hour, study_source,
                                test_source, notes
                            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                        ''', (
                            report_id, USERNAME, rep_date, p['subject'],
                            p['minutes'], p['tests'], p['correct'], p['wrong'],
                            p['start_hour'], p['end_hour'], p['study_source'],
                            p['test_source'], p['notes']
                        ))

                    # ─── ذخیره اشتباهات ───
                    for e in error_data:
                        c.execute('''
                            INSERT INTO error_vault (
                                report_id, username, report_date,
                                subject, error_tag, count
                            ) VALUES (?,?,?,?,?,?)
                        ''', (
                            report_id, USERNAME, rep_date,
                            e['subject'], e['tag'], e['count']
                        ))

                    db_commit()

                    # ─── بررسی مدال‌ها ───
                    report_obj = {
                        'total_tests': total_tests,
                        'study_hours': study_hours,
                        'percentage': overall_perc,
                        'screen_time': screen_t,
                        'social_time': social_t,
                    }
                    new_badges = check_and_unlock_badges(
                        USERNAME, report_obj, parts_data
                    )

                    # ─── جشن ───
                    st.balloons()

                    if new_badges:
                        badge_html = "".join([
                            f'<span class="badge-ach unlocked" '
                            f'style="display:inline-block; margin:4px;">'
                            f'{BADGES[b][0]} {BADGES[b][1]}</span>'
                            for b in new_badges
                        ])
                        st.markdown(f"""
                        <div class="glass-card"
                             style="border-color:#facc15;
                                    animation: popIn 0.8s ease;">
                            <h3 style="color:#facc15 !important;">
                                🎉 {len(new_badges)} مدال جدید باز شد!
                            </h3>
                            {badge_html}
                        </div>
                        """, unsafe_allow_html=True)

                    # ─── ذخیره در session برای کارت ───
                    st.session_state['last_report'] = {
                        'date': str(rep_date),
                        'satisfaction': satisfaction,
                        'hours': study_hours,
                        'tests': total_tests,
                        'perc': overall_perc,
                        'screen': screen_t,
                        'social': social_t,
                        'ddi': ddi_val,
                        'ddi_lvl': ddi_lvl,
                        'xp_today': xp_today,
                        'new_badges': new_badges,
                        'parts_summary': parts_summary,
                        'correct': total_correct,
                        'wrong': total_wrong,
                    }

                    st.rerun()

                except Exception as e:
                    st.error(f"❌ خطا در ذخیره: {e}")

    # ═══════════════════════════════════════════════════════════
    # ▌ بخش کارت‌های تصویری و اشتراک
    # ═══════════════════════════════════════════════════════════

    st.markdown("---")
    st.markdown("#### 🖼️ کارنامه‌های تصویری و اشتراک‌گذاری")

    co1, co2 = st.columns(2)

    # ─── کارنامه عادی ───
    with co1:
        st.caption("📄 کارنامه عادی (۱۰۰۰×۷۰۰)")
        try:
            card_html = render_html_report_card(
                USER_NAME,
                str(rep_date),
                satisfaction,
                study_hours,
                total_tests,
                overall_perc,
                screen_t,
                ddi_val,
                ddi_lvl,
                cur_lvl[1],
                total_xp + xp_today,
                streak,
                card_id="main_card",
            )
            components.html(card_html, height=850, scrolling=False)
        except Exception as e:
            st.error(f"خطا در تولید کارت: {e}")

    # ─── کارنامه استوری ───
    with co2:
        st.caption("📱 کارنامه استوری (۱۰۸۰×۱۹۲۰)")
        try:
            last_rep = st.session_state.get('last_report') or {}
            badges_for_story = last_rep.get('new_badges', [])

            story_html = render_html_story_card(
                USER_NAME,
                str(rep_date),
                study_hours,
                total_tests,
                overall_perc,
                ddi_val,
                ddi_lvl,
                cur_lvl[1],
                xp_today,
                streak,
                badges_for_story,
                story_id="story_card",
            )
            components.html(story_html, height=900, scrolling=True)
        except Exception as e:
            st.error(f"خطا در تولید استوری: {e}")

    # ─── متن گزارش برای تلگرام ───
    st.markdown("#### 📤 متن آماده برای اشتراک‌گذاری")

    report_text = f"""📊 گزارش کار | آکادمی ۲۰
━━━━━━━━━━━━━━━━━━━━
👤 دانش‌آموز: {USER_NAME}
🎮 سطح: {cur_lvl[2]} {cur_lvl[1]}
⚡ XP امروز: +{xp_today:,}
📅 تاریخ: {rep_date}
⭐ رضایت: {satisfaction}/10
━━━━━━━━━━━━━━━━━━━━
⏳ مطالعه: {study_hours} ساعت
📝 تست‌ها: {total_tests}
   ✅ صحیح: {total_correct}
   ❌ غلط: {total_wrong}
🎯 درصد خالص: {overall_perc}%
━━━━━━━━━━━━━━━━━━━━
📱 اسکرین‌تایم: {screen_t}
📲 شبکه اجتماعی: {social_t}
💎 DDI: {ddi_val}%
🔥 زنجیره: {streak} روز
━━━━━━━━━━━━━━━━━━━━
📚 ریز پارت‌ها:
""" + "\n".join(parts_summary) + f"""
━━━━━━━━━━━━━━━━━━━━
👨‍🏫 مشاور: دکتر خشایار اشکبوس
📱 @Kh_Ashkboos"""

    st.text_area(
        "متن گزارش:",
        report_text,
        height=250,
        key="report_text_area",
    )

    # ─── دکمه‌های اشتراک ───
    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        tg_url = "https://t.me/share/url?url=" + urllib.parse.quote(report_text)
        st.markdown(
            f'<a href="{tg_url}" target="_blank" class="tg-button">'
            f'🚀 ارسال به تلگرام مشاور</a>',
            unsafe_allow_html=True,
        )

    with btn_col2:
        wa_url = "https://wa.me/?text=" + urllib.parse.quote(report_text)
        st.markdown(
            f'''<a href="{wa_url}" target="_blank"
            style="display:block; width:100%; text-align:center;
            background:linear-gradient(90deg,#25d366,#128c7e);
            color:#fff !important; font-size:16px; font-weight:800;
            padding:14px; border-radius:12px; text-decoration:none;
            margin-top:15px; box-shadow:0 6px 18px rgba(37,211,102,0.45);">
            💬 ارسال به واتساپ</a>''',
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۲۱. تب دوم — پومودورو کامل
# ═══════════════════════════════════════════════════════════════════════════

with t2:
    st.markdown("### 🍅 تایمر پومودورو و استاپ‌واچ کنکوری")

    st.markdown("""
    <div class="glass-card" style="font-size:13.5px; color:#cbd5e1;">
        🎯 <b>روش پومودورو:</b> ۲۵ دقیقه تمرکز عمیق + ۵ دقیقه استراحت.
        این روش برای مطالعه‌ی مؤثر و جلوگیری از فرسودگی ذهنی طراحی شده.<br>
        ⚡ <b>تست سرعتی:</b> ۱۰ دقیقه، برای تمرین سرعت تست‌زنی.<br>
        🧘 <b>تمرکز طولانی:</b> ۵۰ دقیقه، برای مباحث سنگین.<br>
        🌙 <b>شبانه:</b> ۴۵ دقیقه، برای مرور شب قبل از خواب.
    </div>
    """, unsafe_allow_html=True)

    # ─── انتخاب حالت ───
    col_mode1, col_mode2 = st.columns([3, 1])

    with col_mode1:
        mode = st.radio(
            "حالت تمرکز:",
            list(POMO_MODES.keys()),
            key="pomo_mode",
            horizontal=True,
        )

    with col_mode2:
        custom_min = st.number_input(
            "یا دقیقه دلخواه:",
            min_value=1, max_value=180, value=25,
            key="pomo_custom",
        )

    # ─── تعیین مدت ───
    if mode in POMO_MODES:
        selected_dur = POMO_MODES[mode]
        st.session_state.pomo['mode'] = mode
    else:
        selected_dur = custom_min * 60

    st.session_state.pomo['duration'] = selected_dur

    # ─── نمایش تایمر ───
    if HAS_FRAG:
        render_timer_fragment()
    else:
        p = st.session_state.pomo
        rem = (
            max(0, int((p['end_time'] - datetime.datetime.now()).total_seconds()))
            if p['running'] and p['end_time']
            else p.get('last_remaining', selected_dur)
        )
        m, s = divmod(rem, 60)
        st.markdown(
            f'<div class="pomodoro-box">'
            f'<div class="pomo-time">{m:02d}:{s:02d}</div>'
            f'<div class="pomo-label">'
            f'{"🔥 در حال اجرا" if p["running"] else "⏸️ آماده شروع"}'
            f'</div></div>',
            unsafe_allow_html=True,
        )

    # ─── کنترل‌ها ───
    render_pomodoro_controls()

    # ─── آمار پومودورو ───
    st.markdown("---")
    st.markdown("#### 📊 آمار جلسات پومودورو")

    try:
        pomo_stats = pd.read_sql_query(
            """SELECT
                COUNT(*) as total_sessions,
                SUM(duration_minutes) as total_minutes,
                AVG(duration_minutes) as avg_minutes
            FROM pomodoro_sessions
            WHERE username=? AND session_date >= ?""",
            DB_CONN,
            params=(USERNAME, (datetime.date.today() - datetime.timedelta(days=30)).isoformat()),
        )

        if not pomo_stats.empty and pomo_stats['total_sessions'].iloc[0]:
            total_sess = int(pomo_stats['total_sessions'].iloc[0])
            total_min = int(pomo_stats['total_minutes'].iloc[0] or 0)
            avg_min = float(pomo_stats['avg_minutes'].iloc[0] or 0)

            ps1, ps2, ps3 = st.columns(3)
            with ps1:
                st.markdown(f"""
                <div class="metric-card">
                    <span class="metric-icon">🍅</span>
                    <div class="metric-num">{total_sess}</div>
                    <div class="metric-txt">تعداد جلسات ۳۰ روز</div>
                </div>
                """, unsafe_allow_html=True)
            with ps2:
                hours = total_min / 60
                st.markdown(f"""
                <div class="metric-card">
                    <span class="metric-icon">⏱️</span>
                    <div class="metric-num">{hours:.1f}</div>
                    <div class="metric-txt">ساعت پومودورو</div>
                </div>
                """, unsafe_allow_html=True)
            with ps3:
                st.markdown(f"""
                <div class="metric-card">
                    <span class="metric-icon">📈</span>
                    <div class="metric-num">{avg_min:.0f}</div>
                    <div class="metric-txt">میانگین دقیقه</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("💡 هنوز جلسه پومودورو کامل نکردی")
    except Exception:
        st.info("💡 آمار در دسترس نیست")

    # ─── نمودار جلسات اخیر ───
    try:
        pomo_daily = pd.read_sql_query(
            """SELECT
                session_date,
                COUNT(*) as sessions,
                SUM(duration_minutes) as minutes
            FROM pomodoro_sessions
            WHERE username=? AND session_date >= ?
            GROUP BY session_date
            ORDER BY session_date ASC""",
            DB_CONN,
            params=(USERNAME, (datetime.date.today() - datetime.timedelta(days=14)).isoformat()),
        )

        if not pomo_daily.empty:
            fig_pomo = px.bar(
                pomo_daily,
                x='session_date',
                y='sessions',
                title="📊 جلسات پومودورو ۱۴ روز اخیر",
                labels={'sessions': 'تعداد جلسات', 'session_date': 'تاریخ'},
                color='sessions',
                color_continuous_scale=['#0ea5e9', '#7c3aed', '#f472b6'],
            )
            fig_pomo.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font={'family': 'Vazirmatn'},
                coloraxis_showscale=False,
                height=320,
            )
            st.plotly_chart(fig_pomo, use_container_width=True)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۲۲. تب سوم — پیش‌بینی رتبه
# ═══════════════════════════════════════════════════════════════════════════

with t3:
    st.markdown("### 🔮 شبیه‌ساز تراز و تخمین رتبه زنده")

    st.markdown("""
    <div class="glass-card" style="font-size:13.5px; color:#cbd5e1;">
        🤖 بر اساس میانگین ۳۰ روز اخیر شما (ساعت مطالعه + حجم تست + درصد خالص)،
        یک بازه‌ی احتمالی رتبه‌ی کنکور با استفاده از مدل رگرسیون سبک تخمین زده می‌شود.
        <br><br>
        <b style="color:#facc15;">⚠️ توجه:</b> این تخمین صرفاً آموزشی است
        و جایگزین آزمون‌های آزمایشی واقعی نمی‌شود.
    </div>
    """, unsafe_allow_html=True)

    if df_all.empty:
        st.info("⚠️ برای فعال شدن این بخش، حداقل یک گزارش ثبت کن.")
    else:
        # ─── فیلتر بازه ۳۰ روز ───
        df30 = df_all[
            pd.to_datetime(df_all['report_date']) >=
            pd.Timestamp(datetime.date.today() - datetime.timedelta(days=30))
        ]

        if df30.empty:
            st.warning("⚠️ در ۳۰ روز اخیر گزارشی نداری. از کل داده‌ها استفاده می‌شود.")
            df30 = df_all

        # ─── میانگین‌ها ───
        ah = df30['study_hours'].mean()
        at = df30['total_tests'].mean()
        ap = df30['percentage'].mean()

        # ─── پیش‌بینی ───
        traz, rlo, rmid, rhi, comp = predict_rank(ah, at, ap)
        tier, tcol = rank_tier(rmid)

        # ─── کارت‌های اصلی ───
        cA, cB = st.columns(2)

        with cA:
            st.markdown(f"""
            <div class="rank-card" style="text-align:center;">
                <div style="font-size:13px; color:#94a3b8;">
                    🎯 بازه احتمالی رتبه (۳۰ روز اخیر)
                </div>
                <div class="rank-number" style="margin:18px 0;">
                    {rlo:,} - {rhi:,}
                </div>
                <div class="rank-label">
                    مرکز تخمین:
                    <b style="color:#38bdf8;">{rmid:,}</b>
                </div>
                <div style="margin-top:18px;
                            font-size:19px; font-weight:900;
                            color:{tcol};">
                    {tier}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with cB:
            st.markdown(f"""
            <div class="rank-card"
                 style="text-align:center;
                        border-color:rgba(56,189,248,.4);">
                <div style="font-size:13px; color:#94a3b8;">
                    📈 تراز تخمینی
                </div>
                <div class="rank-number" style="margin:18px 0;">
                    {traz:,}
                </div>
                <div class="rank-label">از ۱۰,۰۰۰</div>
                <div style="margin-top:18px;
                            font-size:13px; color:#94a3b8;">
                    امتیاز ترکیبی:
                    <b style="color:#facc15;">{comp*100:.1f}%</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ─── میانگین‌های ورودی ───
        st.markdown("#### 📊 داده‌های پایه (میانگین ۳۰ روز)")
        m1, m2, m3 = st.columns(3)

        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-icon">⏳</span>
                <div class="metric-num">{ah:.1f}</div>
                <div class="metric-txt">میانگین ساعت روزانه</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-icon">📝</span>
                <div class="metric-num">{at:.0f}</div>
                <div class="metric-txt">میانگین تست روزانه</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-icon">🎯</span>
                <div class="metric-num">{ap:.1f}%</div>
                <div class="metric-txt">میانگین درصد خالص</div>
            </div>
            """, unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════
        # ▌ شبیه‌سازی سناریوهای What-If
        # ═══════════════════════════════════════════════════════════
        st.markdown("---")
        st.markdown("#### 🎮 شبیه‌سازی «چی می‌شه اگر...»")
        st.caption(
            "ببین اگه این هفته تلاشت رو تغییر بدی، رتبه‌ت چقدر جابجا می‌شه!"
        )

        scenarios = [
            (0, 0, 0, "📍 وضعیت فعلی", "#38bdf8"),
            (0.5, 10, 2, "📈 کمی بهتر", "#4ade80"),
            (1.0, 20, 5, "🚀 جدی‌تر", "#22d3ee"),
            (1.5, 35, 8, "🔥 حالت حرفه‌ای", "#facc15"),
            (2.0, 50, 12, "💎 منطقه المپیک", "#f472b6"),
        ]

        scen_data = []
        for dh, dt, dp, lbl, col in scenarios:
            nh = min(ah + dh, 14)
            nt = min(at + dt, 250)
            np_ = min(ap + dp, 100)

            _, rl2, rm2, rh2, _ = predict_rank(nh, nt, np_)
            diff = rmid - rm2
            diff_txt = f"{diff:+,}" if diff != 0 else "—"

            scen_data.append({
                'سناریو': lbl,
                'ساعت': round(nh, 1),
                'تست': int(nt),
                'درصد': round(np_, 1),
                'رتبه تخمینی': f"{rl2:,} - {rh2:,}",
                'تغییر': diff_txt,
                'color': col,
                '_rmid': rm2,
                '_rlo': rl2,
                '_rhi': rh2,
            })

        # جدول سناریوها
        scen_df = pd.DataFrame([
            {k: v for k, v in s.items() if not k.startswith('_') and k != 'color'}
            for s in scen_data
        ])
        st.dataframe(
            scen_df,
            use_container_width=True,
            hide_index=True,
        )

        # نمودار سناریوها
        fig_what = go.Figure()
        for s in scen_data:
            fig_what.add_trace(go.Bar(
                x=[s['سناریو']],
                y=[s['_rmid']],
                name=s['سناریو'],
                marker_color=s['color'],
                text=[f"{s['_rmid']:,}"],
                textposition='outside',
                error_y=dict(
                    type='data',
                    symmetric=False,
                    array=[s['_rhi'] - s['_rmid']],
                    arrayminus=[s['_rmid'] - s['_rlo']],
                    color=s['color'],
                    thickness=1.5,
                    width=8,
                ),
                showlegend=False,
            ))

        fig_what.update_layout(
            title="📊 تخمین رتبه در سناریوهای مختلف (کمتر = بهتر)",
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font={'family': 'Vazirmatn'},
            yaxis_title="رتبه تخمینی",
            yaxis_autorange="reversed",
            height=420,
        )
        st.plotly_chart(fig_what, use_container_width=True)

        # ═══════════════════════════════════════════════════════════
        # ▌ روند رتبه در طول زمان
        # ═══════════════════════════════════════════════════════════
        st.markdown("---")
        st.markdown("#### 📉 روند رتبه تخمینی شما (روز به روز)")

        dfs = df_all.sort_values('report_date').copy()
        dfs['date'] = pd.to_datetime(dfs['report_date'])
        dfs['predicted_rank'] = [
            predict_rank(r['study_hours'], r['total_tests'], r['percentage'])[2]
            for _, r in dfs.iterrows()
        ]

        # محاسبه میانگین متحرک ۷ روز
        dfs['ma7'] = dfs['predicted_rank'].rolling(window=7, min_periods=1).mean()

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=dfs['date'],
            y=dfs['predicted_rank'],
            mode='markers+lines',
            name='رتبه تخمینی',
            line=dict(color='#a78bfa', width=2),
            marker=dict(size=8, color='#a78bfa',
                        line=dict(width=2, color='#0b0f19')),
        ))
        fig_trend.add_trace(go.Scatter(
            x=dfs['date'],
            y=dfs['ma7'],
            mode='lines',
            name='میانگین ۷ روز',
            line=dict(color='#facc15', width=3, dash='dash'),
        ))

        fig_trend.update_layout(
            title="📊 روند رتبه تخمینی در طول زمان",
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font={'family': 'Vazirmatn'},
            yaxis_title="رتبه تخمینی",
            yaxis_autorange="reversed",
            hovermode='x unified',
            height=420,
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        # ═══════════════════════════════════════════════════════════
        # ▌ تحلیل پیشرفته
        # ═══════════════════════════════════════════════════════════
        st.markdown("---")
        st.markdown("#### 🤖 تحلیل هوشمند رتبه")

        # محاسبه بهترین و بدترین روز
        best_idx = dfs['predicted_rank'].idxmin()
        worst_idx = dfs['predicted_rank'].idxmax()
        best_day = dfs.loc[best_idx]
        worst_day = dfs.loc[worst_idx]

        st.markdown(f"""
        <div class="ai-coach">
            <div class="ai-tip success">
                🏆 <b>بهترین روز:</b>
                {best_day['date'].strftime('%Y/%m/%d')} با رتبه تخمینی
                <b style="color:#4ade80;">{best_day['predicted_rank']:,}</b>
                ({best_day['study_hours']:.1f} ساعت - {best_day['total_tests']} تست)
            </div>
            <div class="ai-tip warning">
                📉 <b>ضعیف‌ترین روز:</b>
                {worst_day['date'].strftime('%Y/%m/%d')} با رتبه تخمینی
                <b style="color:#facc15;">{worst_day['predicted_rank']:,}</b>
                ({worst_day['study_hours']:.1f} ساعت - {worst_day['total_tests']} تست)
            </div>
            <div class="ai-tip info">
                📊 <b>اختلاف بهترین و ضعیف‌ترین:</b>
                {int(best_day['predicted_rank'] - worst_day['predicted_rank']):,} رتبه
                — این نشون می‌ده ثباتت چقدر مهمه!
            </div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۲۳. تب چهارم — اتاق جنگ (Arena)
# ═══════════════════════════════════════════════════════════════════════════

with t4:
    st.markdown("### ⚔️ اتاق جنگ — دو﻿ئل دوستانه کنکوری")

    st.markdown("""
    <div class="glass-card" style="font-size:13.5px; color:#cbd5e1;">
        🔥 با دوستات <b>اتاق مطالعه گروهی</b> بساز، اسم مستعار بذار
        و در <b>لیدربورد هفتگی</b> با هم رقابت کن!
        <br>
        🎯 امتیاز بر اساس: ساعت مطالعه × ۵۰ + تعداد تست × ۲ + تست صحیح × ۱
    </div>
    """, unsafe_allow_html=True)

    # ─── اتاق‌های کاربر ───
    try:
        my_rooms = get_user_rooms(USERNAME)
    except Exception:
        my_rooms = pd.DataFrame()

    # ─── دو ستون: ساخت و پیوستن ───
    a1, a2 = st.columns(2)

    with a1:
        st.markdown("##### 🏗️ ساخت اتاق جدید")
        new_room_name = st.text_input(
            "اسم اتاق:",
            placeholder="مثلاً: جنگجویان پزشکی ۱۴۰۵",
            key="new_room_name",
        )
        new_nickname = st.text_input(
            "اسم مستعار خودت:",
            placeholder="مثلاً: دکتر X",
            key="new_nick",
            max_chars=20,
        )

        if st.button("✨ ساخت اتاق", use_container_width=True):
            if not new_room_name or not new_nickname:
                st.warning("همه فیلدها را پر کن")
            else:
                try:
                    # تولید کد یکتا
                    code = (
                        f"{random.randint(1000, 9999)}-"
                        f"{random.choice('ABCDEFGHJK')}"
                        f"{random.choice('ABCDEFGHJK')}"
                    )

                    c = db_cursor()
                    c.execute(
                        "INSERT INTO arena_rooms (code, name, created_by) VALUES (?,?,?)",
                        (code, new_room_name, USERNAME),
                    )
                    c.execute(
                        "INSERT INTO arena_members (code, username, nickname) VALUES (?,?,?)",
                        (code, USERNAME, new_nickname),
                    )
                    db_commit()

                    st.success(f"🎉 اتاق ساخته شد! کد دعوت: `{code}`")
                    st.info("📋 کد رو به دوستات بده تا بهت ملحق بشن")
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"خطا: {e}")

    with a2:
        st.markdown("##### 🎟️ پیوستن به اتاق")
        join_code = st.text_input(
            "کد اتاق:",
            key="join_code",
            placeholder="1234-AB",
        ).strip()
        join_nick = st.text_input(
            "اسم مستعار خودت:",
            key="join_nick",
            max_chars=20,
        )

        if st.button("🚀 پیوستن به اتاق", use_container_width=True):
            if not join_code or not join_nick:
                st.warning("همه فیلدها را پر کن")
            else:
                try:
                    c = db_cursor()
                    c.execute(
                        "SELECT name FROM arena_rooms WHERE code=?",
                        (join_code,),
                    )
                    r = c.fetchone()

                    if not r:
                        st.error("❌ اتاق پیدا نشد. کد رو چک کن.")
                    else:
                        try:
                            c.execute(
                                "INSERT INTO arena_members (code, username, nickname) "
                                "VALUES (?,?,?)",
                                (join_code, USERNAME, join_nick),
                            )
                            db_commit()
                            st.success(f"🎉 به «{r[0]}» پیوستی!")
                            st.balloons()
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.info("ℹ️ قبلاً عضو این اتاق بودی")
                except Exception as e:
                    st.error(f"خطا: {e}")

    # ═══════════════════════════════════════════════════════════
    # ▌ نمایش اتاق و لیدربورد
    # ═══════════════════════════════════════════════════════════
    st.markdown("---")

    if my_rooms.empty:
        st.info("💡 هنوز توی هیچ اتاقی نیستی. یکی بساز یا به دوستت ملحق شو!")
    else:
        room_options = [
            f"{r['name']} ({r['code']}) - {r['nickname']}"
            for _, r in my_rooms.iterrows()
        ]
        selected = st.selectbox(
            "🏠 اتاق‌های تو:",
            room_options,
            key="selected_room",
        )

        sel_code = selected.split("(")[1].split(")")[0]
        lb = arena_leaderboard(sel_code, days=7)

        if lb.empty:
            st.info("اتاق خالیه")
        else:
            st.markdown(f"#### 🏆 لیدربورد ۷ روز اخیر — {selected}")

            rank_icons = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣",
                          "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

            for idx, row in lb.iterrows():
                icon = (rank_icons[idx - 1] if idx <= 10 else f"{idx}.")
                me_cls = "arena-me" if row['is_me'] else ""
                me_badge = (
                    " <span style='color:#38bdf8; font-size:11px;'>(تو)</span>"
                    if row['is_me'] else ""
                )

                st.markdown(f"""
                <div class="arena-card {me_cls}">
                    <div class="arena-rank">{icon}</div>
                    <div style="flex:1;">
                        <div style="font-weight:800; font-size:15px;">
                            {escape_html(row['nickname'])}{me_badge}
                        </div>
                        <div style="font-size:12px; color:#94a3b8;">
                            ⏳ {row['hours']} ساعت &nbsp;•&nbsp;
                            📝 {row['tests']} تست
                        </div>
                    </div>
                    <div style="font-size:18px; font-weight:900; color:#facc15;">
                        {row['score']:,}
                        <span style="font-size:11px; color:#94a3b8;">XP</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ─── نمودار مقایسه ───
            fig_lb = px.bar(
                lb.reset_index(),
                x='nickname',
                y='score',
                title="📊 مقایسه امتیاز اعضای اتاق",
                labels={'nickname': 'نام مستعار', 'score': 'امتیاز XP'},
                color='score',
                color_continuous_scale=['#0ea5e9', '#7c3aed', '#f472b6', '#facc15'],
            )
            fig_lb.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font={'family': 'Vazirmatn'},
                coloraxis_showscale=False,
                height=420,
            )
            st.plotly_chart(fig_lb, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۲۴. تب پنجم — تحلیل‌ها
# ═══════════════════════════════════════════════════════════════════════════

with t5:
    st.markdown("### 📈 داشبورد تحلیل هوشمند")

    if df_all.empty:
        st.info("⚠️ هنوز گزارشی ثبت نکرده‌ای!")
    else:
        # ─── فیلتر بازه ───
        df_all['report_date'] = pd.to_datetime(df_all['report_date'])

        cf1, cf2 = st.columns([1, 3])
        with cf1:
            tf_ = st.radio(
                "انتخاب بازه:",
                ["۷ روز اخیر", "۳۰ روز اخیر", "همه"],
                horizontal=False,
                key="analysis_range",
            )

        if "۷" in tf_:
            fdf = df_all[
                df_all['report_date'] >=
                pd.Timestamp(datetime.date.today() - datetime.timedelta(days=7))
            ]
        elif "۳۰" in tf_:
            fdf = df_all[
                df_all['report_date'] >=
                pd.Timestamp(datetime.date.today() - datetime.timedelta(days=30))
            ]
        else:
            fdf = df_all

        if fdf.empty:
            st.warning("در این بازه داده‌ای وجود نداره.")
        else:
            # ─── شاخص‌های کلیدی ───
            sh = fdf['study_hours'].sum()
            stt = fdf['total_tests'].sum()
            sc_ = fdf['correct_tests'].sum()
            sw_ = fdf['wrong_tests'].sum()
            ap = fdf['percentage'].mean()
            asat = fdf['satisfaction'].mean()
            pXP = calculate_session_xp(sh, stt, sc_)

            st.markdown(f"""
            <div style="display:grid;
                        grid-template-columns: repeat(6, 1fr);
                        gap:10px; margin-bottom:22px;">
                <div class="metric-card">
                    <span class="metric-icon">⚡</span>
                    <div class="metric-num">{pXP:,}</div>
                    <div class="metric-txt">XP بازه</div>
                </div>
                <div class="metric-card">
                    <span class="metric-icon">⏳</span>
                    <div class="metric-num">{sh:.1f}</div>
                    <div class="metric-txt">ساعت مطالعه</div>
                </div>
                <div class="metric-card">
                    <span class="metric-icon">📝</span>
                    <div class="metric-num">{stt}</div>
                    <div class="metric-txt">تعداد تست</div>
                </div>
                <div class="metric-card">
                    <span class="metric-icon">✅</span>
                    <div class="metric-num">{sc_}</div>
                    <div class="metric-txt">صحیح</div>
                </div>
                <div class="metric-card">
                    <span class="metric-icon">🎯</span>
                    <div class="metric-num">{ap:.1f}%</div>
                    <div class="metric-txt">میانگین درصد</div>
                </div>
                <div class="metric-card">
                    <span class="metric-icon">⭐</span>
                    <div class="metric-num">{asat:.1f}</div>
                    <div class="metric-txt">میانگین رضایت</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ═══════════════════════════════════════════════════════════
            # ▌ AI Coach
            # ═══════════════════════════════════════════════════════════
            st.markdown("#### 🤖 تحلیلگر هوشمند AI Coach")
            tips = ai_coach_analysis(fdf, df_all.iloc[-1].to_dict())
            tips_html = "".join([
                f'<div class="ai-tip {cls}">{txt}</div>'
                for cls, txt in tips
            ])
            st.markdown(f'<div class="ai-coach">{tips_html}</div>',
                        unsafe_allow_html=True)

            # ═══════════════════════════════════════════════════════════
            # ▌ جعبه سیاه اشتباهات
            # ═══════════════════════════════════════════════════════════
            st.markdown("#### 🎯 جعبه سیاه اشتباهات (Smart Error Vault)")

            try:
                ev = pd.read_sql_query(
                    """SELECT subject, error_tag, SUM(count) as cnt
                    FROM error_vault
                    WHERE username=?
                    GROUP BY subject, error_tag""",
                    DB_CONN,
                    params=(USERNAME,),
                )
            except Exception:
                ev = pd.DataFrame()

            if ev.empty:
                st.info("💡 تا حالا اشتباهی تگ نکردی. دفعه بعد علت غلط رو تگ کن!")
            else:
                ec1, ec2 = st.columns(2)

                with ec1:
                    # توزیع کلی
                    tag_total = ev.groupby('error_tag')['cnt'].sum().reset_index()
                    fig_et = px.pie(
                        tag_total,
                        names='error_tag',
                        values='cnt',
                        hole=0.5,
                        title="📊 توزیع کل علل غلط‌ها",
                        color_discrete_sequence=px.colors.qualitative.Bold,
                    )
                    fig_et.update_traces(
                        textposition='inside',
                        textinfo='percent+label',
                    )
                    fig_et.update_layout(
                        template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font={'family': 'Vazirmatn'},
                        showlegend=True,
                        height=420,
                    )
                    st.plotly_chart(fig_et, use_container_width=True)

                with ec2:
                    # تفکیک بر اساس درس
                    fig_es = px.bar(
                        ev,
                        x='subject',
                        y='cnt',
                        color='error_tag',
                        title="🎓 تفکیک علل غلط بر اساس درس",
                        color_discrete_sequence=px.colors.qualitative.Bold,
                    )
                    fig_es.update_layout(
                        template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font={'family': 'Vazirmatn'},
                        height=420,
                        barmode='stack',
                    )
                    st.plotly_chart(fig_es, use_container_width=True)

                # ─── تحلیل مشاور ───
                top_err = ev.groupby('error_tag')['cnt'].sum().sort_values(ascending=False)

                if len(top_err) >= 1:
                    top_name = top_err.index[0]
                    top_pct = (top_err.iloc[0] / top_err.sum()) * 100

                    if any(k in top_name for k in ["دقت", "وقت", "خواندن"]):
                        suggestion = (
                            "این یعنی مشکل تو «دانش» نیست، بلکه «اجرا»ست "
                            "— تمرین تمرکز و مدیریت زمان کن."
                        )
                    elif "فراموشی" in top_name:
                        suggestion = "روی مرور و تثبیت مباحث با فاصله‌گذاری تمرکز کن."
                    elif "دام" in top_name:
                        suggestion = "با دقت بیشتر در خواندن صورت سؤال، دام‌ها رو خنثی کن."
                    else:
                        suggestion = "روی تسلط عمیق‌تر روی مبحث کار کن."

                    st.markdown(f"""
                    <div class="ai-coach">
                        <div class="ai-tip info">
                            🧠 <b>تحلیل مشاور:</b> بیشترین علت غلط‌های تو
                            <b style="color:#facc15;">{top_name}</b> است
                            ({top_pct:.0f}٪ از کل غلط‌ها).
                            {suggestion}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # ═══════════════════════════════════════════════════════════
            # ▌ روند DDI
            # ═══════════════════════════════════════════════════════════
            st.markdown("#### 💎 شاخص تخلیه تمرکز (DDI)")

            ddi_rows = []
            for _, r in fdf.iterrows():
                dv, dl = compute_ddi(r['study_hours'], r['social_time'])
                ddi_rows.append({
                    'date': r['report_date'],
                    'ddi': dv,
                    'level': dl,
                })

            if ddi_rows:
                ddf = pd.DataFrame(ddi_rows)

                colors_map = {
                    'green': '#4ade80',
                    'yellow': '#facc15',
                    'red': '#f87171',
                }

                fig_ddi = go.Figure()

                for lv, cc in colors_map.items():
                    s = ddf[ddf['level'] == lv]
                    if not s.empty:
                        fig_ddi.add_trace(go.Scatter(
                            x=s['date'],
                            y=s['ddi'],
                            mode='markers',
                            name={'green': '💎 مغز الماسی',
                                  'yellow': '⚠️ افت دوپامین',
                                  'red': '🔥 بحرانی'}[lv],
                            marker=dict(
                                color=cc,
                                size=14,
                                line=dict(width=2, color='#0b0f19'),
                            ),
                        ))

                fig_ddi.add_hline(
                    y=DDI_GREEN_MAX,
                    line_dash="dash",
                    line_color="#4ade80",
                    annotation_text="مرز سبز (۱۰٪)",
                )
                fig_ddi.add_hline(
                    y=DDI_YELLOW_MAX,
                    line_dash="dash",
                    line_color="#f87171",
                    annotation_text="مرز قرمز (۲۵٪)",
                )

                fig_ddi.update_layout(
                    template="plotly_dark",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font={'family': 'Vazirmatn'},
                    title="📊 روند DDI روزانه — پایین‌تر = بهتر",
                    yaxis_title="DDI (%)",
                    height=420,
                    hovermode='x unified',
                )
                st.plotly_chart(fig_ddi, use_container_width=True)

            # ═══════════════════════════════════════════════════════════
            # ▌ سبد مطالعاتی (Sunburst)
            # ═══════════════════════════════════════════════════════════
            st.markdown("#### 🌞 سبد مطالعاتی ۳۰ روز اخیر")

            try:
                pd30 = pd.read_sql_query(
                    """SELECT subject, minutes, tests
                    FROM parts
                    WHERE username=? AND report_date >= ?""",
                    DB_CONN,
                    params=(USERNAME,
                            (datetime.date.today() -
                             datetime.timedelta(days=30)).isoformat()),
                )
            except Exception:
                pd30 = pd.DataFrame()

            if not pd30.empty:
                sc1, sc2 = st.columns(2)

                with sc1:
                    fs = px.sunburst(
                        pd30,
                        path=['subject'],
                        values='minutes',
                        color='minutes',
                        color_continuous_scale=['#0ea5e9', '#7c3aed', '#f472b6'],
                        title="⏱️ توزیع زمان بین دروس",
                    )
                    fs.update_layout(
                        template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)',
                        font={'family': 'Vazirmatn'},
                        height=420,
                    )
                    st.plotly_chart(fs, use_container_width=True)

                with sc2:
                    sg = (
                        pd30.groupby('subject')
                        .agg({'minutes': 'sum', 'tests': 'sum'})
                        .reset_index()
                        .sort_values('minutes', ascending=False)
                    )
                    fb = px.bar(
                        sg,
                        x='subject',
                        y='minutes',
                        color='tests',
                        title="📊 رتبه‌بندی دروس بر اساس زمان",
                        color_continuous_scale=['#38bdf8', '#f472b6'],
                    )
                    fb.update_layout(
                        template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font={'family': 'Vazirmatn'},
                        height=420,
                    )
                    st.plotly_chart(fb, use_container_width=True)

            # ═══════════════════════════════════════════════════════════
            # ▌ نمودارهای روند
            # ═══════════════════════════════════════════════════════════
            st.markdown("#### 📈 روندهای عملکرد")

            g1, g2 = st.columns([1, 2])

            with g1:
                # گیج درصد
                gg = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=float(ap),
                    number={
                        'suffix': '%',
                        'font': {'color': '#38bdf8', 'size': 34},
                    },
                    gauge={
                        'axis': {'range': [0, 100],
                                 'tickcolor': '#94a3b8'},
                        'bar': {'color': "#4ade80"},
                        'bgcolor': "#1e293b",
                        'steps': [
                            {'range': [0, 40],
                             'color': 'rgba(248,113,113,.18)'},
                            {'range': [40, 70],
                             'color': 'rgba(250,204,21,.18)'},
                            {'range': [70, 100],
                             'color': 'rgba(74,222,128,.18)'},
                        ],
                    },
                    title={
                        'text': "میانگین درصد خالص",
                        'font': {'color': '#cbd5e1', 'size': 14},
                    },
                ))
                gg.update_layout(
                    template="plotly_dark",
                    height=280,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font={'family': 'Vazirmatn'},
                )
                st.plotly_chart(gg, use_container_width=True)

            with g2:
                # ساعت مطالعه روزانه
                fh = px.bar(
                    fdf,
                    x='report_date',
                    y='study_hours',
                    title=f"⏳ ساعت مطالعه روزانه ({tf_})",
                    labels={
                        'study_hours': 'ساعت مطالعه',
                        'report_date': 'تاریخ',
                    },
                    color='study_hours',
                    color_continuous_scale=['#0ea5e9', '#7c3aed', '#f472b6'],
                )
                fh.update_layout(
                    template="plotly_dark",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font={'family': 'Vazirmatn'},
                    coloraxis_showscale=False,
                    height=280,
                )
                st.plotly_chart(fh, use_container_width=True)

            # ─── روند تست ───
            ft = px.area(
                fdf,
                x='report_date',
                y='total_tests',
                title=f"📝 روند تست‌زنی ({tf_})",
                labels={
                    'total_tests': 'تعداد تست',
                    'report_date': 'تاریخ',
                },
                color_discrete_sequence=['#4ade80'],
            )
            ft.update_traces(
                line=dict(width=3),
                fillcolor='rgba(74,222,128,0.15)',
            )
            ft.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font={'family': 'Vazirmatn'},
                height=320,
            )
            st.plotly_chart(ft, use_container_width=True)

            # ─── روند رضایت ───
            fsat = px.area(
                fdf,
                x='report_date',
                y='satisfaction',
                title=f"⭐ روند رضایت روزانه ({tf_})",
                labels={
                    'satisfaction': 'امتیاز رضایت',
                    'report_date': 'تاریخ',
                },
                color_discrete_sequence=['#facc15'],
            )
            fsat.update_traces(
                line=dict(width=3),
                fillcolor='rgba(250,204,21,0.15)',
            )
            fsat.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font={'family': 'Vazirmatn'},
                height=320,
            )
            st.plotly_chart(fsat, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۲۵. تب ششم — دستاوردها و مدال‌ها
# ═══════════════════════════════════════════════════════════════════════════

with t6:
    st.markdown("### 🏆 تالار افتخارات و مدال‌ها")

    # ─── دریافت مدال‌های کاربر ───
    unlocked = get_unlocked_badges(USERNAME)
    total_badges = len(BADGES)
    unlocked_count = len(unlocked)
    pct = (unlocked_count / total_badges) * 100 if total_badges > 0 else 0

    # ─── خلاصه پیشرفت ───
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:14px; color:#94a3b8;">
            🎖️ پیشرفت مدال‌ها
        </div>
        <div style="font-size:42px; font-weight:900;
                    color:#facc15; margin:14px 0;">
            {unlocked_count} / {total_badges}
        </div>
        <div style="font-size:13px; color:#38bdf8;
                    font-weight:800; margin-bottom:12px;">
            {pct:.0f}٪ از کل مدال‌ها
        </div>
        <div class="xp-track" style="height:18px;">
            <div class="xp-fill"
                 style="--target:{pct:.0f}%; width:{pct:.0f}%;
                        background:linear-gradient(90deg,
                        #facc15, #f472b6, #a78bfa, #38bdf8);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─── فیلتر دستاوردها ───
    fb1, fb2 = st.columns([1, 3])
    with fb1:
        filter_type = st.radio(
            "نمایش:",
            ["همه", "باز‌شده", "قفل"],
            key="badge_filter",
        )

    # ─── فیلتر مدال‌ها ───
    filtered_badges = {}
    for bid, badge_data in BADGES.items():
        is_unlocked = bid in unlocked
        if filter_type == "باز‌شده" and not is_unlocked:
            continue
        if filter_type == "قفل" and is_unlocked:
            continue
        filtered_badges[bid] = badge_data

    # ─── نمایش مدال‌ها ───
    st.markdown(f"#### 🎖️ گالری مدال‌ها ({len(filtered_badges)} مدال)")

    if not filtered_badges:
        st.info("هیچ مدالی در این دسته وجود نداره")
    else:
        cols = st.columns(4)

        for idx, (bid, (icon, name, desc)) in enumerate(filtered_badges.items()):
            is_unlocked = bid in unlocked
            cls = "unlocked" if is_unlocked else "locked"

            date_unlocked = ""
            if is_unlocked:
                try:
                    dt = pd.to_datetime(unlocked[bid])
                    date_unlocked = (
                        f"<div style='font-size:10px; color:#94a3b8; "
                        f"margin-top:8px;'>📅 "
                        f"{dt.strftime('%Y/%m/%d')}</div>"
                    )
                except Exception:
                    pass

            with cols[idx % 4]:
                st.markdown(f"""
                <div class="badge-ach {cls}">
                    <div style="font-size:38px;">{icon}</div>
                    <div style="font-size:14px; font-weight:900;
                                margin-top:8px;">{name}</div>
                    <div style="font-size:11px; color:#94a3b8;
                                margin-top:6px;">{desc}</div>
                    {date_unlocked}
                </div>
                """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # ▌ پیشرفت به سمت مدال‌های بعدی
    # ═══════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("#### 🎯 مدال‌های نزدیک به باز شدن")

    locked_badges = [
        (bid, data) for bid, data in BADGES.items()
        if bid not in unlocked
    ]

    if not locked_badges:
        st.success("🎉 همه مدال‌ها رو باز کردی! افسانه‌ای هستی!")
    else:
        # محاسبه پیشرفت هر مدال
        progress_data = []

        for bid, (icon, name, desc) in locked_badges[:5]:
            prog_val = 0
            prog_txt = ""

            if bid.startswith("hunter_"):
                target = int(bid.split("_")[1])
                current = df_all['total_tests'].max() if not df_all.empty else 0
                prog_val = min(100, (current / target) * 100)
                prog_txt = f"{int(current)}/{target} تست"

            elif bid == "streak_7":
                current = streak
                prog_val = min(100, (current / 7) * 100)
                prog_txt = f"{current}/7 روز"

            elif bid == "streak_30":
                current = streak
                prog_val = min(100, (current / 30) * 100)
                prog_txt = f"{current}/30 روز"

            elif bid == "centurion":
                current = df_all['study_hours'].sum() if not df_all.empty else 0
                prog_val = min(100, (current / 100) * 100)
                prog_txt = f"{current:.1f}/100 ساعت"

            elif bid == "thousand":
                current = df_all['study_hours'].sum() if not df_all.empty else 0
                prog_val = min(100, (current / 1000) * 100)
                prog_txt = f"{current:.1f}/1000 ساعت"

            elif bid == "marathon_day":
                current = df_all['study_hours'].max() if not df_all.empty else 0
                prog_val = min(100, (current / 8) * 100)
                prog_txt = f"{current:.1f}/8 ساعت"

            elif bid == "mega_marathon":
                current = df_all['study_hours'].max() if not df_all.empty else 0
                prog_val = min(100, (current / 12) * 100)
                prog_txt = f"{current:.1f}/12 ساعت"

            else:
                prog_val = 0
                prog_txt = "در حال پیگیری"

            progress_data.append({
                'icon': icon,
                'name': name,
                'desc': desc,
                'progress': prog_val,
                'progress_txt': prog_txt,
            })

        for p in progress_data:
            st.markdown(f"""
            <div class="glass-card" style="padding:14px;">
                <div style="display:flex; align-items:center; gap:14px;">
                    <div style="font-size:36px;">{p['icon']}</div>
                    <div style="flex:1;">
                        <div style="font-weight:800; font-size:15px;
                                    color:#38bdf8;">
                            {p['name']}
                        </div>
                        <div style="font-size:12px; color:#94a3b8;
                                    margin:4px 0 8px 0;">
                            {p['desc']}
                        </div>
                        <div class="xp-track" style="height:12px;">
                            <div class="xp-fill"
                                 style="--target:{p['progress']:.0f}%;
                                        width:{p['progress']:.0f}%;"></div>
                        </div>
                        <div style="font-size:11px; color:#64748b;
                                    margin-top:6px; text-align:left;">
                            {p['progress_txt']} ({p['progress']:.0f}%)
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۲۶. تب هفتم — تنظیمات و پروفایل
# ═══════════════════════════════════════════════════════════════════════════

with t7:
    st.markdown("### ⚙️ تنظیمات و پروفایل قهرمان")

    # ─── اطلاعات پروفایل ───
    col_p1, col_p2 = st.columns([2, 1])

    with col_p1:
        st.markdown(f"""
        <div class="glass-card">
            <h3 style="margin:0 0 18px 0; color:#38bdf8 !important;">
                👤 پروفایل من
            </h3>
            <table style="width:100%; font-size:14px;">
                <tr>
                    <td style="padding:8px 0; color:#94a3b8;">نام:</td>
                    <td style="padding:8px 0; font-weight:800;">
                        {escape_html(USER_NAME)}
                    </td>
                </tr>
                <tr>
                    <td style="padding:8px 0; color:#94a3b8;">نام کاربری:</td>
                    <td style="padding:8px 0;">
                        <code style="color:#38bdf8;
                                     background:rgba(15,23,42,0.6);
                                     padding:3px 10px; border-radius:6px;">
                            {escape_html(USERNAME)}
                        </code>
                    </td>
                </tr>
                <tr>
                    <td style="padding:8px 0; color:#94a3b8;">سطح فعلی:</td>
                    <td style="padding:8px 0;">
                        <span style="color:{cur_lvl[3]};
                                     font-weight:900; font-size:16px;">
                            {cur_lvl[2]} {cur_lvl[1]}
                        </span>
                    </td>
                </tr>
                <tr>
                    <td style="padding:8px 0; color:#94a3b8;">⚡ XP کل:</td>
                    <td style="padding:8px 0; color:#facc15;
                               font-weight:900;">
                        {total_xp:,}
                    </td>
                </tr>
                <tr>
                    <td style="padding:8px 0; color:#94a3b8;">🔥 زنجیره:</td>
                    <td style="padding:8px 0; color:#fb923c;
                               font-weight:900;">
                        {streak} روز متوالی
                    </td>
                </tr>
                <tr>
                    <td style="padding:8px 0; color:#94a3b8;">
                        📊 تعداد گزارش‌ها:
                    </td>
                    <td style="padding:8px 0; font-weight:900;">
                        {len(df_all)}
                    </td>
                </tr>
                <tr>
                    <td style="padding:8px 0; color:#94a3b8;">
                        🏆 مدال‌های باز‌شده:
                    </td>
                    <td style="padding:8px 0; color:#facc15;
                               font-weight:900;">
                        {len(get_unlocked_badges(USERNAME))} از {len(BADGES)}
                    </td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col_p2:
        # ─── کارت خلاصه ───
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
            <div style="font-size:48px;">
                {cur_lvl[2]}
            </div>
            <div style="font-size:18px; font-weight:900;
                        color:{cur_lvl[3]}; margin-top:8px;">
                {cur_lvl[1]}
            </div>
            <div style="font-size:12px; color:#94a3b8; margin-top:8px;">
                پیشرفت به {nxt_lvl[1] if nxt_lvl else "پایان"}
            </div>
            <div class="xp-track" style="height:16px; margin-top:12px;">
                <div class="xp-fill"
                     style="--target:{prog:.1f}%;
                            width:{prog:.1f}%;"></div>
            </div>
            <div style="font-size:13px; color:#facc15;
                        margin-top:8px; font-weight:800;">
                {prog:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # ▌ آمار تفصیلی
    # ═══════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("#### 📊 آمار کلی حساب")

    if not df_all.empty:
        # بهترین و بدترین روز
        best_study = df_all['study_hours'].max()
        best_study_date = df_all.loc[df_all['study_hours'].idxmax(), 'report_date']
        best_tests = df_all['total_tests'].max()
        best_tests_date = df_all.loc[df_all['total_tests'].idxmax(), 'report_date']
        first_date = df_all['report_date'].min()
        last_date = df_all['report_date'].max()

        # روزهای فعال
        active_days = len(df_all)

        # میانگین‌ها
        avg_hours = df_all['study_hours'].mean()
        avg_tests = df_all['total_tests'].mean()
        avg_perc = df_all['percentage'].mean()
        avg_sat = df_all['satisfaction'].mean()

        stat_cols = st.columns(4)

        with stat_cols[0]:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-icon">🏆</span>
                <div class="metric-num">{best_study:.1f}</div>
                <div class="metric-txt">بهترین روز (ساعت)</div>
                <div style="font-size:10px; color:#64748b;
                            margin-top:4px;">
                    {best_study_date}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with stat_cols[1]:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-icon">⚡</span>
                <div class="metric-num">{best_tests}</div>
                <div class="metric-txt">بیشترین تست روزانه</div>
                <div style="font-size:10px; color:#64748b;
                            margin-top:4px;">
                    {best_tests_date}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with stat_cols[2]:
            days_active = (
                pd.to_datetime(last_date) -
                pd.to_datetime(first_date)
            ).days + 1
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-icon">📅</span>
                <div class="metric-num">{active_days}</div>
                <div class="metric-txt">روز فعال از {days_active} روز</div>
            </div>
            """, unsafe_allow_html=True)

        with stat_cols[3]:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-icon">📈</span>
                <div class="metric-num">{avg_hours:.1f}</div>
                <div class="metric-txt">میانگین ساعت روزانه</div>
            </div>
            """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # ▌ خروجی گرفتن از داده‌ها
    # ═══════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("#### 💾 پشتیبان‌گیری و خروجی")

    if not df_all.empty:
        # تبدیل به CSV
        csv_data = df_all.to_csv(index=False).encode('utf-8-sig')

        st.download_button(
            label="📥 دانلود گزارش‌ها (CSV)",
            data=csv_data,
            file_name=f"academy20_reports_{USERNAME}_{datetime.date.today()}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # ═══════════════════════════════════════════════════════════
    # ▌ دکمه خروج
    # ═══════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("#### 🚪 خروج از حساب کاربری")

    col_exit1, col_exit2 = st.columns([1, 3])

    with col_exit1:
        if st.button("🚪 خروج از حساب", use_container_width=True):
            # پاکسازی session
            for k in ['logged_in', 'username', 'name', 'last_report']:
                if k in st.session_state:
                    st.session_state[k] = None if k == 'last_report' else False

            st.session_state['logged_in'] = False
            st.session_state['username'] = ''
            st.session_state['name'] = ''

            # پاکسازی مقادیر ساعت
            keys_to_clear = [k for k in st.session_state.keys()
                             if '_H' in k or '_M' in k or
                             k.startswith('modal_open_')]
            for k in keys_to_clear:
                try:
                    del st.session_state[k]
                except Exception:
                    pass

            st.rerun()

    with col_exit2:
        st.caption(
            "⚠️ توجه: داده‌های شما در دیتابیس محفوظ می‌مانند و "
            "با ورود مجدد در دسترس خواهند بود."
        )

    # ═══════════════════════════════════════════════════════════
    # ▌ اطلاعات فنی
    # ═══════════════════════════════════════════════════════════
    st.markdown("---")

    with st.expander("ℹ️ اطلاعات فنی برنامه"):
        st.markdown(f"""
        - **نسخه برنامه:** {APP_VERSION}
        - **پایگاه داده:** SQLite (`{DB_FILE}`)
        - **وضعیت Streamlit Dialog:** {"✅ فعال" if HAS_DIALOG else "❌ غیرفعال"}
        - **وضعیت Streamlit Fragment:** {"✅ فعال" if HAS_FRAG else "❌ غیرفعال"}
        - **پشتیبانی PIL:** {"✅ نصب" if HAS_PIL else "❌ نصب نیست"}
        - **پشتیبانی RTL:** {"✅ نصب" if HAS_RTL else "❌ نصب نیست"}
        - **تاریخ امروز:** {datetime.date.today()}
        """)


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۲۷. فوتر سراسری
# ═══════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<div style="text-align:center; padding:30px 10px 20px 10px;
            color:#64748b; font-size:12px; border-top:1px solid
            rgba(56,189,248,0.15); margin-top:40px;">
    <div style="font-size:14px; color:#38bdf8; font-weight:800;
                margin-bottom:8px;">
        👑 آکادمی ۲۰ — نسخه {APP_VERSION}
    </div>
    <div style="margin-bottom:6px;">
        🎓 مشاور علمی: دکتر خشایار اشکبوس
    </div>
    <div style="margin-bottom:6px;">
        📱 تلگرام: <a href="https://t.me/Kh_Ashkboos"
                     style="color:#facc15; text-decoration:none;
                            font-weight:700;">
            @Kh_Ashkboos
        </a>
    </div>
    <div style="color:#475569; font-size:11px; margin-top:12px;">
        ساخته‌شده با ❤️ برای دانش‌آموزان کنکوری ایران
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# ▌ پایان برنامه
# ═══════════════════════════════════════════════════════════════════════════
