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
            PRIMARY KEY (code, username),
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

# ═══════════════════════════════════════════════════════════════════════
    # ادامه تب ۱: حلقه ثبت پارت‌های مطالعه و تست‌ها
    # ═══════════════════════════════════════════════════════════════════════

    total_tests, total_c, total_w = 0, 0, 0
    total_minutes = 0
    parts_summary = []
    parts_data_for_db = []
    errors_today = []

    for i in range(int(num_slots)):
        with st.expander(f"📌 پارت درسی {i+1}", expanded=(i == 0)):
            c_s1, c_s2 = st.columns([2, 1])
            subj = c_s1.selectbox(f"درس (پارت {i+1})", SUBJECTS, key=f"s_{i}")
            if subj == "سایر":
                subj = c_s1.text_input(f"نام درس انتخابی (پارت {i+1})", key=f"cs_{i}")
            
            test_type = c_s2.radio("نوع تست", ["آموزشی", "زمان‌دار"], horizontal=True, key=f"tt_{i}")

            # ⏰ انتخابگر ساعت لوکس با مودال
            c_t1, c_t2 = st.columns(2)
            with c_t1:
                st_t = time_picker_trigger("ساعت شروع", f"st_{i}", default_h=8, default_m=0)
            with c_t2:
                et_t = time_picker_trigger("ساعت پایان", f"et_{i}", default_h=9, default_m=30)

            # محاسبه مدت زمان
            start_dt = datetime.datetime.combine(datetime.date.today(), st_t)
            end_dt = datetime.datetime.combine(datetime.date.today(), et_t)
            dur = (end_dt - start_dt).total_seconds() / 60
            if dur <= 0:
                dur += 24 * 60  # عبور از نیمه‌شب
            total_minutes += dur

            hrs = int(dur // 60)
            mins = int(dur % 60)
            st.markdown(f"""
            <div style="background:rgba(56,189,248,0.1); border-right:3px solid #38bdf8; 
                        padding:6px 12px; border-radius:8px; margin:6px 0; font-size:12.5px;">
                ⏱️ مدت پارت: <b style="color:#38bdf8;">{hrs} ساعت و {mins} دقیقه</b>
            </div>
            """, unsafe_allow_html=True)

            c_src1, c_src2 = st.columns(2)
            src_study = c_src1.text_input("منبع درسنامه", key=f"src_s_{i}")
            src_test = c_src2.text_input("منبع تست", key=f"src_t_{i}")

            st.caption("🎯 آمار تست‌ها:")
            tc, tw, tu, td = st.columns(4)
            c_val = tc.number_input("صحیح", min_value=0, value=0, key=f"c_{i}")
            w_val = tw.number_input("غلط", min_value=0, value=0, key=f"w_{i}")
            u_val = tu.number_input("نزده", min_value=0, value=0, key=f"u_{i}")
            d_val = td.number_input("شک‌دار", min_value=0, value=0, key=f"d_{i}")

            # ─── جعبه سیاه اشتباهات (Error Vault) درون هر پارت ───
            if w_val > 0:
                with st.expander(f"⚠️ تحلیل غلط‌های {subj} ({w_val} غلط)", expanded=False):
                    err_tag = st.selectbox(f"علت عمده تست‌های غلط {subj}:", ERROR_TAGS, key=f"err_tag_{i}")
                    err_notes = st.text_input(f"نکته کلیدی رفع اشکال {subj}:", key=f"err_note_{i}")
                    errors_today.append({
                        'subject': subj,
                        'tag': err_tag,
                        'count': w_val,
                        'notes': err_notes
                    })

            notes = st.text_input("مبحث و خلاصه یادداشت", key=f"nt_{i}")
            s_tests = c_val + w_val + u_val
            total_tests += s_tests
            total_c += c_val
            total_w += w_val

            parts_summary.append(
                f"{i+1}. {subj} ({st_t.strftime('%H:%M')}-{et_t.strftime('%H:%M')}) | "
                f"{s_tests} تست ({c_val}ص/{w_val}غ/{d_val}شک) | مبحث: {notes or 'عمومی'}"
            )
            parts_data_for_db.append({
                'subject': subj,
                'minutes': dur,
                'tests': s_tests,
                'correct': c_val,
                'wrong': w_val,
                'start_hour': st_t.hour,
                'end_hour': et_t.hour,
                'study_source': src_study,
                'test_source': src_test,
                'notes': notes
            })

    # ─── بخش اسکرین‌تایم و محاسبه DDI ───
    st.markdown("#### 📱 کنترل دیجیتال و سلامت ذهن")
    c_sc1, c_sc2 = st.columns(2)
    screen_t = c_sc1.text_input("کل مصرف گوشی امروز (مثلاً ۲:۱۵):", "۱:۴۵")
    social_t = c_sc2.text_input("فضای مجازی (اینستاگرام، تلگرام و...):", "۳۰ دقیقه")

    study_hours = round(total_minutes / 60, 2)
    overall_perc = calculate_percentage(total_c, total_w, total_tests - (total_c + total_w))
    ddi_val, ddi_lvl = compute_ddi(study_hours, social_t)
    xp_today = calculate_session_xp(study_hours, total_tests, total_c)

    # نمایش زنده پنل DDI و خلاصه روز
    st.markdown(ddi_badge_html(ddi_val, ddi_lvl), unsafe_allow_html=True)

    # ─── دکمه ثبت نهایی در دیتابیس ───
    if st.button("💾 ثبت نهایی گزارش در دیتابیس آکادمی", use_container_width=True):
        c = db_cursor()
        try:
            c.execute('''
                INSERT INTO reports 
                (username, report_date, satisfaction, study_hours, total_tests, 
                 correct_tests, wrong_tests, percentage, screen_time, social_time, 
                 details, xp_earned, ddi)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(username, report_date) DO UPDATE SET
                    satisfaction=excluded.satisfaction,
                    study_hours=excluded.study_hours,
                    total_tests=excluded.total_tests,
                    correct_tests=excluded.correct_tests,
                    wrong_tests=excluded.wrong_tests,
                    percentage=excluded.percentage,
                    screen_time=excluded.screen_time,
                    social_time=excluded.social_time,
                    details=excluded.details,
                    xp_earned=excluded.xp_earned,
                    ddi=excluded.ddi
            ''', (
                USERNAME, rep_date, satisfaction, study_hours, total_tests,
                total_c, total_w, overall_perc, screen_t, social_t,
                "\n".join(parts_summary), xp_today, ddi_val
            ))
            
            # ذخیره گزارش آی‌دی برای کلید خارجی
            c.execute("SELECT id FROM reports WHERE username=? AND report_date=?", (USERNAME, rep_date))
            rep_id = c.fetchone()[0]

            # پاک کردن و ثبت مجدد پارت‌ها
            c.execute("DELETE FROM parts WHERE report_id=?", (rep_id,))
            for p in parts_data_for_db:
                c.execute('''
                    INSERT INTO parts 
                    (report_id, username, report_date, subject, minutes, tests, 
                     correct, wrong, start_hour, end_hour, study_source, test_source, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    rep_id, USERNAME, rep_date, p['subject'], p['minutes'],
                    p['tests'], p['correct'], p['wrong'], p['start_hour'],
                    p['end_hour'], p['study_source'], p['test_source'], p['notes']
                ))

            # ثبت خطاهای جعبه سیاه
            for err in errors_today:
                c.execute('''
                    INSERT INTO error_vault (report_id, username, report_date, subject, error_tag, count, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (rep_id, USERNAME, rep_date, err['subject'], err['tag'], err['count'], err['notes']))

            db_commit()

            # بررسی و باز کردن مدال‌ها
            today_rep_dict = {
                'study_hours': study_hours,
                'total_tests': total_tests,
                'percentage': overall_perc,
                'screen_time': screen_t,
                'social_time': social_t
            }
            new_badges = check_and_unlock_badges(USERNAME, today_rep_dict, parts_data_for_db)

            st.balloons()
            st.success(f"✅ گزارش کار با موفقیت ذخیره شد! (+{xp_today} XP کسب کردی)")
            if new_badges:
                badge_names = " ، ".join([BADGES[b][1] for b in new_badges])
                st.toast(f"🎖️ مدال‌های جدید آنلاک شد: {badge_names}", icon="✨")

        except Exception as e:
            st.error(f"خطا در ثبت پایگاه داده: {e}")

    # ─── کارنامه‌های تصویری و اشتراک‌گذاری ───
    st.markdown("---")
    st.markdown("#### 🖼 کارنامه‌های تعاملی و اشتراک تلگرام")

    report_text = f"""📊 گزارش کار شبانه | آکادمی ۲۰
👤 دانش‌آموز: {USER_NAME}
📅 تاریخ: {rep_date} | ⭐ رضایت: {satisfaction}/10
⏳ مجموع مطالعه: {study_hours} ساعت
📝 کل تست‌ها: {total_tests} (✅ {total_c} | ❌ {total_w})
🎯 درصد خالص: {overall_perc}%
📱 اسکرین‌تایم: {screen_t} (مجازی: {social_t})
🧠 شاخص تخلیه تمرکز (DDI): {ddi_val}% ({DDI_META[ddi_lvl][1]})
⚡ امتیاز تجربه: +{xp_today} XP | جایگاه: {cur_lvl[1]}
━━━━━━━━━━━━━━━━━━━━
📚 ریز پارت‌های مطالعه:
""" + "\n".join(parts_summary) + f"""
━━━━━━━━━━━━━━━━━━━━
👨‍🏫 مشاور: دکتر خشایار اشکبوس | @Kh_Ashkboos"""

    col_c1, col_c2 = st.columns([1, 1])

    with col_c1:
        st.markdown("##### 📋 متن تلگرام و کپی")
        st.text_area("متن گزارش جهت ارسال به مشاور:", report_text, height=220)
        tg_url = "https://t.me/share/url?url=" + urllib.parse.quote(report_text)
        st.markdown(f'<a href="{tg_url}" target="_blank" class="tg-button">🚀 ارسال مستقیم متن به تلگرام مشاور</a>', unsafe_allow_html=True)

    with col_c2:
        st.markdown("##### 🎴 کارت گرافیکی HTML2Canvas")
        card_html = render_html_report_card(
            USER_NAME, str(rep_date), satisfaction, study_hours,
            total_tests, overall_perc, screen_t, ddi_val, ddi_lvl,
            cur_lvl[1], total_xp + xp_today, streak, card_id="daily_card"
        )
        components.html(card_html, height=620, scrolling=True)

    st.markdown("##### 📱 کارت استوری اینستاگرام / تلگرام (۹:۱۶)")
    user_badges_now = list(get_unlocked_badges(USERNAME).keys())
    story_html = render_html_story_card(
        USER_NAME, str(rep_date), study_hours, total_tests,
        overall_perc, ddi_val, ddi_lvl, cur_lvl[1], xp_today,
        streak, user_badges_now, story_id="story_card"
    )
    components.html(story_html, height=880, scrolling=True)


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۲۱. تب ۲: اتاق تمرکز و پومودورو (Pomodoro Engine)
# ═══════════════════════════════════════════════════════════════════════════
with t2:
    st.markdown("### 🍅 اتاق تمرکز پومودورو و تایمر آزمون")
    st.markdown("""
    <div class="glass-card" style="font-size:13.5px; color:#cbd5e1;">
    تکنیک پومودورو مغز را در وضعیت غوطه‌وری (Deep Work) نگه می‌دارد. یکی از حالت‌های زیر را انتخاب کن و وارد مدار تمرکز شو!
    </div>
    """, unsafe_allow_html=True)

    c_mode1, c_mode2 = st.columns([2, 1])
    selected_mode = c_mode1.selectbox("انتخاب حالت تایمر:", list(POMO_MODES.keys()))
    
    if c_mode2.button("تنظیم تایمر", use_container_width=True):
        st.session_state.pomo = {
            'running': False,
            'end_time': None,
            'duration': POMO_MODES[selected_mode],
            'last_remaining': POMO_MODES[selected_mode],
            'mode': selected_mode
        }
        st.rerun()

    # رندر تایمر پومودورو
    if HAS_FRAG:
        render_timer_fragment()
    else:
        rem_sec = st.session_state.pomo.get('last_remaining', 25*60)
        m, s = divmod(rem_sec, 60)
        st.markdown(f"""
        <div class="pomodoro-box">
            <div class="pomo-time">{m:02d}:{s:02d}</div>
            <div class="pomo-label">{st.session_state.pomo.get('mode', 'آماده شروع')}</div>
        </div>
        """, unsafe_allow_html=True)

    render_pomodoro_controls()

    # تاریخچه جلسات اخیر پومودورو
    df_pomo = pd.read_sql_query(
        "SELECT session_date, duration_minutes, mode FROM pomodoro_sessions WHERE username=? ORDER BY id DESC LIMIT 5",
        DB_CONN, params=(USERNAME,)
    )
    if not df_pomo.empty:
        st.markdown("##### 📜 آخرین جلسات تمرکز کامل شما:")
        st.dataframe(df_pomo, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۲۲. تب ۳: شبیه‌ساز و پیش‌بینی رتبه کنکور (Predictive Rank)
# ═══════════════════════════════════════════════════════════════════════════
with t3:
    st.markdown("### 🔮 پیش‌بینی هوشمند رتبه و تراز کنکور")
    st.markdown("""
    <div class="glass-card" style="font-size:13.5px; color:#cbd5e1;">
    این مدل رگرسیونی عملکرد اخیر شما را با بانک داده رتبه‌برترهای پیشین دکتر اشکبوس مقایسه کرده و بازه رتبه شما را تخمین می‌زند.
    </div>
    """, unsafe_allow_html=True)

    # مقادیر پیش‌فرض بر اساس داده‌های کاربر
    def_h = float(df_all['study_hours'].mean()) if not df_all.empty else 7.0
    def_t = float(df_all['total_tests'].mean()) if not df_all.empty else 80.0
    def_p = float(df_all['percentage'].mean()) if not df_all.empty else 55.0

    st.markdown("#### 🎛 سناریوسازی فرضی (What-If Analysis):")
    col_w1, col_w2, col_w3 = st.columns(3)
    sim_h = col_w1.slider("ساعت مطالعه میانگین روزانه:", 1.0, 15.0, def_h, step=0.5)
    sim_t = col_w2.slider("تعداد تست میانگین روزانه:", 10, 300, int(def_t), step=10)
    sim_p = col_w3.slider("میانگین درصد پاسخ‌گویی:", 10.0, 100.0, def_p, step=1.0)

    traz, r_low, r_mid, r_high, score = predict_rank(sim_h, sim_t, sim_p)
    tier_name, tier_col = rank_tier(r_mid)

    st.markdown(f"""
    <div class="rank-card" style="text-align:center;">
        <span style="background:{tier_col}; color:#000; padding:6px 16px; border-radius:20px; font-weight:900; font-size:14px;">
            {tier_name}
        </span>
        <div class="rank-number" style="margin-top:14px;">~ {r_mid:,}</div>
        <div class="rank-label">رتبه احتمالی منطقه شما در کنکور سراسری تجربی</div>
        <div style="font-size:15px; color:#38bdf8; margin-top:8px; font-weight:800;">
            بازه تخمینی: {r_low:,} تا {r_high:,} | تراز پیش‌بینی شده: {traz:,}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # توصیه اختصاصی مشاور
    if r_mid < 1000:
        st.success("💎 در وضعیت رتبه زیر ۱۰۰۰ (پزشکی و دندانپزشکی دانشگاه‌های برتر) قرار داری! همین ثبات را حفظ کن.")
    elif r_mid < 3000:
        st.info("⚡ بسیار عالی! در یک قدمی پزشکی‌های تهران و کلان‌شهرها هستی؛ روزی ۳۰ تست بیشتر معجزه می‌کند.")
    else:
        st.warning("⚠️ برای قبولی در رشته‌های تاپ تجربی، سرعت تست‌زنی و ساعت مطالعه‌ات باید یک پله بالاتر بیاید.")


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۲۳. تب ۴: اتاق جنگ و دوئل گروهی (Study Arena)
# ═══════════════════════════════════════════════════════════════════════════
with t4:
    st.markdown("### ⚔️ اتاق جنگ و لیدربورد رقابتی (Study Arena)")
    st.markdown("""
    <div class="glass-card" style="font-size:13.5px; color:#cbd5e1;">
    با دوستان خود یا بچه‌های آکادمی گروه بسازید، کد را به اشتراک بگذارید و بر سر ساعت مطالعه و تعداد تست در جدول رده‌بندی بجنگید!
    </div>
    """, unsafe_allow_html=True)

    user_rooms = get_user_rooms(USERNAME)

    ar_tab1, ar_tab2 = st.tabs(["🏆 لیدربورد اتاق‌ها", "➕ ساخت یا عضویت در اتاق"])

    with ar_tab1:
        if user_rooms.empty:
            st.info("هنوز در اتاقی عضو نیستی! از تب بعدی یک اتاق بساز یا به اتاق دوستانت ملحق شو.")
        else:
            sel_room = st.selectbox("انتخاب اتاق مطالعاتی:", user_rooms['name'].tolist())
            room_code = user_rooms[user_rooms['name'] == sel_room]['code'].values[0]

            st.markdown(f"##### 🏅 رده‌بندی ۷ روز اخیر اتاق `{sel_room}` (کد: `{room_code}`):")
            lb_df = arena_leaderboard(room_code, days=7)

            if lb_df.empty:
                st.write("هنوز داده‌ای در این اتاق ثبت نشده است.")
            else:
                for idx, row in lb_df.iterrows():
                    me_class = "arena-me" if row['is_me'] else ""
                    medal = "🥇" if idx == 1 else ("🥈" if idx == 2 else ("🥉" if idx == 3 else f"#{idx}"))
                    st.markdown(f"""
                    <div class="arena-card {me_class}">
                        <div style="display:flex; align-items:center; gap:12px;">
                            <div class="arena-rank">{medal}</div>
                            <div>
                                <b style="font-size:16px; color:#fff;">{row['nickname']}</b>
                                <div style="font-size:12px; color:#94a3b8;">{row['hours']} ساعت مطالعه | {row['tests']} تست</div>
                            </div>
                        </div>
                        <div style="font-size:18px; font-weight:900; color:#facc15;">
                            ⚡ {row['score']:,} XP
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    with ar_tab2:
        c_rm1, c_rm2 = st.columns(2)
        with c_rm1:
            st.markdown("##### ساخت اتاق جدید")
            new_r_name = st.text_input("نام اتاق (مثلاً: رتبه‌برترهای ۱۴۰۴):")
            new_r_nick = st.text_input("لقب شما در این اتاق:", value=USER_NAME)
            if st.button("ایجاد اتاق جنگ", use_container_width=True):
                if new_r_name:
                    code = f"A20-{random.randint(1000, 9999)}"
                    c = db_cursor()
                    c.execute("INSERT INTO arena_rooms (code, name, created_by) VALUES (?, ?, ?)", (code, new_r_name, USERNAME))
                    c.execute("INSERT INTO arena_members (code, username, nickname) VALUES (?, ?, ?)", (code, USERNAME, new_r_nick))
                    db_commit()
                    st.success(f"🎉 اتاق ساخته شد! کد اشتراک: `{code}`")
                    st.rerun()

        with c_rm2:
            st.markdown("##### پیوستن به اتاق موجود")
            join_code = st.text_input("کد اتاق (مثلاً: A20-1234):")
            join_nick = st.text_input("لقب نمایشی شما:", value=USER_NAME, key="join_nick")
            if st.button("پیوستن به رقابت", use_container_width=True):
                if join_code:
                    c = db_cursor()
                    c.execute("SELECT code FROM arena_rooms WHERE code=?", (join_code.strip(),))
                    if c.fetchone():
                        try:
                            c.execute("INSERT INTO arena_members (code, username, nickname) VALUES (?, ?, ?)", (join_code.strip(), USERNAME, join_nick))
                            db_commit()
                            st.success("✅ با موفقیت وارد اتاق شدی!")
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.warning("قبلاً در این اتاق عضو شدی!")
                    else:
                        st.error("اتاقی با این کد پیدا نشد.")


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۲۴. تب ۵: آنالیز پیشرفته، هوش مصنوعی و جعبه سیاه
# ═══════════════════════════════════════════════════════════════════════════
with t5:
    st.markdown("### 📈 داشبورد تحلیلی و جعبه سیاه اشتباهات")

    if df_all.empty:
        st.info("گزارشی برای رسم نمودار وجود ندارد.")
    else:
        df_all['report_date'] = pd.to_datetime(df_all['report_date'])

        # هوش مصنوعی دستیار مشاور
        st.markdown("#### 🤖 تحلیل‌های هوشمند دکتر اشکبوس (AI Coach):")
        ai_tips = ai_coach_analysis(df_all)
        st.markdown('<div class="ai-coach">', unsafe_allow_html=True)
        for t_type, t_msg in ai_tips:
            st.markdown(f'<div class="ai-tip {t_type}">{t_msg}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ─── جعبه سیاه اشتباهات (Error Vault Analysis) ───
        df_errors = pd.read_sql_query(
            "SELECT subject, error_tag, SUM(count) as total_err FROM error_vault WHERE username=? GROUP BY error_tag, subject",
            DB_CONN, params=(USERNAME,)
        )
        if not df_errors.empty:
            st.markdown("#### ⚠️ تحلیل جعبه سیاه تست‌های اشتباه:")
            ce1, ce2 = st.columns(2)
            with ce1:
                fig_err = px.pie(
                    df_errors, values='total_err', names='error_tag',
                    title="سهم علل غلط زدن تست‌ها", hole=0.45,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_err.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_err, use_container_width=True)
            with ce2:
                fig_err_bar = px.bar(
                    df_errors, x='subject', y='total_err', color='error_tag',
                    title="تفکیک اشتباهات در هر درس", labels={'total_err': 'تعداد غلط', 'subject': 'درس'}
                )
                fig_err_bar.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_err_bar, use_container_width=True)

        # ─── نمودارهای ترند مطالعاتی ───
        st.markdown("#### 📊 نمودارهای جامع روند پیشرفت:")
        g_c1, g_c2 = st.columns(2)
        with g_c1:
            fig_hours = px.bar(
                df_all, x='report_date', y='study_hours', title="روند ساعت مطالعه",
                labels={'study_hours': 'ساعت مطالعه', 'report_date': 'تاریخ'},
                color='study_hours', color_continuous_scale=['#0ea5e9', '#7c3aed']
            )
            fig_hours.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_hours, use_container_width=True)

        with g_c2:
            fig_perc = px.line(
                df_all, x='report_date', y='percentage', title="نوسان درصد آزمون‌ها",
                labels={'percentage': 'درصد خالص', 'report_date': 'تاریخ'}, markers=True
            )
            fig_perc.update_traces(line_color='#4ade80', line_width=3)
            fig_perc.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_perc, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۲۵. تب ۶: تالار افتخارات و دستاوردها (Achievements)
# ═══════════════════════════════════════════════════════════════════════════
with t6:
    st.markdown("### 🏆 تالار افتخارات و مدال‌های کسب‌شده")
    st.markdown("""
    <div class="glass-card" style="font-size:13.5px; color:#cbd5e1;">
    با استمرار در مطالعه، کم کردن اسکرین‌تایم و زدن تست‌های بیشتر، مدال‌های ویژه آکادمی را آنلاک کن!
    </div>
    """, unsafe_allow_html=True)

    unlocked_dict = get_unlocked_badges(USERNAME)
    total_unlocked = len(unlocked_dict)
    st.markdown(f"##### پیشرفت مدال‌ها: **{total_unlocked} از {len(BADGES)} مدال** باز شده است.")

    cols = st.columns(4)
    for idx, (b_id, (b_icon, b_title, b_desc)) in enumerate(BADGES.items()):
        is_unlocked = b_id in unlocked_dict
        u_class = "unlocked" if is_unlocked else "locked"
        status_txt = f"آنلاک در: {unlocked_dict[b_id][:10]}" if is_unlocked else "🔒 قفل"

        with cols[idx % 4]:
            st.markdown(f"""
            <div class="badge-ach {u_class}">
                <div style="font-size:32px; margin-bottom:6px;">{b_icon}</div>
                <div style="font-size:15px; font-weight:900;">{b_title}</div>
                <div style="font-size:11.5px; color:#94a3b8; margin:4px 0;">{b_desc}</div>
                <div style="font-size:10px; color:#64748b; font-weight:700;">{status_txt}</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# ▌ ۲۶. تب ۷: پروفایل کاربری، خروجی داده و خروج
# ═══════════════════════════════════════════════════════════════════════════
with t7:
    st.markdown("### ⚙️ پروفایل و تنظیمات سامانه")

    st.markdown(f"""
    <div class="glass-card">
        <h3>دانش‌آموز گرامی: {USER_NAME}</h3>
        <p style="color:#94a3b8;">نام کاربری سامانه: <code>{USERNAME}</code></p>
        <p style="color:#94a3b8;">کل ساعات مطالعه ثبت‌شده: <b style="color:#38bdf8;">{df_all['study_hours'].sum():.1f} ساعت</b></p>
        <p style="color:#94a3b8;">کل تست‌های حل‌شده: <b style="color:#4ade80;">{df_all['total_tests'].sum():,} تست</b></p>
        <p style="color:#94a3b8;">امتیاز تجربه کل: <b style="color:#facc15;">{total_xp:,} XP</b> | رده: <span class="level-badge">{cur_lvl[2]} {cur_lvl[1]}</span></p>
    </div>
    """, unsafe_allow_html=True)

    # دکمه خروجی اکسل کامل
    if not df_all.empty:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_all.to_excel(writer, index=False, sheet_name='گزارشات_روزانه')
        st.download_button(
            label="📥 دانلود کامل کارنامه به صورت اکسل (Excel)",
            data=output.getvalue(),
            file_name=f"Academy20_{USERNAME}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.markdown("---")
    if st.button("🚪 خروج امن از حساب کاربری", use_container_width=True):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ''
        st.session_state['name'] = ''
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
# پایان برنامه — آکادمی ۲۰
# ═══════════════════════════════════════════════════════════════════════════
