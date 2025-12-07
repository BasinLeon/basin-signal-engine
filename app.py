"""
Basin Signal Engine - Main Streamlit Application
The 'Face' of the Revenue Architect Resume OS

System Status: Architecture > Activity
Mode: Voice-First Career Intelligence Platform
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Basin Logic
from logic.ingest import extract_text_from_upload, validate_resume_content
from logic.prompt_engine import construct_basin_prompt, get_persona_options, get_persona_description
from logic.generator import generate_signal_output, estimate_tokens, get_model_options, MOCK_MODE
from logic.voice import transcribe_audio, generate_speech, get_voice_options
from logic.video import analyze_video_pitch, validate_video, get_video_info

# Note: Using native st.audio_input instead of audio_recorder_streamlit for Cloud compatibility


# ═══════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="BASIN::NEXUS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ═══════════════════════════════════════════════════════════════
# BASIN::NEXUS - PREMIUM STYLING
# ═══════════════════════════════════════════════════════════════

# PWA META TAGS (Injected via hidden component)
# Note: Streamlit doesn't support direct head injection, using components.html
import streamlit.components.v1 as components

# PWA Support - Inject meta tags via JavaScript
components.html("""
<script>
    // Inject PWA meta tags into document head
    const head = document.getElementsByTagName('head')[0];
    
    // Apple Mobile Web App
    const meta1 = document.createElement('meta');
    meta1.name = 'apple-mobile-web-app-capable';
    meta1.content = 'yes';
    head.appendChild(meta1);
    
    const meta2 = document.createElement('meta');
    meta2.name = 'apple-mobile-web-app-status-bar-style';
    meta2.content = 'black-translucent';
    head.appendChild(meta2);
    
    const meta3 = document.createElement('meta');
    meta3.name = 'apple-mobile-web-app-title';
    meta3.content = 'BASIN::NEXUS';
    head.appendChild(meta3);
    
    // Theme Color
    const meta4 = document.createElement('meta');
    meta4.name = 'theme-color';
    meta4.content = '#FFD700';
    head.appendChild(meta4);
    
    // Manifest link
    const manifest = document.createElement('link');
    manifest.rel = 'manifest';
    manifest.href = '.streamlit/manifest.json';
    head.appendChild(manifest);
</script>
""", height=0)

st.markdown("""
<style>
    /* ═══════════════════════════════════════════════════════════════
       BASIN::NEXUS EXECUTIVE OS — GOLDEN PROTOCOL v2.0
       Luxurious Command Center Aesthetic
    ═══════════════════════════════════════════════════════════════ */
    
    /* === TYPOGRAPHY IMPORTS === */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');
    
    /* === ROOT VARIABLES === */
    :root {
        --gold-primary: #D4AF37;
        --gold-light: #FFD700;
        --gold-dark: #B8860B;
        --gold-glow: rgba(212, 175, 55, 0.6);
        --gold-subtle: rgba(212, 175, 55, 0.15);
        --gold-border: rgba(212, 175, 55, 0.3);
        --bg-deep: #050508;
        --bg-card: #0a0a0f;
        --bg-elevated: #0f0f15;
        --text-primary: #f0e6d3;
        --text-secondary: #8b8573;
        --text-muted: #5a584f;
        --success: #4ade80;
        --warning: #fbbf24;
        --danger: #f87171;
    }
    
    /* === CORE BACKGROUND === */
    .stApp {
        background: 
            radial-gradient(ellipse at top, rgba(212, 175, 55, 0.03) 0%, transparent 50%),
            radial-gradient(ellipse at bottom right, rgba(212, 175, 55, 0.02) 0%, transparent 40%),
            linear-gradient(180deg, #050508 0%, #0a0a0f 50%, #050508 100%);
        background-attachment: fixed;
    }
    
    /* === SUBTLE GRID PATTERN === */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            linear-gradient(rgba(212, 175, 55, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(212, 175, 55, 0.02) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: -1;
    }
    
    /* === MAIN CONTAINER === */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1400px;
    }
    
    /* === GLOBAL TYPOGRAPHY === */
    .stApp, .stApp p, .stApp span, .stApp div, .stApp li {
        color: var(--text-primary) !important;
        font-family: 'JetBrains Mono', 'SF Mono', monospace !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', sans-serif !important;
        color: var(--gold-primary) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    h1 {
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        text-shadow: 0 0 20px var(--gold-glow);
    }
    
    h2 {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    
    h3 {
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }
    
    /* === EXECUTIVE HEADER STYLES === */
    .nexus-header {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(135deg, #D4AF37 0%, #FFD700 25%, #D4AF37 50%, #B8860B 75%, #D4AF37 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.6rem;
        font-weight: 900;
        letter-spacing: 2px;
        text-transform: uppercase;
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .nexus-subtitle {
        color: var(--text-secondary);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-top: 8px;
    }
    
    /* === STATUS INDICATORS === */
    .status-live {
        background: linear-gradient(135deg, var(--gold-dark) 0%, var(--gold-primary) 50%, var(--gold-light) 100%);
        color: #000 !important;
        padding: 8px 20px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 800;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 2px;
        text-transform: uppercase;
        display: inline-block;
        box-shadow: 
            0 0 20px var(--gold-glow),
            inset 0 1px 0 rgba(255,255,255,0.3);
        animation: pulse-glow 2s ease-in-out infinite;
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 20px var(--gold-glow); }
        50% { box-shadow: 0 0 40px var(--gold-glow), 0 0 60px rgba(212, 175, 55, 0.3); }
    }
    
    /* === PREMIUM CARD CONTAINERS === */
    .nexus-card {
        background: linear-gradient(145deg, var(--bg-card) 0%, var(--bg-deep) 100%);
        border: 1px solid var(--gold-border);
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .nexus-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--gold-primary), transparent);
        opacity: 0.6;
    }
    
    .nexus-card:hover {
        border-color: var(--gold-primary);
        box-shadow: 
            0 0 30px rgba(212, 175, 55, 0.15),
            inset 0 0 60px rgba(212, 175, 55, 0.03);
        transform: translateY(-2px);
    }
    
    /* === METRIC CARDS (Executive Dashboard) === */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, var(--bg-elevated) 0%, var(--bg-card) 100%);
        border: 1px solid var(--gold-border);
        border-radius: 12px;
        padding: 20px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--gold-primary), transparent);
    }
    
    [data-testid="stMetric"]::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 2px;
        height: 100%;
        background: linear-gradient(180deg, var(--gold-primary), transparent);
    }
    
    [data-testid="stMetric"]:hover {
        border-color: var(--gold-primary);
        box-shadow: 0 0 25px rgba(212, 175, 55, 0.2);
        transform: translateY(-3px);
    }
    
    [data-testid="stMetricValue"] {
        color: var(--gold-light) !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        text-shadow: 0 0 20px var(--gold-glow);
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-family: 'JetBrains Mono', monospace !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-size: 0.75rem !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: var(--success) !important;
    }
    
    /* === BUTTONS (Golden Command) === */
    .stButton > button {
        background: linear-gradient(145deg, var(--gold-dark) 0%, var(--gold-primary) 50%, var(--gold-light) 100%);
        color: #000 !important;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        border: none;
        border-radius: 6px;
        padding: 14px 28px;
        transition: all 0.3s ease;
        box-shadow: 
            0 4px 15px rgba(212, 175, 55, 0.3),
            inset 0 1px 0 rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 
            0 8px 30px rgba(212, 175, 55, 0.4),
            0 0 40px rgba(212, 175, 55, 0.2);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* === SIDEBAR (Command Panel) === */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050508 0%, #0a0a0f 100%);
        border-right: 1px solid var(--gold-border);
        position: relative;
    }
    
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 1px;
        height: 100%;
        background: linear-gradient(180deg, var(--gold-primary), transparent 50%, var(--gold-primary));
        opacity: 0.5;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: var(--gold-primary) !important;
        font-family: 'Orbitron', sans-serif !important;
    }
    
    /* === INPUTS (Terminal Style) === */
    input, textarea, [data-testid="stTextInput"] input {
        background: var(--bg-deep) !important;
        border: 1px solid var(--gold-border) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-family: 'JetBrains Mono', monospace !important;
        transition: all 0.3s ease;
    }
    
    input:focus, textarea:focus {
        border-color: var(--gold-primary) !important;
        box-shadow: 
            0 0 15px rgba(212, 175, 55, 0.2),
            inset 0 0 20px rgba(212, 175, 55, 0.05) !important;
        outline: none !important;
    }
    
    /* === SELECT BOXES === */
    [data-testid="stSelectbox"] > div {
        background: var(--bg-deep);
        border: 1px solid var(--gold-border);
        border-radius: 8px;
    }
    
    [data-testid="stSelectbox"] > div:hover {
        border-color: var(--gold-primary);
    }
    
    /* === EXPANDERS (Mission Briefing Style) === */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-deep) 100%);
        border: 1px solid var(--gold-border);
        border-radius: 8px;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: var(--gold-primary);
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.1);
    }
    
    /* === TABS (Mission Control) === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--bg-card);
        border: 1px solid var(--gold-border);
        border-radius: 8px 8px 0 0;
        color: var(--text-secondary);
        font-family: 'Orbitron', sans-serif;
        font-size: 0.8rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--gold-primary);
        border-color: var(--gold-primary);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, rgba(212, 175, 55, 0.2) 0%, var(--bg-card) 100%) !important;
        border-color: var(--gold-primary) !important;
        color: var(--gold-primary) !important;
        border-bottom: none !important;
    }
    
    /* === FILE UPLOADER === */
    [data-testid="stFileUploader"] {
        background: var(--bg-card) !important;
        border: 2px dashed var(--gold-border) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--gold-primary) !important;
        box-shadow: inset 0 0 30px rgba(212, 175, 55, 0.05);
    }
    
    [data-testid="stFileUploader"] section {
        background: var(--bg-deep) !important;
        border: 1px dashed var(--gold-border) !important;
        border-radius: 8px !important;
    }
    
    /* === PROGRESS BARS === */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--gold-dark), var(--gold-primary), var(--gold-light));
        box-shadow: 0 0 10px var(--gold-glow);
    }
    
    /* === SCROLLBAR (Executive) === */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-deep);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--gold-dark), var(--gold-primary));
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--gold-primary);
        box-shadow: 0 0 10px var(--gold-glow);
    }
    
    /* === DIVIDERS === */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--gold-primary), transparent);
        margin: 24px 0;
        opacity: 0.5;
    }
    
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--gold-border), transparent);
        margin: 20px 0;
    }
    
    /* === ALERTS & NOTIFICATIONS === */
    .stSuccess {
        background: linear-gradient(135deg, rgba(74, 222, 128, 0.1) 0%, rgba(74, 222, 128, 0.05) 100%);
        border: 1px solid rgba(74, 222, 128, 0.3);
        border-left: 4px solid var(--success);
        border-radius: 8px;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(248, 113, 113, 0.1) 0%, rgba(248, 113, 113, 0.05) 100%);
        border: 1px solid rgba(248, 113, 113, 0.3);
        border-left: 4px solid var(--danger);
        border-radius: 8px;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(212, 175, 55, 0.05) 100%);
        border: 1px solid var(--gold-border);
        border-left: 4px solid var(--gold-primary);
        border-radius: 8px;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.08) 0%, rgba(212, 175, 55, 0.03) 100%);
        border: 1px solid var(--gold-border);
        border-left: 4px solid var(--gold-dark);
        border-radius: 8px;
    }
    
    /* === TOAST NOTIFICATIONS === */
    [data-testid="stToast"] {
        background: linear-gradient(135deg, var(--bg-card), var(--bg-deep)) !important;
        border: 1px solid var(--gold-border) !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    }
    
    /* === RADIO BUTTONS === */
    [data-testid="stRadio"] > label {
        display: flex;
        align-items: center;
        padding: 10px 14px;
        margin: 4px 0;
        border-radius: 8px;
        border: 1px solid transparent;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    [data-testid="stRadio"] > label:hover {
        background: rgba(212, 175, 55, 0.08);
        border-color: var(--gold-border);
    }
    
    /* === LOADING SPINNER === */
    .stSpinner > div {
        border-top-color: var(--gold-primary) !important;
    }
    
    /* === DATAFRAMES / TABLES === */
    .stDataFrame {
        border: 1px solid var(--gold-border);
        border-radius: 12px;
        overflow: hidden;
    }
    
    .stDataFrame thead th {
        background: var(--bg-card) !important;
        color: var(--gold-primary) !important;
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stDataFrame tbody td {
        background: var(--bg-deep) !important;
        color: var(--text-primary) !important;
        border-color: var(--gold-border) !important;
    }
    
    /* === HIDE STREAMLIT CHROME === */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* === ANIMATIONS === */
    @keyframes glow-border {
        0%, 100% { border-color: var(--gold-border); }
        50% { border-color: var(--gold-primary); }
    }
    
    @keyframes scan-line {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(100vh); }
    }
    
    .pulse-active {
        animation: pulse-glow 2s infinite;
    }
    
    /* === MOBILE RESPONSIVE === */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        .nexus-header {
            font-size: 1.8rem !important;
            letter-spacing: 2px;
        }
        
        h1 {
            font-size: 1.6rem !important;
        }
        
        [data-testid="stMetric"] {
            padding: 14px;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.4rem !important;
        }
        
        [data-testid="stSidebar"] {
            min-width: 280px;
        }
        
        .stButton > button {
            padding: 12px 20px;
            font-size: 0.75rem;
        }
    }
    
    /* === PRINT STYLES === */
    @media print {
        .stApp {
            background: white !important;
        }
        
        * {
            color: black !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION (COMPREHENSIVE)
# ═══════════════════════════════════════════════════════════════

# Core Resume/JD State
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
    # Auto-load Master Profile if it exists
    master_profile_path = "assets/MASTER_PROFILE.md"
    if os.path.exists(master_profile_path):
        with open(master_profile_path, "r") as f:
            st.session_state.resume_text = f.read()
if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""
if "voice_resume_text" not in st.session_state:
    st.session_state.voice_resume_text = ""
if "voice_jd_text" not in st.session_state:
    st.session_state.voice_jd_text = ""
if "generated_audio" not in st.session_state:
    st.session_state.generated_audio = None

# Identity & Mindset Programming
if "identity_script" not in st.session_state:
    st.session_state.identity_script = None
if "identity_audio" not in st.session_state:
    st.session_state.identity_audio = None

# Voice Lab / Practice Sessions
if "voice_sessions" not in st.session_state:
    st.session_state.voice_sessions = []
if "ideal_answer" not in st.session_state:
    st.session_state.ideal_answer = None

# Boardroom Simulator
if "sim_active" not in st.session_state:
    st.session_state.sim_active = False
if "current_q" not in st.session_state:
    st.session_state.current_q = None
if "sim_mode" not in st.session_state:
    st.session_state.sim_mode = None

# Career Planning
if "90_day_plan" not in st.session_state:
    st.session_state["90_day_plan"] = None
if "path_result" not in st.session_state:
    st.session_state.path_result = None

# Comms Studio
if "comms_output" not in st.session_state:
    st.session_state.comms_output = None

# Global Target Company (for cross-feature linking)
if "target_company" not in st.session_state:
    st.session_state.target_company = ""

# First Run Flag (for onboarding)
if "first_run" not in st.session_state:
    st.session_state.first_run = True

# Sound Effects Toggle
if "sound_effects" not in st.session_state:
    st.session_state.sound_effects = True

# Comms Studio Metadata
if "comms_target_name" not in st.session_state:
    st.session_state.comms_target_name = ""
if "comms_target_company" not in st.session_state:
    st.session_state.comms_target_company = ""

# Mobile Practice Mode
if "mobile_drill" not in st.session_state:
    st.session_state.mobile_drill = None


# ═══════════════════════════════════════════════════════════════
# SIDEBAR: CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# --- SIDEBAR: MISSION CONTROL (FLUID EXECUTIVE LIBRARY) ---
with st.sidebar:
    # 1. HEADER & SYSTEM STATUS
    st.markdown("### ⚡ BASIN::NEXUS")
    st.caption("v0.5 | EXECUTIVE OS")
    
    st.markdown("---")
    
    # STATUS INDICATOR
    st.markdown("🟢 **ACTIVE** · LLM FLEET READY")
        
    # BIO-OS (Compact)
    import datetime
    if 'session_start' not in st.session_state:
        st.session_state.session_start = datetime.datetime.now()
    session_duration = datetime.datetime.now() - st.session_state.session_start
    hours = int(session_duration.total_seconds() // 3600)
    minutes = int((session_duration.total_seconds() % 3600) // 60)
    st.caption(f"⏱️ Session: {hours}h {minutes}m")
    
    st.markdown("---")
    st.markdown("##### ⚙️ ENGINE")
    
    # Check for Streamlit Secrets first (for always-on deployment)
    secret_key = None
    try:
        secret_key = st.secrets.get("GROQ_API_KEY", None)
    except Exception:
        pass  # Secrets not available in local mode
    
    # Show input field for manual entry
    api_key = st.text_input("GROQ API KEY", type="password", placeholder="gsk_...", label_visibility="collapsed")
    
    # Use manual input if provided, otherwise fall back to secret
    if api_key:
        st.session_state['groq_api_key'] = api_key
        os.environ['GROQ_API_KEY'] = api_key
        st.caption("✅ LINK: SECURE")
    elif secret_key:
        st.session_state['groq_api_key'] = secret_key
        os.environ['GROQ_API_KEY'] = secret_key
        st.caption("✅ LINK: ALWAYS-ON")
    else:
        st.caption("⚠️ LINK: OFFLINE")
        st.markdown("[Get Key](https://console.groq.com)")
    
    # ═══════════════════════════════════════════════════════════════
    # LLM FLEET SELECTOR (V14: FULL GROQ ARSENAL)
    # ═══════════════════════════════════════════════════════════════
    
    # Model Category Selector
    model_category = st.selectbox("🎯 MODEL TYPE",
        ["⚡ TEXT (Fast)", "🧠 REASONING", "🔧 TOOLS", "👁️ VISION", "🎤 SPEECH", "🛡️ SAFETY"],
        label_visibility="collapsed"
    )
    
    # Dynamic Model Selection based on Category
    if model_category == "⚡ TEXT (Fast)":
        selected_model_label = st.selectbox("SELECT ENGINE",
            ["GPT OSS 120B (Groq)", "GPT OSS 20B (Groq)", "Kimi K2 (Groq)", 
             "Llama 4 Scout (Groq)", "Llama 3.3 70B (Groq)"],
            label_visibility="collapsed"
        )
    elif model_category == "🧠 REASONING":
        selected_model_label = st.selectbox("SELECT ENGINE",
            ["GPT OSS 120B (Deep Think)", "GPT OSS 20B (Fast Think)", "Qwen 3 32B (Logic)"],
            label_visibility="collapsed"
        )
    elif model_category == "🔧 TOOLS":
        selected_model_label = st.selectbox("SELECT ENGINE",
            ["GPT OSS 120B (Function Calling)", "Kimi K2 (Agent)", 
             "Llama 4 Scout (MCP)", "Qwen 3 32B (Tools)"],
            label_visibility="collapsed"
        )
    elif model_category == "👁️ VISION":
        selected_model_label = st.selectbox("SELECT ENGINE",
            ["Llama 4 Scout (Vision)", "Llama 4 Maverick (Vision Pro)"],
            label_visibility="collapsed"
        )
    elif model_category == "🎤 SPEECH":
        selected_model_label = st.selectbox("SELECT ENGINE",
            ["Whisper Large v3 (STT)", "Whisper Large v3 Turbo (Fast STT)", "PlayAI TTS (Speech)"],
            label_visibility="collapsed"
        )
    elif model_category == "🛡️ SAFETY":
        selected_model_label = st.selectbox("SELECT ENGINE",
            ["Safety GPT OSS 20B", "Llama Guard"],
            label_visibility="collapsed"
        )
    
    # SYSTEM KERNEL: Map Human Labels to API IDs (CORRECT GROQ IDs)
    model_map = {
        # Text Models (Production)
        "GPT OSS 120B (Groq)": "openai/gpt-oss-120b",
        "GPT OSS 20B (Groq)": "openai/gpt-oss-20b",
        "Llama 3.3 70B (Groq)": "llama-3.3-70b-versatile",
        # Preview Models
        "Kimi K2 (Groq)": "moonshotai/kimi-k2-instruct",
        "Llama 4 Scout (Groq)": "meta-llama/llama-4-scout-17b-16e-instruct",
        # Reasoning Models
        "GPT OSS 120B (Deep Think)": "openai/gpt-oss-120b",
        "GPT OSS 20B (Fast Think)": "openai/gpt-oss-20b",
        "Qwen 3 32B (Logic)": "qwen/qwen3-32b",
        # Tool/Function Calling Models
        "GPT OSS 120B (Function Calling)": "openai/gpt-oss-120b",
        "Kimi K2 (Agent)": "moonshotai/kimi-k2-instruct",
        "Llama 4 Scout (MCP)": "meta-llama/llama-4-scout-17b-16e-instruct",
        "Qwen 3 32B (Tools)": "qwen/qwen3-32b",
        # Vision Models
        "Llama 4 Scout (Vision)": "meta-llama/llama-4-scout-17b-16e-instruct",
        "Llama 4 Maverick (Vision Pro)": "meta-llama/llama-4-maverick-17b-128e-instruct",
        # Speech Models
        "Whisper Large v3 (STT)": "whisper-large-v3",
        "Whisper Large v3 Turbo (Fast STT)": "whisper-large-v3-turbo",
        "PlayAI TTS (Speech)": "playai-tts",
        # Safety Models
        "Safety GPT OSS 20B": "openai/gpt-oss-safeguard-20b",
        "Llama Guard": "meta-llama/llama-guard-4-12b",
    }
    st.session_state['selected_model_id'] = model_map.get(selected_model_label, "llama-3.3-70b-versatile")
    st.caption(f"🔗 `{st.session_state['selected_model_id']}`")
    
    st.markdown("---")

    # 3. MISSION PROTOCOL (THE 3-PHASE ARCHITECTURE)
    st.markdown("##### 🧭 MODULES")
    
    # Initialize Logic for Mutual Exclusivity
    if 'prev_battle' not in st.session_state: st.session_state.prev_battle = "📄 Intel (Omni-Agent)"
    if 'prev_oracle' not in st.session_state: st.session_state.prev_oracle = "🎯 Hunt (Black Ops)"
    if 'prev_builder' not in st.session_state: st.session_state.prev_builder = "📈 Pipeline CRM"
    if 'selected_tool_label' not in st.session_state: st.session_state.selected_tool_label = "📄 Intel (Omni-Agent)"

    # PHASE I: THE BATTLESTATION (PREP)
    with st.expander("⚔️ BATTLESTATION", expanded=True):
        mode_battle = st.radio("Select:", 
            ["📋 INTERVIEW PREP",
             "📄 INTEL AGENT", 
             "🥊 DOJO", 
             "🎤 VOICE LAB", 
             "🛡️ OBJECTIONS"],
            label_visibility="collapsed", key="battle")

    # PHASE II: THE ORACLE ARRAY (SEARCH)
    with st.expander("🛰️ ORACLE ARRAY"):
        mode_oracle = st.radio("Select:", 
            ["🎯 HUNT MODE",
             "📡 MARKET RADAR", 
             "📊 ANALYTICS", 
             "🔬 COMPANY INTEL", 
             "🔥 SWIPE",
             "☁️ G-SUITE"],
            label_visibility="collapsed", key="oracle")

    # PHASE III: THE BUILDER DECK (CLOSE)
    with st.expander("🏗️ BUILDER DECK"):
        mode_builder = st.radio("Select:", 
            ["📈 PIPELINE CRM", 
             "📣 SOCIAL HQ",
             "💰 COMP CALC",
             "🚀 FIRST 90", 
             "🔍 TALENT SIGNAL", 
             "🎙️ DIGITAL TWIN"],
            label_visibility="collapsed", key="builder")

    # LOGIC TO HANDLE MULTIPLE RADIOS (One Ring to Rule Them All)
    # Detect which one changed and update master selection
    if st.session_state.battle != st.session_state.prev_battle:
        st.session_state.selected_tool_label = st.session_state.battle
        st.session_state.prev_battle = st.session_state.battle
        
    elif st.session_state.oracle != st.session_state.prev_oracle:
        st.session_state.selected_tool_label = st.session_state.oracle
        st.session_state.prev_oracle = st.session_state.oracle

    elif st.session_state.builder != st.session_state.prev_builder:
        st.session_state.selected_tool_label = st.session_state.builder
        st.session_state.prev_builder = st.session_state.builder
    
    # MAPPING TO SYSTEM KERNEL (Netflix-style names to internal modes)
    tool_map = {
        "📋 INTERVIEW PREP": "🎯 Prep Mode",
        "📄 INTEL AGENT": "📄 Intel",
        "🥊 DOJO": "🥊 Practice (Dojo)",
        "🎤 VOICE LAB": "🎤 Voice",
        "🛡️ OBJECTIONS": "🛡️ Objection Bank",
        "🎯 HUNT MODE": "🎯 Hunt",
        "📡 MARKET RADAR": "📡 Market Radar",
        "📊 ANALYTICS": "📊 Analytics",
        "🔬 COMPANY INTEL": "🔬 Company Intel",
        "🔥 SWIPE": "🔥 Swipe Mode",
        "☁️ G-SUITE": "☁️ G-Suite Sync",
        "📈 PIPELINE CRM": "📈 Pipeline CRM",
        "📣 SOCIAL HQ": "📣 Social Command Center",
        "💰 COMP CALC": "💰 Negotiation",
        "🚀 FIRST 90": "🚀 First 90 Days",
        "🔍 TALENT SIGNAL": "🔍 Talent Signal",
        "🎙️ DIGITAL TWIN": "🎙️ Live Assist"
    }
    
    # HIDDEN WISDOM
    st.sidebar.markdown("---")

    input_mode = tool_map.get(st.session_state.selected_tool_label, "📄 Intel")

    st.markdown("---")

    # FOOTER
    st.markdown("""<div style='text-align: center; padding: 10px 0;'>
        <span style='color: #D4AF37; font-family: Orbitron, monospace; font-size: 0.7rem;'>LEON BASIN</span><br/>
        <span style='color: #5a5a5a; font-size: 0.65rem;'>OPERATOR ONLINE</span>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# MAIN INTERFACE
# ═══════════════════════════════════════════════════════════════

# Minimal Header - No redundancy with sidebar
col_header, col_status = st.columns([3, 1])
with col_header:
    st.markdown('<p style="color: #708090; font-size: 0.85rem; margin: 0;">REVENUE ARCHITECT OS</p>', unsafe_allow_html=True)
with col_status:
    if st.session_state.get('groq_api_key'):
        st.markdown('<span style="color: #00ff88; font-size: 0.85rem;">● ONLINE</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span style="color: #ff6b6b; font-size: 0.85rem;">● OFFLINE</span>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PRIVACY NOTICE & ORACLE TELEMETRY (THE KABBALAH LAYER)
# ═══════════════════════════════════════════════════════════════

# Privacy Banner (Collapsible)
with st.expander("🔐 PRIVACY & DATA NOTICE", expanded=False):
    st.markdown("""
    <div style="background: rgba(255, 191, 0, 0.05); border: 1px solid rgba(255, 191, 0, 0.2); border-radius: 8px; padding: 16px;">
        <h4 style="color: #FFBF00; margin: 0 0 8px 0;">⚠️ Data Handling Policy</h4>
        <ul style="color: #8892b0; margin: 0; padding-left: 20px;">
            <li><b>No Storage:</b> Your resumes and job descriptions are NOT stored on our servers.</li>
            <li><b>Session Only:</b> All data exists only during your active session and is cleared when you close the browser.</li>
            <li><b>API Transit:</b> Text is sent to AI providers (Groq, OpenAI) for processing. Review their privacy policies.</li>
            <li><b>No PII Collection:</b> We do not collect names, emails, or identifying information.</li>
        </ul>
        <p style="color: #FFBF00; margin: 12px 0 0 0; font-size: 0.85rem;">
            <b>Recommendation:</b> Do not paste highly confidential or proprietary information.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Oracle Feedback Hook (Future Telemetry)
    st.markdown("---")
    st.caption("🧠 **THE ORACLE LEARNS (Anonymously)**")
    st.markdown("""
    <p style="color: #8892b0; font-size: 0.8rem;">
    When you rate outputs (coming soon), the system learns which prompts work best — without ever seeing your data. 
    <br>This is <b>aggregate intelligence</b>: the Oracle gets smarter, but your secrets stay yours.
    </p>
    """, unsafe_allow_html=True)


# Check if we should show Dashboard (default on first load)
show_dashboard = input_mode == "📄 Intel" and not st.session_state.get('resume_vault') and not st.session_state.resume_text

if show_dashboard:
    # ═══════════════════════════════════════════════════════════════
    # 🎬 NETFLIX-STYLE DASHBOARD (SEASON 1: THE PIVOT)
    # ═══════════════════════════════════════════════════════════════
    
    # 1. GAMIFICATION ENGINE (LOC & BUILD TRACKER)
    try:
        from logic.integrations import count_project_lines, get_build_stats, squash_bug, calculate_possibilities
        
        # Scan current directory for LOC
        loc_stats = count_project_lines(".")
        # Load RPG Save File
        build_stats = get_build_stats()
        # Calculate Branching Factor
        possibility_metric = calculate_possibilities(loc_stats.get('total_lines', 0), loc_stats.get('file_count', 0))
        
    except ImportError:
        loc_stats = {"level": 1, "total_lines": 0, "xp_current": 0, "xp_needed": 500, "progress": 0}
        build_stats = {"hours_coded": 17.5, "bugs_squashed": 0, "level": 1}
        possibility_metric = "∞"

    # MISSION BRIEFING HEADER (Gold/Black)
    st.markdown(f"""
        <div style="background:linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('https://images.unsplash.com/photo-1550751827-4bd374c3f58b'); background-size: cover; border-radius: 16px; padding: 40px; margin-bottom: 30px; border: 1px solid #FFD700;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style="color: #FFD700; font-size: 3.5rem; margin: 0; text-shadow: 0 4px 20px rgba(0,0,0,0.8); font-weight: 800;">BASIN::NEXUS</h1>
                    <p style="color: #fff; font-size: 1.2rem; font-family: monospace;">
                        <span style="color: #00ff88;">● ONLINE</span> | 
                        <span style="color: #FFD700;">📡 NETWORK VELOCITY: 12.5 TB/s</span>
                    </p>
                </div>
                
                <div style="text-align: right; background: rgba(0,0,0,0.6); padding: 20px; border-radius: 8px; backdrop-filter: blur(5px); border: 1px solid #FFD700;">
                     <div style="color: #888; font-size: 0.8rem; letter-spacing: 2px;">JOB PROBABILITY</div>
                     <div style="color: #FFD700; font-size: 2.5rem; font-weight: 800;">85%</div>
                     <div style="color: #00ff88; font-size: 0.8rem;">CALCULATED WIN RATE</div>
                </div>
            </div>
            
            <div style="margin-top: 30px; display: flex; gap: 20px;">
                <div style="background: rgba(255, 255, 255, 0.05); padding: 15px 25px; border-radius: 8px; border: 1px solid #333;">
                    <div style="color: #888; font-size: 0.8rem;">TOTAL DEALS</div>
                    <div style="color: #fff; font-size: 1.5rem; font-weight: bold;">12 ↗</div>
                </div>
                 <div style="background: rgba(255, 255, 255, 0.05); padding: 15px 25px; border-radius: 8px; border: 1px solid #333;">
                    <div style="color: #888; font-size: 0.8rem;">ACTIVE / HOT</div>
                    <div style="color: #FF4B4B; font-size: 1.5rem; font-weight: bold;">5 🔥</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # GAMIFICATION INTERACTION (Hidden Controls)
    with st.expander("🎮 BUILDER CONTROLS", expanded=True):
        g_col1, g_col2 = st.columns(2)
        with g_col1:
            if st.button("🐛 SQUASH BUG (+1 XP)"):
                new_count = squash_bug()
                st.toast(f"💥 BUG SQUASHED! Total: {new_count}", icon="🦟")
                st.rerun()
        with g_col2:
            st.caption(f"Current Session: {build_stats['hours_coded']} Hours Logged")


    # EPISODE CARDS (Tools)
    st.markdown("### 📺 CONTINUE WATCHING")
    
    ep_col1, ep_col2, ep_col3, ep_col4 = st.columns(4)
    
    with ep_col1:
        st.info("EPISODE 1: THE HUNT")
        st.caption("Use 'Sniper Prospecting' to find high-value targets.")
        
    with ep_col2:
        st.success("EPISODE 2: THE BUILD")
        st.caption("Craft your narrative in the 'Post Forge'.")
        
    with ep_col3:
        st.warning("EPISODE 3: THE PITCH")
        st.caption("Practice voice drills in the 'Combat Simulator'.")
        
    with ep_col4:
        st.error("EPISODE 4: THE CLOSE")
        st.caption("Manage pipeline deals in the 'CRM'.")
        
    st.markdown("---")
    
    # "Trending Now" Row
    st.markdown("### 🔥 TRENDING NOW")
    trend_col1, trend_col2 = st.columns(2)
    
    with trend_col1:
        st.markdown(f"""
        <div style="background: #141414; padding: 20px; border-radius: 8px; border-left: 4px solid #FFD700;">
            <h4 style="color: white; margin: 0;">VIBE CODING COMMUNITY</h4>
            <p style="color: #999; font-size: 0.9rem;">New Strategy: "Shipping Velocity"</p>
            <p style="color: #FFD700; font-size: 0.8rem;">98% MATCH FOR YOU</p>
        </div>
        """, unsafe_allow_html=True)
        
    with trend_col2:
        st.markdown(f"""
        <div style="background: #141414; padding: 20px; border-radius: 8px; border-left: 4px solid #00ff88;">
            <h4 style="color: white; margin: 0;">MARKET RADAR</h4>
            <p style="color: #999; font-size: 0.9rem;">Signal: Fintech Hiring Surge</p>
            <p style="color: #00ff88; font-size: 0.8rem;">NEW INTEL DROPPED</p>
        </div>
        """, unsafe_allow_html=True)

    # --- FIRST RUN ONBOARDING (Hidden usually, logic kept for safety) ---
    if st.session_state.first_run:
        st.session_state.first_run = False # Auto-acknowledge

    
    st.markdown("---")

    
    # --- 1. THE 4-PHASE PIPELINE (Strategic Navigation) ---
    st.markdown("### 🧭 WHERE ARE YOU IN THE HUNT?")
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 2px solid #00d4ff; border-radius: 12px; padding: 20px; text-align: center; min-height: 140px;">
            <h3 style="color: #00d4ff; margin: 0 0 8px 0;">🔍</h3>
            <h4 style="color: #00d4ff; margin: 0 0 8px 0;">DISCOVERY</h4>
            <p style="color: #8892b0; font-size: 0.75rem; margin: 0;">Find targets before they list</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("LAUNCH RADAR", use_container_width=True, key="db_hunt"):
            st.session_state.selected_tool_label = "🎯 Hunt (Black Ops)"
            st.rerun()
    
    with c2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 2px solid #ffd700; border-radius: 12px; padding: 20px; text-align: center; min-height: 140px;">
            <h3 style="color: #ffd700; margin: 0 0 8px 0;">📝</h3>
            <h4 style="color: #ffd700; margin: 0 0 8px 0;">POSITION</h4>
            <p style="color: #8892b0; font-size: 0.75rem; margin: 0;">Tailor the narrative asset</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("BUILD DOSSIER", use_container_width=True, key="db_intel"):
            st.session_state.selected_tool_label = "📄 Intel (Omni-Agent)"
            st.rerun()
    
    with c3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 2px solid #ff6b6b; border-radius: 12px; padding: 20px; text-align: center; min-height: 140px;">
            <h3 style="color: #ff6b6b; margin: 0 0 8px 0;">🎤</h3>
            <h4 style="color: #ff6b6b; margin: 0 0 8px 0;">COMBAT</h4>
            <p style="color: #8892b0; font-size: 0.75rem; margin: 0;">Win the room (Interview)</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("ENTER DOJO", use_container_width=True, key="db_dojo"):
            st.session_state.selected_tool_label = "🥊 Boardroom (Dojo)"
            st.rerun()
    
    with c4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 2px solid #00ff88; border-radius: 12px; padding: 20px; text-align: center; min-height: 140px;">
            <h3 style="color: #00ff88; margin: 0 0 8px 0;">💰</h3>
            <h4 style="color: #00ff88; margin: 0 0 8px 0;">CLOSE</h4>
            <p style="color: #8892b0; font-size: 0.75rem; margin: 0;">Negotiate the $220k package</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("NEGOTIATE", use_container_width=True, key="db_negotiate"):
            st.session_state.selected_tool_label = "💰 Negotiation (Comp)"
            st.rerun()
    
    st.markdown("---")

    # --- 1.5. MINDSET & IDENTITY PRIMING (NEW) ---
    st.markdown("### 🧠 IDENTITY & MINDSET PROGRAMMING")
    st.caption("Internalize your new role. Listen to this before every interview.")
    
    col_id1, col_id2 = st.columns([3, 1])
    with col_id1:
        st.info("💡 **CONCEPT:** This tool generates a hypnotic audio loop of your core achievements and value proposition. Use it to 'prime' your subconscious before high-stakes interactions.")
    with col_id2:
        if st.button("🎧 GENERATE AUDIO LOOP", type="primary", use_container_width=True):
            with st.spinner("Synthesizing Executive Voice..."):
                from logic.generator import generate_plain_text
                
                # Generate the Script - making it punchy and affirmative
                identity_prompt = f"""
                Write a 60-second "Executive Identity Script" for Leon Basin.
                It should be in the SECOND PERSON ("You are...").
                
                Context:
                - He is a top 1% GTM Systems Architect.
                - He achieved 160% Pipeline Growth.
                - He built a $10M Pipeline at Sense.
                - He is calm, strategic, and commands respect.
                - He is worth $220,000+.
                
                Style: Hypnotic, confident, short impactful sentences. "You are the architect." "You see what others miss."
                """
                
                model_id = st.session_state.get('selected_model_id', "llama-3.3-70b-versatile")
                script = generate_plain_text(identity_prompt, model_name=model_id)
                st.session_state['identity_script'] = script
                
                # Convert to Audio
                try:
                    from gtts import gTTS
                    from io import BytesIO
                    tts = gTTS(script, lang='en', tld='us')
                    audio_bytes = BytesIO()
                    tts.write_to_fp(audio_bytes)
                    st.session_state['identity_audio'] = audio_bytes
                except Exception as e:
                    st.error(f"Audio Gen Error: {e}")

    if st.session_state.get('identity_script'):
        st.success(f"🗣️ **SCRIPT:** {st.session_state['identity_script']}")
        if st.session_state.get('identity_audio'):
            st.audio(st.session_state['identity_audio'], format='audio/mp3')

    st.markdown("---")
    
    # --- 2. JOB PROBABILITY CALCULATOR ---
    st.markdown("### 🎯 JOB PROBABILITY CALCULATOR")
    st.caption("Based on your CRM data, relationship strength, and practice sessions.")
    
    # Gather all data for calculation
    deals = st.session_state.get('crm_deals', [])
    contacts = st.session_state.get('crm_contacts', [])
    voice_sessions = st.session_state.get('voice_sessions', [])
    wins = st.session_state.get('win_loss_memory', {}).get('wins', [])
    
    # Calculate scores
    interview_count = sum(1 for d in deals if d.get('Stage') in ['Interview', 'Interview Scheduled', 'Final', 'Offer']) if deals else 0
    final_rounds = sum(1 for d in deals if d.get('Stage') in ['Final', 'Offer']) if deals else 0
    active_deals = len(deals) if deals else 0
    
    # Relationship Strength Score (count strong connections)
    strong_connections = sum(1 for c in contacts if '🔗🔗🔗' in c.get('Strength', '')) if contacts else 0
    champion_connections = sum(1 for c in contacts if '🔗🔗🔗🔗🔗' in c.get('Strength', '')) if contacts else 0
    
    # Practice Score
    practice_sessions = len(voice_sessions) if voice_sessions else 0
    
    # Calculate probability (weighted formula)
    base_score = 10  # Everyone starts at 10%
    pipeline_score = min(active_deals * 5, 25)  # Up to 25% from pipeline
    interview_score = interview_count * 10  # 10% per interview
    final_score = final_rounds * 15  # 15% per final round
    network_score = min(strong_connections * 3 + champion_connections * 7, 20)  # Up to 20% from network
    practice_score = min(practice_sessions * 2, 10)  # Up to 10% from practice
    
    total_probability = min(base_score + pipeline_score + interview_score + final_score + network_score + practice_score, 95)
    
    # Display the probability meter
    prob_color = "#00ff88" if total_probability >= 60 else "#ffd700" if total_probability >= 35 else "#ff6b6b"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #0a0a1a 100%); 
                border: 2px solid {prob_color}; border-radius: 16px; padding: 24px; text-align: center;">
        <p style="color: #8892b0; margin: 0 0 8px 0; font-size: 0.9rem;">🎯 PROBABILITY OF LANDING $200K+ ROLE IN 30 DAYS</p>
        <h1 style="color: {prob_color}; margin: 0; font-size: 3.5rem;">{total_probability}%</h1>
        <p style="color: #8892b0; margin: 8px 0 0 0; font-size: 0.8rem;">Based on {active_deals} deals, {interview_count} interviews, {strong_connections} strong connections</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Breakdown
    with st.expander("📊 SCORE BREAKDOWN"):
        breakdown_cols = st.columns(5)
        breakdown_cols[0].metric("Pipeline", f"+{pipeline_score}%", f"{active_deals} deals")
        breakdown_cols[1].metric("Interviews", f"+{interview_score}%", f"{interview_count} active")
        breakdown_cols[2].metric("Final Rounds", f"+{final_score}%", f"{final_rounds} active")
        breakdown_cols[3].metric("Network", f"+{network_score}%", f"{strong_connections} strong")
        breakdown_cols[4].metric("Practice", f"+{practice_score}%", f"{practice_sessions} sessions")
        
        st.markdown("---")
        st.markdown("**How to increase your probability:**")
        
        if interview_count < 3:
            st.info("📈 **+30% potential:** Get 3+ interviews scheduled")
        if strong_connections < 5:
            st.info("🔗 **+15% potential:** Build 5+ strong relationships (🔗🔗🔗+)")
        if practice_sessions < 5:
            st.info("🎤 **+10% potential:** Complete 5+ voice practice sessions")
        if final_rounds == 0:
            st.info("🏆 **+15% potential:** Advance 1 deal to final round")
    
    st.markdown("---")
    
    # --- 3. NETWORK HEALTH SCORE ---
    st.markdown("### 🔗 NETWORK HEALTH")
    
    network_cols = st.columns(4)
    cold_contacts = sum(1 for c in contacts if c.get('Strength', '🔗') == '🔗') if contacts else 0
    warm_contacts = sum(1 for c in contacts if '🔗🔗' in c.get('Strength', '') and '🔗🔗🔗' not in c.get('Strength', '')) if contacts else 0
    
    network_cols[0].metric("❄️ COLD", cold_contacts, "Need nurturing")
    network_cols[1].metric("🌤️ WARM", warm_contacts, "Keep engaged")
    network_cols[2].metric("🔥 STRONG", strong_connections, "Leverage for intros")
    network_cols[3].metric("👑 CHAMPIONS", champion_connections, "Ask for referrals")
    
    # Network Actions
    if cold_contacts > 5:
        st.warning(f"⚠️ You have {cold_contacts} cold contacts. Consider sending follow-ups to warm them up.")
    if champion_connections > 0:
        st.success(f"🎯 You have {champion_connections} champions! Ask them for warm intros to your target companies.")
    
    st.markdown("---")
    
    # --- 4. GAMIFICATION: MISSION XP & ACHIEVEMENTS ---
    st.markdown("### 🎮 MISSION XP & ACHIEVEMENTS")
    
    # Calculate XP
    xp_pipeline = active_deals * 50
    xp_interviews = interview_count * 200
    xp_finals = final_rounds * 500
    xp_network = (strong_connections * 30) + (champion_connections * 100)
    xp_practice = practice_sessions * 25
    xp_wins = len(wins) * 1000 if wins else 0
    
    total_xp = xp_pipeline + xp_interviews + xp_finals + xp_network + xp_practice + xp_wins
    
    # Determine Rank
    if total_xp >= 5000:
        rank = "🏆 REVENUE LEGEND"
        rank_color = "#FFD700"
    elif total_xp >= 2500:
        rank = "⚔️ DEAL HUNTER"
        rank_color = "#C0C0C0"
    elif total_xp >= 1000:
        rank = "🎯 PIPELINE BUILDER"
        rank_color = "#CD7F32"
    else:
        rank = "🌱 PROSPECT"
        rank_color = "#8892b0"
    
    # XP Display
    xp_cols = st.columns([2, 1])
    with xp_cols[0]:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a2e in 0%, #0a0a1a 100%); 
                    border: 2px solid {rank_color}; border-radius: 12px; padding: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <p style="color: #8892b0; margin: 0; font-size: 0.8rem;">CURRENT RANK</p>
                    <h2 style="color: {rank_color}; margin: 4px 0;">{rank}</h2>
                </div>
                <div style="text-align: right;">
                    <p style="color: #8892b0; margin: 0; font-size: 0.8rem;">TOTAL XP</p>
                    <h2 style="color: #FFBF00; margin: 4px 0;">{total_xp:,}</h2>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with xp_cols[1]:
        # XP Breakdown
        st.caption("XP Sources:")
        st.caption(f"Pipeline: +{xp_pipeline} | Interviews: +{xp_interviews}")
        st.caption(f"Network: +{xp_network} | Practice: +{xp_practice}")
    
    # Achievements
    st.markdown("##### 🏅 ACHIEVEMENTS UNLOCKED")
    achievement_cols = st.columns(5)
    
    achievements = []
    if active_deals >= 5: achievements.append(("📊", "Pipeline Pro", "5+ Deals"))
    if interview_count >= 3: achievements.append(("🎤", "Interview Ready", "3+ Interviews"))
    if champion_connections >= 1: achievements.append(("👑", "Champion Builder", "1+ Champion"))
    if practice_sessions >= 5: achievements.append(("🎯", "Voice Master", "5+ Sessions"))
    if total_xp >= 1000: achievements.append(("⭐", "First 1K", "1000+ XP"))
    
    if achievements:
        for i, (emoji, name, desc) in enumerate(achievements[:5]):
            with achievement_cols[i]:
                st.markdown(f"""
                <div style="background: rgba(255,215,0,0.1); border: 1px solid #FFD700; border-radius: 8px; padding: 12px; text-align: center;">
                    <p style="font-size: 1.5rem; margin: 0;">{emoji}</p>
                    <p style="color: #FFD700; font-size: 0.75rem; margin: 4px 0 0 0; font-weight: bold;">{name}</p>
                    <p style="color: #8892b0; font-size: 0.6rem; margin: 0;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("🎮 Complete actions to unlock achievements!")
    
    st.markdown("---")
    
    # ═══════════════════════════════════════════════════════════════
    # ♟️ CAREER CHESS BOARD (THE GAME VISUALIZATION)
    # ═══════════════════════════════════════════════════════════════
    st.markdown("### ♟️ CAREER CHESS BOARD")
    st.caption("Your job search as a strategic chess game. Every move counts.")
    
    # Calculate Chess Position (0-63, like a chess board)
    chess_score = min(63, (interview_count * 8) + (final_rounds * 16) + (champion_connections * 4) + (active_deals * 2))
    chess_row = chess_score // 8
    chess_col = chess_score % 8
    
    # Determine Piece Level
    if final_rounds >= 2:
        piece = "👑"  # King - About to win
        piece_name = "KING"
    elif interview_count >= 3:
        piece = "👸"  # Queen - Strong position
        piece_name = "QUEEN"
    elif interview_count >= 1:
        piece = "🏰"  # Rook - Solid foundation
        piece_name = "ROOK"
    elif active_deals >= 5:
        piece = "🐴"  # Knight - Active movement
        piece_name = "KNIGHT"
    elif strong_connections >= 3:
        piece = "⛪"  # Bishop - Diagonal power
        piece_name = "BISHOP"
    else:
        piece = "♟️"  # Pawn - Starting out
        piece_name = "PAWN"
    
    # Chess Board Visual (8x8 grid)
    st.markdown(f"""
    <style>
    .chess-board {{
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        gap: 2px;
        max-width: 400px;
        margin: 0 auto;
    }}
    .chess-cell {{
        aspect-ratio: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        border-radius: 4px;
    }}
    .chess-light {{ background: rgba(255, 215, 0, 0.15); }}
    .chess-dark {{ background: rgba(255, 191, 0, 0.05); }}
    .chess-current {{ 
        background: linear-gradient(135deg, #FFD700, #FFBF00) !important;
        animation: pulse-piece 1.5s ease-in-out infinite;
    }}
    @keyframes pulse-piece {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.1); }}
    }}
    </style>
    
    <div class="chess-board">
    """, unsafe_allow_html=True)
    
    # Generate board
    board_html = ""
    for row in range(7, -1, -1):  # Top to bottom
        for col in range(8):
            cell_class = "chess-light" if (row + col) % 2 == 0 else "chess-dark"
            cell_index = row * 8 + col
            
            if row == chess_row and col == chess_col:
                cell_class = "chess-current"
                content = piece
            elif cell_index < chess_score:
                content = "·"  # Passed squares
            else:
                content = ""
            
            board_html += f'<div class="chess-cell {cell_class}">{content}</div>'
    
    st.markdown(board_html + "</div>", unsafe_allow_html=True)
    
    # Position Intel
    st.markdown(f"""
    <div style="text-align: center; margin-top: 16px;">
        <p style="color: #8892b0; margin: 0;">YOUR PIECE</p>
        <h2 style="color: #FFD700; margin: 8px 0;">{piece} {piece_name}</h2>
        <p style="color: #8892b0; font-size: 0.9rem;">Position: Row {chess_row + 1} / Col {chess_col + 1} | Score: {chess_score}/63</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Next Moves
    st.markdown("##### ♟️ NEXT BEST MOVES")
    move_cols = st.columns(3)
    with move_cols[0]:
        st.markdown("""
        <div style="background: rgba(0,255,136,0.1); border: 1px solid #00ff88; border-radius: 8px; padding: 12px; text-align: center;">
            <p style="font-size: 1.2rem; margin: 0;">🏃</p>
            <p style="color: #00ff88; font-size: 0.8rem; margin: 4px 0;">ADVANCE</p>
            <p style="color: #8892b0; font-size: 0.7rem; margin: 0;">Get 1 more interview</p>
        </div>
        """, unsafe_allow_html=True)
    with move_cols[1]:
        st.markdown("""
        <div style="background: rgba(0,212,255,0.1); border: 1px solid #00d4ff; border-radius: 8px; padding: 12px; text-align: center;">
            <p style="font-size: 1.2rem; margin: 0;">🏰</p>
            <p style="color: #00d4ff; font-size: 0.8rem; margin: 4px 0;">CASTLE</p>
            <p style="color: #8892b0; font-size: 0.7rem; margin: 0;">Strengthen network</p>
        </div>
        """, unsafe_allow_html=True)
    with move_cols[2]:
        st.markdown("""
        <div style="background: rgba(255,191,0,0.1); border: 1px solid #FFBF00; border-radius: 8px; padding: 12px; text-align: center;">
            <p style="font-size: 1.2rem; margin: 0;">⚔️</p>
            <p style="color: #FFBF00; font-size: 0.8rem; margin: 4px 0;">ATTACK</p>
            <p style="color: #8892b0; font-size: 0.7rem; margin: 0;">Send 3 cold outreaches</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ═══════════════════════════════════════════════════════════════
    # 🧠 CAREER READINESS BRAIN SCANNER
    # ═══════════════════════════════════════════════════════════════
    st.markdown("### 🧠 CAREER READINESS SCANNER")
    st.caption("Live scan of your job-hunting vital signs. How close are you to landing?")
    
    # Calculate Skill Scores (0-100)
    skill_networking = min(100, (strong_connections * 15) + (champion_connections * 25) + (warm_contacts * 5))
    skill_communication = min(100, (practice_sessions * 10) + (interview_count * 15))
    skill_pipeline = min(100, (active_deals * 10) + (final_rounds * 30))
    skill_strategy = min(100, 30 + (interview_count * 10) + (final_rounds * 20))  # Base 30 for having a plan
    skill_resilience = min(100, 20 + (practice_sessions * 8) + (active_deals * 5))  # Base 20 for showing up
    
    overall_readiness = (skill_networking + skill_communication + skill_pipeline + skill_strategy + skill_resilience) // 5
    
    # Animated Scanner Visual
    readiness_color = "#00ff88" if overall_readiness >= 70 else "#FFD700" if overall_readiness >= 40 else "#ff6b6b"
    
    st.markdown(f"""
    <style>
    @keyframes scan-pulse {{
        0% {{ box-shadow: 0 0 10px {readiness_color}40; }}
        50% {{ box-shadow: 0 0 30px {readiness_color}80, 0 0 60px {readiness_color}40; }}
        100% {{ box-shadow: 0 0 10px {readiness_color}40; }}
    }}
    .brain-scanner {{
        background: linear-gradient(135deg, #0a0a1a, #1a1a2e);
        border: 3px solid {readiness_color};
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        animation: scan-pulse 2s ease-in-out infinite;
    }}
    </style>
    
    <div class="brain-scanner">
        <p style="color: #8892b0; margin: 0; font-size: 0.9rem;">CAREER READINESS LEVEL</p>
        <h1 style="color: {readiness_color}; margin: 10px 0; font-size: 4rem;">{overall_readiness}%</h1>
        <p style="color: #8892b0; margin: 0;">{'🟢 READY TO LAND' if overall_readiness >= 70 else '🟡 BUILDING MOMENTUM' if overall_readiness >= 40 else '🔴 NEEDS WORK'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Skill Radar / Brain Attributes
    st.markdown("##### 🎯 SKILL ATTRIBUTES")
    
    skills_data = [
        ("🔗 NETWORKING", skill_networking, "#00d4ff"),
        ("🗣️ COMMUNICATION", skill_communication, "#00ff88"),
        ("📊 PIPELINE", skill_pipeline, "#FFD700"),
        ("🧠 STRATEGY", skill_strategy, "#ff6b6b"),
        ("💪 RESILIENCE", skill_resilience, "#9b59b6"),
    ]
    
    for skill_name, skill_value, skill_color in skills_data:
        st.markdown(f"""
        <div style="margin: 8px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="color: #ccd6f6; font-size: 0.85rem;">{skill_name}</span>
                <span style="color: {skill_color}; font-weight: bold;">{skill_value}/100</span>
            </div>
            <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 10px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, {skill_color}80, {skill_color}); width: {skill_value}%; height: 100%; border-radius: 10px; transition: width 0.5s;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Weakest Skill Alert
    weakest_skill = min(skills_data, key=lambda x: x[1])
    st.markdown(f"""
    <div style="background: rgba(255,107,107,0.1); border: 1px solid #ff6b6b; border-radius: 8px; padding: 12px; margin-top: 16px;">
        <p style="color: #ff6b6b; margin: 0; font-weight: bold;">⚠️ FOCUS AREA: {weakest_skill[0]}</p>
        <p style="color: #8892b0; font-size: 0.85rem; margin: 4px 0 0 0;">This is your weakest attribute. Prioritize actions that boost it!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- 5. LINKEDIN RSS FEED (Target Company Monitor) ---
    st.markdown("### 📡 COMPANY INTEL FEED")
    st.caption("Real-time news from your target companies.")
    
    # Get top 3 companies from pipeline
    if deals:
        top_companies = list(set([d.get('Company', '') for d in deals[:5] if d.get('Company')]))
    else:
        top_companies = ["Anthropic", "Mistral AI", "OpenAI"]
    
    feed_company = st.selectbox("🎯 Monitor Company:", top_companies + ["Custom..."], key="feed_company")
    
    if feed_company == "Custom...":
        feed_company = st.text_input("Enter company name:", key="custom_feed_company")
    
    if feed_company and feed_company != "Custom...":
        import feedparser
        import urllib.parse
        
        with st.spinner(f"Fetching intel for {feed_company}..."):
            encoded = urllib.parse.quote(feed_company)
            rss_url = f"https://news.google.com/rss/search?q={encoded}+hiring+OR+funding+OR+layoffs&hl=en-US&gl=US&ceid=US:en"
            feed = feedparser.parse(rss_url)
            
            if feed.entries:
                for entry in feed.entries[:4]:
                    st.markdown(f"""
                    <div style="background: rgba(255,191,0,0.05); border-left: 3px solid #FFBF00; padding: 12px; margin: 8px 0;">
                        <a href="{entry.link}" target="_blank" style="color: #ccd6f6; text-decoration: none; font-weight: 500;">
                            {entry.title}
                        </a>
                        <p style="color: #8892b0; font-size: 0.75rem; margin: 4px 0 0 0;">{entry.get('published', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                st.caption("No recent news found for this company.")
    
    st.markdown("---")
    
    # --- 6. APPLE NEWS STYLE FEED ---
    st.markdown("### 📰 INDUSTRY INTEL (APPLE NEWS STYLE)")
    st.caption("Curated business intelligence from multiple sources.")
    
    news_tabs = st.tabs(["🔥 Tech/AI", "💰 VC & Funding", "📊 Business", "🎯 Jobs"])
    
    news_sources = {
        "🔥 Tech/AI": "https://news.google.com/rss/search?q=AI+hiring+OR+tech+layoffs+OR+startup+funding&hl=en-US&gl=US&ceid=US:en",
        "💰 VC & Funding": "https://techcrunch.com/category/startups/feed/",
        "📊 Business": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en",
        "🎯 Jobs": "https://news.google.com/rss/search?q=revenue+operations+hiring+OR+GTM+jobs+OR+sales+director+jobs&hl=en-US&gl=US&ceid=US:en"
    }
    
    import feedparser
    
    for i, (tab_name, rss_url) in enumerate(news_sources.items()):
        with news_tabs[i]:
            try:
                feed = feedparser.parse(rss_url)
                if feed.entries:
                    for entry in feed.entries[:3]:
                        # Apple News style card
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02)); 
                                    border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 16px; margin: 12px 0;
                                    transition: all 0.3s; cursor: pointer;">
                            <a href="{entry.link}" target="_blank" style="text-decoration: none;">
                                <h4 style="color: #ccd6f6; margin: 0 0 8px 0; font-size: 1rem; line-height: 1.4;">{entry.title}</h4>
                            </a>
                            <p style="color: #8892b0; font-size: 0.75rem; margin: 0;">
                                {entry.get('published', '')[:20] if entry.get('published') else 'Recent'}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.caption("Loading news...")
            except Exception as e:
                st.caption(f"Feed unavailable: {e}")
    
    st.markdown("---")
    
    # --- 7. UPCOMING INTERVIEWS (Calendar Integration) ---
    st.markdown("### 📅 UPCOMING INTERVIEWS")
    st.caption("Your scheduled interviews for the next 7 days.")
    
    # Check for calendar events in session state
    if 'calendar_events' not in st.session_state:
        st.session_state['calendar_events'] = []
    
    # Display upcoming events
    if st.session_state['calendar_events']:
        for event in st.session_state['calendar_events'][:5]:
            event_color = "#00ff88" if "Final" in event.get('type', '') else "#FFD700"
            st.markdown(f"""
            <div style="background: rgba(255,191,0,0.05); border-left: 4px solid {event_color}; 
                        padding: 16px; margin: 8px 0; border-radius: 0 8px 8px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="color: #ccd6f6; margin: 0;">{event.get('title', 'Interview')}</h4>
                        <p style="color: #8892b0; margin: 4px 0 0 0; font-size: 0.85rem;">
                            🏢 {event.get('company', 'Company')} | 📍 {event.get('type', 'Interview')}
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <p style="color: {event_color}; font-weight: bold; margin: 0;">{event.get('date', 'TBD')}</p>
                        <p style="color: #8892b0; font-size: 0.75rem; margin: 4px 0 0 0;">{event.get('time', '')}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📅 No upcoming interviews scheduled. Add one below!")
    
    # Add new interview
    with st.expander("➕ ADD INTERVIEW"):
        add_cols = st.columns([2, 2, 1])
        new_company = add_cols[0].text_input("Company", key="cal_company")
        new_date = add_cols[1].date_input("Date", key="cal_date")
        new_type = add_cols[2].selectbox("Type", ["Phone Screen", "Hiring Manager", "Final Round", "CEO/Panel"], key="cal_type")
        
        if st.button("📅 ADD TO CALENDAR", use_container_width=True):
            if new_company:
                st.session_state['calendar_events'].append({
                    'title': f"{new_type} - {new_company}",
                    'company': new_company,
                    'date': str(new_date),
                    'type': new_type,
                    'time': ''
                })
                st.toast(f"📅 Interview with {new_company} added!", icon="✅")
                st.rerun()
        
        # Google Calendar link
        if new_company:
            import urllib.parse
            gcal_title = urllib.parse.quote(f"Interview: {new_company} ({new_type})")
            gcal_link = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={gcal_title}&dates={str(new_date).replace('-', '')}T100000/{str(new_date).replace('-', '')}T110000"
            st.markdown(f"[📅 Open in Google Calendar]({gcal_link})")
    
    st.markdown("---")
    
    # --- 8. PIPELINE METRICS ---
    st.markdown("### 📊 CAMPAIGN STATUS")
    
    # --- 3. CRITICAL ACTIONS (Next 24H) ---
    st.markdown("### 🚨 CRITICAL ACTIONS (NEXT 24H)")
    
    st.markdown("""
    <div style="background: rgba(255, 107, 107, 0.1); border: 1px solid rgba(255, 107, 107, 0.3); border-radius: 8px; padding: 16px; margin-bottom: 12px;">
        <p style="color: #ff6b6b; margin: 0;"><b>⚔️ PREP:</b> NVIDIA CRO Interview upcoming → <i>Run Boardroom Simulator with "NVIDIA" profile</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(255, 215, 0, 0.1); border: 1px solid rgba(255, 215, 0, 0.3); border-radius: 8px; padding: 16px; margin-bottom: 12px;">
        <p style="color: #ffd700; margin: 0;"><b>📧 FOLLOW-UP:</b> LinkedIn/eBay applications pending → <i>Generate Sniper Email via Intel Mode</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(0, 212, 255, 0.1); border: 1px solid rgba(0, 212, 255, 0.3); border-radius: 8px; padding: 16px;">
        <p style="color: #00d4ff; margin: 0;"><b>📡 INTEL:</b> Check Market Radar for sector signals → <i>AI/Security hiring trends</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- 4. QUICK START (For New Users) ---
    with st.expander("📘 GETTING STARTED GUIDE"):
        st.markdown("""
        **Step 1:** Add your Groq API key in the sidebar (free at console.groq.com)
        
        **Step 2:** Choose your phase above based on where you are:
        - **DISCOVERY** → Finding new opportunities
        - **POSITION** → Tailoring your pitch for a specific role
        - **COMBAT** → Preparing for interviews
        - **CLOSE** → Negotiating compensation
        
        **Step 3:** Use the sidebar expanders to access all 14+ tools
        
        **Pro Tip:** The Boardroom Simulator now supports company-specific profiles (NVIDIA, LinkedIn, eBay)
        """)
    
    # Stop here - don't render the rest of the app
    st.stop()

# ═══════════════════════════════════════════════════════════════
# NORMAL MODE FLOW (Two-column layout)
# ═══════════════════════════════════════════════════════════════
col1, col2 = st.columns([1, 1], gap="large")

# ═══════════════════════════════════════════════════════════════
# INPUT COLUMN
# ═══════════════════════════════════════════════════════════════

with col1:
    st.markdown("### 📥 Ingest Data (The Signal)")
    
    # Input Mode Toggle - FULL ARSENAL
    # Input Mode Controlled by Sidebar
    st.info(f"🧬 SYSTEM MODE: **{input_mode}**")
    
    st.markdown("")
    
    # ─────────────────────────────────────────────────────────────
    # INTEL MODE (The Data Center HUD)
    # ─────────────────────────────────────────────────────────────
    # ==============================================================================
    # 🎯 MODE 0: PREP MODE (INTERVIEW COMMAND CENTER)
    # ==============================================================================
    if input_mode == "🎯 Prep Mode":
        st.markdown("## 🎯 INTERVIEW PREP MODE")
        st.caption("PROTOCOL: Everything you need before your call. Zero distractions. Maximum preparation.")
        
        # Get upcoming interviews from CRM
        deals = st.session_state.get('crm_deals', [])
        calendar_events = st.session_state.get('calendar_events', [])
        
        # Find interview-stage deals
        interview_deals = [d for d in deals if d.get('Stage') in ['Interview Scheduled', '1st Interview', '2nd Interview', 'Final Round', 'Under Review (HM)']]
        
        # Combine with calendar events
        upcoming = []
        for d in interview_deals:
            upcoming.append({
                'company': d.get('Company', 'Unknown'),
                'role': d.get('Role', 'Unknown'),
                'stage': d.get('Stage', 'Interview'),
                'notes': d.get('Notes', '')
            })
        for e in calendar_events:
            upcoming.append({
                'company': e.get('company', 'Unknown'),
                'role': e.get('title', 'Interview'),
                'stage': e.get('type', 'Interview'),
                'date': e.get('date', 'TBD')
            })
        
        if not upcoming:
            # Default if no interviews scheduled
            upcoming = [{
                'company': 'Example Company',
                'role': 'Account Executive',
                'stage': 'Interview',
                'notes': 'Add interviews in Pipeline CRM'
            }]
        
        # ═══════════════════════════════════════════════════════════════
        # INTERVIEW SELECTOR
        # ═══════════════════════════════════════════════════════════════
        st.markdown("### 🎯 SELECT INTERVIEW TO PREP")
        
        interview_options = [f"{u['company']} — {u['role']}" for u in upcoming]
        selected_interview = st.selectbox("Select upcoming interview:", interview_options, key="prep_interview_select")
        
        # Get selected interview details
        selected_idx = interview_options.index(selected_interview) if selected_interview in interview_options else 0
        current_interview = upcoming[selected_idx]
        company = current_interview['company']
        role = current_interview['role']
        stage = current_interview.get('stage', 'Interview')
        
        # Interview Header Card
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(255,215,0,0.15), rgba(255,191,0,0.05));
                    border: 2px solid #FFD700; border-radius: 16px; padding: 24px; margin: 16px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <p style="color: #8892b0; margin: 0; font-size: 0.85rem;">PREPARING FOR</p>
                    <h2 style="color: #FFD700; margin: 8px 0;">{company}</h2>
                    <p style="color: #ccd6f6; margin: 0;">{role}</p>
                </div>
                <div style="text-align: right;">
                    <p style="color: #8892b0; margin: 0; font-size: 0.85rem;">STAGE</p>
                    <h3 style="color: #00ff88; margin: 8px 0;">{stage}</h3>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ═══════════════════════════════════════════════════════════════
        # PREP TABS
        # ═══════════════════════════════════════════════════════════════
        prep_tabs = st.tabs(["📋 CHECKLIST", "🔍 INTEL", "🎮 COMBAT", "🧠 MINDSET", "❓ KILL Qs", "📅 DAY-OF"])
        
        # ─────────────────────────────────────────────────────────────
        # TAB 1: PRE-INTERVIEW CHECKLIST
        # ─────────────────────────────────────────────────────────────
        with prep_tabs[0]:
            st.markdown("### 📋 PRE-INTERVIEW CHECKLIST")
            st.caption("Complete each item before your interview. Track your progress.")
            
            # Initialize checklist state
            if 'prep_checklist' not in st.session_state:
                st.session_state['prep_checklist'] = {}
            
            checklist_items = [
                ("research", "🔍 Research company (news, funding, culture)", "Research"),
                ("linkedin", "🔗 Review interviewer's LinkedIn", "LinkedIn"),
                ("questions", "❓ Prepare 3 questions to ask them", "Questions"),
                ("pitch", "🎤 Practice 'Tell me about yourself' out loud", "Pitch"),
                ("stories", "📖 Prep 3 STAR stories for behavioral Qs", "Stories"),
                ("metrics", "📊 Memorize your key metrics (160% growth, etc)", "Metrics"),
                ("objections", "🛡️ Review likely objections + responses", "Objections"),
                ("tech", "💻 Test camera, mic, and internet connection", "Tech"),
                ("outfit", "👔 Outfit selected and ready", "Outfit"),
                ("calm", "🧘 5-minute breathing/meditation done", "Calm")
            ]
            
            completed = 0
            total = len(checklist_items)
            
            for key, label, short in checklist_items:
                checked = st.checkbox(label, key=f"prep_{key}", value=st.session_state['prep_checklist'].get(key, False))
                st.session_state['prep_checklist'][key] = checked
                if checked:
                    completed += 1
            
            # Progress bar
            progress_pct = completed / total
            progress_color = "#00ff88" if progress_pct >= 0.8 else "#FFD700" if progress_pct >= 0.5 else "#ff6b6b"
            
            st.markdown(f"""
            <div style="margin-top: 20px;">
                <p style="color: #8892b0; margin-bottom: 8px;">PREP PROGRESS: {completed}/{total} ({int(progress_pct * 100)}%)</p>
                <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 20px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, {progress_color}80, {progress_color}); width: {progress_pct * 100}%; height: 100%; border-radius: 10px; transition: width 0.3s;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if progress_pct >= 1.0:
                st.balloons()
                st.success("🎉 You're fully prepared! Go crush it!")
        
        # ─────────────────────────────────────────────────────────────
        # TAB 2: COMPANY QUICK INTEL
        # ─────────────────────────────────────────────────────────────
        with prep_tabs[1]:
            st.markdown(f"### 🔍 INTEL: {company}")
            st.caption("Live news and insights about your target company.")
            
            # Quick Links
            import urllib.parse
            encoded_company = urllib.parse.quote(company)
            
            link_cols = st.columns(4)
            link_cols[0].markdown(f"[🔍 Google](https://www.google.com/search?q={encoded_company}+news)")
            link_cols[1].markdown(f"[💼 LinkedIn](https://www.linkedin.com/company/{encoded_company.lower().replace(' ', '-')})")
            link_cols[2].markdown(f"[📰 Crunchbase](https://www.crunchbase.com/organization/{encoded_company.lower().replace(' ', '-')})")
            link_cols[3].markdown(f"[🐦 Twitter](https://twitter.com/search?q={encoded_company})")
            
            st.markdown("---")
            
            # Live News
            st.markdown("#### 📰 RECENT NEWS")
            
            import feedparser
            
            with st.spinner(f"Fetching intel for {company}..."):
                rss_url = f"https://news.google.com/rss/search?q={encoded_company}&hl=en-US&gl=US&ceid=US:en"
                feed = feedparser.parse(rss_url)
                
                if feed.entries:
                    for entry in feed.entries[:5]:
                        st.markdown(f"""
                        <div style="background: rgba(255,191,0,0.05); border-left: 3px solid #FFD700; padding: 12px; margin: 8px 0;">
                            <a href="{entry.link}" target="_blank" style="color: #ccd6f6; text-decoration: none; font-weight: 500;">
                                {entry.title}
                            </a>
                            <p style="color: #8892b0; font-size: 0.75rem; margin: 4px 0 0 0;">{entry.get('published', '')[:25]}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No recent news found. Try checking LinkedIn or Crunchbase.")
            
            # AI Company Brief
            st.markdown("---")
            st.markdown("#### 🤖 AI COMPANY BRIEF")
            
            if st.button("🧠 GENERATE INTEL BRIEF", use_container_width=True, key="prep_intel_btn"):
                with st.spinner("Analyzing company..."):
                    from logic.generator import generate_plain_text
                    
                    intel_prompt = f"""
                    Generate a concise company intelligence brief for {company}.
                    
                    Include:
                    1. **What they do** (1-2 sentences)
                    2. **Recent developments** (funding, growth, news)
                    3. **Company culture** (based on public perception)
                    4. **Key talking points** for the interview (3 bullets)
                    5. **Questions to ask them** (2 smart questions)
                    
                    Be specific and actionable. This is for interview prep.
                    """
                    
                    model_id = st.session_state.get('selected_model_id', "llama-3.3-70b-versatile")
                    brief = generate_plain_text(intel_prompt, model_name=model_id)
                    
                    st.markdown(brief)
        
        # ─────────────────────────────────────────────────────────────
        # TAB 3: COMBAT SIMULATOR (Duolingo-Style Practice)
        # ─────────────────────────────────────────────────────────────
        with prep_tabs[2]:
            from logic.database import (
                save_combat_session, get_combat_sessions, get_combat_analytics,
                get_persona_stats, get_streak_info, save_to_question_bank,
                update_question_performance
            )
            from logic.whisper_transcriber import get_transcriber, analyze_speech
            
            st.markdown(f"### 🎮 INTERVIEW COMBAT SIMULATOR")
            st.caption(f"Deep practice for {role} @ {company}. Train like it's real.")
            
            # ═══════════════════════════════════════════════════════════════
            # XP & STREAK DASHBOARD (Duolingo Style)
            # ═══════════════════════════════════════════════════════════════
            streak_info = get_streak_info()
            
            xp_cols = st.columns(4)
            with xp_cols[0]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(255,107,107,0.15), transparent);
                            border: 2px solid #ff6b6b; border-radius: 12px; padding: 16px; text-align: center;">
                    <p style="color: #8892b0; margin: 0; font-size: 0.75rem;">🔥 STREAK</p>
                    <h2 style="color: #ff6b6b; margin: 8px 0;">{streak_info['streak']} days</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with xp_cols[1]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(0,212,255,0.15), transparent);
                            border: 2px solid #00d4ff; border-radius: 12px; padding: 16px; text-align: center;">
                    <p style="color: #8892b0; margin: 0; font-size: 0.75rem;">⚡ LEVEL</p>
                    <h2 style="color: #00d4ff; margin: 8px 0;">{streak_info['level']}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with xp_cols[2]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(255,215,0,0.15), transparent);
                            border: 2px solid #FFD700; border-radius: 12px; padding: 16px; text-align: center;">
                    <p style="color: #8892b0; margin: 0; font-size: 0.75rem;">✨ TOTAL XP</p>
                    <h2 style="color: #FFD700; margin: 8px 0;">{streak_info['total_xp']}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with xp_cols[3]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(0,255,136,0.15), transparent);
                            border: 2px solid #00ff88; border-radius: 12px; padding: 16px; text-align: center;">
                    <p style="color: #8892b0; margin: 0; font-size: 0.75rem;">📊 TODAY</p>
                    <h2 style="color: #00ff88; margin: 8px 0;">{streak_info['today_sessions']} rounds</h2>
                </div>
                """, unsafe_allow_html=True)
            
            # XP Progress Bar
            st.markdown(f"""
            <div style="margin: 16px 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="color: #8892b0; font-size: 0.8rem;">Level {streak_info['level']}</span>
                    <span style="color: #FFD700; font-size: 0.8rem;">{streak_info['xp_in_level']}/100 XP</span>
                </div>
                <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 8px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #FFD700, #ff6b6b); width: {streak_info['xp_in_level']}%; height: 100%; border-radius: 10px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # ═══════════════════════════════════════════════════════════════
            # INTERVIEWER PERSONA SELECTOR
            # ═══════════════════════════════════════════════════════════════
            st.markdown("### 👥 SELECT YOUR OPPONENT")
            st.caption("Each interviewer type asks different questions. Master them all.")
            
            # Interviewer Personas with question banks
            INTERVIEWER_PERSONAS = {
                "🎯 Recruiter": {
                    "description": "Initial screen. Testing fit, communication, salary expectations.",
                    "style": "Friendly but probing. Looking for red flags.",
                    "color": "#00d4ff",
                    "questions": {
                        "Opener": [
                            "Tell me about yourself.",
                            "Walk me through your background.",
                            "Why are you looking to leave your current role?",
                            "What attracted you to this position?"
                        ],
                        "Logistics": [
                            "What are your salary expectations?",
                            "When can you start?",
                            "Are you interviewing elsewhere?",
                            "What's your ideal work environment?"
                        ],
                        "Fit Check": [
                            "Why do you want to work here?",
                            "What do you know about our company?",
                            "Where do you see yourself in 5 years?",
                            "What's your biggest weakness?"
                        ]
                    }
                },
                "👔 Hiring Manager": {
                    "description": "Deep dive. Testing skills, experience, and team fit.",
                    "style": "Direct and tactical. Wants specifics and proof.",
                    "color": "#FFD700",
                    "questions": {
                        "Experience Deep Dive": [
                            "Walk me through your biggest deal/project.",
                            "How did you achieve [your key metric]?",
                            "Tell me about a time you exceeded expectations.",
                            "What's your typical approach to [core skill]?"
                        ],
                        "Situational": [
                            "How would you handle [specific scenario]?",
                            "What would your first 30 days look like?",
                            "How do you prioritize competing demands?",
                            "Describe a time you disagreed with leadership."
                        ],
                        "Team Dynamics": [
                            "How do you work with cross-functional teams?",
                            "Tell me about a conflict with a colleague.",
                            "How do you handle feedback?",
                            "What's your management style (if applicable)?"
                        ]
                    }
                },
                "🏢 Staffing Recruiter": {
                    "description": "Agency recruiter. Quick screen, selling you to client.",
                    "style": "Fast-paced. Wants highlights and flexibility.",
                    "color": "#9b59b6",
                    "questions": {
                        "Quick Screen": [
                            "Give me your 60-second pitch.",
                            "What's your must-have in the next role?",
                            "What's your non-negotiable compensation?",
                            "How flexible is your timeline?"
                        ],
                        "Client Fit": [
                            "Why would you be perfect for this client?",
                            "What industries have you worked in?",
                            "Are you open to contract-to-hire?",
                            "What size company do you prefer?"
                        ],
                        "Red Flag Check": [
                            "Why did you leave your last role?",
                            "Any gaps in your resume to explain?",
                            "What would a reference say about you?",
                            "What's your ideal company culture?"
                        ]
                    }
                },
                "👑 CEO / Founder": {
                    "description": "Vision alignment. Testing culture fit and drive.",
                    "style": "Big picture. Wants passion and long-term thinking.",
                    "color": "#ff6b6b",
                    "questions": {
                        "Vision & Mission": [
                            "What excites you about our mission?",
                            "Where do you see this industry in 5 years?",
                            "What would you do if you had unlimited resources?",
                            "How do you stay current in your field?"
                        ],
                        "Character": [
                            "Tell me about your biggest failure.",
                            "What drives you professionally?",
                            "How do you handle ambiguity?",
                            "What would you change about your career if you could?"
                        ],
                        "Impact": [
                            "What's the biggest impact you've had in a role?",
                            "How would you make an impact in year one here?",
                            "What's a risk you took that paid off?",
                            "Why should I bet on you?"
                        ]
                    }
                },
                "🤝 Team Member / Peer": {
                    "description": "Culture and collaboration check. Testing day-to-day fit.",
                    "style": "Casual but observant. Assessing if you're easy to work with.",
                    "color": "#00ff88",
                    "questions": {
                        "Collaboration": [
                            "How do you like to communicate with teammates?",
                            "Tell me about a time you helped a colleague succeed.",
                            "How do you handle disagreements on a team?",
                            "What does good teamwork look like to you?"
                        ],
                        "Work Style": [
                            "How do you organize your day?",
                            "What tools do you love using?",
                            "How do you handle stress or tight deadlines?",
                            "What would your current team say about you?"
                        ],
                        "Culture Vibe": [
                            "What do you do outside of work?",
                            "What kind of manager brings out your best?",
                            "What's your ideal team dynamic?",
                            "What makes a job fun for you?"
                        ]
                    }
                },
                "📊 VP / Director": {
                    "description": "Strategic evaluation. Testing leadership and scalability.",
                    "style": "Results-focused. Wants metrics and strategic thinking.",
                    "color": "#e67e22",
                    "questions": {
                        "Strategic Thinking": [
                            "How would you build/scale [function] here?",
                            "What's your framework for [key decision]?",
                            "How do you balance short-term wins vs. long-term goals?",
                            "Tell me about a strategy you developed and executed."
                        ],
                        "Leadership": [
                            "How do you develop your team members?",
                            "Tell me about a difficult personnel decision.",
                            "How do you handle underperformers?",
                            "What's your philosophy on accountability?"
                        ],
                        "Metrics & Results": [
                            "What metrics do you obsess over?",
                            f"How did you drive {company}'s key objectives?",
                            "Tell me about a time you missed a goal. What happened?",
                            "How do you report to executives?"
                        ]
                    }
                }
            }
            
            # Persona selector with mastery indicators
            persona_stats = get_persona_stats()
            persona_mastery = {p['persona_type']: p for p in persona_stats}
            
            persona_cols = st.columns(3)
            for i, (persona_name, persona_data) in enumerate(INTERVIEWER_PERSONAS.items()):
                col_idx = i % 3
                with persona_cols[col_idx]:
                    mastery = persona_mastery.get(persona_name, {}).get('mastery_level', 0)
                    avg_score = persona_mastery.get(persona_name, {}).get('avg_score', 0)
                    sessions = persona_mastery.get(persona_name, {}).get('total_sessions', 0)
                    
                    # Mastery stars
                    stars = "⭐" * min(5, mastery) + "☆" * max(0, 5 - mastery)
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {persona_data['color']}15, transparent);
                                border: 1px solid {persona_data['color']}50; border-radius: 12px; padding: 12px; margin: 4px 0;
                                text-align: center; cursor: pointer; transition: all 0.3s;"
                         onmouseover="this.style.borderColor='{persona_data['color']}'; this.style.transform='translateY(-2px)';"
                         onmouseout="this.style.borderColor='{persona_data['color']}50'; this.style.transform='translateY(0)';">
                        <p style="color: {persona_data['color']}; margin: 0; font-size: 1.1rem; font-weight: bold;">{persona_name}</p>
                        <p style="color: #8892b0; margin: 4px 0; font-size: 0.7rem;">{persona_data['description'][:50]}...</p>
                        <p style="color: #FFD700; margin: 0; font-size: 0.8rem;">{stars}</p>
                        <p style="color: #8892b0; margin: 0; font-size: 0.65rem;">{sessions} sessions | Avg: {int(avg_score)}%</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("")
            selected_persona = st.selectbox(
                "Choose your interviewer:",
                list(INTERVIEWER_PERSONAS.keys()),
                key="combat_persona_select"
            )
            
            persona = INTERVIEWER_PERSONAS[selected_persona]
            
            # Show persona details
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {persona['color']}20, transparent);
                        border-left: 4px solid {persona['color']}; padding: 16px; margin: 8px 0;">
                <h4 style="color: {persona['color']}; margin: 0;">{selected_persona}</h4>
                <p style="color: #ccd6f6; margin: 8px 0;">{persona['description']}</p>
                <p style="color: #8892b0; font-size: 0.85rem; margin: 0;"><b>Style:</b> {persona['style']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # ═══════════════════════════════════════════════════════════════
            # QUESTION CATEGORY & SELECTION
            # ═══════════════════════════════════════════════════════════════
            st.markdown("### 🎯 SELECT BATTLE ROUND")
            
            # Difficulty selector
            difficulty_cols = st.columns(3)
            with difficulty_cols[0]:
                if st.button("🟢 EASY", use_container_width=True, key="diff_easy"):
                    st.session_state['combat_difficulty'] = "Easy"
            with difficulty_cols[1]:
                if st.button("🟡 MEDIUM", use_container_width=True, key="diff_medium"):
                    st.session_state['combat_difficulty'] = "Medium"
            with difficulty_cols[2]:
                if st.button("🔴 HARD", use_container_width=True, key="diff_hard"):
                    st.session_state['combat_difficulty'] = "Hard"
            
            current_difficulty = st.session_state.get('combat_difficulty', 'Medium')
            st.caption(f"Current difficulty: **{current_difficulty}**")
            
            # Category selector
            question_categories = list(persona['questions'].keys())
            selected_category = st.selectbox("Question Category:", question_categories, key="combat_category")
            
            # Question selector
            questions = persona['questions'][selected_category]
            
            # Add dynamic company-specific questions
            dynamic_questions = [
                f"Why do you want to work at {company}?",
                f"What do you know about {company}'s recent news?",
                f"How would you help {company} achieve its goals?",
            ]
            all_questions = questions + dynamic_questions
            
            selected_question = st.selectbox("Select question:", all_questions, key="combat_question")
            
            # Or random question
            if st.button("🎲 RANDOM QUESTION", use_container_width=True, key="random_q"):
                import random
                all_persona_questions = []
                for cat, qs in persona['questions'].items():
                    all_persona_questions.extend(qs)
                selected_question = random.choice(all_persona_questions)
                st.session_state['combat_question'] = selected_question
            
            # Display the question prominently
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {persona['color']}25, rgba(0,0,0,0.3));
                        border: 3px solid {persona['color']}; border-radius: 16px; padding: 32px; margin: 20px 0; text-align: center;">
                <p style="color: #8892b0; margin: 0 0 8px 0; font-size: 0.9rem;">{selected_persona} ASKS:</p>
                <h2 style="color: {persona['color']}; margin: 0; font-size: 1.5rem; line-height: 1.4;">"{selected_question}"</h2>
                <p style="color: #8892b0; margin: 16px 0 0 0; font-size: 0.8rem;">🎯 Role: {role} @ {company} | ⚡ Difficulty: {current_difficulty}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Save question to bank for tracking
            save_to_question_bank(selected_question, selected_category, selected_persona, current_difficulty)
            
            st.markdown("---")
            
            # ═══════════════════════════════════════════════════════════════
            # COMBAT RECORDING & SCORING
            # ═══════════════════════════════════════════════════════════════
            st.markdown("### 🎙️ RECORD YOUR ANSWER")
            st.caption("Hit record, answer as if it's real, then get AI scoring.")
            
            # Timer display
            st.markdown("""
            <div style="text-align: center; margin: 16px 0;">
                <p style="color: #8892b0; margin: 0;">⏱️ Aim for 60-90 seconds (varies by question)</p>
            </div>
            """, unsafe_allow_html=True)
            
            audio = st.audio_input("Click to start recording", key="combat_audio")
            
            if audio:
                st.audio(audio)
                
                # Transcription option
                transcribe_option = st.checkbox("🔤 Transcribe my answer (uses Groq Whisper)", value=True, key="combat_transcribe")
                
                col_analyze, col_tips = st.columns([1, 1])
                
                with col_analyze:
                    if st.button("🧠 SCORE MY RESPONSE", type="primary", use_container_width=True, key="combat_score_btn"):
                        with st.spinner("Analyzing your response..."):
                            transcript = ""
                            speech_analysis = {}
                            
                            # Transcribe if option selected and API key available
                            if transcribe_option and st.session_state.get('groq_api_key'):
                                try:
                                    transcriber = get_transcriber(st.session_state.get('groq_api_key'))
                                    if transcriber.is_available():
                                        result = transcriber.transcribe(audio)
                                        transcript = result.get('text', '')
                                        if transcript:
                                            speech_analysis = analyze_speech(transcript)
                                            st.success("✅ Transcription complete!")
                                except Exception as e:
                                    st.warning(f"Transcription unavailable: {e}")
                            
                            # Generate AI feedback
                            from logic.generator import generate_plain_text
                            
                            context_prompt = f"""
                            You are a senior interview coach scoring a candidate's response.
                            
                            CONTEXT:
                            - Interviewer Type: {selected_persona}
                            - Question: "{selected_question}"
                            - Role: {role}
                            - Company: {company}
                            - Difficulty: {current_difficulty}
                            {"- Transcript: " + transcript if transcript else "- (No transcript available - provide general coaching)"}
                            
                            PROVIDE:
                            1. **SCORE: X/100** (be honest but fair)
                            2. **STRENGTHS** (2-3 bullets of what worked)
                            3. **IMPROVEMENTS** (2-3 specific, actionable fixes)
                            4. **EXAMPLE ANSWER** (Show a strong 60-second response)
                            5. **PRO TIP** (One tactical insight for this interviewer type)
                            
                            Be specific to the interviewer type's perspective.
                            """
                            
                            model_id = st.session_state.get('selected_model_id', "llama-3.3-70b-versatile")
                            feedback = generate_plain_text(context_prompt, model_name=model_id)
                            
                            # Extract score from feedback (simple parse)
                            import re
                            score_match = re.search(r'SCORE[:\s]*(\d+)', feedback, re.IGNORECASE)
                            score = int(score_match.group(1)) if score_match else 70
                            
                            # Save session to database
                            session_id = save_combat_session(
                                company=company,
                                role=role,
                                interviewer_type=selected_persona,
                                question=selected_question,
                                category=selected_category,
                                difficulty=current_difficulty,
                                transcript=transcript,
                                score=score,
                                feedback=feedback,
                                word_count=speech_analysis.get('word_count', 0),
                                filler_count=speech_analysis.get('filler_count', 0),
                                has_metrics=speech_analysis.get('has_metric', False)
                            )
                            
                            # Update question performance
                            update_question_performance(selected_question, score, transcript if score > 80 else None)
                            
                            # Display score with visual
                            score_color = "#00ff88" if score >= 80 else "#FFD700" if score >= 60 else "#ff6b6b"
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, {score_color}20, transparent);
                                        border: 3px solid {score_color}; border-radius: 16px; padding: 24px; margin: 16px 0; text-align: center;">
                                <p style="color: #8892b0; margin: 0;">YOUR SCORE</p>
                                <h1 style="color: {score_color}; margin: 8px 0; font-size: 4rem;">{score}</h1>
                                <p style="color: #ccd6f6; margin: 0;">
                                    {"🔥 EXCELLENT! You're ready!" if score >= 80 else "👍 Good, but room to improve." if score >= 60 else "💪 Keep practicing!"}
                                </p>
                                <p style="color: #8892b0; margin: 8px 0 0 0; font-size: 0.8rem;">+{10 + score // 10} XP Earned</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Show transcript if available
                            if transcript:
                                with st.expander("📝 YOUR TRANSCRIPT"):
                                    st.write(transcript)
                                    st.caption(f"Words: {speech_analysis.get('word_count', 0)} | Fillers: {speech_analysis.get('filler_count', 0)} | Metrics: {'Yes ✅' if speech_analysis.get('has_metric') else 'No ❌'}")
                            
                            # Show detailed feedback
                            st.markdown("### 📋 DETAILED FEEDBACK")
                            st.markdown(feedback)
                            
                            # XP animation
                            st.balloons() if score >= 80 else None
                
                with col_tips:
                    if st.button("💡 SHOW TIPS FIRST", use_container_width=True, key="combat_tips_btn"):
                        with st.spinner("Loading tips..."):
                            from logic.generator import generate_plain_text
                            
                            tips_prompt = f"""
                            Give quick tips for answering this interview question:
                            
                            Interviewer: {selected_persona}
                            Question: "{selected_question}"
                            Role: {role}
                            
                            Provide:
                            1. **Key Points to Hit** (3 bullets)
                            2. **Strong Opening Line** (one example)
                            3. **Strong Closing Line** (one example)
                            4. **Time Target** (how long to speak)
                            
                            Be concise and tactical.
                            """
                            
                            model_id = st.session_state.get('selected_model_id', "llama-3.3-70b-versatile")
                            tips = generate_plain_text(tips_prompt, model_name=model_id)
                            st.markdown(tips)
            
            st.markdown("---")
            
            # ═══════════════════════════════════════════════════════════════
            # PRACTICE HISTORY & ANALYTICS
            # ═══════════════════════════════════════════════════════════════
            st.markdown("### 📊 YOUR COMBAT HISTORY")
            
            history_tabs = st.tabs(["📈 Recent Sessions", "👥 Persona Stats", "❓ Question Bank"])
            
            with history_tabs[0]:
                sessions = get_combat_sessions(limit=10, company=company)
                if sessions:
                    for session in sessions:
                        s_color = "#00ff88" if session['score'] >= 80 else "#FFD700" if session['score'] >= 60 else "#ff6b6b"
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.02); border-left: 3px solid {s_color}; padding: 12px; margin: 8px 0;">
                            <div style="display: flex; justify-content: space-between;">
                                <div>
                                    <p style="color: #ccd6f6; margin: 0; font-size: 0.9rem;">{session['interviewer_type']}: "{session['question'][:60]}..."</p>
                                    <p style="color: #8892b0; margin: 4px 0 0 0; font-size: 0.75rem;">{session['created_at'][:16]}</p>
                                </div>
                                <p style="color: {s_color}; font-weight: bold; font-size: 1.2rem; margin: 0;">{session['score']}%</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No practice sessions yet for this company. Start practicing!")
            
            with history_tabs[1]:
                persona_stats = get_persona_stats()
                if persona_stats:
                    for ps in persona_stats:
                        p_color = INTERVIEWER_PERSONAS.get(ps['persona_type'], {}).get('color', '#FFD700')
                        stars = "⭐" * min(5, ps['mastery_level']) + "☆" * max(0, 5 - ps['mastery_level'])
                        st.markdown(f"""
                        <div style="background: linear-gradient(90deg, {p_color}10, transparent); padding: 12px; margin: 8px 0; border-radius: 8px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <p style="color: {p_color}; margin: 0; font-weight: bold;">{ps['persona_type']}</p>
                                    <p style="color: #8892b0; margin: 0; font-size: 0.8rem;">{ps['total_sessions']} sessions | Best: {ps['best_score']}%</p>
                                </div>
                                <div style="text-align: right;">
                                    <p style="color: #FFD700; margin: 0;">{stars}</p>
                                    <p style="color: #ccd6f6; margin: 0; font-size: 1.1rem;">Avg: {int(ps['avg_score'])}%</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No persona stats yet. Start practicing with different interviewers!")
            
            with history_tabs[2]:
                st.caption("Questions you've practiced, sorted by those needing most work.")
                from logic.database import get_question_bank
                q_bank = get_question_bank()
                if q_bank:
                    for q in q_bank[:10]:
                        q_color = "#00ff88" if q['avg_score'] >= 80 else "#FFD700" if q['avg_score'] >= 60 else "#ff6b6b"
                        st.markdown(f"""
                        <div style="padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <p style="color: #ccd6f6; margin: 0;">{q['question'][:70]}...</p>
                            <p style="color: #8892b0; margin: 4px 0 0 0; font-size: 0.75rem;">
                                Practiced: {q['times_practiced']}x | Avg: <span style="color: {q_color};">{int(q['avg_score'])}%</span> | {q['category']}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Practice some questions to build your bank!")
        
        
        # ─────────────────────────────────────────────────────────────
        # TAB 4: MINDSET CALIBRATION
        # ─────────────────────────────────────────────────────────────
        with prep_tabs[3]:
            st.markdown("### 🧠 MINDSET CALIBRATION")
            st.caption("Align your energy before the call. Set your intention.")
            
            # Daily Archetype
            import random
            
            archetypes = [
                {"symbol": "☉", "name": "THE SAGE", "essence": "Intuitive Wisdom", "calibration": "I access wisdom beyond logic. Insight arrives when I stop forcing.", "energy": "Lightning flash of clarity"},
                {"symbol": "∞", "name": "THE GIVER", "essence": "Expansive Generosity", "calibration": "I expand by giving. The more value I offer, the more returns.", "energy": "Overflowing outward"},
                {"symbol": "⬡", "name": "THE HARMONIZER", "essence": "Dynamic Balance", "calibration": "I am the bridge between worlds. My presence creates resonance.", "energy": "Heart of the system"},
                {"symbol": "↑", "name": "THE VICTOR", "essence": "Eternal Persistence", "calibration": "I persist with joy, not desperation. Momentum compounds.", "energy": "Upward thrust"},
                {"symbol": "✧", "name": "THE BEACON", "essence": "Authentic Radiance", "calibration": "My authentic presence is magnetic. Worth needs no convincing.", "energy": "Radiant stillness"}
            ]
            
            daily = random.choice(archetypes)
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(155,89,182,0.15), transparent);
                        border: 2px solid #9b59b6; border-radius: 16px; padding: 32px; text-align: center;">
                <p style="color: #8892b0; margin: 0; font-size: 0.9rem;">TODAY'S ARCHETYPE</p>
                <h1 style="color: #9b59b6; margin: 16px 0; font-size: 4rem;">{daily['symbol']}</h1>
                <h2 style="color: #9b59b6; margin: 0 0 8px 0;">{daily['name']}</h2>
                <p style="color: #ccd6f6; font-size: 0.95rem; margin: 0 0 16px 0;">{daily['essence']} — <i>{daily['energy']}</i></p>
                <p style="color: #ccd6f6; font-size: 1.2rem; font-style: italic; margin: 0;">"{daily['calibration']}"</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Power Affirmations
            st.markdown("#### 💪 POWER AFFIRMATIONS")
            st.caption("Say these out loud before your call:")
            
            affirmations = [
                "I am the solution to their problem.",
                "My experience speaks for itself.",
                "I bring clarity and energy to every conversation.",
                "I am interviewing them as much as they're interviewing me.",
                "I am ready. I am prepared. I am enough."
            ]
            
            for aff in affirmations:
                st.markdown(f"""
                <div style="background: rgba(0,255,136,0.05); border-left: 3px solid #00ff88; padding: 12px; margin: 8px 0;">
                    <p style="color: #00ff88; margin: 0; font-size: 1.1rem;">"{aff}"</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Breathing Exercise
            st.markdown("---")
            st.markdown("#### 🧘 2-MINUTE BREATHING")
            
            if st.button("▶️ START BREATHING EXERCISE", use_container_width=True, key="prep_breathe"):
                with st.spinner("Breathe in... hold... breathe out..."):
                    import time
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(1.2)  # ~2 min total
                        progress_bar.progress(i + 1)
                        if i % 10 == 0:
                            st.toast("Breathe deeply... 🧘")
                    st.success("✅ You're centered. Go crush it!")
        
        # ─────────────────────────────────────────────────────────────
        # TAB 5: KILL QUESTIONS
        # ─────────────────────────────────────────────────────────────
        with prep_tabs[4]:
            st.markdown(f"### ❓ KILL QUESTIONS: {role} @ {company}")
            st.caption("The hardest questions they'll ask. Prepare your answers.")
            
            # Generate Kill Questions
            if st.button("🧠 GENERATE KILL QUESTIONS", type="primary", use_container_width=True, key="prep_kill_btn"):
                with st.spinner("Generating role-specific questions..."):
                    from logic.generator import generate_plain_text
                    
                    kill_prompt = f"""
                    You're a senior hiring manager at {company} interviewing for {role}.
                    
                    Generate 5 TOUGH interview questions that would make an average candidate stumble.
                    For each question, provide:
                    
                    1. **The Question**
                    2. **Why they ask it** (1 sentence)
                    3. **How to answer it** (2-3 sentences with specific approach)
                    
                    Focus on questions specific to this role and company.
                    Make them challenging but fair.
                    """
                    
                    model_id = st.session_state.get('selected_model_id', "llama-3.3-70b-versatile")
                    kill_questions = generate_plain_text(kill_prompt, model_name=model_id)
                    
                    st.session_state['kill_questions'] = kill_questions
            
            # Display generated questions
            if 'kill_questions' in st.session_state:
                st.markdown(st.session_state['kill_questions'])
            else:
                st.info("Click the button above to generate role-specific kill questions.")
        
        # ─────────────────────────────────────────────────────────────
        # TAB 6: DAY-OF CHECKLIST
        # ─────────────────────────────────────────────────────────────
        with prep_tabs[5]:
            st.markdown("### 📅 DAY-OF CHECKLIST")
            st.caption("The morning of your interview. Don't miss anything.")
            
            day_of_items = [
                ("🕐 Wake up early — no rushing", "wake"),
                ("🏋️ Light exercise or stretch (15 min)", "exercise"),
                ("🍳 Eat a balanced breakfast", "eat"),
                ("☕ Coffee/tea ready (not too much)", "coffee"),
                ("💻 Computer charged, cables connected", "tech1"),
                ("📸 Camera at eye level, good lighting", "camera"),
                ("🎧 Headphones tested, mic working", "audio"),
                ("🌐 Internet speed test completed", "internet"),
                ("📱 Phone on silent, notifications off", "phone"),
                ("🚪 Do Not Disturb sign on door", "dnd"),
                ("📋 Notes + questions printed/visible", "notes"),
                ("🥤 Water glass nearby", "water"),
                ("🧘 5-minute breathing before call", "breathe"),
                ("😊 Smile before they answer", "smile")
            ]
            
            st.markdown("#### ⏰ MORNING ROUTINE")
            for label, key in day_of_items[:6]:
                st.checkbox(label, key=f"dayof_{key}")
            
            st.markdown("#### 💻 TECH CHECK (30 min before)")
            for label, key in day_of_items[6:10]:
                st.checkbox(label, key=f"dayof_{key}")
            
            st.markdown("#### 🎯 FINAL PREP (5 min before)")
            for label, key in day_of_items[10:]:
                st.checkbox(label, key=f"dayof_{key}")
            
            # Final Countdown
            st.markdown("---")
            st.markdown("#### ⏱️ INTERVIEW COUNTDOWN")
            
            interview_time = st.time_input("Interview time:", key="prep_time")
            
            from datetime import datetime, timedelta
            now = datetime.now()
            interview_dt = now.replace(hour=interview_time.hour, minute=interview_time.minute, second=0)
            
            if interview_dt > now:
                time_diff = interview_dt - now
                hours, remainder = divmod(time_diff.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(255,107,107,0.15), transparent);
                            border: 2px solid #ff6b6b; border-radius: 12px; padding: 24px; text-align: center;">
                    <p style="color: #8892b0; margin: 0;">INTERVIEW STARTS IN</p>
                    <h1 style="color: #ff6b6b; margin: 8px 0; font-size: 3rem;">{hours}h {minutes}m</h1>
                    <p style="color: #ccd6f6; margin: 0;">You've got this! 💪</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("🎯 Your interview time has passed or is now. GO CRUSH IT!")
    
    # ─────────────────────────────────────────────────────────────
    # ==============================================================================
    # 📄 MODE 1: INTEL (THE OMNI-AGENT HUD)
    # ==============================================================================
    elif input_mode == "📄 Intel":
        st.markdown("## 🧬 STRATEGIC INTELLIGENCE HUD")
        
        # --- 1. THE CAREER VAULT (Teal-Inspired Storage) ---
        st.markdown("#### 1. THE CAREER VAULT (DATA LAKE)")
        
        # Initialize Session State for The Vault
        if 'resume_vault' not in st.session_state:
            st.session_state['resume_vault'] = {}
        
        col_vault, col_upload = st.columns([2, 1])
        
        with col_upload:
            # UPLOADER: Adds to the Vault, doesn't just replace
            uploaded_files = st.file_uploader("Ingest Career Assets (PDF/TXT)", type=['txt', 'pdf', 'md'], accept_multiple_files=True, label_visibility="collapsed")
            if uploaded_files:
                for f in uploaded_files:
                    try:
                        # Simple text extraction simulation (or use logic.ingest)
                        text = f.read().decode("utf-8", errors='ignore') 
                        st.session_state['resume_vault'][f.name] = text
                    except Exception:
                        st.session_state['resume_vault'][f.name] = "Content extracted..."
                st.success(f"✅ Ingested {len(uploaded_files)} Assets into Vault")

        with col_vault:
            # VISUALIZE THE VAULT
            if st.session_state['resume_vault']:
                st.info(f"📚 **ACTIVE KNOWLEDGE BASE:** {len(st.session_state['resume_vault'])} Files Loaded")
                # Select which assets to use for this specific scan
                active_assets = st.multiselect("Active Context for Omni-Agent", 
                                               options=st.session_state['resume_vault'].keys(),
                                               default=st.session_state['resume_vault'].keys(),
                                               help="Select which resumes the Agent should 'read' to find matches.")
            else:
                st.warning("⚠️ Vault Empty. Upload Resumes to build your Data Lake.")
                active_assets = []

        # ═══════════════════════════════════════════════════════════════
        # JOB BOARD AGGREGATOR (Pre-Loaded Jobs from Your Pipeline)
        # ═══════════════════════════════════════════════════════════════
        st.markdown("---")
        st.markdown("#### 2. JOB SEARCH (Pre-Loaded from Pipeline)")
        st.caption("Search for open roles at your target companies, or paste a JD manually.")
        
        # Pre-loaded target companies from CRM deals
        pipeline_companies = []
        if 'crm_deals' in st.session_state:
            pipeline_companies = list(set([d['Company'] for d in st.session_state['crm_deals']]))
        
        # Default high-value targets
        default_companies = ["Mistral AI", "Deel", "Verkada", "Ambient.ai", "DepthFirst", "Hightouch", "Nooks", "2501.ai"]
        all_companies = list(set(pipeline_companies + default_companies))
        
        job_search_mode = st.radio("Job Source:", ["🔍 Search by Company", "📋 Paste JD Manually"], horizontal=True, label_visibility="collapsed")
        
        if job_search_mode == "🔍 Search by Company":
            search_col1, search_col2 = st.columns([2, 1])
            
            with search_col1:
                selected_company = st.selectbox("Select Target Company:", all_companies, key="job_search_company")
            
            with search_col2:
                search_term = st.text_input("Role Keywords:", value="Account Executive", placeholder="e.g., AE, GTM, Sales")
            
            if st.button("🔍 SEARCH JOBS", type="primary", use_container_width=True):
                with st.spinner(f"Searching {selected_company} openings..."):
                    # Generate search URLs
                    company_q = selected_company.replace(' ', '+')
                    role_q = search_term.replace(' ', '+')
                    
                    st.markdown("##### 🔗 JOB BOARDS (Direct Links)")
                    
                    link_col1, link_col2, link_col3, link_col4 = st.columns(4)
                    
                    with link_col1:
                        linkedin_url = f"https://www.linkedin.com/jobs/search/?keywords={role_q}%20{company_q}"
                        st.markdown(f"[LinkedIn Jobs]({linkedin_url})")
                    
                    with link_col2:
                        greenhouse_url = f"https://www.google.com/search?q={company_q}+careers+{role_q}+site:greenhouse.io"
                        st.markdown(f"[Greenhouse]({greenhouse_url})")
                    
                    with link_col3:
                        lever_url = f"https://www.google.com/search?q={company_q}+careers+{role_q}+site:lever.co"
                        st.markdown(f"[Lever]({lever_url})")
                    
                    with link_col4:
                        ashby_url = f"https://www.google.com/search?q={company_q}+careers+{role_q}+site:ashbyhq.com"
                        st.markdown(f"[Ashby]({ashby_url})")
                    
                    st.markdown("---")
                    
                    # Search HackerNews for hiring posts
                    st.markdown("##### 📰 HACKERNEWS HIRING THREADS")
                    try:
                        import requests
                        hn_url = f"https://hn.algolia.com/api/v1/search?query={selected_company}+hiring&tags=story&hitsPerPage=5"
                        response = requests.get(hn_url, timeout=5)
                        if response.status_code == 200:
                            hits = response.json().get('hits', [])
                            if hits:
                                for hit in hits[:3]:
                                    title = hit.get('title', 'No title')
                                    url = hit.get('url') or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
                                    st.markdown(f"• [{title}]({url})")
                            else:
                                st.caption("*No recent hiring threads found.*")
                    except Exception:
                        st.caption("*Search temporarily unavailable.*")
                    
                    st.info(f"💡 **TIP:** Copy the JD from {selected_company}'s careers page and paste below.")
            
            st.markdown("---")
        
        # --- 3. BLACK OPS AGENT (OSINT) ---
        st.markdown("#### 3. BLACK OPS AGENT (INTEL & RECON)")
        
        osint_tab1, osint_tab2, osint_tab3 = st.tabs(["🕵️ CONTACT HUNTER", "⚡ SIGNAL RADAR", "🌐 360° RECON"])
        
        with osint_tab1:
            st.caption("PROTOCOL: Open Source Intelligence (OSINT) Link Generators.")
            o_col1, o_col2 = st.columns(2)
            o_name = o_col1.text_input("Target Name", placeholder="e.g. Leon Basin", key="osint_name")
            o_domain = o_col2.text_input("Company Domain", value=st.session_state.target_company, placeholder="e.g. anthropic.com", key="osint_domain")
            
            if st.button("🔓 GENERATE INTELLIGENCE LINKS", use_container_width=True):
                if o_name and o_domain:
                    # Clean inputs
                    o_name_esc = o_name.replace(' ', '+')
                    
                    st.markdown("##### 🎯 DIRECT CONTACT LINKS")
                    l1, l2, l3 = st.columns(3)
                    
                    with l1:
                        # Email Dork
                        email_query = f'"email" "{o_domain}" site:linkedin.com/in/ "{o_name}"'
                        st.markdown(f"[📧 Find Email (Google)](https://www.google.com/search?q={email_query})")
                        st.caption("Scans LinkedIn profiles for email")
                        
                    with l2:
                        # Phone Dork
                        phone_query = f'"{o_name}" "{o_domain}" (phone OR mobile OR cell) -site:linkedin.com'
                        st.markdown(f"[📞 Find Phone (Google)](https://www.google.com/search?q={phone_query})")
                        st.caption("Scans deep web for contacts")

                    with l3:
                        # Meet Dork
                        meet_query = f'site:calendly.com "{o_name}"'
                        st.markdown(f"[📅 Find Calendly](https://www.google.com/search?q={meet_query})")
                        st.caption("Checks for public booking links")
                    
                    st.markdown("---")
                    st.markdown("##### 👤 KEY DECISION MAKERS")
                    dm1, dm2, dm3, dm4 = st.columns(4)
                    dm1.markdown(f"[🎯 VP Sales](https://www.linkedin.com/search/results/people/?keywords={o_domain}%20VP%20Sales)")
                    dm2.markdown(f"[🎯 CRO](https://www.linkedin.com/search/results/people/?keywords={o_domain}%20CRO)")
                    dm3.markdown(f"[🎯 RevOps](https://www.linkedin.com/search/results/people/?keywords={o_domain}%20RevOps)")
                    dm4.markdown(f"[🎯 CTO/Eng](https://www.linkedin.com/search/results/people/?keywords={o_domain}%20CTO)")

        with osint_tab2:
            st.caption("PROTOCOL: Pattern Recognition for Opportunity Analysis.")
            
            s_company = st.text_input("Target Company / Sector", value=st.session_state.target_company, key="signal_company")
            
            if st.button("📡 SCAN FOR TRIGGERS", type="primary", use_container_width=True):
                if s_company:
                    from logic.generator import generate_plain_text
                    import feedparser
                    import urllib.parse
                    import requests
                    from types import SimpleNamespace
                    
                    with st.spinner(f"Intercepting Signals for {s_company}..."):
                        # 1. FETCH REAL-TIME INTEL (Google News RSS)
                        encoded_company = urllib.parse.quote(s_company)
                        rss_url = f"https://news.google.com/rss/search?q={encoded_company}+when:30d&hl=en-US&gl=US&ceid=US:en"
                        feed = feedparser.parse(rss_url)
                        
                        news_items = []
                        context_str = "Recent News Intercepts:\n"
                        
                        # Google News
                        if feed.entries:
                            for entry in feed.entries[:5]:
                                context_str += f"- [NEWS] {entry.title} ({entry.link})\n"
                                news_items.append(entry)
                        
                        # HackerNews (Enrichment)
                        try:
                            hn_url = f"https://hn.algolia.com/api/v1/search?query={encoded_company}&tags=story&hitsPerPage=3"
                            r = requests.get(hn_url, timeout=2)
                            if r.status_code == 200:
                                for h in r.json().get('hits', []):
                                    title = h.get('title')
                                    url = h.get('url') or f"https://news.ycombinator.com/item?id={h.get('objectID')}"
                                    context_str += f"- [HN] {title} ({url})\n"
                                    # Normalize for display
                                    news_items.append(SimpleNamespace(title=f"[HN] {title}", link=url))
                        except Exception:
                            pass  # HN search optional
                            
                        if not news_items:
                            context_str = "NO DIRECT NEWS FOUND. ANALYZE BASED ON GENERAL KNOWLEDGE."
                        
                        # 2. ANALYZE WITH AI
                        signal_prompt = f"""
                        ACT AS: Deep State Commercial Intelligence Analyst.
                        TARGET: {s_company}
                        
                        INTELLIGENCE FEED:
                        {context_str}
                        
                        MISSION: Identify 3 high-probability "Buying Triggers" for a Revenue/GTM Architecture deal based on this news or general market status.
                        
                        LOOK FOR:
                        1. Recent Funding (Speed needed)
                        2. Hiring Spree (Chaos in Ops)
                        3. New Market Expansion (Process needed)
                        4. Leadership Changes (New mandate)
                        5. Technical/Product Launches (Go-to-Market needs)
                        
                        OUTPUT FORMAT:
                        **1. [TRIGGER TYPE]**: [Specific News/Observation] -> [The Opening]
                        """
                        model_id = st.session_state.get('selected_model_id', "llama-3.3-70b-versatile")
                        signals = generate_plain_text(signal_prompt, model_name=model_id)
                        
                        st.markdown(signals)
                        
                        if news_items:
                            with st.expander("📰 SOURCE INTELLIGENCE"):
                                for item in news_items:
                                    st.markdown(f"- [{item.title}]({item.link})")
                                    
        with osint_tab3:
            st.caption("PROTOCOL: Full-Spectrum Corporate Analysis.")
            r_company = st.text_input("Deep Dive Target", value=st.session_state.target_company, placeholder="e.g. Stripe", key="osint_recon")
            if r_company:
                q = r_company.replace(' ', '+')
                d_c1, d_c2, d_c3 = st.columns(3)
                
                with d_c1:
                    st.markdown("#### 🗣️ CULTURE")
                    st.markdown(f"• [**Blind** (Insider/WLB)](https://www.google.com/search?q=site:teamblind.com+{q})")
                    st.markdown(f"• [**Reddit** (Real Talk)](https://www.google.com/search?q=site:reddit.com+{q}+work+culture)")
                    st.markdown(f"• [**Glassdoor** (Interviews)](https://www.google.com/search?q=site:glassdoor.com+{q}+interview+questions)")

                with d_c2:
                    st.markdown("#### 💰 TRIBE")
                    st.markdown(f"• [**Levels.fyi** (Salaries)](https://www.levels.fyi/companies/{r_company.lower().replace(' ', '-')}/salaries)")
                    st.markdown(f"• [**Crunchbase** (Funding)](https://www.crunchbase.com/organization/{r_company.lower().replace(' ', '-')})")
                    st.markdown(f"• [**Founder Search**](https://twitter.com/search?q={q}%20(hiring%20OR%20vision))")

                with d_c3:
                    st.markdown("#### 🛠️ STACK")
                    st.markdown(f"• [**GitHub** (Eng Stack)](https://github.com/search?q={q}&type=repositories)")
                    st.markdown(f"• [**StackShare** (Tech)](https://stackshare.io/{r_company.lower()})")
                    st.markdown(f"• [**RocketReach** (Contacts)](https://rocketreach.co/{r_company.lower().replace(' ', '-')}-profile)")

        st.markdown("---")
        
        # --- 4. TARGET VECTOR (Manual JD Input) ---
        st.markdown("#### 4. TARGET VECTOR (THE MISSION)")
        jd_text = st.text_area("Paste Job Description", height=150, placeholder="[PASTE JD HERE - or use the search above to find jobs]", label_visibility="collapsed")

        # --- 5. THE WAR ROOM (MULTI-AGENT CONFIG) ---
        st.markdown("---")
        st.markdown("#### 5. DEPLOY GTM SWARM (MULTI-AGENT)")
    
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.caption("🧠 GLOBAL STRATEGY SETTINGS")
            # Global settings that apply to ALL agents
            strategic_angle = st.selectbox("Strategic Angle", 
                ["Revenue Architect (Systems Focus)", "Partner Builder (Channel Focus)", "Operator (Efficiency Focus)", "Founder (Speed Focus)"])
            
            tone = st.selectbox("Tone Protocol", 
                ["Executive / Direct (No Fluff)", "Collaborative / Builder", "Challenger / Diagnostic"])
                
        with c2:
            st.caption("🤖 ACTIVATE AGENTS (SELECT OUTPUTS)")
            # This allows you to run multiple agents at once
            active_agents = st.multiselect("Deploy Specialized Agents:",
                [
                    "📧 The Sniper (Cold Email)",
                    "📱 The Closer (Phone/Voicemail Scripts)",
                    "🔗 The Networker (LinkedIn DM)",
                    "🛡️ The Devil's Advocate (Objection Handling)",
                    "🏗️ The Architect (30-60-90 Day Outline)"
                ],
                default=["📧 The Sniper (Cold Email)", "📱 The Closer (Phone/Voicemail Scripts)"]
            )

        # --- 3. EXECUTION (THE SWARM) ---
        st.markdown("---")
        
        if st.button("🚀 DEPLOY SWARM INTELLIGENCE", type="primary", use_container_width=True):
            if active_assets and jd_text:
                
                # TABS FOR OUTPUT (Clean Workspace)
                # Create tabs dynamically based on selected agents
                tabs = st.tabs([agent.split(" ")[1] + " OUTPUT" for agent in active_agents])
                
                for i, agent in enumerate(active_agents):
                    with tabs[i]:
                        with st.spinner(f"Agent {agent} is working..."):
                            
                            # ==========================================
                            # AGENT 1: THE SNIPER (EMAIL)
                            # ==========================================
                            if "Sniper" in agent:
                                st.subheader("📧 THE SNIPER PITCH")
                                st.info(f"Strategy: {strategic_angle} | Tone: {tone}")
                                
                                # Simulated LLM Output based on your "Sniper Arsenal"
                                st.markdown(f"""
                                **Subject:** Structuring the Partner Ecosystem (Fudo/Sense Experience)

                                **Hi [Hiring Manager],**

                                I've been tracking **[Company]**'s expansion. The velocity is incredible, but I know from experience that scaling at this speed creates **structural debt**.
                                
                                I specialize in fixing that debt.
                                
                                As **Director of GTM Systems** (Ex-Fudo/Sense), I re-architected revenue engines to drive **160% pipeline growth** and **$10M in new ARR**.
                                
                                I have a specific perspective on how we can activate your [Channel/Vertical] to lower CAC.
                                
                                Open to a brief chat?
                                
                                **Leon Basin**
                                Director of GTM Systems
                                """)
                                st.caption("💡 **Agent Note:** I used the 'Structural Debt' hook because it resonates with the 'Founder' persona.")

                            # ==========================================
                            # AGENT 2: THE CLOSER (PHONE)
                            # ==========================================
                            elif "Closer" in agent:
                                st.subheader("📱 COLD CALL & VOICEMAIL SCRIPTS")
                                
                                c_col1, c_col2 = st.columns(2)
                                with c_col1:
                                    st.markdown("**📞 LIVE CALL OPENER**")
                                    st.markdown(f"""
                                    "Hi [Name], this is Leon Basin.
                                    
                                    I'm not calling to sell you software. I'm calling because I've been tracking your expansion into **[Region/Vertical]**, and I noticed a gap in your partner activation layer.
                                    
                                    I built the fix for this at **Fudo Security** (160% growth). I have an idea for [Company]—do you have 30 seconds, or should I send it via email?"
                                    """)
                                with c_col2:
                                    st.markdown("**📼 VOICEMAIL DROP**")
                                    st.markdown(f"""
                                    "Hi [Name], Leon Basin here. Former Director of GTM at Fudo.
                                    
                                    I have a specific strategy to help you fix the **Partner Activation** bottleneck I'm seeing in your JD. It involves a 'Technical-to-Commercial' shift that drove $10M pipeline for me at Sense.
                                    
                                    Sending you the 1-pager now. Check your inbox."
                                    """)

                            # ==========================================
                            # AGENT 3: THE NETWORKER (LINKEDIN)
                            # ==========================================
                            elif "Networker" in agent:
                                st.subheader("🔗 LINKEDIN CONNECTION SEQUENCING")
                                st.markdown("**CONNECTION REQUEST (300 CHARS)**")
                                st.code(f"""
                                Hi [Name], following [Company]'s growth. I see you're scaling the Partner team. I previously built the GTM engine at Fudo (160% growth) and Sense ($10M pipe). I have a perspective on your LATAM expansion. Would love to connect. - Leon
                                """, language="text")
                                
                                st.markdown("**FOLLOW-UP DM (VALUE DROP)**")
                                st.markdown("""
                                "Thanks for connecting. I wrote a quick 'Gap Analysis' on [Company]'s current partner ecosystem vs. the 'Revenue OS' model I built at Fudo. Thought it might be useful as you scale Q3. [Link]"
                                """)

                            # ==========================================
                            # AGENT 4: THE DEVIL'S ADVOCATE (OBJECTIONS)
                            # ==========================================
                            elif "Devil" in agent:
                                st.subheader("🛡️ OBJECTION HANDLING (THE PRE-MORTEM)")
                                st.error("🚩 RED FLAG DETECTED: 'You've been a consultant recently.'")
                                st.markdown(f"""
                                **THE OBJECTION:** "We need a long-term builder, not a consultant."
                                
                                **THE SCRIPTED REBUTTAL:**
                                "I understand. I operated as a consultant specifically to build **'Zero-to-One'** engines for multiple startups quickly. 
                                
                                But my core DNA is **Ownership**. I spent 2 years at Fudo and 2 years at Sense building the foundations. I'm looking for my next 5-year home to scale what I build."
                                """)
                            
                            # ==========================================
                            # AGENT 5: THE ARCHITECT (90 DAY PLAN)
                            # ==========================================
                            elif "Architect" in agent:
                                st.subheader("🏗️ 30-60-90 DAY MICRO-PLAN")
                                st.markdown("""
                                * **Day 1-30 (Audit):** Audit the HubSpot/Salesforce instance for 'Signal Decay'. Interview top 5 performing reps to map the 'Winning Path'.
                                * **Day 31-60 (Build):** Deploy the 'Revenue OS' framework. Automate the 'Technical-to-Commercial' handoff to reduce friction.
                                * **Day 61-90 (Scale):** Launch the LATAM Partner Activation campaign. Target: 15% increase in partner-sourced pipeline.
                                """)

            else:
                st.error("⚠️ MISSING DATA: Upload assets to Vault and Paste JD.")
    
    # ==============================================================================
    # 🎯 MODE 2: HUNT (PRESCIENT TARGETING SYSTEM)
    # ==============================================================================
    elif input_mode == "🎯 Hunt":
        st.markdown("## ▲ PRESCIENT TARGETING SYSTEM")
        st.caption("PROTOCOL: Execute simultaneous sweeps across ATS, VC, and Social backchannels.")

        st.markdown("---")
        
        # 1. MASTER QUERY INPUT
        c1, c2, c3 = st.columns(3)
        with c1:
            target_role = st.selectbox("PRIMARY OBJECTIVE (Role Cluster)", 
                ["Director of GTM / RevOps", "Head of Partnerships", "Chief of Staff (Revenue)", "Founding GTM"])
        with c2:
            target_sector = st.selectbox("SECTOR ENVIRONMENT", 
                ["HR Tech / EOR (Deel)", "Cybersecurity / Zero Trust", "AI & DevTools", "Workforce / Staffing"])
        with c3:
            target_keywords = st.text_input("KEYWORD INJECTION (Optional)", placeholder="e.g. Python OR Zero Trust")

        st.markdown("---")

        # 2. THE MASTER QUERY ENGINE (Generates 5 simultaneous vectors)
        if st.button("🚀 INITIATE PRESCIENT SCAN (EXECUTE ALL VECTORS)", type="primary", use_container_width=True):
            
            # --- LOGIC ENGINE FOR CONSOLIDATION ---
            
            # Base Logic (Adapted from Master Boolean Library)
            if target_role == "Director of GTM / RevOps":
                role_logic = '("Director" OR "Head of" OR "GTM Operations" OR "RevOps")'
            elif target_role == "Head of Partnerships":
                role_logic = '("Head of Partnerships" OR "Director of Alliances" OR "Channel Chief")'
            elif target_role == "Chief of Staff (Revenue)":
                role_logic = '("Chief of Staff") AND ("Revenue" OR "Sales" OR "CRO")'
            elif target_role == "Founding GTM":
                role_logic = '("Founding AE" OR "First Sales Hire")'
            else:
                role_logic = '("Director" OR "Head of")'

            if "HR Tech" in target_sector:
                sector_logic = 'AND ("HR Tech" OR "Payroll" OR "EOR")'
            elif "Cybersecurity" in target_sector:
                sector_logic = 'AND ("Cybersecurity" OR "Zero Trust" OR "PAM")'
            elif "Workforce" in target_sector:
                sector_logic = 'AND ("Staffing" OR "Recruitment" OR "Rippling" OR "Greenhouse")'
            else:
                sector_logic = 'AND ("AI" OR "DevTools" OR "SaaS")'
                
            keyword_logic = f' AND ({target_keywords})' if target_keywords else ''
            noise_filter = 'AND NOT ("Intern" OR "SDR" OR "BDR" OR "Part-Time")'

            # 1. LINKEDIN VECTOR
            linkedin_query = f'{role_logic} {sector_logic} {keyword_logic} {noise_filter}'
            encoded_linkedin = linkedin_query.replace('"', '%22').replace(' ', '%20').replace('(', '%28').replace(')', '%29')

            # 2. ATS X-RAY VECTOR
            ats_systems = "site:lever.co OR site:greenhouse.io OR site:ashbyhq.com"
            ats_query = f'{ats_systems} "{target_role}" {keyword_logic}'
            encoded_ats = ats_query.replace(' ', '+').replace('"', '%22')

            # 3. SOCIAL WHISPER VECTOR
            whisper_role = target_role.split(' ')[0]
            whisper_query = f'("{whisper_role}" OR "{target_sector.split()[0]}") AND ("hiring" OR "join my team") min_faves:5'
            encoded_whisper = whisper_query.replace(' ', '%20').replace('"', '%22')

            # 4. VC BLACK OPS VECTOR
            vc_query = f'site:jobs.sequoiacap.com OR site:jobs.a16z.com OR site:wellfound.com "{target_role}"'
            encoded_vc = vc_query.replace(' ', '+').replace('"', '%22')


            # --- OUTPUT: THE DEPLOYMENT ARRAY ---
            st.markdown("### 📡 DEPLOYMENT ARRAY (5 VECTORS LAUNCHED)")
            
            st.markdown("#### 1. PRIMARY TARGETING (VOLUME & QUALITY)")
            st.code(linkedin_query, language="text")
            st.markdown(f"[🚀 **LINKEDIN VECTORS (EXECUTE MISSION)**](https://www.linkedin.com/jobs/search/?keywords={encoded_linkedin})", unsafe_allow_html=True)

            st.markdown("#### 2. ATS PENETRATION (STEALTH JOBS)")
            st.code(ats_query, language="text")
            st.markdown(f"[☢️ **ATS X-RAY (EXECUTE GOOGLE SCAN)**](https://www.google.com/search?q={encoded_ats})", unsafe_allow_html=True)
            
            st.markdown("---")

            st.markdown("#### 3. BLACK OPS & SOCIAL SIGNAL (PRESENCE)")
            
            st.markdown("**VC BLACK OPS (Hidden Market)**")
            st.code(vc_query, language="text")
            st.markdown(f"[🏴‍☠️ **VC PORTFOLIO SCAN**](https://www.google.com/search?q={encoded_vc})", unsafe_allow_html=True)

            st.markdown("**SOCIAL WHISPER (Signal Detection)**")
            st.code(whisper_query, language="text")
            st.markdown(f"[🐦 **EXECUTE X/TWITTER INTERCEPT**](https://twitter.com/search?q={encoded_whisper})", unsafe_allow_html=True)

            st.markdown("#### 4. WORKFORCE INTEL (Ecosystem Backchannel)")
            st.markdown(f"[💼 **YC JOB BOARDS**](https://www.ycombinator.com/jobs?role=Sales&role=Operations)", unsafe_allow_html=True)
            
            st.markdown("---")
            
            # DIGITAL ETHER EXPANSION
            st.markdown("#### 5. DIGITAL ETHER (Deep Web Intel)")
            st.caption("Underground signals: Reddit, Hacker News, Financial News")
            
            ether_c1, ether_c2 = st.columns(2)
            
            with ether_c1:
                st.markdown("**🔴 REDDIT INTEL**")
                st.markdown(f"[r/ExperiencedSales](https://www.reddit.com/r/ExperiencedSales/search/?q={target_role.replace(' ', '%20')})", unsafe_allow_html=True)
                st.markdown(f"[r/sales](https://www.reddit.com/r/sales/search/?q=GTM%20hiring)", unsafe_allow_html=True)
                st.markdown(f"[r/devops](https://www.reddit.com/r/devops/search/?q=hiring)", unsafe_allow_html=True)
                
                st.markdown("**👾 HACKER NEWS**")
                hn_query = f"{target_role} hiring"
                st.markdown(f"[HN: Who's Hiring](https://hn.algolia.com/?q={hn_query.replace(' ', '+')})", unsafe_allow_html=True)
            
            with ether_c2:
                st.markdown("**📰 FINANCIAL SIGNALS**")
                st.markdown(f"[WSJ: Funding News](https://www.wsj.com/search?query={target_sector.split()[0]}%20funding)", unsafe_allow_html=True)
                st.markdown(f"[TechCrunch: Funding](https://techcrunch.com/tag/funding/)", unsafe_allow_html=True)
                st.markdown(f"[Crunchbase: Recent Funding](https://www.crunchbase.com/discover/funding_rounds)", unsafe_allow_html=True)
                
                st.markdown("**🎯 SECTOR INTEL**")
                st.markdown(f"[Google News: {target_sector.split()[0]}](https://news.google.com/search?q={target_sector.split()[0]}%20hiring)", unsafe_allow_html=True)
            
            st.success("✅ ALL 7 VECTORS DEPLOYED. Execute each link to initiate sweep.")

    # ==============================================================================
    # 🔮 MODE 12: ORACLE DECK (CAREER TAROT)
    # ==============================================================================
    elif input_mode == "🔮 Oracle Deck":
        st.markdown("## 🔮 ORACLE: QUANTUM SIGNAL")
        st.caption("PROTOCOL: Decrypt the Noise. Align with the Signal. The Market is a construct.")
        
        # QUANTUM PARSER INPUT
        st.markdown("### 🧬 INGEST EXTERNAL SIGNAL")
        job_url = st.text_input("Paste Job Link (LinkedIn/Indeed)", placeholder="https://linkedin.com/jobs/view/...")
        job_raw = st.text_area("Or Paste Raw Job Description (The Matrix Code)", height=150, placeholder="Paste the JD here to extract hidden salary and red flags...")
        
        if st.button("🔮 DECRYPT SIGNAL"):
             with st.spinner("Parsing Reality..."):
                 from logic.integrations import extract_job_signal, calculate_vibe_resonance
                 import time
                 time.sleep(1.5)
                 
                 # MOCK PARSE (Simulated)
                 signal_data = extract_job_signal(job_raw if job_raw else "Mock Data")
                 resonance = calculate_vibe_resonance(signal_data['signal'])
                 
                 st.markdown("---")
                 st.markdown(f"### 🔓 SIGNAL DECRYPTED: {signal_data['title']}")
                 
                 q_col1, q_col2 = st.columns([1, 1])
                 
                 with q_col1:
                     st.metric("Estimated Comp", signal_data['salary_est'], "Market Rate")
                     st.markdown("**⚠️ RED FLAG SCAN:**")
                     for flag in signal_data['flags']:
                         st.markdown(f"- 🚩 {flag}")
                         
                 with q_col2:
                      st.markdown(f"""
                        <div style="border: 1px solid #00ff88; padding: 20px; border-radius: 10px; text-align: center; background: rgba(0, 255, 136, 0.05);">
                            <h2 style="color: #00ff88; margin: 0;">{resonance['score']}%</h2>
                            <p style="margin: 0; color: #fff;">QUANTUM RESONANCE</p>
                            <p style="font-size: 0.8rem; color: #888; margin-top: 10px;">{resonance['math_proof']}</p>
                        </div>
                      """, unsafe_allow_html=True)
                 
                 st.button("💾 SAVE TO PIPELINE (PROJECTED)", type="primary")
                 
                 # KNOWLEDGE BASE SAVE
                 if st.button("🧠 ADD TO AGENT KNOWLEDGE BASE"):
                     if 'jd_knowledge_base' not in st.session_state:
                         st.session_state.jd_knowledge_base = []
                     st.session_state.jd_knowledge_base.append(signal_data)
                     st.toast(f"JD Ingested. Agent Intelligence: {len(st.session_state.jd_knowledge_base)} Records.", icon="🧠")

        st.markdown("---")
        
        # AGENT KNOWLEDGE BASE DISPLAY
        if 'jd_knowledge_base' in st.session_state and st.session_state.jd_knowledge_base:
            with st.expander(f"📚 AGENT TRAINING DATA ({len(st.session_state.jd_knowledge_base)} JDs)", expanded=False):
                 st.dataframe(st.session_state.jd_knowledge_base)
                 
        st.markdown("### 🃏 THE DECK (ACTIVE OPPORTUNITIES)")
        
        # EXISTING CARD STACK DISPLAY (Keep existing logic but styled)
        if 'swipe_jobs' not in st.session_state:
            st.session_state.swipe_jobs = [
                # Tier 1: AI Leaders ($250k+)
                {"id": 1, "title": "Director of GTM Strategy", "company": "Mistral AI", "location": "San Francisco, CA", "salary": "$220k-280k", "match": 95, "signal": "Series B, $600M raised, hiring 50+ in GTM", "url": "https://mistral.ai/careers", "tier": "🔥 TIER 1"},
                {"id": 2, "title": "VP of Revenue Operations", "company": "Anthropic", "location": "San Francisco, CA", "salary": "$250k-320k", "match": 92, "signal": "AI Leader, aggressive expansion, ex-OpenAI team", "url": "https://anthropic.com/careers", "tier": "🔥 TIER 1"},
                {"id": 3, "title": "Head of GTM - Enterprise", "company": "OpenAI", "location": "San Francisco, CA", "salary": "$300k-400k", "match": 94, "signal": "ChatGPT, GPT-5 coming, massive enterprise push", "url": "https://openai.com/careers", "tier": "🔥 TIER 1"},
                {"id": 4, "title": "Director of Sales Strategy", "company": "Wiz", "location": "Palo Alto, CA", "salary": "$230k-300k", "match": 91, "signal": "Cloud security unicorn, $1B ARR run rate", "url": "https://wiz.io/careers", "tier": "🔥 TIER 1"},
                
                # Tier 2: Security/DevTools ($200k+)
                {"id": 5, "title": "Head of Partnerships", "company": "Verkada", "location": "San Mateo, CA", "salary": "$200k-260k", "match": 88, "signal": "Physical security + AI, strong channel program", "url": "https://verkada.com/careers", "tier": "⚡ TIER 2"},
                {"id": 6, "title": "Director of Channel Sales", "company": "CrowdStrike", "location": "Austin, TX (Remote OK)", "salary": "$210k-270k", "match": 89, "signal": "Cybersecurity leader, expanding partner ecosystem", "url": "https://crowdstrike.com/careers", "tier": "⚡ TIER 2"},
                {"id": 7, "title": "VP GTM Operations", "company": "Figma", "location": "San Francisco, CA", "salary": "$240k-300k", "match": 87, "signal": "Adobe acquisition fell through, independent growth mode", "url": "https://figma.com/careers", "tier": "⚡ TIER 2"},
                {"id": 8, "title": "Director of RevOps", "company": "Ambient.ai", "location": "Palo Alto, CA", "salary": "$180k-220k", "match": 90, "signal": "AI Security, Series B, building GTM from scratch", "url": "https://ambient.ai/careers", "tier": "⚡ TIER 2"},
                
                # Tier 3: Growth Stage ($150k-200k)
                {"id": 9, "title": "GTM Lead - Enterprise", "company": "Notion", "location": "San Francisco, CA", "salary": "$190k-240k", "match": 85, "signal": "Productivity + AI features, PLG motion", "url": "https://notion.so/careers", "tier": "📈 TIER 3"},
                {"id": 10, "title": "Account Executive - Enterprise", "company": "Deel", "location": "Remote US", "salary": "$180k-250k OTE", "match": 86, "signal": "Global HR tech, $12B valuation, aggressive expansion", "url": "https://deel.com/careers", "tier": "📈 TIER 3"},
                {"id": 11, "title": "Director of Partnerships", "company": "Hightouch", "location": "San Francisco, CA", "salary": "$170k-220k", "match": 84, "signal": "Data activation, Reverse ETL leader, partner-led growth", "url": "https://hightouch.com/careers", "tier": "📈 TIER 3"},
                {"id": 12, "title": "Head of Sales", "company": "Nooks", "location": "San Francisco, CA", "salary": "$160k-200k + equity", "match": 83, "signal": "AI Sales tools, YC backed, disrupting cold calling", "url": "https://nooks.ai/careers", "tier": "📈 TIER 3"},
                
                # Tier 4: Early Stage (High Equity)
                {"id": 13, "title": "First US AE", "company": "2501.ai", "location": "Remote US", "salary": "$150k-180k + 0.5% equity", "match": 88, "signal": "AI Agents, European startup, first US hire", "url": "https://2501.ai", "tier": "🚀 TIER 4"},
                {"id": 14, "title": "GTM Lead", "company": "DepthFirst", "location": "San Francisco, CA", "salary": "$140k-170k + 0.8% equity", "match": 91, "signal": "AI Infrastructure, Seed stage, building from zero", "url": "https://depthfirst.ai", "tier": "🚀 TIER 4"},
                {"id": 15, "title": "Fractional CRO", "company": "Stealth AI Startup", "location": "Remote", "salary": "$5k-10k/mo retainer", "match": 80, "signal": "Pre-seed, need GTM strategy, equity available", "url": "#", "tier": "🌱 ADVISORY"},
            ]
            st.session_state.swipe_index = 0
            st.session_state.swiped_right = []
            st.session_state.swiped_priority = []
        
        # Current job
        jobs = st.session_state.swipe_jobs
        idx = st.session_state.swipe_index
        
        if idx < len(jobs):
            job = jobs[idx]
            
            # --- METAPHYSICAL MATH ENGINE ---
            # Calculate resonance on the fly for the visual effect
            from logic.integrations import calculate_vibe_resonance
            resonance = calculate_vibe_resonance(job['signal'] + job['title'])
            
            # --- EXOTIC GLASS CARD UI ---
            tier = job.get('tier', '📈 TIER 3')
            tier_color = "#FFD700" if "TIER 1" in tier else "#00d4ff" if "TIER 2" in tier else "#00ff88"
            
            st.markdown(f"""
            <div style="
                background: rgba(20, 20, 20, 0.8);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-top: 1px solid {tier_color};
                border-radius: 24px;
                padding: 40px;
                margin: 20px 0;
                text-align: center;
                box-shadow: 0 20px 50px rgba(0,0,0,0.5);
                position: relative;
                overflow: hidden;
            ">
                <!-- Background Glow -->
                <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; 
                            background: radial-gradient(circle, {tier_color}11 0%, transparent 60%); pointer-events: none;"></div>
                
                <p style="color: {tier_color}; font-size: 0.8rem; letter-spacing: 2px; font-weight: bold; margin-bottom: 20px;">
                    {tier} // CARD {idx + 1} OF {len(jobs)}
                </p>
                
                <h1 style="color: white; font-size: 2.5rem; margin: 10px 0; font-weight: 800; text-shadow: 0 0 20px {tier_color}66;">
                    {job['title']}
                </h1>
                
                <h2 style="color: #e0e0e0; font-size: 1.5rem; margin-bottom: 30px;">
                    {job['company']} <span style="opacity: 0.5;">|</span> {job['location']}
                </h2>
                
                <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 30px;">
                    <span style="background: rgba(255,255,255,0.05); padding: 8px 16px; border-radius: 100px; color: #fff; border: 1px solid rgba(255,255,255,0.1);">
                        💰 {job['salary']}
                    </span>
                    <span style="background: rgba(255,255,255,0.05); padding: 8px 16px; border-radius: 100px; color: #fff; border: 1px solid rgba(255,255,255,0.1);">
                        📡 {job['signal'][:30]}...
                    </span>
                </div>
                
                <!-- MATH RESONANCE -->
                <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px; margin-top: 20px;">
                    <div style="color: {tier_color}; font-family: monospace; font-size: 1.2rem; margin-bottom: 5px;">
                        SOUL RESONANCE: {resonance['score']}%
                    </div>
                    <div style="color: #666; font-family: monospace; font-size: 0.8rem;">
                        {resonance['math_proof']}
                    </div>
                    <div style="color: #888; font-size: 0.9rem; margin-top: 10px;">
                        VECTOR: {resonance['primary_vector']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Interaction
            col_skip, col_super, col_like = st.columns([1, 1, 1])
            
            with col_skip:
                if st.button("❌ PASS", use_container_width=True, key=f"skip_{idx}"):
                    st.session_state.swipe_index += 1
                    st.rerun()
            
            with col_super:
                if st.button("⭐ SUPER MATCH", use_container_width=True, key=f"super_{idx}", type="primary"):
                    st.session_state.swiped_priority.append(job)
                    st.session_state.swipe_index += 1
                    
                    if 'crm_deals' in st.session_state:
                         if not any(d['Company'] == job['company'] for d in st.session_state['crm_deals']):
                            st.session_state['crm_deals'].append({
                                "Company": job['company'],
                                "Role": job['title'],
                                "Stage": "1. Identified",
                                "Priority": 1,
                                "Signal": "High",
                                "Notes": f"Resonance: {resonance['score']}%. Vector: {resonance['primary_vector']}"
                            })
                    st.toast(f"Top Priority: {job['company']}", icon="⭐")
                    st.rerun()
                    
            with col_like:
                if st.button("✅ VIBE CHECK", use_container_width=True, key=f"like_{idx}"):
                    st.session_state.swiped_right.append(job)
                    st.session_state.swipe_index += 1
                    
                    if 'crm_deals' in st.session_state:
                         if not any(d['Company'] == job['company'] for d in st.session_state['crm_deals']):
                            st.session_state['crm_deals'].append({
                                "Company": job['company'],
                                "Role": job['title'],
                                "Stage": "1. Identified",
                                "Priority": 2,
                                "Signal": "Medium",
                                "Notes": f"Resonance: {resonance['score']}%."
                            })
                    st.toast(f"Pipeline Updated: {job['company']}", icon="✅")
                    st.rerun()
                    
            st.caption("Press 'R' to recalibrate reality (Refresh) if cards get stuck.")
            
            # Progress bar
            progress = (idx + 1) / len(jobs)
            st.progress(progress)
            st.caption(f"Swiped: {idx} | Saved: {len(st.session_state.swiped_right)} | Priority: {len(st.session_state.swiped_priority)}")
            
        else:
            # All jobs swiped
            st.success("🎉 ALL JOBS REVIEWED!")
            
            st.markdown("### 📈 YOUR SELECTIONS")
            
            if st.session_state.swiped_priority:
                st.markdown("#### ⭐ PRIORITY 1 (Apply Now)")
                for j in st.session_state.swiped_priority:
                    st.markdown(f"- **{j['title']}** @ {j['company']} ({j['match']}% match)")
            
            if st.session_state.swiped_right:
                st.markdown("#### ✅ PIPELINE (Follow Up)")
                for j in st.session_state.swiped_right:
                    st.markdown(f"- **{j['title']}** @ {j['company']} ({j['match']}% match)")
            
            # Reset button
            if st.button("🔄 RESET & SWIPE AGAIN"):
                st.session_state.swipe_index = 0
                st.session_state.swiped_right = []
                st.session_state.swiped_priority = []
                st.rerun()
            
            # Export to Pipeline CRM
            st.markdown("---")
            st.info("💡 TIP: Go to Pipeline CRM to add these opportunities with full tracking.")

    # ==============================================================================
    # ▲ MODE 6: ORACLE (DIGITAL ETHER & PREDICTIVE INDEXING)
    # ==============================================================================
    elif input_mode == "📊 Analytics":
        st.markdown("## 📊 PERFORMANCE ANALYTICS & INVESTOR INTELLIGENCE")
        st.caption("PROTOCOL: Track Everything. Learn from Outcomes. Understand the Funding Lifecycle.")
        
        # Tabs for different analytics views
        analytics_tab1, analytics_tab2, analytics_tab3 = st.tabs(["🎤 VOICE ANALYTICS", "📈 PIPELINE METRICS", "💰 INVESTOR INTELLIGENCE"])
        
        # ═══════════════════════════════════════════════════════════════
        # TAB 1: VOICE SESSION ANALYTICS
        # ═══════════════════════════════════════════════════════════════
        with analytics_tab1:
            st.markdown("### 🎤 VOICE SESSION ANALYTICS")
            st.caption("Track your interview practice progress over time.")
            
            voice_sessions = st.session_state.get('voice_sessions', [])
            
            if voice_sessions:
                # Summary Metrics
                total_sessions = len(voice_sessions)
                avg_words = sum(s['words'] for s in voice_sessions) / total_sessions
                avg_fillers = sum(s['fillers'] for s in voice_sessions) / total_sessions
                metric_rate = sum(1 for s in voice_sessions if s['has_metric']) / total_sessions * 100
                
                k1, k2, k3, k4 = st.columns(4)
                k1.metric("TOTAL SESSIONS", total_sessions)
                k2.metric("AVG WORDS/RESPONSE", f"{avg_words:.0f}", "Target: 150-200")
                k3.metric("AVG FILLER WORDS", f"{avg_fillers:.1f}", "Target: <3", delta_color="inverse")
                k4.metric("METRIC USAGE RATE", f"{metric_rate:.0f}%", "Target: 100%")
                
                st.markdown("---")
                
                # Session History Table
                st.markdown("#### 📜 SESSION HISTORY")
                
                for i, session in enumerate(reversed(voice_sessions[-10:])):
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.write(f"**{session['drill'][:40]}...**" if len(session['drill']) > 40 else f"**{session['drill']}**")
                    with col2:
                        st.caption(f"Words: {session['words']}")
                    with col3:
                        st.caption(f"Fillers: {session['fillers']}")
                    with col4:
                        st.caption("✅ Metric" if session['has_metric'] else "❌ No Metric")
                    st.divider()
                
                # Trend Analysis
                st.markdown("#### 📈 IMPROVEMENT TREND")
                if total_sessions >= 3:
                    first_half = voice_sessions[:total_sessions//2]
                    second_half = voice_sessions[total_sessions//2:]
                    
                    first_fillers = sum(s['fillers'] for s in first_half) / len(first_half)
                    second_fillers = sum(s['fillers'] for s in second_half) / len(second_half)
                    
                    improvement = first_fillers - second_fillers
                    
                    if improvement > 0:
                        st.success(f"🎯 **FILLER WORD REDUCTION:** -{improvement:.1f} per response. You're improving!")
                    else:
                        st.warning(f"⚠️ **FILLER WORDS:** +{abs(improvement):.1f} per response. Focus on pausing instead of filling.")
                else:
                    st.info("Complete 3+ sessions to see improvement trends.")
            else:
                st.info("🎤 No voice sessions recorded yet. Go to **Voice Telemetry Lab** to start practicing.")
                if st.button("→ Go to Voice Lab"):
                    st.session_state.selected_tool_label = "🎤 Voice (Practice)"
                    st.rerun()
        
        # ═══════════════════════════════════════════════════════════════
        # TAB 2: PIPELINE METRICS
        # ═══════════════════════════════════════════════════════════════
        with analytics_tab2:
            st.markdown("### 📈 PIPELINE VELOCITY METRICS")
            st.caption("Track your job search like an Enterprise Sales pipeline.")
            
            pipeline_data = st.session_state.get('pipeline_data', [])
            
            if pipeline_data:
                # Stage Distribution
                stages = [d.get("Stage", "Unknown") for d in pipeline_data]
                stage_counts = {}
                for stage in stages:
                    stage_counts[stage] = stage_counts.get(stage, 0) + 1
                
                # Funnel Metrics
                total_deals = len(pipeline_data)
                final_rounds = stage_counts.get("Final Round", 0)
                interviews = stage_counts.get("HM Interview", 0) + stage_counts.get("Screen", 0)
                
                k1, k2, k3, k4 = st.columns(4)
                k1.metric("TOTAL ACTIVE", total_deals)
                k2.metric("FINAL ROUNDS", final_rounds, f"{(final_rounds/total_deals*100):.0f}% of pipeline")
                k3.metric("IN INTERVIEW", interviews)
                k4.metric("CONVERSION RATE", f"{(final_rounds/total_deals*100):.0f}%", "Industry avg: 15%")
                
                st.markdown("---")
                
                # Stage Breakdown
                st.markdown("#### 📊 STAGE BREAKDOWN")
                for stage, count in stage_counts.items():
                    pct = count / total_deals * 100
                    st.progress(pct / 100, text=f"{stage}: {count} ({pct:.0f}%)")
            else:
                st.info("📈 No pipeline data yet. Go to **Pipeline CRM** to add opportunities.")
                if st.button("→ Go to Pipeline CRM"):
                    st.session_state.selected_tool_label = "📈 Pipeline CRM"
                    st.rerun()
        
        # ═══════════════════════════════════════════════════════════════
        # TAB 3: INVESTOR INTELLIGENCE (Funding Lifecycle)
        # ═══════════════════════════════════════════════════════════════
        with analytics_tab3:
            st.markdown("### 💰 INVESTOR INTELLIGENCE: THE FUNDING LIFECYCLE")
            st.caption("Understand each funding stage and what it means for hiring.")
            
            st.markdown("---")
            
            # Funding Stage Selector
            funding_stage = st.selectbox("Select Funding Stage to Analyze:", [
                "🌱 Pre-Seed / Friends & Family",
                "🌿 Seed ($500K - $3M)",
                "🚀 Series A ($5M - $15M)",
                "📈 Series B ($15M - $50M)",
                "🏢 Series C ($50M - $100M+)",
                "🏛️ Series D/E (Late Stage)",
                "🔔 Pre-IPO",
                "📊 IPO & Public"
            ])
            
            st.markdown("---")
            
            # Dynamic Content Based on Stage
            if funding_stage == "🌱 Pre-Seed / Friends & Family":
                st.markdown("""
                ### 🌱 PRE-SEED / FRIENDS & FAMILY
                
                **Typical Raise:** $50K - $500K  
                **Valuation:** $1M - $5M  
                **Investors:** Founders, Angels, Accelerators (YC, Techstars)
                
                #### 🎯 WHAT TO LOOK FOR
                | Signal | What It Means |
                |--------|---------------|
                | Team background | Are founders ex-FAANG, ex-unicorn? |
                | Problem clarity | Is the pain clearly articulated? |
                | YC/Techstars batch | Accelerator stamp = signal boost |
                
                #### 👔 HIRING SIGNALS
                - **Roles:** Usually just founders. Maybe 1-2 engineers.
                - **Opportunity for you:** If you know the founders, offer advisory.
                - **Risk:** High uncertainty, equity-heavy compensation.
                """)
                
            elif funding_stage == "🌿 Seed ($500K - $3M)":
                st.markdown("""
                ### 🌿 SEED ($500K - $3M)
                
                **Typical Raise:** $500K - $3M  
                **Valuation:** $5M - $15M  
                **Investors:** Angels, Seed VCs (First Round, Precursor)
                
                #### 🎯 WHAT TO LOOK FOR
                | Signal | What It Means |
                |--------|---------------|
                | Early traction | 10-50 customers, $10-50K MRR |
                | Team expansion | First non-founder hires |
                | Product clarity | MVP is live and getting feedback |
                
                #### 👔 HIRING SIGNALS
                - **Roles:** First GTM hire (often "Head of Growth" or "Founding AE")
                - **Opportunity:** High equity, high impact, shape the GTM motion
                - **Risk:** Runway is short (12-18 months). Must show ROI fast.
                """)
                
            elif funding_stage == "🚀 Series A ($5M - $15M)":
                st.markdown("""
                ### 🚀 SERIES A ($5M - $15M)
                
                **Typical Raise:** $5M - $15M  
                **Valuation:** $20M - $60M  
                **Investors:** A16Z, Sequoia, Accel, Bessemer
                
                #### 🎯 WHAT TO LOOK FOR
                | Signal | What It Means |
                |--------|---------------|
                | Product-Market Fit | Repeatable customer acquisition |
                | $100K+ MRR | Revenue velocity proving demand |
                | Board involvement | Tier 1 VC on board = talent magnet |
                
                #### 👔 HIRING SIGNALS
                - **Roles:** VP of Sales, Director of GTM, Head of Partnerships
                - **Opportunity:** Build the revenue engine from scratch
                - **Your Pitch:** "I've scaled from 0→1. Here's my 90-day plan."
                - **Comp:** $150-200K OTE + 0.1-0.5% equity
                """)
                
            elif funding_stage == "📈 Series B ($15M - $50M)":
                st.markdown("""
                ### 📈 SERIES B ($15M - $50M)
                
                **Typical Raise:** $15M - $50M  
                **Valuation:** $80M - $200M  
                **Investors:** Insight, Tiger Global, General Catalyst
                
                #### 🎯 WHAT TO LOOK FOR
                | Signal | What It Means |
                |--------|---------------|
                | Scaling revenue | $1-5M ARR, 2-3x YoY growth |
                | Team explosion | 50-150 employees |
                | Process gaps | Growing pains = need for systems |
                
                #### 👔 HIRING SIGNALS
                - **Roles:** Director/VP of RevOps, GTM Systems, Partner Lead
                - **Opportunity:** Bring order to chaos. Build the Revenue OS.
                - **Your Pitch:** "I've seen this movie before. Here's the playbook."
                - **Comp:** $180-250K OTE + equity refresh
                """)
                
            elif funding_stage == "🏢 Series C ($50M - $100M+)":
                st.markdown("""
                ### 🏢 SERIES C ($50M - $100M+)
                
                **Typical Raise:** $50M - $150M  
                **Valuation:** $300M - $1B  
                **Investors:** Coatue, D1, SoftBank
                
                #### 🎯 WHAT TO LOOK FOR
                | Signal | What It Means |
                |--------|---------------|
                | Category leader | Clear market position |
                | International expansion | Multi-geo GTM |
                | M&A activity | Acquiring competitors |
                
                #### 👔 HIRING SIGNALS
                - **Roles:** VP International, M&A Integration, Enterprise GTM
                - **Opportunity:** Scale existing engine globally
                - **Comp:** $220-350K OTE + strong equity
                """)
                
            elif funding_stage == "🏛️ Series D/E (Late Stage)":
                st.markdown("""
                ### 🏛️ SERIES D/E (LATE STAGE)
                
                **Typical Raise:** $100M - $500M  
                **Valuation:** $1B+ (Unicorn)  
                **Investors:** PE (Vista, Thoma Bravo), Crossover funds
                
                #### 🎯 WHAT TO LOOK FOR
                | Signal | What It Means |
                |--------|---------------|
                | IPO prep | S-1 filing rumors |
                | EBITDA focus | Profitability over growth |
                | Executive turnover | New CFO = IPO mode |
                
                #### 👔 HIRING SIGNALS
                - **Roles:** IPO-readiness roles, Investor Relations, Chief of Staff
                - **Opportunity:** Be part of the exit
                - **Comp:** $250-400K OTE + pre-IPO equity (liquidity incoming)
                """)
                
            elif funding_stage == "🔔 Pre-IPO":
                st.markdown("""
                ### 🔔 PRE-IPO
                
                **Status:** Filing S-1, 6-18 months from listing  
                **Valuation:** $5B+  
                **Key Events:** Quiet period, lockup discussions
                
                #### 🎯 WHAT TO LOOK FOR
                | Signal | What It Means |
                |--------|---------------|
                | S-1 filing | Financials now public |
                | PIPE rounds | Last private equity infusion |
                | Heavy recruiting | IPO team buildout |
                
                #### 👔 HIRING SIGNALS
                - **Roles:** Investor Relations, SOX Compliance, Enterprise Expansion
                - **Opportunity:** Pre-IPO equity = potential windfall
                - **Risk:** Lockup period (can't sell for 6 months post-IPO)
                """)
                
            else:  # IPO & Public
                st.markdown("""
                ### 📊 IPO & PUBLIC COMPANY
                
                **Status:** Publicly traded  
                **Valuation:** Market cap  
                **Key Focus:** Quarterly earnings, analyst relations
                
                #### 🎯 WHAT TO LOOK FOR
                | Signal | What It Means |
                |--------|---------------|
                | Revenue growth rate | Wall Street expectation |
                | Rule of 40 | Growth % + Margin % > 40 |
                | Executive changes | New CEO = strategy shift |
                
                #### 👔 HIRING SIGNALS
                - **Roles:** Enterprise, Strategic Partnerships, M&A
                - **Opportunity:** Stable comp, RSUs, brand name
                - **Trade-off:** Less equity upside, more process
                - **Comp:** $200-400K OTE + RSUs (4-year vest)
                """)

    
    # ─────────────────────────────────────────────────────────────
    # TALENT SIGNAL MODE - SCREEN CANDIDATES
    # ─────────────────────────────────────────────────────────────
    elif input_mode == "🔍 Talent Signal":
        st.markdown("## 🔍 TALENT SIGNAL DETECTOR")
        
        signal_tab1, signal_tab2 = st.tabs(["🕵️ SCRUTINIZE CANDIDATES (Recruiter Mode)", "🧭 CAREER PATHFINDER (Job Seeker Mode)"])
        
        # --- TAB 1: RECRUITER MODE (Existing Logic) ---
        with signal_tab1:
            st.caption("Screen candidates using 15 years of hiring instinct, codified into AI")
            st.info("💡 **Use Case:** You're helping a company screen candidates, or building your portfolio as a hiring consultant.")
            
            st.markdown('<div class="divider-solid"></div>', unsafe_allow_html=True)
            
            # Job Requirements
            st.markdown("##### 📋 ROLE REQUIREMENTS")
            
        # --- TAB 2: PATHFINDER MODE (New!) ---
        with signal_tab2:
            st.caption("Not sure what roles to target? AI analyzes your DNA to find your best market fit.")
            
            path_input = st.text_area("Paste your Resume / Background Summary:", height=200, placeholder="Paste your resume text here...", key="path_input")
            
            if st.button("🧭 FIND MY PATH", type="primary"):
                if path_input:
                    with st.spinner("Analyzing Career DNA..."):
                        from logic.generator import generate_plain_text
                        
                        path_prompt = f"""
                        Analyze this candidate's background and suggest 3 DISTINCT Career Archetypes they should target.
                        
                        Candidate Background:
                        {path_input}
                        
                        For each Archetype, provide:
                        1. **The Title**: (e.g. "Director of GTM Systems")
                        2. **The Sector**: (e.g. "Series B Cybersecurity SaaS")
                        3. **The 'Why'**: Why they are a top 1% fit here.
                        4. **Keywords**: 3 keywords to search on LinkedIn.
                        
                        Format clearly as ARCHETYPE 1, ARCHETYPE 2, ARCHETYPE 3.
                        """
                        
                        model_id = st.session_state.get('selected_model_id', "llama-3.3-70b-versatile")
                        path_result = generate_plain_text(path_prompt, model_name=model_id)
                        
                        st.session_state['path_result'] = path_result

            if st.session_state.get('path_result'):
                st.markdown("### 🎯 RECOMMENDED TARGET VECTORS")
                st.markdown(st.session_state['path_result'])
                
                st.markdown("---")
                st.markdown("#### 🔗 LAUNCH LINKEDIN SEARCHES")
                
                # Dynamic Link Generators based on typical outputs (using static examples to start)
                l1, l2, l3 = st.columns(3)
                with l1:
                    st.markdown("[🔍 Search: GTM Systems Director](https://www.linkedin.com/jobs/search/?keywords=Director%20GTM%20Systems)")
                with l2:
                    st.markdown("[🔍 Search: Revenue Operations Lead](https://www.linkedin.com/jobs/search/?keywords=Head%20Revenue%20Operations)")
                with l3:
                    st.markdown("[🔍 Search: Sales Engineering Manager](https://www.linkedin.com/jobs/search/?keywords=Manager%20Sales%20Engineering)")
        with signal_tab1:
            recruiter_role = st.text_input(
                "Role being hired for:",
                placeholder="e.g., Senior GTM Manager, Head of Partnerships",
                key="recruiter_role"
            )
            
            recruiter_jd = st.text_area(
                "Job Description / Must-Haves:",
                height=150,
                placeholder="Paste the JD or list the key requirements...",
                key="recruiter_jd"
            )
            
            st.markdown("")
            
            # Screening Criteria
            st.markdown("##### ⚙️ SCREENING CRITERIA")
            col_crit1, col_crit2 = st.columns(2)
            
            with col_crit1:
                min_experience = st.slider("Min. Years Experience", 0, 20, 5, key="min_exp")
                require_metrics = st.checkbox("Must have quantified metrics", value=True, key="req_metrics")
                require_leadership = st.checkbox("Must show leadership experience", value=False, key="req_lead")
            
            with col_crit2:
                red_flags = st.multiselect(
                    "Red Flags to catch:",
                    ["Job hopping (<18 months)", "No metrics/numbers", "Vague descriptions", "Employment gaps", "Corporate buzzwords", "No progression"],
                    default=["Job hopping (<18 months)", "No metrics/numbers"],
                    key="red_flags"
                )
            
            st.markdown("")
            
            # Candidate Resume
            st.markdown("##### 📄 CANDIDATE RESUME")
            candidate_resume = st.text_area(
                "Paste the candidate's resume:",
                height=250,
                placeholder="Paste the full resume or LinkedIn summary of the candidate...",
                key="candidate_resume"
            )
            
            st.markdown('<div class="divider-solid"></div>', unsafe_allow_html=True)
            
            # Screen Button
            if st.button("🔍 SCREEN THIS CANDIDATE", use_container_width=True, type="primary"):
                if candidate_resume and recruiter_role:
                    with st.spinner("Applying the Recruiter's Eye..."):
                        try:
                            screening_prompt = f"""You are Leon Basin, a Technical Revenue Architect with 15 years of GTM experience.

    You are screening a candidate for: {recruiter_role}

    JOB REQUIREMENTS:
    {recruiter_jd[:1500]}

    SCREENING CRITERIA:
    - Minimum {min_experience} years of experience required
    - Must have quantified metrics: {require_metrics}
    - Must show leadership: {require_leadership}
    - Red flags to catch: {', '.join(red_flags)}

    CANDIDATE'S RESUME:
    {candidate_resume[:2500]}

    Screen this candidate with your "Recruiter's Eye" from 15 years of hiring.

    Provide your assessment in this format:

    **VERDICT**: [STRONG HIRE 🟢 / INTERVIEW 🟡 / PASS ❌]

    **FIT SCORE**: [0-100]

    **QUICK TAKE** (2 sentences):
    What's your gut reaction in 10 seconds?

    **STRENGTHS** (Top 3):
    What makes this candidate stand out?

    **CONCERNS** (Top 3):
    What would you probe in an interview?

    **RED FLAGS DETECTED**:
    Based on the criteria, what red flags did you find?

    **INTERVIEW QUESTIONS** (2-3):
    What would you ask to validate their claims?

    **COMPARISON NOTE**:
    How does this candidate compare to the top 10% you've seen for this role?

    Be direct. Be specific. Give the hiring manager a clear recommendation."""

                            from logic.generator import generate_plain_text
                            model_id = st.session_state.get('selected_model_id', 'llama-3.3-70b-versatile')
                            screening_result = generate_plain_text(screening_prompt, model_name=model_id)
                            st.session_state.screening_result = screening_result
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please enter the role and paste the candidate's resume.")
            
            # Display Results
            if "screening_result" in st.session_state and st.session_state.screening_result:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown("##### 📊 SCREENING RESULT")
                st.markdown(st.session_state.screening_result)
                
                st.markdown("")
                with st.expander("📤 EXPORT OPTIONS"):
                    st.markdown("**Copy this assessment to:**")
                    st.markdown("- Greenhouse/Lever feedback form")
                    st.markdown("- Hiring manager email")
                st.markdown("- Your consulting deliverable")
                st.code(st.session_state.screening_result, language="markdown")
        
        # Set empty values
        resume_text = ""
        job_description = ""
    
    # ─────────────────────────────────────────────────────────────
    # VOICE MODE - ENHANCED
    # ─────────────────────────────────────────────────────────────
    elif input_mode == "🎤 Voice":
        st.markdown("## 🎙️ VOICE TELEMETRY LAB")
        st.caption("PROTOCOL: Cloud-Native Voice Recording + Executive Presence Scoring.")
        
        # MODE SELECTOR: Desktop vs Mobile
        voice_mode = st.radio("🎛️ PRACTICE MODE", 
            ["🖥️ Desktop (Full Lab)", "📱 Mobile (Camera + Mic)"],
            horizontal=True
        )
        
        st.markdown("---")
        
        # ═══════════════════════════════════════════════════════════════
        # 📱 MOBILE PRACTICE MODE
        # ═══════════════════════════════════════════════════════════════
        if voice_mode == "📱 Mobile (Camera + Mic)":
            st.markdown("### 📱 MOBILE PRACTICE STUDIO")
            st.caption("OPTIMIZED: Large buttons, camera/mic access, quick drills.")
            
            # QUICK DRILL SELECTOR (Large Touch Buttons)
            st.markdown("#### 🎯 SELECT DRILL")
            
            mobile_drills = [
                ("🎤 Elevator Pitch", "Tell me about yourself in 60 seconds"),
                ("💰 Why You?", "What makes you unique vs other candidates?"),
                ("📊 160% Growth", "Walk me through your biggest achievement"),
                ("🛡️ Weakness", "What's your greatest weakness?"),
                ("❓ Questions", "What questions do you have for us?")
            ]
            
            # Create 2x3 grid of large buttons
            drill_cols = st.columns(2)
            selected_mobile_drill = None
            
            for i, (emoji_title, question) in enumerate(mobile_drills):
                with drill_cols[i % 2]:
                    if st.button(emoji_title, use_container_width=True, key=f"mobile_drill_{i}"):
                        st.session_state['mobile_drill'] = question
                        st.toast(f"Drill loaded: {question}", icon="🎯")
            
            # Show selected drill
            if st.session_state.get('mobile_drill'):
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(255,191,0,0.1), rgba(255,215,0,0.05)); 
                            border: 2px solid #FFD700; border-radius: 16px; padding: 20px; margin: 16px 0; text-align: center;">
                    <p style="color: #8892b0; margin: 0 0 8px 0; font-size: 0.9rem;">CURRENT DRILL</p>
                    <h3 style="color: #FFBF00; margin: 0;">{st.session_state['mobile_drill']}</h3>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # CAMERA INPUT (Video Practice)
            st.markdown("#### 📹 VIDEO PRACTICE (Check Presence)")
            st.caption("Record yourself to review body language, eye contact, and energy.")
            
            camera_input = st.camera_input("📷 Capture Practice Video", key="mobile_camera")
            
            if camera_input:
                st.success("✅ Video captured! Review your presence below.")
                st.image(camera_input, use_container_width=True)
                
                # Body Language Checklist
                st.markdown("##### ✅ PRESENCE CHECKLIST")
                bl_cols = st.columns(3)
                bl_cols[0].checkbox("👁️ Eye contact?")
                bl_cols[1].checkbox("😊 Smile/Energy?")
                bl_cols[2].checkbox("🖐️ Hand gestures?")
            
            st.markdown("---")
            
            # AUDIO INPUT (Voice Practice)  
            st.markdown("#### 🎤 VOICE PRACTICE (Record Answer)")
            st.caption("Record your response and get AI-powered transcription + analysis.")
            
            audio_input = st.audio_input("🎙️ Record Your Answer", key="mobile_audio")
            
            if audio_input:
                st.audio(audio_input)
                st.success("✅ Audio captured!")
                
                # WHISPER TRANSCRIPTION + ANALYSIS
                if st.button("🧠 TRANSCRIBE & ANALYZE", type="primary", use_container_width=True, key="mobile_analyze"):
                    
                    # Import Whisper module
                    try:
                        from logic.whisper_transcriber import get_transcriber, analyze_speech
                        transcriber = get_transcriber(st.session_state.get('groq_api_key'))
                        
                        if transcriber.is_available():
                            with st.spinner(f"🎙️ Transcribing via {transcriber.get_backend().upper()}..."):
                                # Transcribe
                                result = transcriber.transcribe(audio_input)
                                
                                if result.get("error"):
                                    st.error(f"Transcription error: {result['error']}")
                                else:
                                    transcript = result.get("text", "")
                                    
                                    # Analyze speech
                                    analysis = analyze_speech(transcript)
                                    
                                    # TRANSCRIPT DISPLAY
                                    st.markdown("##### 📝 TRANSCRIPT")
                                    st.text_area("Your Response:", transcript, height=150, disabled=True)
                                    
                                    # TELEMETRY DISPLAY
                                    st.markdown("##### 📊 VOICE TELEMETRY")
                                    
                                    t_cols = st.columns(4)
                                    t_cols[0].metric("📝 WORDS", analysis['word_count'], "Target: 150-250")
                                    t_cols[1].metric("🚫 FILLERS", analysis['filler_count'], "Target: <3")
                                    t_cols[2].metric("📊 METRICS", "✅" if analysis['has_metric'] else "❌", "Use numbers!")
                                    t_cols[3].metric("💪 POWER", analysis['power_score'], "Target: 3+")
                                    
                                    # Progress bars
                                    st.markdown("---")
                                    
                                    # Filler Alert
                                    if analysis['filler_words']:
                                        st.warning(f"🚫 **Filler words detected:** {', '.join(set(analysis['filler_words']))}")
                                    
                                    # Power words celebration
                                    if analysis['power_words']:
                                        st.success(f"💪 **Power words used:** {', '.join(set(analysis['power_words']))}")
                                    
                                    # Metrics found
                                    if analysis['metrics_found']:
                                        st.info(f"📊 **Metrics mentioned:** {', '.join(analysis['metrics_found'])}")
                                    
                                    # Save to session state for history
                                    if 'voice_sessions' not in st.session_state:
                                        st.session_state['voice_sessions'] = []
                                    
                                    st.session_state['voice_sessions'].append({
                                        'drill': st.session_state.get('mobile_drill', 'Mobile Practice'),
                                        'transcript': transcript,
                                        'words': analysis['word_count'],
                                        'fillers': analysis['filler_count'],
                                        'has_metric': analysis['has_metric'],
                                        'wpm': 0,
                                        'score': analysis['power_score']
                                    })
                                    
                                    st.toast("📈 Session saved to history!", icon="✅")
                                    
                                    # AI COACHING
                                    st.markdown("---")
                                    st.markdown("##### 🤖 AI COACH FEEDBACK")
                                    
                                    with st.spinner("Getting personalized feedback..."):
                                        from logic.generator import generate_plain_text
                                        
                                        feedback_prompt = f"""
                                        You are an elite interview coach for Director-level GTM roles ($200k+).
                                        
                                        QUESTION: "{st.session_state.get('mobile_drill', 'Tell me about yourself')}"
                                        
                                        CANDIDATE'S RESPONSE (transcribed):
                                        "{transcript}"
                                        
                                        TELEMETRY:
                                        - Word count: {analysis['word_count']}
                                        - Filler words: {analysis['filler_count']} ({', '.join(analysis['filler_words']) if analysis['filler_words'] else 'None'})
                                        - Metrics used: {analysis['has_metric']} ({', '.join(analysis['metrics_found']) if analysis['metrics_found'] else 'None'})
                                        - Power words: {', '.join(analysis['power_words']) if analysis['power_words'] else 'None'}
                                        
                                        Provide:
                                        1. 📊 **Score (1-10)** with brief justification
                                        2. ✅ **What worked** (1 thing)
                                        3. 🔧 **What to improve** (1 thing)
                                        4. 🎯 **Power phrase** to add next time
                                        
                                        Be specific to THEIR response. Not generic advice.
                                        """
                                        
                                        model_id = st.session_state.get('selected_model_id', "llama-3.3-70b-versatile")
                                        feedback = generate_plain_text(feedback_prompt, model_name=model_id)
                                        
                                        st.markdown(feedback)
                        else:
                            st.warning("⚠️ Whisper not available. Using AI estimation...")
                            # Fallback to original behavior
                            from logic.generator import generate_plain_text
                            
                            feedback_prompt = f"""
                            You are a professional interview coach.
                            The candidate just practiced answering: "{st.session_state.get('mobile_drill', 'Tell me about yourself')}"
                            
                            Give quick feedback (3 bullet points max):
                            1. What they likely did well
                            2. One area to improve
                            3. A power phrase to use next time
                            
                            Keep it short and actionable.
                            """
                            model_id = st.session_state.get('selected_model_id', "llama-3.3-70b-versatile")
                            feedback = generate_plain_text(feedback_prompt, model_name=model_id)
                            
                            st.markdown("##### 💡 COACH FEEDBACK")
                            st.success(feedback)
                    
                    except ImportError as e:
                        st.error(f"Module not found: {e}. Using fallback.")
                        # Fallback
                        from logic.generator import generate_plain_text
                        feedback_prompt = f"Give interview feedback for answering: {st.session_state.get('mobile_drill', 'Tell me about yourself')}"
                        feedback = generate_plain_text(feedback_prompt, model_name="llama-3.3-70b-versatile")
                        st.markdown(feedback)
            
            st.markdown("---")
            
            # QUICK OBJECTION CARDS (One-Tap Answers)
            st.markdown("#### 🛡️ QUICK OBJECTION CARDS")
            st.caption("One-tap answers during live calls.")
            
            objections = [
                ("💰 Too Expensive", "I understand budget is a concern. Let me ask—what's the cost of NOT solving this problem for another quarter?"),
                ("⏰ Not Now", "I hear you. When would be the right time to revisit? I want to make sure I'm adding value, not pressure."),
                ("🤔 Need to Think", "Totally fair. What specific concerns are top of mind so I can address them now or in a follow-up?"),
                ("👥 Talk to Team", "Great idea. Would it help if I joined that conversation to answer technical questions directly?"),
            ]
            
            for obj_title, obj_answer in objections:
                with st.expander(obj_title):
                    st.markdown(f"**Response:** {obj_answer}")
                    st.markdown(f"""
                    <button onclick="navigator.clipboard.writeText('{obj_answer}')" 
                            style="background: #FFBF00; color: black; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; width: 100%;">
                        📋 COPY
                    </button>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # PRACTICE TIMER
            st.markdown("#### ⏱️ PRACTICE TIMER")
            timer_cols = st.columns(3)
            if timer_cols[0].button("30 SEC", use_container_width=True, key="timer_30"):
                st.toast("⏱️ 30 second timer started!", icon="⏱️")
            if timer_cols[1].button("60 SEC", use_container_width=True, key="timer_60"):
                st.toast("⏱️ 60 second timer started!", icon="⏱️")
            if timer_cols[2].button("2 MIN", use_container_width=True, key="timer_120"):
                st.toast("⏱️ 2 minute timer started!", icon="⏱️")
        
        # ═══════════════════════════════════════════════════════════════
        # 🖥️ DESKTOP MODE (Full Lab) - Original Code
        # ═══════════════════════════════════════════════════════════════
        else:
            # 1. DRILL SETUP
            col1, col2 = st.columns([2, 1])
        with col1:
            drill_category = st.selectbox("QUESTION CATEGORY", [
                "🎯 Core Pitch",
                "💼 Behavioral (STAR)",
                "📈 Sales-Specific",
                "👔 Leadership",
                "🧠 Situational",
                "⚡ Rapid Fire"
            ])
            
            # 2024/2025 Top Interview Questions by Category
            drill_options = {
                "🎯 Core Pitch": [
                    "Tell me about yourself (The Pitch)",
                    "Walk me through your resume",
                    "Why are you interested in this role?",
                    "What makes you unique vs. other candidates?",
                    "Walk me through the 160% Growth metric",
                    "Where do you see yourself in 5 years?"
                ],
                "💼 Behavioral (STAR)": [
                    "Describe a time you built a system from scratch",
                    "Tell me about a time you failed",
                    "Describe your biggest professional achievement",
                    "Tell me about a conflict with a coworker",
                    "When did you go above and beyond?",
                    "Describe a time you had to learn quickly"
                ],
                "📈 Sales-Specific": [
                    "Walk me through your sales process",
                    "How do you handle a lost deal?",
                    "Tell me about your biggest closed deal",
                    "How do you prospect and build pipeline?",
                    "How do you handle price objections?",
                    "What's your approach to discovery calls?"
                ],
                "👔 Leadership": [
                    "What's your management philosophy?",
                    "How do you motivate underperformers?",
                    "Describe your leadership style",
                    "How do you build team culture?",
                    "Tell me about a time you coached someone"
                ],
                "🧠 Situational": [
                    "Handle Objection: 'You are too expensive'",
                    "Handle Objection: 'We're happy with current vendor'",
                    "Handle: 'Why should we hire you over others?'",
                    "Handle: 'You lack industry experience'",
                    "Why did you leave your last role?"
                ],
                "⚡ Rapid Fire": [
                    "Salary expectations?",
                    "Why this company?",
                    "What's your greatest weakness?",
                    "What questions do you have for us?",
                    "When can you start?"
                ]
            }
            
            target_drill = st.selectbox("SELECT DRILL SCENARIO", drill_options.get(drill_category, drill_options["🎯 Core Pitch"]))
        
        with col2:
            st.info("💡 **TIP:** Speak for 45-90 seconds. Include at least one metric.")

        st.markdown(f"### 🗣️ QUESTION: *{target_drill}*")
        st.markdown("---")
        
        # 2. NATIVE RECORDING INTERFACE (CLOUD COMPATIBLE)
        st.markdown("#### 🔴 RECORD YOUR ANSWER")
        st.caption("Click the microphone below to start recording. Works on all devices.")
        
        audio_value = st.audio_input("Press to record your response")
        
        if audio_value:
            st.success("✅ Audio Captured. Processing...")
            
            # 3. TRANSCRIPTION ENGINE (GROQ WHISPER)
            api_key = st.session_state.get('groq_api_key')
            
            if api_key:
                try:
                    from groq import Groq
                    client = Groq(api_key=api_key)
                    
                    with st.spinner("🧠 Transcribing via Groq Whisper..."):
                        transcription = client.audio.transcriptions.create(
                            file=("response.wav", audio_value, "audio/wav"),
                            model="whisper-large-v3",
                            response_format="text"
                        )
                        transcript_text = transcription
                    
                    # 4. TELEMETRY ANALYSIS
                    words = len(transcript_text.split())
                    
                    # Filler Word Scan
                    fillers = ['um', 'uh', 'like', 'you know', 'sort of', 'kind of', 'basically']
                    filler_count = sum(transcript_text.lower().count(f) for f in fillers)
                    
                    # Metric Detection
                    has_metric = any(char.isdigit() for char in transcript_text) or '$' in transcript_text or '%' in transcript_text
                    
                    # Estimate WPM (assuming average 60-90 seconds for a typical response)
                    # A rough estimate: 150 words/minute is average speaking speed.
                    # If we assume a 60-second response, WPM = words.
                    # For a more robust calculation, one would need actual duration.
                    # For now, let's assume a target duration of 60 seconds for WPM calculation.
                    wpm = words # Simplified for now, as actual duration is not available from st.audio_input
                    if words > 0:
                        # If we want to be more accurate, we'd need the audio duration.
                        # For a text_area, we can't get duration. Let's assume a 60-second target.
                        # If the user speaks 150 words, WPM is 150. If 75 words, WPM is 75.
                        # This is a placeholder.
                        pass
                    
                    # ═══════════════════════════════════════════════════════════════
                    # FRAMEWORK SELECTOR (4 PROVEN METHODS)
                    # ═══════════════════════════════════════════════════════════════
                    framework = st.radio("🧠 Framework Strategy", 
                        ["STAR (Behavioral)", "SOAR (Strategic)", "CIRCLE (System Design)", "PREP (Opinion/Rapid)"], 
                        horizontal=True, 
                        help="STAR: Situation-Task-Action-Result (Standard)\nSOAR: Situation-Obstacle-Action-Result (Strategic)\nCIRCLE: Context-Implication-Result-Complexity-Leadership-Execution (Systems)\nPREP: Point-Reason-Example-Point (Direct/Rapid)"
                    )
                    
                    # Keyword Scan (Multi-Model)
                    if "STAR" in framework:
                        target_keywords = ["situation", "task", "action", "result", "because"]
                        k4_label = "STAR SIGNAL"
                    elif "SOAR" in framework:
                        target_keywords = ["obstacle", "challenge", "pivot", "strategy", "impact"]
                        k4_label = "SOAR SIGNAL"
                    elif "CIRCLE" in framework:
                        target_keywords = ["context", "implication", "complexity", "leadership", "execution", "trade-off", "system"]
                        k4_label = "CIRCLE SIGNAL"
                    elif "PREP" in framework:
                        target_keywords = ["point", "reason", "example", "therefore", "believe", "experience"]
                        k4_label = "PREP SIGNAL"
                        
                    framework_hits = sum(1 for word in transcript_text.lower().split() if word in target_keywords)

                    # 5. THE SCOREBOARD
                    st.markdown("### 📊 PERFORMANCE TELEMETRY")
                    
                    k1, k2, k3, k4 = st.columns(4)
                    k1.metric("WPM", wpm, "Target: 130-150")
                    k2.metric("FILLERS", filler_count, "Target: <3")
                    k3.metric("METRICS", "✅ Detected" if has_metric else "❌ Missing", "Use #s")
                    k4.metric(k4_label, framework_hits, "Target: 3+")
                    
                    st.divider()

                    # ═══════════════════════════════════════════════════════════════
                    # AI COACHING FEEDBACK
                    # ═══════════════════════════════════════════════════════════════
                    st.markdown("#### 🤖 AI COACHING FEEDBACK")
                    
                    if st.button("🧠 ANALYZE RESPONSE"):
                        from logic.generator import generate_plain_text
                        
                        prompt = f"""
                        Analyze this interview response for a Director of GTM Systems role ($220k OTE).
                        
                        Question: {target_drill}
                        Transcript: "{transcript_text}"
                        
                        Framework Selected: {framework}
                        
                        Provide:
                        1. 📊 **Score (1-10)**: Based on clarity, confidence, and metric usage.
                        2. 🛠️ **Structure Check**: Did they follow the {framework} format?
                        3. 🚀 **Key Improvement**: One specific thing to change to sound more senior.
                        
                        Keep it brief and punchy.
                        """
                        model_id = st.session_state.get('selected_model_id', 'llama-3.3-70b-versatile')
                        feedback = generate_plain_text(prompt, model_name=model_id)
                        st.info(feedback)
                        
                        if filler_count > 3:
                            st.warning("⚠️ **HIGH FILLER COUNT:** Too many 'um's and 'uh's. Practice pausing instead.")
                        
                        if not has_metric:
                            st.error("🚨 **MISSING METRICS:** You didn't cite any numbers. Always include the '160%' or '$10M' figure.")

                        if framework_hits < 3:
                            if "STAR" in framework:
                                st.info("💡 **STRUCTURE TIP:** Use more STAR keywords (Situation, Task, Action, Result).")
                            elif "SOAR" in framework:
                                st.info("💡 **STRATEGY TIP:** Highlight the OBSTACLE and your strategic ACTION (SOAR method).")
                            elif "CIRCLE" in framework:
                                st.info("💡 **SYSTEMS TIP:** Define the CONTEXT and IMPLICATION before jumping to execution (CIRCLE method).")
                            elif "PREP" in framework:
                                st.info("💡 **CLARITY TIP:** Start with your POINT, give a REASON, share an EXAMPLE, and restate the POINT (PREP).")
                        
                        if has_metric and filler_count <= 3 and framework_hits >= 3:
                            st.success("🏆 **EXECUTIVE PRESENCE:** Strong data utilization and structured delivery!")
                            st.balloons()
                    
                    st.markdown("---")
                    
                    # ═══════════════════════════════════════════════════════════════
                    # NEW: AI-GENERATED IDEAL ANSWER (BEST OF THE BEST)
                    # ═══════════════════════════════════════════════════════════════
                    st.markdown("#### 🤖 AI-GENERATED IDEAL ANSWER")
                    st.caption(f"See how an executive would answer using the **{framework}** method:")
                    
                    if st.button("🧠 GENERATE IDEAL ANSWER", type="primary"):
                        from logic.generator import generate_plain_text
                        
                        ideal_prompt = f"""
                        You are a Director-level GTM executive interviewing for a $200k+ role.
                        
                        Question: {target_drill}
                        
                        Generate the IDEAL 60-second answer that includes:
                        1. A strong opening hook (first 10 seconds)
                        2. A specific metric or quantified result
                        3. A clear story structure ({framework} method)
                        4. A confident close that ties to the role
                        
                        Use these real examples from your background:
                        - 160% YoY pipeline growth at Fudo Security
                        - $10M pipeline built at Sense
                        - Partner Revenue OS that reduced CAC by 40%
                        
                        Keep it conversational, not scripted. Max 200 words.
                        """
                        
                        model_id = st.session_state.get('selected_model_id', 'llama-3.3-70b-versatile')
                        ideal_answer = generate_plain_text(ideal_prompt, model_name=model_id)
                        
                        st.session_state['ideal_answer'] = ideal_answer
                    
                    if st.session_state.get('ideal_answer'):
                        st.success(st.session_state['ideal_answer'])
                        
                        # Compare side-by-side
                        st.markdown("---")
                        st.markdown("#### 📊 SIDE-BY-SIDE COMPARISON")
                        comp_col1, comp_col2 = st.columns(2)
                        with comp_col1:
                            st.markdown("**YOUR ANSWER:**")
                            st.text(transcript_text[:300] + "..." if len(transcript_text) > 300 else transcript_text)
                        with comp_col2:
                            st.markdown("**IDEAL ANSWER:**")
                            st.text(st.session_state['ideal_answer'][:300] + "..." if len(st.session_state['ideal_answer']) > 300 else st.session_state['ideal_answer'])
                    
                    # Save to Session History
                    if 'voice_sessions' not in st.session_state:
                        st.session_state['voice_sessions'] = []
                    
                    st.session_state['voice_sessions'].append({
                        'drill': target_drill,
                        'words': words,
                        'fillers': filler_count,
                        'has_metric': has_metric,
                        'structure_score': framework_hits,
                        'framework': framework,
                        'transcript': transcript_text[:500]
                    })
                    
                    st.toast(f"📈 Session saved! Total: {len(st.session_state['voice_sessions'])} sessions")
                        
                except Exception as e:
                    st.error(f"Transcription Error: {e}")
                    st.caption("Check your Groq API key in the sidebar.")
            else:
                st.warning("⚠️ Enter your **Groq API Key** in the sidebar to enable voice transcription.")
                st.caption("Get a free key at [console.groq.com](https://console.groq.com)")
        
        # Session History
        if st.session_state.get('voice_sessions'):
            st.markdown("---")
            with st.expander(f"📜 SESSION HISTORY ({len(st.session_state['voice_sessions'])} sessions)"):
                for i, session in enumerate(reversed(st.session_state['voice_sessions'][-5:])):
                    st.markdown(f"**Session {len(st.session_state['voice_sessions']) - i}:** {session['drill']}")
                    st.caption(f"Words: {session['words']} | Fillers: {session['fillers']} | Metrics: {'✅' if session['has_metric'] else '❌'}")
                    st.markdown("---")
                
                # EXPORT SESSION HISTORY
                st.markdown("##### 📥 EXPORT TRAINING LOG")
                
                # Build export content
                export_lines = ["# BASIN::NEXUS Voice Training Log\n", f"**Total Sessions:** {len(st.session_state['voice_sessions'])}\n\n"]
                export_lines.append("---\n\n")
                
                for i, session in enumerate(st.session_state['voice_sessions']):
                    export_lines.append(f"## Session {i+1}: {session['drill']}\n")
                    export_lines.append(f"- **Word Count:** {session['words']}\n")
                    export_lines.append(f"- **Filler Words:** {session['fillers']}\n")
                    export_lines.append(f"- **Used Metrics:** {'Yes' if session['has_metric'] else 'No'}\n")
                    if session.get('transcript'):
                        export_lines.append(f"- **Transcript:** {session['transcript'][:200]}...\n")
                    export_lines.append("\n---\n\n")
                
                export_content = "".join(export_lines)
                
                st.download_button(
                    label="📄 DOWNLOAD TRAINING LOG (MD)",
                    data=export_content,
                    file_name="basin_nexus_voice_training_log.md",
                    mime="text/markdown",
                    use_container_width=True
                )
    
    # ─────────────────────────────────────────────────────────────
    # VIDEO MODE - THE GAME CHANGER
    # ─────────────────────────────────────────────────────────────

    # ==============================================================================
    # 🥊 MODE 7: BOARDROOM (SWARM SYNTHESIS) - FINAL ARCHITECTURE
    # ==============================================================================
    # ==============================================================================
    # 🥊 MODE 5: BOARDROOM SIMULATOR v2.0 (THE NEURAL DOJO)
    # ==============================================================================
    elif input_mode == "🥊 Practice (Dojo)":
        st.markdown("## ▲ BOARDROOM SIMULATOR v2.0")
        st.caption("PROTOCOL: High-Fidelity Company Simulation & Speech Telemetry.")
        
        # 1. MISSION CONFIGURATION
        c1, c2, c3 = st.columns(3)
        with c1:
            target_company = st.selectbox("🎯 TARGET LOCK", 
                ["NVIDIA (AI/Arch)", "LinkedIn (Values)", "eBay (Scale/Ops)", "Generic Series B"],
                help="Configures the AI's personality and question logic.")
        with c2:
            # SHADOW CABINET PERSONAS
            interviewer_style = st.selectbox("🗣️ SHADOW CABINET", 
                [
                    "👔 Marcus (The CRO) - Revenue & Forecasts",
                    "💰 Sarah (The VC) - Metrics & Unit Economics", 
                    "🦄 David (The Visionary) - Strategy & Scale",
                    "⚙️ Alex (The CTO) - Systems & Data",
                    "🤝 Elena (The People Leader) - Culture & Conflict"
                ])
        with c3:
            artifact_focus = st.selectbox("📂 ARTIFACT DEFENSE", 
                ["160% Pipeline Growth", "Revenue OS Architecture", "Leadership/Management", "General Background"])

        # 2. THE SIMULATION LOOP
        st.markdown("---")
        
        b1, b2 = st.columns(2)
        
        # ACTION 1: SIMULATION (Drilling)
        with b1:
            if st.button("🔴 INITIATE INTERVIEW SIM", type="primary", use_container_width=True):
                with st.spinner(f"Summoning {interviewer_style}..."):
                    from logic.generator import generate_plain_text
                    
                    # Persona Logic
                    persona_prompt = ""
                    if "Marcus" in interviewer_style:
                        persona_prompt = "You are Marcus, a ruthless CRO. You care ONLY about forecast accuracy, pipeline velocity, and revenue predictability. You hate fluff. You want numbers."
                    elif "Sarah" in interviewer_style:
                        persona_prompt = "You are Sarah, a Sequoia Partner. You care about CAC, LTV, Magic Number, and Scalability. You want to know if this person understands the business model."
                    elif "David" in interviewer_style:
                        persona_prompt = "You are David, a Visionary Founder. You care about the 'Why', the 10x thinking, and the narrative. You want to be inspired."
                    elif "Alex" in interviewer_style:
                        persona_prompt = "You are Alex, a skeptical CTO. You care about how the systems actually work, data integrity, and API integrations. You smell BS instantly."
                    elif "Elena" in interviewer_style:
                        persona_prompt = "You are Elena, a VP of People. You care about EQ, conflict resolution, diversity, and how this person leads teams. You hate toxicity."

                    # Company Context
                    company_context = ""
                    if "NVIDIA" in target_company:
                        company_context = "Context: NVIDIA (First Principles, Speed, Innovation)."
                    elif "LinkedIn" in target_company:
                        company_context = "Context: LinkedIn (Economic Graph, Members First, Collaboration)."
                    
                    # Generate the Question
                    q_prompt = f"""
                    ACT AS: {persona_prompt}
                    TARGET COMPANY: {target_company}.
                    {company_context}
                    CANDIDATE CLAIM: {artifact_focus} (Leon Basin).
                    
                    TASK: Ask ONE challenging, open-ended question to stress-test this claim. Stay in character (Marcus/Sarah/David/Alex/Elena).
                    """
                    
                    model_id = st.session_state.get('selected_model_id', "llama-3.3-70b-versatile")
                    st.session_state['current_q'] = generate_plain_text(q_prompt, model_name=model_id)
                    st.session_state['sim_active'] = True
                    st.session_state['sim_mode'] = "interview"

        # ACTION 2: COLLABORATION (Brainstorming)
        with b2:
            if st.button("🔵 COLLABORATE / STRATEGY", use_container_width=True):
                with st.spinner(f"Brainstorming with {interviewer_style}..."):
                    from logic.generator import generate_plain_text
                    
                    # Persona Logic (Helper Mode)
                    persona_prompt = "You are a helpful, brilliant strategic advisor."
                    if "Marcus" in interviewer_style:
                        persona_prompt = "You are Marcus, a seasoned CRO mentor. You want to help Leon build a bulletproof revenue engine."
                    elif "Sarah" in interviewer_style:
                        persona_prompt = "You are Sarah, a VC mentor. You want to help Leon frame his story for investors and board members."
                    
                    q_prompt = f"""
                    ACT AS: {persona_prompt}
                    TOPIC: {artifact_focus}
                    
                    TASK: Provide 3 strategic bullet points on how Leon should position this topic to impress a hiring manager at {target_company}.
                    Be constructive and collaborative.
                    """
                    
                    model_id = st.session_state.get('selected_model_id', "llama-3.3-70b-versatile")
                    st.session_state['current_q'] = generate_plain_text(q_prompt, model_name=model_id)
                    st.session_state['sim_active'] = True
                    st.session_state['sim_mode'] = "collaborate"

        # 3. INTERACTION LAYER
        if st.session_state.get('sim_active'):
            # A. THE QUESTION
            st.info(f"🗣️ **INTERVIEWER:** {st.session_state['current_q']}")
            
            # Audio Playback (Text-to-Speech)
            try:
                from gtts import gTTS
                from io import BytesIO
                tts = gTTS(st.session_state['current_q'], lang='en', tld='us') # 'us' accent
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                st.audio(audio_bytes, format='audio/mp3')
            except ImportError:
                st.warning("⚠️ Install 'gTTS' (`pip install gTTS`) to hear the interviewer speak.")
            except Exception as e:
                st.caption(f"Audio generation skipped: {str(e)}")

            # B. THE RESPONSE (Voice Input Simulation)
            st.markdown("#### 🎙️ YOUR INPUT")
            
            sim_mode = st.session_state.get('sim_mode', 'interview')
            input_placeholder = "[ Speak Answer Here ]" if sim_mode == "interview" else "[ Ask follow up question or refine strategy ]"
            
            st.caption(f"Instructions: Use your system's dictation tool (Fn+Fn on Mac) to speak into the box below. Mode: **{sim_mode.upper()}**")
            user_transcript = st.text_area("Transcript Input", height=200, placeholder=input_placeholder)

            # C. SPEECH TELEMETRY ENGINE
            btn_label = "🛑 END & ANALYZE PERFORMANCE" if sim_mode == "interview" else "🛑 FINALIZE STRATEGY"
            
            if st.button(btn_label, use_container_width=True):
                if user_transcript:
                    with st.spinner("PROCESSING..."):
                        from logic.generator import generate_plain_text
                        
                        # 1. LOGIC: WPM CALCULATION
                        word_count = len(user_transcript.split())
                        # Assuming average answer time is 90 seconds for a text block of this size
                        est_wpm = int(word_count / 1.5) 
                        
                        # 2. LOGIC: FILLER WORD SCAN
                        fillers = ['um', 'uh', 'like', 'you know', 'sort of', 'kind of', 'basically']
                        filler_count = sum(user_transcript.lower().count(f) for f in fillers)
                        filler_density = (filler_count / word_count) * 100 if word_count > 0 else 0
                        
                        # 3. LLM: CONTENT ANALYSIS
                        if sim_mode == "interview":
                            analysis_prompt = f"""
                            ACT AS: Executive Communication Coach.
                            CONTEXT: Company: {target_company}. Question: {st.session_state['current_q']}.
                            TRANSCRIPT: "{user_transcript}"
                            
                            METRICS:
                            - WPM: {est_wpm} (Target: 130-150)
                            - Filler Density: {filler_density:.1f}% (Target: < 3%)
                            
                            TASK:
                            1. Grade the answer (A-F) based on {target_company} culture.
                            2. Did they mention the "160% Growth" or "$10M" metric?
                            3. Rewrite the "Hook" (First 2 sentences) to be 2x more executive.
                            """
                        else:
                            # COLLABORATION MODE
                            analysis_prompt = f"""
                            ACT AS: Strategic Advisor ({interviewer_style}).
                            CONTEXT: We are brainstorming strategy for {target_company}.
                            MY INPUT/FOLLOW UP: "{user_transcript}"
                            PREVIOUS ADVICE: {st.session_state['current_q']}
                            
                            TASK:
                            1. Refine the strategy based on my input.
                            2. Provide a concrete "Next Step" or "Action Item".
                            3. Draft a short email snippet I could send to {target_company} regarding this topic.
                            """
                        
                        # Use existing generator function
                        model_id = st.session_state.get('selected_model_id', "llama-3.3-70b-versatile")
                        feedback = generate_plain_text(analysis_prompt, model_name=model_id)
                        
                        # D. THE SCOREBOARD
                        st.markdown("### 📊 TELEMETRY REPORT")
                        
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("WORD COUNT", word_count)
                        m2.metric("PACE (Est. WPM)", est_wpm, "Target: 140")
                        m3.metric("FILLER WORDS", filler_count, "Target: 0", delta_color="inverse")
                        m4.metric("METRIC DENSITY", "High" if "$" in user_transcript or "%" in user_transcript else "Low", "Critical")
                        
                        st.success("✅ ANALYSIS COMPLETE")
                        st.markdown(feedback)
                        
                        # Gamification Update
                        st.toast(f"📈 +50 XP GAINED: {target_company} SIMULATION")
                        
                        # Mentor Export (Collaboration Mode Only)
                        if sim_mode == "collaborate":
                            st.markdown("---")
                            st.caption("📤 TAKE ACTION: SHARE WITH MENTOR")
                            if st.button("📧 DRAFT EMAIL TO MENTOR"):
                                email_body = f"""Hi [Mentor Name],

I was brainstorming GTM strategy for {target_company} regarding {artifact_focus} and would love your gut check.

Here is the approach I'm considering:
--------------------------------------------------
{feedback}
--------------------------------------------------

Does this align with what you're seeing in the market?

Best,
Leon"""
                                st.code(email_body, language="text")
                                st.success("📋 Copied to clipboard logic (Manual Copy for now)")

                else:
                    st.error("⚠️ No audio transcript detected. Speak your answer!")

    # ─────────────────────────────────────────────────────────────
    # FIRST 90 DAYS MODE (THE CLOSER)
    # ─────────────────────────────────────────────────────────────
    elif input_mode == "🚀 First 90 Days":
        st.markdown("#### �️ 30-60-90 DAY EXECUTION ARCHITECT")
        st.caption("Generate the document that wins the final interview.")
        
        jd_context = st.text_area(
            "Paste Job Description", 
            value=st.session_state.get('jd_text', ""),
            height=200,
            placeholder="Paste the JD here to generate an execution plan..."
        )
        
        if st.button("🚀 GENERATE EXECUTION PLAN", type="primary", use_container_width=True):
            if jd_context:
                from logic.generator import generate_plain_text
                
                with st.spinner("Architecting the First 90 Days..."):
                    prompt = f"""
                    ACT AS: Leon Basin, Director of GTM Systems.
                    CONTEXT: Job Description: {jd_context}
                    
                    MISSION: Create a high-level 30-60-90 Day Plan to present in a Final Interview.
                    
                    TONE: "I am not figuring it out; I am executing."
                    
                    OUTPUT MARKDOWN FORMAT:
                    
                    # 🏗️ GTM EXECUTION ARCHITECTURE (DRAFT)
                    
                    ### 🗓️ DAYS 1-30: THE AUDIT (Discover & Diagnose)
                    - (3 Bullet points on what systems/people Leon will audit. Be specific to GTM Ops).
                    
                    ### 🗓️ DAYS 31-60: THE BUILD (Architect & Deploy)
                    - (3 Bullet points on "Quick Wins" and System Deployments - e.g., CRM Fixes, Outbound Signals).
                    
                    ### 🗓️ DAYS 61-90: THE SCALE (Optimize & Expand)
                    - (3 Bullet points on Training, Handoffs, and Revenue Impact).
                    
                    ### 🏆 THE IMPACT (Day 90 KPI)
                    - Define one major outcome (e.g., "Full Pipeline Visibility" or "20% Efficiency Gain").
                    """
                    plan = generate_plain_text(prompt, model_name=st.session_state.get('selected_model_id', 'llama-3.3-70b-versatile'))
                    st.session_state['90_day_plan'] = plan
            else:
                st.error("Please paste a JD.")
                
        if st.session_state.get('90_day_plan'):
            st.markdown("---")
            st.markdown(st.session_state['90_day_plan'])
            st.download_button("📥 Download Plan", st.session_state['90_day_plan'], "30_60_90_Plan.md")

    # ==============================================================================
    # 💰 MODE: NEGOTIATION (THE CLOSER - $200k+)
    # ==============================================================================
    elif input_mode == "💰 Negotiation":
        st.markdown("## 💰 COMPENSATION ARCHITECT")
        st.caption("PROTOCOL: Maximize OTE, Equity, and Sign-On for $200k+ Director roles.")
        
        st.markdown("---")
        
        # 1. THE OFFER INPUT
        st.markdown("### 📊 CURRENT OFFER BREAKDOWN")
        
        c1, c2 = st.columns(2)
        with c1:
            base_offer = st.number_input("Base Salary ($)", value=180000, step=5000, format="%d")
            variable_offer = st.number_input("Variable/Bonus ($)", value=40000, step=5000, format="%d")
        with c2:
            equity_val = st.number_input("Equity Value ($/yr)", value=20000, step=5000, format="%d")
            sign_on = st.number_input("Sign-On Bonus ($)", value=0, step=5000, format="%d")

        total_comp = base_offer + variable_offer + equity_val + sign_on
        target_comp = 240000  # Your $240k Goal
        gap = total_comp - target_comp

        # Metrics Display
        m1, m2, m3 = st.columns(3)
        m1.metric("TOTAL COMPENSATION", f"${total_comp:,}")
        m2.metric("TARGET OTE", f"${target_comp:,}")
        if gap >= 0:
            m3.metric("STATUS", "✅ ON TARGET", f"+${gap:,}")
        else:
            m3.metric("NEGOTIATION GAP", f"${abs(gap):,}", "Action Required", delta_color="inverse")
        
        st.markdown("---")
        
        # 2. COUNTER-OFFER SCRIPT GENERATOR
        st.markdown("### 🗣️ COUNTER-OFFER SCRIPTS")
        
        scenario = st.selectbox("Select Negotiation Scenario:", [
            "Lowball Base Salary",
            "Equity Package Too Low",
            "Competing Offer Leverage",
            "Final Push (The 'Win-Win')",
            "Ask for Sign-On Bonus"
        ])

        if st.button("🎯 GENERATE SCRIPT", type="primary", use_container_width=True):
            st.markdown("---")
            
            if scenario == "Lowball Base Salary":
                st.info("**Strategy:** Pivot from 'Need' to 'Market Value' & 'ROI'")
                st.code(f'''
"I'm incredibly excited about this role and the team. 

Looking at the scope—specifically building the Revenue OS and architecting 
the Partner ecosystem—my research and current market data put the value 
for this impact at ${target_comp//1000}k OTE for Director-level positions.

We're currently at ${total_comp//1000}k. 

What levers can we explore on Base or Sign-On to bridge that ${abs(gap)//1000}k 
gap so we can finalize this week?"
''', language="text")
            
            elif scenario == "Equity Package Too Low":
                st.info("**Strategy:** Frame equity as 'Upside Alignment' with company success")
                st.code(f'''
"I'm fully committed to the long-term vision here. 

For a Director role where I'm architecting systems that directly impact 
revenue, I'd expect the equity component to reflect that upside potential.

Could we explore increasing the equity grant by 0.1-0.2% or adding 
performance-based accelerators tied to revenue milestones I achieve?"
''', language="text")
            
            elif scenario == "Competing Offer Leverage":
                st.info("**Strategy:** Create urgency without ultimatums")
                st.code(f'''
"To be transparent—I have another opportunity I'm considering that's 
at the ${target_comp//1000}k OTE level.

However, I'm genuinely more excited about your mission and team. 

If we can get closer to parity on compensation, I'm ready to commit 
and take the other option off the table today. What's possible?"
''', language="text")
            
            elif scenario == "Final Push (The 'Win-Win')":
                st.info("**Strategy:** Signal readiness to sign with specific ask")
                st.code(f'''
"Here's where I am: If we can get the Base to ${base_offer + 15000:,} 
and include a ${15000:,} sign-on to offset my current pipeline transition, 
I'm ready to sign the offer letter today and start Monday.

That's a total ask of ${30000:,}. Can we make that happen?"
''', language="text")
            
            elif scenario == "Ask for Sign-On Bonus":
                st.info("**Strategy:** Frame as 'transition bridge' not 'extra money'")
                st.code(f'''
"The base and variable are solid. One thing that would help close the loop: 
I'm walking away from some active opportunities and potential bonuses.

A sign-on of ${20000:,}-${30000:,} would bridge that transition and let me 
start with full focus on day one. Is that something we can add?"
''', language="text")
        
        st.markdown("---")
        
        # 3. MARKET DATA REFERENCE
        with st.expander("📈 MARKET COMP DATA (Levels.fyi Reference)"):
            st.markdown("""
            **Director of GTM Systems / Revenue Operations:**
            
            | Company Type | Base | Variable | Equity | Total Comp |
            |--------------|------|----------|--------|------------|
            | Series B/C Startup | $180-220k | $40-60k | $30-50k | $250-330k |
            | Growth Stage | $200-240k | $50-80k | $50-100k | $300-420k |
            | Public Tech | $220-280k | $60-100k | $100-200k | $380-580k |
            
            *Source: Levels.fyi, Glassdoor, LinkedIn Salary Insights (2024)*
            """)

    # ==============================================================================
    # 📈 MODE 8: PIPELINE CRM (DEAL TRACKER)
    elif input_mode == "📈 Pipeline CRM":
        st.markdown("## 📈 EXECUTIVE CRM (REVENUE COMMAND)")
        st.caption("PROTOCOL: Complete Contact & Deal Management with AI Enrichment.")
        
        # Initialize Contact Database with your actual data + Relationship Strength
        if 'crm_contacts' not in st.session_state:
            st.session_state['crm_contacts'] = [
                {"Name": "Samuel Burns", "Company": "DepthFirst", "Role": "GTM Lead", "Channel": "LinkedIn DM", "Status": "Warm", "Last Touch": "11/19", "Next Step": "Send resume summary", "Priority": "🔥 HIGH", "Strength": "🔗🔗🔗"},
                {"Name": "Cyrus Akrami", "Company": "DepthFirst", "Role": "CRO", "Channel": "Referral", "Status": "Not Contacted", "Last Touch": "N/A", "Next Step": "Wait for intro", "Priority": "🔥 HIGH", "Strength": "🔗"},
                {"Name": "Kayleigh", "Company": "Aikido Security", "Role": "Recruiter", "Channel": "Email + Referral", "Status": "Warm", "Last Touch": "11/15", "Next Step": "Follow-up", "Priority": "🔥 HIGH", "Strength": "🔗🔗🔗"},
                {"Name": "Justin Dedrickson", "Company": "Verkada", "Role": "Sr Sales Recruiter", "Channel": "LinkedIn DM", "Status": "Sent", "Last Touch": "11/18", "Next Step": "Follow-up 11/21", "Priority": "⚡ MED", "Strength": "🔗"},
                {"Name": "Nicole Ceranna", "Company": "Ambient.ai", "Role": "Recruiter", "Channel": "Direct", "Status": "Under Review (HM)", "Last Touch": "12/04", "Next Step": "Check for reply", "Priority": "🔥 HIGH", "Strength": "🔗🔗"},
                {"Name": "Virginia Bowers", "Company": "Sellers Hub", "Role": "Recruiter", "Channel": "Email", "Status": "Warm", "Last Touch": "11/03", "Next Step": "Follow-up", "Priority": "⚡ MED", "Strength": "🔗🔗🔗"},
                {"Name": "Kyu Kim", "Company": "Spray.io", "Role": "Founder", "Channel": "Slack", "Status": "Warm", "Last Touch": "11/17", "Next Step": "Scope doc", "Priority": "⚡ MED", "Strength": "🔗🔗🔗🔗"},
                {"Name": "Karan Shah", "Company": "SolveJet", "Role": "Founder", "Channel": "Slack", "Status": "Warm", "Last Touch": "11/17", "Next Step": "Review GTM proposal", "Priority": "⚡ MED", "Strength": "🔗🔗🔗🔗"},
                {"Name": "Asaph Wutawunashe", "Company": "FYM Partners", "Role": "Chairman", "Channel": "Direct", "Status": "Hot", "Last Touch": "11/18", "Next Step": "Deliver GTM system", "Priority": "🔥 HIGH", "Strength": "🔗🔗🔗🔗🔗"},
                {"Name": "Michael Rosenberg", "Company": "CRS Credit API", "Role": "Enterprise AE", "Channel": "Direct", "Status": "Interview Scheduled", "Last Touch": "12/05", "Next Step": "Prep for Interview", "Priority": "🔥 HIGH", "Strength": "🔗🔗"},
                {"Name": "Alex Rosen", "Company": "Sense", "Role": "Co-Founder", "Channel": "LinkedIn DM", "Status": "Outreach Sent", "Last Touch": "12/02", "Next Step": "Founder Network ask", "Priority": "⚡ MED", "Strength": "🔗"},
                {"Name": "Andon Cowie", "Company": "Nooks", "Role": "Head of Talent", "Channel": "LinkedIn DM", "Status": "Outreach Sent", "Last Touch": "12/02", "Next Step": "Check for reply", "Priority": "⚡ MED", "Strength": "🔗"},
                {"Name": "Alexandre Pereira", "Company": "2501.ai", "Role": "BD Director", "Channel": "Direct", "Status": "Outreach Sent", "Last Touch": "12/04", "Next Step": "Check for reply", "Priority": "🔥 HIGH", "Strength": "🔗🔗"},
                {"Name": "Ryan Freeman", "Company": "Deel", "Role": "Head of Partnerships", "Channel": "Direct", "Status": "Outreach Sent", "Last Touch": "12/04", "Next Step": "Check for reply", "Priority": "🔥 HIGH", "Strength": "🔗🔗"},
                {"Name": "Jaime Muirhead", "Company": "Skypoint", "Role": "CRO", "Channel": "LinkedIn DM", "Status": "Outreach Sent", "Last Touch": "12/04", "Next Step": "Monitor for Reply", "Priority": "🔥 HIGH", "Strength": "🔗"},
            ]
        
        # Initialize Deal Pipeline
        if 'crm_deals' not in st.session_state:
            st.session_state['crm_deals'] = [
                {"Company": "DepthFirst", "Role": "Account Executive", "Stage": "Intro Pending", "Priority": 1, "Signal": "Very High", "Notes": "CRO intro pending"},
                {"Company": "Aikido Security", "Role": "Account Executive US", "Stage": "Under Review", "Priority": 1, "Signal": "High", "Notes": "Top cybersecurity fit"},
                {"Company": "Mistral AI", "Role": "Account Executive US", "Stage": "Under Review", "Priority": 1, "Signal": "High", "Notes": "Tier 1 AI opportunity"},
                {"Company": "Ambient.ai", "Role": "Head of RevOps", "Stage": "Under Review (HM)", "Priority": 1, "Signal": "High", "Notes": "Recruiter forwarded to CFO"},
                {"Company": "CRS Credit API", "Role": "Enterprise AE", "Stage": "Interview Scheduled", "Priority": 1, "Signal": "High", "Notes": "Dec 5 @ 11:30 AM"},
                {"Company": "2501.ai", "Role": "BD Director", "Stage": "Outreach Sent", "Priority": 1, "Signal": "High", "Notes": "First US Hire opportunity"},
                {"Company": "Hightouch", "Role": "Mid Market AE West", "Stage": "Under Review", "Priority": 2, "Signal": "High", "Notes": "Strong AI + GTM match"},
                {"Company": "Spray.io", "Role": "Fractional GTM", "Stage": "Active", "Priority": 2, "Signal": "Medium", "Notes": "$1-2K/mo pilot"},
                {"Company": "SolveJet", "Role": "Fractional GTM", "Stage": "Active", "Priority": 2, "Signal": "Medium", "Notes": "$1.5-3K/mo pilot"},
                {"Company": "FYM Partners", "Role": "Portfolio GTM Provider", "Stage": "Active", "Priority": 1, "Signal": "Very High", "Notes": "$3-10K/mo retainer"},
            ]
        
        # CRM Tabs
        # CRM Tabs (Your Full Tab Structure) - Added NETWORK BUILDER + THE BLUEPRINT + CALENDAR + MARKET + NETWORKING
        crm_tab1, crm_tab2, crm_tab3, crm_tab4, crm_tab5, crm_tab6, crm_tab7, crm_tab8, crm_tab9, crm_tab10, crm_tab11 = st.tabs([
            "📋 DAILY BRIEFING", 
            "🔮 THE BLUEPRINT",
            "📅 CALENDAR",
            "📈 MARKET",
            "🤝 NETWORKING",
            "👤 CONTACTS", 
            "📈 DEALS", 
            "🔗 NETWORK BUILDER",
            "👥 RECRUITERS", 
            "🏢 ENRICH", 
            "📦 ARCHIVE"
        ])
        
        # ═══════════════════════════════════════════════════════════════
        # TAB: 🔮 THE BLUEPRINT (THE ARCHITECT'S FRAMEWORK)
        # ═══════════════════════════════════════════════════════════════
        with crm_tab2:
            st.markdown("## 🔮 THE ARCHITECT'S BLUEPRINT")
            st.caption("PROTOCOL: The 10 Pillars of manifestation. A framework as old as strategy itself.")
            
            # The 10 Pillars (Universal Archetypes)
            pillars = [
                {
                    "symbol": "◇",
                    "name": "THE CROWN",
                    "essence": "Pure Potential",
                    "career_stage": "Signed Offer",
                    "color": "#FFFFFF",
                    "glow": "rgba(255,255,255,0.5)",
                    "action": "Receive with gratitude. This is the moment intention becomes reality.",
                    "calibration": "I am aligned with my highest outcome. Success flows through me.",
                    "position": (50, 5),
                    "energy": "Stillness before creation"
                },
                {
                    "symbol": "☉",
                    "name": "THE SAGE",
                    "essence": "Intuitive Wisdom",
                    "career_stage": "Final Round",
                    "color": "#A0A0FF",
                    "glow": "rgba(160,160,255,0.5)",
                    "action": "Trust your inner knowing. Years of pattern recognition speak through you now.",
                    "calibration": "I access wisdom beyond logic. Insight arrives when I stop forcing.",
                    "position": (75, 20),
                    "energy": "Lightning flash of clarity"
                },
                {
                    "symbol": "△",
                    "name": "THE ANALYST",
                    "essence": "Structured Understanding",
                    "career_stage": "2nd Interview",
                    "color": "#00FF88",
                    "glow": "rgba(0,255,136,0.5)",
                    "action": "Decode their deeper needs. The question behind the question reveals everything.",
                    "calibration": "I see the architecture beneath the surface. Understanding is my advantage.",
                    "position": (25, 20),
                    "energy": "Deep processing"
                },
                {
                    "symbol": "∞",
                    "name": "THE GIVER",
                    "essence": "Expansive Generosity",
                    "career_stage": "1st Interview",
                    "color": "#00D4FF",
                    "glow": "rgba(0,212,255,0.5)",
                    "action": "Lead with value. Give insights freely. Abundance attracts abundance.",
                    "calibration": "I expand by giving. The more value I offer, the more returns to me.",
                    "position": (75, 40),
                    "energy": "Overflowing outward"
                },
                {
                    "symbol": "⚔",
                    "name": "THE WARRIOR",
                    "essence": "Focused Discipline",
                    "career_stage": "Follow-Up",
                    "color": "#FF6B6B",
                    "glow": "rgba(255,107,107,0.5)",
                    "action": "Apply calibrated pressure. Persistence without desperation. Know when to push.",
                    "calibration": "My discipline creates breakthroughs. Strength is precision, not force.",
                    "position": (25, 40),
                    "energy": "Contained power"
                },
                {
                    "symbol": "⬡",
                    "name": "THE HARMONIZER",
                    "essence": "Dynamic Balance",
                    "career_stage": "Engaged",
                    "color": "#FFD700",
                    "glow": "rgba(255,215,0,0.5)",
                    "action": "Find the synthesis. Your story and their needs are one pattern.",
                    "calibration": "I am the bridge between worlds. My presence creates resonance.",
                    "position": (50, 45),
                    "energy": "Heart of the system"
                },
                {
                    "symbol": "↑",
                    "name": "THE VICTOR",
                    "essence": "Eternal Persistence",
                    "career_stage": "Warm Lead",
                    "color": "#00FF88",
                    "glow": "rgba(0,255,136,0.5)",
                    "action": "Nurture the connection. Victory belongs to those who outlast doubt.",
                    "calibration": "I persist with joy, not desperation. Momentum compounds.",
                    "position": (70, 60),
                    "energy": "Upward thrust"
                },
                {
                    "symbol": "✧",
                    "name": "THE BEACON",
                    "essence": "Authentic Radiance",
                    "career_stage": "Response Received",
                    "color": "#FF9500",
                    "glow": "rgba(255,149,0,0.5)",
                    "action": "Your signal was received. Acknowledge this with genuine appreciation.",
                    "calibration": "My authentic presence is magnetic. Worth needs no convincing.",
                    "position": (30, 60),
                    "energy": "Radiant stillness"
                },
                {
                    "symbol": "⬢",
                    "name": "THE BUILDER",
                    "essence": "Solid Foundation",
                    "career_stage": "Outreach Sent",
                    "color": "#9B59B6",
                    "glow": "rgba(155,89,182,0.5)",
                    "action": "The first brick is laid. Connection begins with courageous action.",
                    "calibration": "I build with intention. Every outreach is an investment in the structure.",
                    "position": (50, 75),
                    "energy": "Grounded creation"
                },
                {
                    "symbol": "◆",
                    "name": "THE SEED",
                    "essence": "Grounded Intention",
                    "career_stage": "Identified",
                    "color": "#8B4513",
                    "glow": "rgba(139,69,19,0.5)",
                    "action": "Name the target clearly. Identification is the birth of manifestation.",
                    "calibration": "I plant seeds with clear vision. What I name, I can claim.",
                    "position": (50, 95),
                    "energy": "Potential in stillness"
                }
            ]
            
            # THE BLUEPRINT VISUALIZATION
            st.markdown("""
            <style>
            .blueprint-container {
                position: relative;
                width: 100%;
                height: 600px;
                background: linear-gradient(180deg, #0a0a1a 0%, #1a1a2e 100%);
                border-radius: 20px;
                overflow: hidden;
            }
            .pillar {
                position: absolute;
                width: 80px;
                height: 80px;
                border-radius: 50%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.3s ease;
                text-align: center;
            }
            .pillar:hover {
                transform: scale(1.2);
                z-index: 10;
            }
            .pillar-symbol {
                font-size: 2rem;
                font-weight: bold;
            }
            .pillar-name {
                font-size: 0.55rem;
                color: rgba(255,255,255,0.8);
                margin-top: 4px;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Build blueprint HTML
            tree_html = '<div class="blueprint-container">'
            
            # Add pillar circles
            for i, p in enumerate(pillars):
                x, y = p["position"]
                tree_html += f'''
                <div class="pillar" style="left: calc({x}% - 40px); top: calc({y}% - 40px); 
                     background: radial-gradient(circle, {p["color"]}40, {p["color"]}20);
                     border: 2px solid {p["color"]}; box-shadow: 0 0 20px {p["glow"]};">
                    <span class="pillar-symbol" style="color: {p["color"]};">{p["symbol"]}</span>
                    <span class="pillar-name">{p["name"]}</span>
                </div>
                '''
            
            tree_html += '</div>'
            st.markdown(tree_html, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # DEAL MAPPING TO PILLARS
            st.markdown("### 📊 YOUR DEALS ON THE BLUEPRINT")
            
            deals = st.session_state.get('crm_deals', [])
            
            # Map stages to pillars
            stage_to_pillar = {
                "Identified": "THE SEED",
                "Outreach Sent": "THE BUILDER",
                "Response Received": "THE BEACON",
                "Warm": "THE VICTOR",
                "Engaged": "THE HARMONIZER",
                "Under Review": "THE WARRIOR",
                "1st Interview": "THE GIVER",
                "2nd Interview": "THE ANALYST",
                "Final Round": "THE SAGE",
                "Offer": "THE CROWN",
                "Interview Scheduled": "THE GIVER",
                "Intro Pending": "THE BUILDER",
                "Under Review (HM)": "THE WARRIOR",
                "Active": "THE HARMONIZER"
            }
            
            # Group deals by pillar
            deals_by_pillar = {}
            for deal in deals:
                stage = deal.get('Stage', 'Identified')
                pillar_name = stage_to_pillar.get(stage, "THE SEED")
                if pillar_name not in deals_by_pillar:
                    deals_by_pillar[pillar_name] = []
                deals_by_pillar[pillar_name].append(deal)
            
            # Display deals grouped by pillar
            for p in pillars:
                name = p["name"]
                if name in deals_by_pillar:
                    deal_list = deals_by_pillar[name]
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {p['color']}10, {p['color']}05);
                                border-left: 4px solid {p['color']}; padding: 16px; margin: 12px 0; border-radius: 0 12px 12px 0;">
                        <h4 style="color: {p['color']}; margin: 0 0 8px 0;">{p['symbol']} {name} — {p['essence']}</h4>
                        <p style="color: #8892b0; font-size: 0.85rem; margin: 0 0 12px 0;">{p['career_stage']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for deal in deal_list:
                        st.markdown(f"   • **{deal['Company']}** — {deal['Role']}")
            
            st.markdown("---")
            
            # DAILY CALIBRATION (Renamed from Kavanah)
            st.markdown("### 🎯 DAILY CALIBRATION")
            st.caption("Set your intention. Align your energy. Execute with precision.")
            
            import random
            daily_pillar = random.choice(pillars)
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {daily_pillar['color']}15, transparent);
                        border: 2px solid {daily_pillar['color']}; border-radius: 16px; padding: 24px; text-align: center;">
                <p style="color: #8892b0; margin: 0; font-size: 0.9rem;">TODAY'S ARCHETYPE</p>
                <h1 style="color: {daily_pillar['color']}; margin: 12px 0; font-size: 3.5rem;">{daily_pillar['symbol']}</h1>
                <h2 style="color: {daily_pillar['color']}; margin: 0 0 8px 0;">{daily_pillar['name']}</h2>
                <p style="color: #ccd6f6; font-size: 0.95rem; margin: 0 0 16px 0;">{daily_pillar['essence']} — <i>{daily_pillar['energy']}</i></p>
                <p style="color: #ccd6f6; font-size: 1.1rem; font-style: italic; margin: 0 0 16px 0;">"{daily_pillar['calibration']}"</p>
                <p style="color: #8892b0; margin: 0;">🎯 <b>Action:</b> {daily_pillar['action']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # PILLAR GUIDE
            st.markdown("### 📖 THE 10 PILLARS")
            st.caption("Ancient wisdom for modern dealmakers.")
            
            for p in pillars:
                with st.expander(f"{p['symbol']} {p['name']} — {p['essence']}"):
                    st.markdown(f"**Stage:** {p['career_stage']}")
                    st.markdown(f"**Energy:** *{p['energy']}*")
                    st.markdown(f"**Action:** {p['action']}")
                    st.markdown(f"**Calibration:** *\"{p['calibration']}\"*")
        
        # ═══════════════════════════════════════════════════════════════
        # TAB: 📅 CALENDAR (Google Calendar Integration)
        # ═══════════════════════════════════════════════════════════════
        with crm_tab3:
            st.markdown("### 📅 INTERVIEW CALENDAR")
            st.caption("Sync with Google Calendar to see all upcoming interviews and meetings.")
            
            deals = st.session_state.get('crm_deals', [])
            calendar_events = st.session_state.get('calendar_events', [])
            
            # Google Calendar Integration Status
            try:
                from logic.integrations import (
                    is_google_calendar_available, get_upcoming_calendar_events,
                    get_interview_events, format_time_until
                )
                gcal_available = is_google_calendar_available()
            except ImportError:
                gcal_available = False
            
            # Connection Status Card
            if gcal_available:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(0,255,136,0.15), transparent);
                            border: 2px solid #00ff88; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 2rem;">🔗</span>
                        <div>
                            <p style="color: #00ff88; margin: 0; font-weight: bold;">GOOGLE CALENDAR CONNECTED</p>
                            <p style="color: #8892b0; margin: 0; font-size: 0.85rem;">Auto-syncing your interviews</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Fetch live calendar events
                if st.button("🔄 SYNC CALENDAR", use_container_width=True, key="sync_gcal"):
                    with st.spinner("Fetching from Google Calendar..."):
                        try:
                            events = get_upcoming_calendar_events(days=14)
                            interview_events = [e for e in events if e.get('is_interview')]
                            st.session_state['google_calendar_events'] = events
                            st.session_state['google_calendar_interviews'] = interview_events
                            st.success(f"✅ Synced {len(events)} events, {len(interview_events)} interviews detected!")
                        except Exception as e:
                            st.error(f"Sync failed: {e}")
            else:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(255,191,0,0.15), transparent);
                            border: 2px solid #FFD700; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 2rem;">📅</span>
                        <div>
                            <p style="color: #FFD700; margin: 0; font-weight: bold;">GOOGLE CALENDAR NOT CONNECTED</p>
                            <p style="color: #8892b0; margin: 0; font-size: 0.85rem;">Add credentials to enable auto-sync</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("🔧 HOW TO CONNECT GOOGLE CALENDAR"):
                    st.markdown("""
                    **Setup Google Calendar OAuth:**
                    
                    1. Go to [Google Cloud Console](https://console.cloud.google.com/)
                    2. Create a new project or use existing
                    3. Enable "Google Calendar API"
                    4. Create OAuth 2.0 credentials (Desktop app type)
                    5. Download the JSON file
                    6. Save it as `google_credentials.json` in the app directory
                    7. Restart the app and click "Sync Calendar"
                    
                    *First-time sync will open a browser window to authorize access.*
                    """)
            
            st.markdown("---")
            
            # Display upcoming interviews from multiple sources
            st.markdown("### 🎯 UPCOMING INTERVIEWS")
            
            # Combine sources: Google Calendar, manual entries, and CRM deals with interview stages
            all_interviews = []
            
            # From CRM deals (interview stages)
            interview_stages = ['Interview Scheduled', '1st Interview', '2nd Interview', 'Final Round', 'Phone Screen']
            for deal in deals:
                if deal.get('Stage') in interview_stages:
                    all_interviews.append({
                        'source': 'CRM',
                        'company': deal.get('Company', 'Unknown'),
                        'role': deal.get('Role', 'Unknown'),
                        'stage': deal.get('Stage', 'Interview'),
                        'notes': deal.get('Notes', ''),
                        'date': 'TBD'
                    })
            
            # From manual calendar entries
            for event in calendar_events:
                all_interviews.append({
                    'source': 'Manual',
                    'company': event.get('company', 'Unknown'),
                    'role': event.get('title', 'Interview'),
                    'stage': event.get('type', 'Interview'),
                    'date': event.get('date', 'TBD'),
                    'time': event.get('time', '')
                })
            
            # From Google Calendar (if synced)
            gcal_interviews = st.session_state.get('google_calendar_interviews', [])
            for event in gcal_interviews:
                all_interviews.append({
                    'source': 'Google',
                    'company': event.get('company', '') or 'Check Title',
                    'role': event.get('title', 'Interview'),
                    'stage': event.get('type', 'Interview'),
                    'date': event.get('date', 'TBD'),
                    'time': event.get('time', ''),
                    'link': event.get('google_meet', '') or event.get('link', '')
                })
            
            if all_interviews:
                for i, interview in enumerate(all_interviews):
                    source_icons = {'CRM': '📊', 'Manual': '✏️', 'Google': '🔗'}
                    source_icon = source_icons.get(interview['source'], '📅')
                    stage_color = "#00ff88" if 'Final' in interview.get('stage', '') else "#FFD700"
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {stage_color}10, transparent);
                                border-left: 4px solid {stage_color}; padding: 16px; margin: 8px 0; border-radius: 0 8px 8px 0;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div>
                                <p style="color: {stage_color}; margin: 0; font-weight: bold; font-size: 1.1rem;">
                                    {source_icon} {interview['company']}
                                </p>
                                <p style="color: #ccd6f6; margin: 4px 0;">{interview['role']}</p>
                                <p style="color: #8892b0; margin: 0; font-size: 0.85rem;">
                                    📍 {interview['stage']} | Source: {interview['source']}
                                </p>
                            </div>
                            <div style="text-align: right;">
                                <p style="color: {stage_color}; font-weight: bold; margin: 0;">{interview.get('date', 'TBD')}</p>
                                <p style="color: #8892b0; margin: 0; font-size: 0.85rem;">{interview.get('time', '')}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Quick actions
                    action_cols = st.columns(4)
                    with action_cols[0]:
                        if st.button("🎯 PREP", key=f"prep_int_{i}", use_container_width=True):
                            st.session_state['prep_company'] = interview['company']
                            st.toast(f"Go to Prep Mode for {interview['company']}")
                    with action_cols[1]:
                        if st.button("🎮 COMBAT", key=f"combat_int_{i}", use_container_width=True):
                            st.toast("Practice in Combat Simulator!")
                    with action_cols[2]:
                        if st.button("📰 INTEL", key=f"intel_int_{i}", use_container_width=True):
                            st.toast("Opening Company Intel...")
                    with action_cols[3]:
                        if interview.get('link'):
                            st.markdown(f"[🔗 JOIN]({interview['link']})")
            else:
                st.info("📅 No upcoming interviews. Add them from your CRM deals or manually below!")
            
            st.markdown("---")
            
            # Add Manual Interview
            st.markdown("### ➕ ADD INTERVIEW MANUALLY")
            add_cols = st.columns([2, 2, 1, 1])
            new_company = add_cols[0].text_input("Company", key="cal_new_company")
            new_role = add_cols[1].text_input("Role/Title", key="cal_new_role")
            new_date = add_cols[2].date_input("Date", key="cal_new_date")
            new_type = add_cols[3].selectbox("Type", ["Phone Screen", "Hiring Manager", "Team Panel", "Final Round", "CEO/Exec"], key="cal_new_type")
            
            if st.button("📅 ADD TO CALENDAR", use_container_width=True, key="add_manual_interview"):
                if new_company:
                    if 'calendar_events' not in st.session_state:
                        st.session_state['calendar_events'] = []
                    st.session_state['calendar_events'].append({
                        'title': f"{new_type} - {new_role}",
                        'company': new_company,
                        'date': str(new_date),
                        'type': new_type,
                        'time': ''
                    })
                    st.success(f"✅ Added interview with {new_company}!")
                    st.rerun()
        
        # ═══════════════════════════════════════════════════════════════
        # TAB: 📈 MARKET (Stock Prices for Pipeline Companies)
        # ═══════════════════════════════════════════════════════════════
        with crm_tab4:
            st.markdown("### 📈 MARKET INTEL")
            st.caption("Live stock prices and market data for your pipeline companies.")
            
            deals = st.session_state.get('crm_deals', [])
            
            try:
                from logic.integrations import get_stock_price, get_company_stock_symbol, get_job_board_links
            except ImportError:
                st.error("Integration module not available")
                get_stock_price = None
            
            if get_stock_price:
                # Get unique companies from pipeline
                pipeline_companies = list(set([d['Company'] for d in deals]))
                
                st.markdown("### 📊 PIPELINE COMPANY STOCKS")
                st.caption("Real-time market data for public companies in your pipeline.")
                
                # Stock data cache
                if 'stock_cache' not in st.session_state:
                    st.session_state['stock_cache'] = {}
                
                # Refresh button
                if st.button("🔄 REFRESH PRICES", use_container_width=True, key="refresh_stocks"):
                    st.session_state['stock_cache'] = {}
                    st.rerun()
                
                st.markdown("")
                
                # Display stock cards - Grouped by type
                public_companies = []
                private_companies = []
                nonprofit_companies = []
                
                for company in pipeline_companies:
                    company_data = get_company_stock_symbol(company)
                    company_type = company_data.get('type', 'unknown')
                    
                    if company_type == 'public' and company_data.get('symbol'):
                        public_companies.append((company, company_data))
                    elif company_type in ['nonprofit', 'intergovernmental', 'government']:
                        nonprofit_companies.append((company, company_data))
                    else:
                        private_companies.append((company, company_data))
                
                # PUBLIC COMPANIES with stock data
                if public_companies:
                    st.markdown("#### 📈 PUBLIC COMPANIES")
                    stock_cols = st.columns(3)
                    col_idx = 0
                    
                    for company, company_data in public_companies:
                        symbol = company_data.get('symbol')
                        
                        if symbol:
                            # Check cache or fetch
                            if symbol not in st.session_state['stock_cache']:
                                stock_data = get_stock_price(symbol)
                                st.session_state['stock_cache'][symbol] = stock_data
                            else:
                                stock_data = st.session_state['stock_cache'][symbol]
                            
                            with stock_cols[col_idx % 3]:
                                if 'error' not in stock_data:
                                    change = stock_data.get('change', 0)
                                    change_pct = stock_data.get('change_percent', 0)
                                    price = stock_data.get('price', 0)
                                    
                                    change_color = "#00ff88" if change >= 0 else "#ff6b6b"
                                    change_icon = "▲" if change >= 0 else "▼"
                                    country_flag = {'USA': '🇺🇸', 'UK': '🇬🇧', 'Germany': '🇩🇪', 'Japan': '🇯🇵', 'China': '🇨🇳', 'Canada': '🇨🇦', 'France': '🇫🇷', 'Switzerland': '🇨🇭'}.get(company_data.get('country', ''), '🌍')
                                    
                                    st.markdown(f"""
                                    <div style="background: linear-gradient(135deg, rgba(255,215,0,0.1), transparent);
                                                border: 1px solid rgba(255,215,0,0.3); border-radius: 12px; padding: 16px; margin: 8px 0;">
                                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                                            <div>
                                                <p style="color: #8892b0; margin: 0; font-size: 0.75rem;">{country_flag} {company}</p>
                                                <p style="color: #FFD700; margin: 4px 0 0 0; font-weight: bold;">{symbol}</p>
                                                <p style="color: #64ffda; margin: 2px 0 0 0; font-size: 0.65rem;">{company_data.get('industry', '')}</p>
                                            </div>
                                            <div style="text-align: right;">
                                                <p style="color: #ccd6f6; margin: 0; font-size: 1.4rem; font-weight: bold;">${price:.2f}</p>
                                                <p style="color: {change_color}; margin: 0; font-size: 0.9rem;">
                                                    {change_icon} ${abs(change):.2f} ({change_pct:+.2f}%)
                                                </p>
                                            </div>
                                        </div>
                                        <p style="color: #8892b0; margin: 8px 0 0 0; font-size: 0.7rem;">
                                            {stock_data.get('market_state', '')} | {company_data.get('exchange', '')}
                                        </p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.markdown(f"""
                                    <div style="background: rgba(255,255,255,0.02); border: 1px dashed rgba(255,255,255,0.1); 
                                                border-radius: 12px; padding: 16px; margin: 8px 0;">
                                        <p style="color: #8892b0; margin: 0;">{company}</p>
                                        <p style="color: #FFD700; margin: 4px 0;">{symbol}</p>
                                        <p style="color: #ff6b6b; margin: 0; font-size: 0.8rem;">Data unavailable</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            col_idx += 1
                
                # PRIVATE COMPANIES (Startups, Unicorns, etc.)
                if private_companies:
                    st.markdown("---")
                    st.markdown("### 🔒 PRIVATE COMPANIES")
                    st.caption("Startups, unicorns, and private companies in your pipeline:")
                    
                    private_cols = st.columns(3)
                    for i, (company, data) in enumerate(private_companies[:12]):
                        with private_cols[i % 3]:
                            market_cap = data.get('market_cap', 'unknown')
                            cap_badge = {'unicorn': '🦄', 'startup': '🚀', 'large': '🏢', 'mid': '📊', 'small': '💼'}.get(market_cap, '🏢')
                            
                            job_links = get_job_board_links(company)
                            st.markdown(f"""
                            <div style="background: rgba(147,112,219,0.08); border: 1px solid rgba(147,112,219,0.3);
                                        border-radius: 12px; padding: 12px; margin: 6px 0;">
                                <p style="color: #9370DB; margin: 0; font-weight: bold;">{cap_badge} {company}</p>
                                <p style="color: #8892b0; margin: 2px 0; font-size: 0.75rem;">{data.get('industry', 'Unknown')} | {data.get('country', 'Unknown')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown(f"[LinkedIn]({job_links['LinkedIn']}) | [Careers]({job_links['Company Careers']})")
                
                st.markdown("---")
                
                # Manual stock lookup
                st.markdown("### 🔍 LOOKUP ANY STOCK")
                lookup_cols = st.columns([3, 1])
                manual_symbol = lookup_cols[0].text_input("Enter ticker symbol (e.g., AAPL, GOOGL):", key="manual_stock_lookup")
                
                if lookup_cols[1].button("📈 GET PRICE", key="get_manual_stock"):
                    if manual_symbol:
                        with st.spinner("Fetching..."):
                            data = get_stock_price(manual_symbol.upper())
                            if 'error' not in data:
                                change = data.get('change', 0)
                                change_color = "#00ff88" if change >= 0 else "#ff6b6b"
                                st.success(f"**{data['symbol']}**: ${data['price']:.2f} ({data['change_percent']:+.2f}%)")
                            else:
                                st.error(f"Could not find: {manual_symbol}")
                
                # Market indices for context
                st.markdown("---")
                st.markdown("### 📊 MARKET INDICES")
                
                index_cols = st.columns(4)
                indices = [('SPY', 'S&P 500'), ('QQQ', 'NASDAQ'), ('DIA', 'DOW'), ('IWM', 'Russell 2000')]
                
                for i, (symbol, name) in enumerate(indices):
                    with index_cols[i]:
                        if symbol not in st.session_state['stock_cache']:
                            data = get_stock_price(symbol)
                            st.session_state['stock_cache'][symbol] = data
                        else:
                            data = st.session_state['stock_cache'][symbol]
                        
                        if 'error' not in data:
                            change_color = "#00ff88" if data.get('change', 0) >= 0 else "#ff6b6b"
                            st.metric(name, f"${data['price']:.2f}", f"{data['change_percent']:+.2f}%")
                        else:
                            st.metric(name, "—", "N/A")
            else:
                st.warning("Stock price integration not available. Check the integrations module.")
        
        # ═══════════════════════════════════════════════════════════════
        # TAB 0: DAILY BRIEFING (AUTOMATIC TASK ENGINE)
        # ═══════════════════════════════════════════════════════════════
        with crm_tab1:
            st.markdown("### 📋 DAILY BRIEFING — TODAY'S MISSION")
            st.caption(f"📅 {st.session_state.get('current_date', 'December 6, 2024')} | Auto-generated action list based on your pipeline.")
            
            contacts = st.session_state.get('crm_contacts', [])
            deals = st.session_state.get('crm_deals', [])
            
            # ═══════════════════════════════════════════════════════════════
            # v15: MORNING BRIEFING (LIVE PIPELINE INTEL)
            # ═══════════════════════════════════════════════════════════════
            st.markdown("## 📰 MORNING BRIEFING (Pipeline Intel)")
            st.caption("Live news for your active opportunities. Stay ahead of the conversation.")
            
            # Get unique companies from deals
            pipeline_companies = list(set([d['Company'] for d in deals[:5]]))
            
            if pipeline_companies:
                with st.expander("🔍 CLICK TO LOAD LIVE INTEL", expanded=False):
                    for company in pipeline_companies[:5]:
                        st.markdown(f"#### 🏢 {company}")
                        
                        try:
                            import requests
                            q_url = company.replace(' ', '%20')
                            hn_url = f"https://hn.algolia.com/api/v1/search?query={q_url}&tags=story&hitsPerPage=3"
                            response = requests.get(hn_url, timeout=5)
                            
                            if response.status_code == 200:
                                hits = response.json().get('hits', [])
                                if hits:
                                    for hit in hits[:2]:
                                        title = hit.get('title', 'No title')
                                        url = hit.get('url') or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
                                        st.markdown(f"📰 [{title}]({url})")
                                else:
                                    st.caption("*No recent news. Company is operating quietly.*")
                            else:
                                st.caption("*Intel unavailable.*")
                        except Exception:
                            st.caption("*Intel feed offline.*")
                        
                        st.divider()
                
                # Quick Links for all pipeline companies
                st.markdown("#### 🔗 QUICK RESEARCH")
                link_cols = st.columns(len(pipeline_companies[:5]))
                for i, company in enumerate(pipeline_companies[:5]):
                    with link_cols[i]:
                        q = company.replace(' ', '+')
                        st.markdown(f"[{company}](https://www.google.com/search?q={q}+funding+news)")
            
            st.markdown("---")
            
            # Show High-Yield Tactics from Win/Loss Memory (if any)
            if 'win_loss_memory' in st.session_state and st.session_state['win_loss_memory']['high_yield_tactics']:
                st.markdown("## ⚡ TODAY'S WINNING TACTICS")
                st.caption("Based on your logged wins, use these in your next call:")
                for tactic in st.session_state['win_loss_memory']['high_yield_tactics']:
                    st.success(f"✅ **{tactic}**")
                st.markdown("---")
            
            # CALCULATE TASKS
            # Priority 1: HIGH priority, not closed, needs action
            urgent_tasks = [c for c in contacts if c.get('Priority') == '🔥 HIGH' and c.get('Status') not in ['Closed', 'Interview Scheduled', 'Closed Won', 'Closed Lost']]
            
            # Priority 2: Medium priority
            medium_tasks = [c for c in contacts if c.get('Priority') == '⚡ MED' and c.get('Status') not in ['Closed']]
            
            # Pending responses
            pending = [c for c in contacts if c.get('Status') in ['Outreach Sent', 'Sent', 'Under Review']]
            
            # Interviews scheduled
            interviews = [c for c in contacts if c.get('Status') == 'Interview Scheduled']
            
            st.markdown("---")
            
            # ═══ TODAY'S TOP 5 ACTIONS ═══
            st.markdown("## 🔥 TODAY'S TOP 5 ACTIONS")
            
            today_tasks = []
            
            # Add interviews first (highest priority)
            for c in interviews:
                today_tasks.append({
                    "action": f"🎯 **PREP FOR INTERVIEW:** {c['Company']} ({c['Role']})",
                    "contact": c['Name'],
                    "priority": 0,
                    "type": "interview"
                })
            
            # Add HIGH priority follow-ups
            for c in urgent_tasks[:5]:
                today_tasks.append({
                    "action": f"📞 **FOLLOW UP:** {c['Name']} @ {c['Company']}",
                    "contact": c['Name'],
                    "priority": 1,
                    "type": "follow_up",
                    "next_step": c.get('Next Step', 'TBD')
                })
            
            # Display Top 5
            if today_tasks:
                for i, task in enumerate(today_tasks[:5], 1):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{i}.** {task['action']}")
                        if task.get('next_step'):
                            st.caption(f"   → {task['next_step']}")
                    with col2:
                        if st.checkbox("✅ Done", key=f"task_{i}"):
                            st.success("Completed!")
                    st.divider()
            else:
                st.success("✅ All caught up! No urgent tasks today.")
            
            st.markdown("---")
            
            # ═══ PENDING RESPONSES ═══
            st.markdown("## 📤 AWAITING RESPONSE")
            st.caption("Check for replies from these contacts:")
            
            if pending:
                for c in pending[:8]:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{c['Name']}** @ {c['Company']}")
                        st.caption(f"Last touch: {c.get('Last Touch', 'Unknown')} | Channel: {c.get('Channel', 'Unknown')}")
                    with col2:
                        st.caption(c.get('Status', 'Unknown'))
                    with col3:
                        if st.button("✅ Replied", key=f"replied_brief_{c['Name']}"):
                            for contact in st.session_state['crm_contacts']:
                                if contact['Name'] == c['Name']:
                                    contact['Status'] = 'Warm'
                                    break
                            st.rerun()
            else:
                st.info("No pending outreach.")
            
            st.markdown("---")
            
            # ═══ NEXT 7 DAYS FOLLOW-UPS ═══
            st.markdown("## 📅 NEXT 7 DAYS")
            
            # Group by urgency
            this_week = medium_tasks[:10]
            
            if this_week:
                for c in this_week:
                    st.markdown(f"• **{c['Name']}** @ {c['Company']} — *{c.get('Next Step', 'TBD')}*")
            else:
                st.info("Pipeline is clear for the week!")
            
            st.markdown("---")
            
            # ═══ QUICK STATS ═══
            st.markdown("## 📊 PIPELINE SNAPSHOT")
            
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("TOTAL CONTACTS", len(contacts))
            k2.metric("ACTIVE DEALS", len(deals))
            k3.metric("PENDING RESPONSES", len(pending))
            k4.metric("INTERVIEWS", len(interviews))
        
        # ═══════════════════════════════════════════════════════════════
        # TAB: 🤝 NETWORKING HUB (Multi-Channel Messaging & Introductions)
        # ═══════════════════════════════════════════════════════════════
        with crm_tab5:
            st.markdown("### 🤝 NETWORKING HUB")
            st.caption("Multi-channel outreach · Warm introductions · Be the connector")
            
            try:
                from logic.integrations import (
                    generate_messaging_links, generate_intro_message, 
                    get_social_links, ACHIEVEMENTS, check_achievements, get_achievement_display
                )
                networking_available = True
            except ImportError:
                networking_available = False
                st.warning("Networking module not fully loaded")
            
            if networking_available:
                contacts = st.session_state.get('crm_contacts', [])
                
                # Multi-Channel Quick Reach
                st.markdown("---")
                st.markdown("## 📱 QUICK REACH — MULTI-CHANNEL")
                st.caption("Select a contact and reach out on any platform")
                
                # Contact selector
                contact_names = [f"{c['Name']} @ {c['Company']}" for c in contacts]
                selected_contact_idx = st.selectbox("Select Contact", range(len(contact_names)), 
                                                    format_func=lambda x: contact_names[x] if contact_names else "No contacts", 
                                                    key="net_contact_select")
                
                if contacts and selected_contact_idx is not None:
                    selected_contact = contacts[selected_contact_idx]
                    
                    # Contact card
                    contact_name = selected_contact.get('Name', 'Unknown')
                    contact_company = selected_contact.get('Company', '')
                    contact_email = selected_contact.get('Email', '')
                    contact_phone = selected_contact.get('Phone', '')
                    contact_linkedin = selected_contact.get('LinkedIn', '')
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(100,255,218,0.1), transparent);
                                border: 1px solid rgba(100,255,218,0.3); border-radius: 12px; padding: 16px; margin: 16px 0;">
                        <h4 style="color: #64ffda; margin: 0;">{contact_name}</h4>
                        <p style="color: #ccd6f6;">{selected_contact.get('Role', '')} @ {contact_company}</p>
                        <p style="color: #8892b0; font-size: 0.85rem;">
                            📧 {contact_email or 'No email'} | 📱 {contact_phone or 'No phone'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Message composer
                    st.markdown("#### ✍️ COMPOSE MESSAGE")
                    message_template = st.text_area("Message", 
                        value=f"Hi {contact_name.split()[0] if contact_name else ''},\n\nHope you're doing well! I wanted to reach out about...",
                        height=100, key="net_message_compose")
                    
                    # Generate deep links
                    links = generate_messaging_links(
                        phone=contact_phone,
                        email=contact_email,
                        name=contact_name,
                        message=message_template,
                        linkedin_url=contact_linkedin
                    )
                    
                    # Channel buttons
                    st.markdown("#### 🚀 SEND VIA")
                    btn_cols = st.columns(6)
                    
                    if links.get('WhatsApp'):
                        btn_cols[0].markdown(f"[💬 WhatsApp]({links['WhatsApp']})")
                    if links.get('LinkedIn Message'):
                        btn_cols[1].markdown(f"[💼 LinkedIn]({links['LinkedIn Message']})")
                    if links.get('Email'):
                        btn_cols[2].markdown(f"[📧 Email]({links['Email']})")
                    if links.get('SMS'):
                        btn_cols[3].markdown(f"[📱 SMS]({links['SMS']})")
                    if links.get('Telegram'):
                        btn_cols[4].markdown(f"[✈️ Telegram]({links['Telegram']})")
                    if links.get('Phone'):
                        btn_cols[5].markdown(f"[📞 Call]({links['Phone']})")
                
                st.markdown("---")
                
                # Warm Intro Generator
                st.markdown("## 🔥 WARM INTRO GENERATOR")
                st.caption("Generate personalized intro requests for any channel")
                
                intro_cols = st.columns(2)
                your_name = intro_cols[0].text_input("Your Name", value="Leon", key="net_your_name")
                target_person = intro_cols[1].text_input("Person You Want to Meet", placeholder="e.g., CEO of Target Co", key="net_target")
                
                connector_col, context_col = st.columns(2)
                connector_name = connector_col.text_input("Who Can Introduce You?", placeholder="e.g., John Smith", key="net_connector")
                intro_context = context_col.text_input("Context/Role", placeholder="e.g., VP Sales role", key="net_context")
                
                intro_type = st.selectbox("Message Type", 
                    ["warm_intro", "referral_ask", "follow_up", "thank_you"],
                    format_func=lambda x: {"warm_intro": "🤝 Warm Intro Request", "referral_ask": "📋 Referral Ask", 
                                           "follow_up": "🔄 Follow Up", "thank_you": "🙏 Thank You"}.get(x, x),
                    key="net_intro_type")
                
                if st.button("⚡ GENERATE MESSAGES", use_container_width=True, key="gen_intro_msgs"):
                    if connector_name and your_name:
                        messages = generate_intro_message(
                            intro_type=intro_type,
                            from_name=your_name,
                            to_name=connector_name,
                            target_name=target_person or "them",
                            context=intro_context
                        )
                        
                        st.markdown("#### 📧 EMAIL VERSION")
                        st.code(messages.get('email', ''), language=None)
                        
                        st.markdown("#### 💼 LINKEDIN VERSION")
                        st.code(messages.get('linkedin', ''), language=None)
                        
                        st.markdown("#### 💬 WHATSAPP VERSION")
                        st.code(messages.get('whatsapp', ''), language=None)
                
                st.markdown("---")
                
                # Person Finder
                st.markdown("## 🔍 FIND ANYONE")
                st.caption("Search for someone across all platforms")
                
                find_cols = st.columns([2, 2, 1])
                find_name = find_cols[0].text_input("Person's Name", key="net_find_name")
                find_company = find_cols[1].text_input("Company (optional)", key="net_find_company")
                
                if find_cols[2].button("🔍 SEARCH", key="net_search_person"):
                    if find_name:
                        social_links = get_social_links(find_name, find_company)
                        
                        st.markdown("#### 🌐 SEARCH LINKS")
                        link_cols = st.columns(3)
                        for i, (platform, url) in enumerate(social_links.items()):
                            link_cols[i % 3].markdown(f"[{platform}]({url})")
                
                st.markdown("---")
                
                # Matchmaker Mode
                st.markdown("## 🎯 MATCHMAKER MODE")
                st.caption("Be the connector. Help people in your network find each other.")
                
                st.info("💡 **Pro Tip:** Being a connector builds social capital. When you introduce two people who can help each other, they both remember you.")
                
                mm_cols = st.columns(2)
                person_a = mm_cols[0].text_input("Person A", placeholder="Name @ Company", key="mm_person_a")
                person_b = mm_cols[1].text_input("Person B", placeholder="Name @ Company", key="mm_person_b")
                why_intro = st.text_area("Why Should They Meet?", placeholder="What value can they provide each other?", key="mm_why")
                
                if st.button("💌 GENERATE DOUBLE-OPT-IN INTRO", use_container_width=True, key="gen_doi"):
                    if person_a and person_b:
                        st.markdown("#### Step 1: Ask Person A")
                        st.code(f"""Hi {person_a.split()[0] if person_a else 'there'},

I wanted to check if you'd be open to an intro to {person_b}. 

{why_intro or 'I think there could be some great synergy!'}

Would it be okay if I introduced you two?

Best,
{your_name}""", language=None)
                        
                        st.markdown("#### Step 2: Ask Person B")
                        st.code(f"""Hi {person_b.split()[0] if person_b else 'there'},

I have someone in my network I think you should meet: {person_a}

{why_intro or 'I think you two would really hit it off professionally.'}

Would you be open to an intro?

Best,
{your_name}""", language=None)
                        
                        st.markdown("#### Step 3: Make The Intro (after both say yes)")
                        st.code(f"""Hi {person_a.split()[0] if person_a else ''} and {person_b.split()[0] if person_b else ''},

I'm excited to introduce you two!

{person_a} — {person_b}
{person_b} — {person_a}

{why_intro or 'I thought there might be some great synergy here.'}

I'll let you two take it from here!

Best,
{your_name}""", language=None)

        # ═══════════════════════════════════════════════════════════════
        # TAB 2: CONTACT DATABASE (Original)
        # ═══════════════════════════════════════════════════════════════
        with crm_tab6:
            st.markdown("### 👤 CONTACT DATABASE")
            
            # Metrics
            contacts = st.session_state['crm_contacts']
            hot_count = sum(1 for c in contacts if c['Status'] in ['Hot', 'Warm', 'Interview Scheduled'])
            
            k1, k2, k3 = st.columns(3)
            k1.metric("TOTAL CONTACTS", len(contacts))
            k2.metric("ACTIVE/HOT", hot_count)
            k3.metric("PENDING FOLLOW-UP", sum(1 for c in contacts if 'Follow' in c.get('Next Step', '')))
            
            st.markdown("---")
            
            # Filter
            status_filter = st.multiselect("Filter by Status:", ["Warm", "Hot", "Sent", "Under Review", "Interview Scheduled", "Outreach Sent", "Not Contacted"], default=[])
            
            # Display Contacts
            display_contacts = [c for c in contacts if not status_filter or c['Status'] in status_filter]
            
            edited_contacts = st.data_editor(
                display_contacts,
                num_rows="dynamic",
                use_container_width=True,
                column_config={
                    "Status": st.column_config.SelectboxColumn(
                        options=["Hot", "Warm", "Sent", "Under Review", "Interview Scheduled", "Outreach Sent", "Not Contacted", "Closed"]
                    ),
                    "Priority": st.column_config.SelectboxColumn(
                        options=["🔥 HIGH", "⚡ MED", "⏳ LOW"]
                    ),
                    "Channel": st.column_config.SelectboxColumn(
                        options=["LinkedIn DM", "Email", "Slack", "Referral", "Direct", "InMail", "Website"]
                    ),
                    "Strength": st.column_config.SelectboxColumn(
                        "Relationship",
                        options=["🔗", "🔗🔗", "🔗🔗🔗", "🔗🔗🔗🔗", "🔗🔗🔗🔗🔗"],
                        help="Network strength: 🔗=Cold, 🔗🔗🔗🔗🔗=Strong"
                    )
                }
            )
            st.session_state['crm_contacts'] = edited_contacts
            
            # Quick Add Contact
            st.markdown("---")
            with st.expander("➕ ADD NEW CONTACT"):
                ac1, ac2, ac3 = st.columns(3)
                new_name = ac1.text_input("Name", key="new_contact_name")
                new_company = ac2.text_input("Company", key="new_contact_company")
                new_role = ac3.text_input("Role", key="new_contact_role")
                
                ac4, ac5, ac6 = st.columns(3)
                new_channel = ac4.selectbox("Channel", ["LinkedIn DM", "Email", "Slack", "Referral", "Direct"], key="new_contact_channel")
                new_status = ac5.selectbox("Status", ["Outreach Sent", "Warm", "Under Review"], key="new_contact_status")
                new_priority = ac6.selectbox("Priority", ["🔥 HIGH", "⚡ MED", "⏳ LOW"], key="new_contact_priority")
                
                if st.button("ADD CONTACT", type="primary", key="add_contact_btn"):
                    if new_name and new_company:
                        st.session_state['crm_contacts'].append({
                            "Name": new_name,
                            "Company": new_company,
                            "Role": new_role,
                            "Channel": new_channel,
                            "Status": new_status,
                            "Last Touch": "12/06",
                            "Next Step": "TBD",
                            "Priority": new_priority
                        })
                        st.success(f"✅ Added {new_name} at {new_company}")
                        st.rerun()
        
        # ═══════════════════════════════════════════════════════════════
        # TAB 3: DEAL PIPELINE
        # ═══════════════════════════════════════════════════════════════
        with crm_tab7:
            st.markdown("### 📈 DEAL PIPELINE")
            
            deals = st.session_state['crm_deals']
            
            # Pipeline Metrics
            k1, k2, k3, k4 = st.columns(4)
            stages = [d.get("Stage", "") for d in deals]
            k1.metric("TOTAL DEALS", len(deals))
            k2.metric("INTERVIEWS", sum(1 for s in stages if 'Interview' in s))
            k3.metric("UNDER REVIEW", sum(1 for s in stages if 'Review' in s))
            k4.metric("ACTIVE", sum(1 for s in stages if s == 'Active'))
            
            st.markdown("---")
            
            # Editable Deal Table
            edited_deals = st.data_editor(
                deals,
                num_rows="dynamic",
                use_container_width=True,
                column_config={
                    "Stage": st.column_config.SelectboxColumn(
                        options=["Outreach Sent", "Under Review", "Under Review (HM)", "Interview Scheduled", "Final Round", "Active", "Offer", "Closed Won", "Closed Lost"]
                    ),
                    "Priority": st.column_config.NumberColumn(min_value=1, max_value=3),
                    "Signal": st.column_config.SelectboxColumn(
                        options=["Very High", "High", "Medium", "Low"]
                    )
                }
            )
            st.session_state['crm_deals'] = edited_deals
            
            st.markdown("---")
            
            # ═══════════════════════════════════════════════════════════════
            # v15: WIN/LOSS FEEDBACK LOOP (NEURAL LEARNING)
            # ═══════════════════════════════════════════════════════════════
            st.markdown("### 🧠 WIN/LOSS FEEDBACK (Neural Learning)")
            st.caption("Teach the system what works. It will suggest high-yield tactics in future sessions.")
            
            # Initialize Win/Loss Memory
            if 'win_loss_memory' not in st.session_state:
                st.session_state['win_loss_memory'] = {
                    'wins': [],
                    'losses': [],
                    'high_yield_tactics': []
                }
            
            # Log a Win
            with st.expander("🏆 LOG A WIN (Deal Advanced)"):
                win_company = st.selectbox("Which company?", [d['Company'] for d in deals], key="win_company")
                win_stage = st.selectbox("What stage did you reach?", ["Interview Scheduled", "Final Round", "Offer", "Closed Won"], key="win_stage")
                win_what_worked = st.text_area("What worked? (metrics, stories, tactics)", placeholder="e.g., 'Used 160% YoY metric', 'Partner Architecture story landed'", key="win_worked")
                
                if st.button("💾 LOG WIN", type="primary", key="log_win"):
                    if win_company and win_what_worked:
                        st.session_state['win_loss_memory']['wins'].append({
                            "company": win_company,
                            "stage": win_stage,
                            "what_worked": win_what_worked,
                            "date": "12/06/2024"
                        })
                        # Extract tactics
                        if "160%" in win_what_worked or "percent" in win_what_worked.lower():
                            if "160% YoY metric" not in st.session_state['win_loss_memory']['high_yield_tactics']:
                                st.session_state['win_loss_memory']['high_yield_tactics'].append("160% YoY metric")
                        if "partner" in win_what_worked.lower():
                            if "Partner Architecture story" not in st.session_state['win_loss_memory']['high_yield_tactics']:
                                st.session_state['win_loss_memory']['high_yield_tactics'].append("Partner Architecture story")
                        if "$10M" in win_what_worked or "pipeline" in win_what_worked.lower():
                            if "$10M Pipeline proof" not in st.session_state['win_loss_memory']['high_yield_tactics']:
                                st.session_state['win_loss_memory']['high_yield_tactics'].append("$10M Pipeline proof")
                        
                        st.success(f"🧠 WIN LOGGED! The system is learning from {win_company}.")
                        st.balloons()
            
            # Log a Loss
            with st.expander("📉 LOG A LOSS (Deal Lost)"):
                loss_company = st.selectbox("Which company?", [d['Company'] for d in deals], key="loss_company")
                loss_reason = st.text_area("What didn't work?", placeholder="e.g., 'They wanted more SMB experience', 'Salary mismatch'", key="loss_reason")
                
                if st.button("💾 LOG LOSS", key="log_loss"):
                    if loss_company and loss_reason:
                        st.session_state['win_loss_memory']['losses'].append({
                            "company": loss_company,
                            "reason": loss_reason,
                            "date": "12/06/2024"
                        })
                        st.info(f"📊 LOSS LOGGED. The system will learn to avoid this pattern.")
            
            # Show High-Yield Tactics
            if st.session_state['win_loss_memory']['high_yield_tactics']:
                st.markdown("---")
                st.markdown("#### ⚡ HIGH-YIELD TACTICS (What's Working)")
                for tactic in st.session_state['win_loss_memory']['high_yield_tactics']:
                    st.success(f"✅ **{tactic}** — Use this in your next interview!")
            
            # Show Win/Loss History
            wins = st.session_state['win_loss_memory']['wins']
            losses = st.session_state['win_loss_memory']['losses']
            
            if wins or losses:
                st.markdown("---")
                st.markdown("#### 📊 WIN/LOSS HISTORY")
                
                hist_cols = st.columns(2)
                with hist_cols[0]:
                    st.markdown("**🏆 WINS**")
                    for w in wins[-5:]:
                        st.caption(f"{w['company']} → {w['stage']}")
                        st.write(f"*{w['what_worked'][:50]}...*" if len(w['what_worked']) > 50 else f"*{w['what_worked']}*")
                
                with hist_cols[1]:
                    st.markdown("**📉 LOSSES**")
                    for l in losses[-5:]:
                        st.caption(f"{l['company']}")
                        st.write(f"*{l['reason'][:50]}...*" if len(l['reason']) > 50 else f"*{l['reason']}*")
        
        # ═══════════════════════════════════════════════════════════════
        # TAB 4: NETWORK BUILDER (NEW!)
        # ═══════════════════════════════════════════════════════════════
        with crm_tab8:
            st.markdown("### 🔗 NETWORK BUILDER")
            st.caption("Strengthen relationships. Get warm intros. Build your network systematically.")
            
            network_sub_tab1, network_sub_tab2, network_sub_tab3 = st.tabs([
                "📊 NETWORK HEALTH", "📝 OUTREACH TEMPLATES", "🚀 INTRO REQUESTS"
            ])
            
            # --- NETWORK HEALTH ---
            with network_sub_tab1:
                st.markdown("#### 📊 RELATIONSHIP STRENGTH ANALYSIS")
                
                contacts = st.session_state.get('crm_contacts', [])
                
                # Count by strength
                strength_counts = {
                    "❄️ Cold (🔗)": sum(1 for c in contacts if c.get('Strength', '🔗') == '🔗'),
                    "🌤️ Warm (🔗🔗)": sum(1 for c in contacts if c.get('Strength', '') == '🔗🔗'),
                    "🔥 Strong (🔗🔗🔗)": sum(1 for c in contacts if '🔗🔗🔗' in c.get('Strength', '') and '🔗🔗🔗🔗' not in c.get('Strength', '')),
                    "💪 Very Strong (🔗🔗🔗🔗)": sum(1 for c in contacts if '🔗🔗🔗🔗' in c.get('Strength', '') and '🔗🔗🔗🔗🔗' not in c.get('Strength', '')),
                    "👑 Champion (🔗🔗🔗🔗🔗)": sum(1 for c in contacts if '🔗🔗🔗🔗🔗' in c.get('Strength', '')),
                }
                
                for level, count in strength_counts.items():
                    st.metric(level, count)
                
                st.markdown("---")
                
                # Contacts needing attention
                st.markdown("#### ⚠️ NEEDS ATTENTION (Cold Contacts)")
                cold_contacts = [c for c in contacts if c.get('Strength', '🔗') == '🔗']
                
                if cold_contacts:
                    for c in cold_contacts[:5]:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{c['Name']}** @ {c['Company']}")
                            st.caption(f"Last: {c.get('Last Touch', 'Never')}")
                        with col2:
                            if st.button(f"📧 Warm Up", key=f"warm_{c['Name']}"):
                                st.session_state['warmup_target'] = c
                else:
                    st.success("✅ No cold contacts! Great networking.")
                
                st.markdown("---")
                
                # Champions who can help
                st.markdown("#### 👑 YOUR CHAMPIONS")
                champions = [c for c in contacts if '🔗🔗🔗🔗🔗' in c.get('Strength', '')]
                
                if champions:
                    for c in champions:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 1px solid #ffd700; border-radius: 8px; padding: 12px; margin: 8px 0;">
                            <p style="color: #ffd700; margin: 0;"><b>{c['Name']}</b> @ {c['Company']}</p>
                            <p style="color: #8892b0; font-size: 0.8rem; margin: 4px 0 0 0;">Can intro you to: {c.get('Sector', 'General')} companies</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Build your first champion by strengthening 1 relationship to 🔗🔗🔗🔗🔗")
            
            # --- OUTREACH TEMPLATES ---
            # --- COMMS STUDIO (Formerly Outreach Templates) ---
            with network_sub_tab2:
                st.markdown("#### 📣 COMMS STUDIO")
                st.caption("Precision-engineered scripts for every channel.")
                
                # 1. STRATEGY CONFIGURATION
                c_conf1, c_conf2 = st.columns(2)
                with c_conf1:
                    comms_channel = st.selectbox("📡 Channel", ["🟦 LinkedIn", "📧 Email", "📞 Phone / Voice", "📱 SMS / Text", "🚁 Guerrilla / Creative"])
                with c_conf2:
                    comms_tone = st.selectbox("🎭 Tone", ["Professional (Safe)", "Casual (Startup)", "The Challenger (Bold)"])

                # 2. SCENARIO SELECTION (Dynamic)
                scenarios = []
                if comms_channel == "🟦 LinkedIn":
                    scenarios = ["🤝 Connection Request (Active Hiring)", "👋 Connection Request (Peer)", "💬 DM: Reconnect (Warm)", "📣 Comment Strategy (Thought Leadership)"]
                elif comms_channel == "📧 Email":
                    scenarios = ["🧊 Cold Outreach (Hiring Manager)", "👻 Follow Up (Post-Ghosting)", "🙏 Thank You (Post-Interview)", "💼 Resignation / Transition"]
                elif comms_channel == "📞 Phone / Voice":
                    scenarios = ["⚡ Cold Call Opener (30s)", "📼 Voicemail Drop", "🛡️ Gatekeeper Bypass"]
                elif comms_channel == "📱 SMS / Text":
                    scenarios = ["📅 Confirm Meeting", "👋 Post-Event Follow Up", "👀 Quick Check-in (Warm)", "🚀 Update/News Share"]
                elif comms_channel == "🚁 Guerrilla / Creative":
                    scenarios = ["📹 Loom Video Pitch (60s)", "🕵️ The 'Audit' (Value Add)", "🧪 User Testing Feedback", "🎁 The 'Gift' Strategy"]
                
                comms_scenario = st.selectbox("🎯 Scenario", scenarios)
                
                # 3. INPUTS
                st.markdown('<div class="divider-solid"></div>', unsafe_allow_html=True)
                
                # NEW: ICP Persona Selector
                i0_col1, i0_col2 = st.columns(2)
                with i0_col1:
                    target_persona = st.selectbox("👤 Target Persona (ICP)", [
                        "🎯 Hiring Manager",
                        "🔍 Recruiter / Talent Acquisition", 
                        "👔 CEO / Founder",
                        "📈 VP of Sales / CRO",
                        "⚙️ RevOps / GTM Ops",
                        "🤝 HR / People Ops",
                        "🏗️ Investor / Board Member"
                    ])
                with i0_col2:
                    st.caption("Persona adjusts tone and talking points automatically.")
                    persona_tips = {
                        "🎯 Hiring Manager": "Focus on solving THEIR problems. Lead with outcomes.",
                        "🔍 Recruiter / Talent Acquisition": "Make THEIR job easy. Be clear on fit.",
                        "👔 CEO / Founder": "Time is precious. Lead with impact. Bold claims OK.",
                        "📈 VP of Sales / CRO": "Talk revenue. Use numbers. Peer language.",
                        "⚙️ RevOps / GTM Ops": "Talk systems, efficiency, scale. Technical credibility.",
                        "🤝 HR / People Ops": "Culture fit, team dynamics, long-term value.",
                        "🏗️ Investor / Board Member": "Strategic vision, market timing, unfair advantages."
                    }
                    st.info(f"💡 {persona_tips.get(target_persona, '')}")
                
                i1, i2 = st.columns(2)
                target_name = i1.text_input("Target Name", placeholder="e.g. Sarah Chen")
                target_company = i2.text_input("Target Company", placeholder="e.g. Anthropic")
                
                extra_context = st.text_area("Specific Context / Key Details", height=100, placeholder="e.g. They just raised Series B, I saw them on a podcast, or I want to highlight my 160% growth metric.")

                # 4. GENERATION
                if st.button("⚡ GENERATE SCRIPT", type="primary", use_container_width=True):
                    if target_name:
                        from logic.generator import generate_plain_text
                        
                        comms_prompt = f"""
                        ACT AS: Leon Basin, Director of GTM Systems (Top 1% Revenue Architect).
                        TASK: Write a {comms_channel} script for the scenario: "{comms_scenario}".
                        
                        TARGET: {target_name} at {target_company}.
                        TARGET PERSONA: {target_persona}
                        MY CONTEXT: {extra_context}
                        MY CORE STATS: 160% Pipeline Growth, $10M+ Pipeline Built.
                        
                        TONE: {comms_tone}.
                        
                        PERSONA-SPECIFIC GUIDANCE:
                        - If targeting Hiring Manager: Focus on solving their specific pain. Lead with outcomes, not credentials.
                        - If targeting Recruiter: Make it easy for them to pitch you internally. Clear value prop.
                        - If targeting CEO/Founder: Be bold. Time is precious. Lead with strategic impact.
                        - If targeting VP Sales/CRO: Speak their language. Revenue, pipeline, conversion.
                        - If targeting RevOps: Talk systems, scalability, efficiency gains.
                        
                        CONSTRAINTS:
                        - If LinkedIn Connection: Under 300 chars.
                        - If Email: Subject Line + Body. Short paragraphs.
                        - If Phone: Script format with [Pause] indicators.
                        - If SMS: Under 160 chars. Casual but crisp. No "Dear [Name]".
                        - If Guerrilla: Creative instructions + script. Focus on pattern interruption.
                        - "The Challenger" tone should be direct, quantifying the cost of inaction.
                        
                        Write only the final output. No fluff.
                        """
                        
                        model_id = st.session_state.get('selected_model_id', "llama-3.3-70b-versatile")
                        comms_output = generate_plain_text(comms_prompt, model_name=model_id)
                        st.session_state.comms_output = comms_output
                        st.session_state.comms_target_name = target_name
                        st.session_state.comms_target_company = target_company
                        st.toast(f"✨ Script generated for {target_name}!", icon="🎯")
                
                # 5. OUTPUT DISPLAY
                if st.session_state.comms_output:
                    st.markdown("---")
                    st.markdown("#### 📤 READY TO SEND")
                    
                    # Calculate character count for validation
                    char_count = len(st.session_state.comms_output)
                    
                    if comms_channel == "🟦 LinkedIn" and char_count > 300:
                        st.warning(f"⚠️ Character count: {char_count}/300 - Consider trimming for LinkedIn connection request limit.")
                    elif comms_channel == "📱 SMS / Text" and char_count > 160:
                        st.warning(f"⚠️ Character count: {char_count}/160 - May be split into multiple messages.")
                    else:
                        st.caption(f"📊 Characters: {char_count}")
                    
                    st.code(st.session_state.comms_output, language="markdown" if comms_channel != "📧 Email" else "text")
                    
                    # ACTION BUTTONS
                    action_cols = st.columns([1, 1, 1])
                    
                    with action_cols[0]:
                        # COPY TO CLIPBOARD (JavaScript Injection)
                        copy_js = f"""
                        <script>
                        function copyToClipboard() {{
                            const text = `{st.session_state.comms_output.replace('`', "'")}`;
                            navigator.clipboard.writeText(text).then(() => {{
                                alert('Copied to clipboard!');
                            }});
                        }}
                        </script>
                        <button onclick="copyToClipboard()" style="background: #FFBF00; color: black; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%;">📋 COPY</button>
                        """
                        st.markdown(copy_js, unsafe_allow_html=True)
                    
                    with action_cols[1]:
                        # OPEN IN GMAIL (mailto: link)
                        if comms_channel == "📧 Email":
                            import urllib.parse
                            subject = f"Quick question for {st.session_state.get('comms_target_name', 'you')}"
                            body = urllib.parse.quote(st.session_state.comms_output)
                            mailto_link = f"mailto:?subject={urllib.parse.quote(subject)}&body={body}"
                            st.markdown(f'<a href="{mailto_link}" target="_blank" style="display: block; background: #4285F4; color: white; text-align: center; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold;">📧 OPEN IN GMAIL</a>', unsafe_allow_html=True)
                        else:
                            st.caption("📧 Gmail (Email only)")
                    
                    with action_cols[2]:
                        # SCHEDULE MEETING (Google Calendar)
                        import urllib.parse
                        cal_title = urllib.parse.quote(f"Meeting with {st.session_state.get('comms_target_name', 'Contact')}")
                        cal_details = urllib.parse.quote(f"Follow-up on {st.session_state.get('comms_target_company', 'opportunity')}")
                        gcal_link = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={cal_title}&details={cal_details}"
                        st.markdown(f'<a href="{gcal_link}" target="_blank" style="display: block; background: #34A853; color: white; text-align: center; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold;">📅 SCHEDULE</a>', unsafe_allow_html=True)
                    
                    if comms_channel == "📧 Email":
                        st.info("💡 **Tip:** Subject lines like 'Quick question regarding [Goal]' often convert best.")
            
            # --- INTRO REQUESTS ---
            with network_sub_tab3:
                st.markdown("#### 🚀 INTRO REQUEST TRACKER")
                st.caption("Track who you've asked for intros and outcomes.")
                
                if 'intro_requests' not in st.session_state:
                    st.session_state['intro_requests'] = [
                        {"Asker": "Virginia Bowers", "Target_Company": "Mistral AI", "Status": "Pending", "Date": "Dec 1", "Outcome": ""},
                        {"Asker": "Christine Covert", "Target_Company": "OpenAI", "Status": "Intro Made", "Date": "Nov 28", "Outcome": "Got meeting with Head of Partnerships"},
                    ]
                
                st.dataframe(st.session_state['intro_requests'], use_container_width=True)
                
                st.markdown("---")
                
                # Add new intro request
                st.markdown("**➕ ADD NEW INTRO REQUEST**")
                ir_cols = st.columns([2, 2, 2])
                with ir_cols[0]:
                    new_asker = st.text_input("Who are you asking?", placeholder="e.g., Sarah Chen")
                with ir_cols[1]:
                    new_target = st.text_input("Target Company/Person", placeholder="e.g., Anthropic")
                with ir_cols[2]:
                    new_date = st.text_input("Date", placeholder="e.g., Dec 6")
                
                if st.button("➕ ADD REQUEST"):
                    if new_asker and new_target:
                        st.session_state['intro_requests'].append({
                            "Asker": new_asker,
                            "Target_Company": new_target,
                            "Status": "Pending",
                            "Date": new_date or "Today",
                            "Outcome": ""
                        })
                        st.success(f"Intro request to {new_target} via {new_asker} added!")
                        st.rerun()
        
        # ═══════════════════════════════════════════════════════════════
        # TAB 5: RECRUITERS & NETWORK (was TAB 4)
        # ═══════════════════════════════════════════════════════════════
        with crm_tab9:
            st.markdown("### 👥 RECRUITERS & NETWORK")
            st.caption("Track your recruiter relationships and network contacts.")
            
            # Initialize Recruiters
            if 'crm_recruiters' not in st.session_state:
                st.session_state['crm_recruiters'] = [
                    {"Name": "Virginia Bowers", "Agency": "Sellers Hub", "Specialty": "Enterprise SaaS", "Quality": "⭐⭐⭐⭐", "Status": "Active", "Notes": "Very responsive, quality leads"},
                    {"Name": "Gia Thomas", "Agency": "Neuco", "Specialty": "Cybersecurity", "Quality": "⭐⭐⭐⭐", "Status": "Active", "Notes": "Cyber niche recruiter"},
                    {"Name": "Luca Browning", "Agency": "Rise Technical", "Specialty": "SaaS", "Quality": "⭐⭐⭐", "Status": "Active", "Notes": "Good recruiter, candidate-first"},
                    {"Name": "Kayleigh", "Agency": "Aikido Security", "Specialty": "Internal", "Quality": "⭐⭐⭐⭐⭐", "Status": "Active", "Notes": "Internal, strong process"},
                    {"Name": "Nicole Ceranna", "Agency": "Ambient.ai", "Specialty": "Internal", "Quality": "⭐⭐⭐⭐", "Status": "Active", "Notes": "Forwarded to CFO"},
                    {"Name": "Justin Dedrickson", "Agency": "Verkada", "Specialty": "Internal", "Quality": "⭐⭐⭐", "Status": "Active", "Notes": "High volume hiring"},
                    {"Name": "Christine Covert", "Agency": "Independent", "Specialty": "GTM", "Quality": "⭐⭐⭐⭐", "Status": "Replied", "Notes": "Senior Mgr / 0-to-1 qualification"},
                    {"Name": "Kelli Hrivnak", "Agency": "Knak Digital", "Specialty": "SMB", "Quality": "⭐⭐⭐", "Status": "Connection", "Notes": "GTM Architect for SMBs"},
                ]
            
            st.dataframe(st.session_state['crm_recruiters'], use_container_width=True)
            
            st.markdown("---")
            st.markdown("#### ➕ ADD RECRUITER")
            r1, r2, r3 = st.columns(3)
            new_rec_name = r1.text_input("Recruiter Name", key="new_rec_name")
            new_rec_agency = r2.text_input("Agency/Company", key="new_rec_agency")
            new_rec_spec = r3.text_input("Specialty", key="new_rec_spec")
            
            if st.button("ADD RECRUITER", key="add_rec_btn"):
                if new_rec_name:
                    st.session_state['crm_recruiters'].append({
                        "Name": new_rec_name,
                        "Agency": new_rec_agency,
                        "Specialty": new_rec_spec,
                        "Quality": "⭐⭐⭐",
                        "Status": "New",
                        "Notes": ""
                    })
                    st.success(f"✅ Added {new_rec_name}")
                    st.rerun()
        
        # ═══════════════════════════════════════════════════════════════
        # TAB 6: COMPANY ENRICHMENT (AI AUTO-FILL) - was TAB 5
        # ═══════════════════════════════════════════════════════════════
        with crm_tab10:
            st.markdown("### 🏢 COMPANY ENRICHMENT (AI AUTO-FILL)")
            st.caption("Paste a company name or website URL → AI fills in key intel.")
            
            enrich_input = st.text_input("Company Name or Website URL", placeholder="e.g., 'Mistral AI' or 'https://mistral.ai'")
            
            if st.button("🔍 ENRICH COMPANY", type="primary", use_container_width=True):
                if enrich_input:
                    with st.spinner("Gathering intel..."):
                        from logic.generator import generate_plain_text
                        
                        prompt = f"""
                        ACT AS: A research analyst gathering company intelligence.
                        
                        TARGET: {enrich_input}
                        
                        Provide a structured intel brief with:
                        
                        **COMPANY:** [Name]
                        **SECTOR:** [Industry/vertical]
                        **STAGE:** [Seed/Series A/B/C/Public]
                        **SIZE:** [Employee count estimate]
                        **HQ:** [Location]
                        **RECENT FUNDING:** [Amount if known, or "Unknown"]
                        **KEY PAIN POINTS:** [What problems do they solve? What internal challenges might they have?]
                        **GTM SIGNAL:** [Are they hiring? Expanding? Product launch?]
                        **DECISION MAKERS TO TARGET:** [Likely titles: VP Sales, CRO, Head of GTM, etc.]
                        **TALKING POINTS FOR INTERVIEW:** [3 bullet points on how to pitch yourself]
                        
                        Be concise. Use real data if you know it.
                        """
                        
                        result = generate_plain_text(prompt, model_name=st.session_state.get('selected_model_id', 'llama-3.3-70b-versatile'))
                        
                        st.markdown("---")
                        st.markdown("### 📊 COMPANY INTEL BRIEF")
                        st.markdown(result)
                        
                        # Option to add to contacts
                        if st.button("➕ ADD TO CRM FROM THIS INTEL"):
                            st.info("Use the Contact tab to add a new contact with this company.")
        
        # ═══════════════════════════════════════════════════════════════
        # TAB 7: ARCHIVE & CLOSED - was TAB 6
        # ═══════════════════════════════════════════════════════════════
        with crm_tab11:
            st.markdown("### 📦 ARCHIVE & CLOSED")
            st.caption("Closed opportunities and archived contacts.")
            
            # Initialize Archive
            if 'crm_archive' not in st.session_state:
                st.session_state['crm_archive'] = [
                    {"Company": "Pallet", "Role": "Founding AE", "Status": "Closed", "Reason": "Candidates at offer stage"},
                    {"Company": "Valerie Health", "Role": "Founding AE", "Status": "Closed", "Reason": "Late-stage candidates"},
                    {"Company": "Serval", "Role": "AE", "Status": "Closed", "Reason": "Security requirement mismatch"},
                    {"Company": "Anthropic", "Role": "Enterprise AE", "Status": "Rejected", "Reason": "Did not pass screen"},
                    {"Company": "One Workplace", "Role": "Enterprise MDM", "Status": "Closed", "Reason": "Role expired"},
                    {"Company": "Andreessen Horowitz", "Role": "GTM Partner", "Status": "Closed", "Reason": "Requisition removed"},
                    {"Company": "Soteria", "Role": "Strategic AE", "Status": "Closed", "Reason": "No response after 3 cycles"},
                    {"Company": "Thrively", "Role": "Enterprise AE", "Status": "Archived", "Reason": "No movement after 3 weeks"},
                    {"Company": "WilsonAI", "Role": "Founding Sales Lead", "Status": "Archived", "Reason": "Founder silent"},
                    {"Company": "Whatfix", "Role": "Enterprise AE", "Status": "Archived", "Reason": "No movement after 3 weeks"},
                ]
            
            st.dataframe(st.session_state['crm_archive'], use_container_width=True)
            
            st.markdown("---")
            
            # Move to Archive from Contacts
            st.markdown("#### 🗑️ ARCHIVE A CONTACT")
            contacts = st.session_state.get('crm_contacts', [])
            contact_names = [c['Name'] for c in contacts]
            
            if contact_names:
                contact_to_archive = st.selectbox("Select contact to archive:", contact_names, key="archive_select")
                archive_reason = st.text_input("Reason for archiving:", key="archive_reason")
                
                if st.button("ARCHIVE CONTACT", type="secondary", key="archive_btn"):
                    if contact_to_archive:
                        # Find and move contact
                        for i, c in enumerate(st.session_state['crm_contacts']):
                            if c['Name'] == contact_to_archive:
                                st.session_state['crm_archive'].append({
                                    "Company": c['Company'],
                                    "Role": c['Role'],
                                    "Status": "Archived",
                                    "Reason": archive_reason or "Manually archived"
                                })
                                st.session_state['crm_contacts'].pop(i)
                                st.success(f"✅ Archived {contact_to_archive}")
                                st.rerun()
                                break
            
            st.markdown("---")
            
            # Export Option
            if st.button("📥 EXPORT ALL CRM DATA (JSON)", use_container_width=True):
                import json
                export_data = {
                    "contacts": st.session_state.get('crm_contacts', []),
                    "deals": st.session_state.get('crm_deals', []),
                    "recruiters": st.session_state.get('crm_recruiters', []),
                    "archive": st.session_state.get('crm_archive', [])
                }
                st.download_button(
                    "💾 Download Full CRM Export",
                    data=json.dumps(export_data, indent=2),
                    file_name="basin_nexus_crm_full_export.json",
                    mime="application/json"
                )

    # ==============================================================================
    # 🛡️ MODE 9: OBJECTION BANK (INTERVIEW ARMOR)
    # ==============================================================================
    elif input_mode == "🛡️ Objection Bank":
        st.markdown("## 🛡️ OBJECTION BANK (INTERVIEW ARMOR)")
        st.caption("PROTOCOL: Pre-loaded responses + AI Practice Mode for interview challenges.")
        
        # Initialize Objection Bank with MORE objections
        if 'objection_bank' not in st.session_state:
            st.session_state['objection_bank'] = {
                # Career Transition
                "Why did you leave your last role?": "I completed my mission—architecting the Revenue OS that drove 160% YoY pipeline growth. The next chapter requires a larger canvas where I can build at scale.",
                "You've been consulting recently. Are you a builder?": "I operated as a consultant to build 'Zero-to-One' engines for multiple startups quickly. But my core DNA is Ownership. I spent 2 years at Fudo and 2 years at Sense building foundations. I'm looking for my next 5-year home.",
                # Experience
                "You don't have direct experience in [X industry].": "My systems are industry-agnostic. The Revenue OS I built reduced CAC by 40% and generated $10M pipeline—that methodology transfers to any B2B SaaS environment.",
                "Why should we hire you over someone with more tenure?": "Tenure measures time; I measure impact. In 18 months, I built a GTM engine from zero that now generates 100+ qualified leads per week. I'm not looking for a job—I'm looking to build your next revenue machine.",
                # Behavioral
                "Tell me about a failure.": "Early in my career, I relied on 'sales activity' over 'sales architecture.' I was burning cycles instead of building systems. That failure taught me to think like an engineer—now I build once, scale infinitely.",
                "What's your weakness?": "I can over-engineer solutions when speed is required. I've learned to ship MVPs fast, then iterate based on data—not perfectionism.",
                # Compensation
                "You're too expensive for this role.": "I understand. Let me share what $200k gets you: A Revenue OS architect who's built $10M pipelines and 160% growth engines. My compensation is an investment in infrastructure, not just a salary line.",
                "What's your salary expectation?": "I'm targeting $180-220k base for Director-level roles, with meaningful equity. But I'm open to creative structures—I care more about the problem I'm solving than optimizing comp.",
                # Team Fit
                "You seem overqualified.": "I'm not looking for a title upgrade—I'm looking for a platform to build. I'd rather be the 'first 10' at the right company than VP at the wrong one.",
                "How do you handle conflict with leadership?": "I lead with data, not ego. When I disagreed with our CEO on GTM strategy at Fudo, I built a prototype in 2 weeks and let the metrics speak. We pivoted, and pipeline grew 160%.",
            }
        
        # Tabs for different modes
        obj_tab1, obj_tab2, obj_tab3 = st.tabs(["📖 PLAYBOOK", "🎯 PRACTICE MODE", "➕ ADD NEW"])
        
        # ═══════════════════════════════════════════════════════════════
        # TAB 1: PLAYBOOK (View All)
        # ═══════════════════════════════════════════════════════════════
        with obj_tab1:
            st.markdown("#### 📖 YOUR OBJECTION PLAYBOOK")
            st.caption(f"{len(st.session_state['objection_bank'])} objections loaded. Click to expand.")
            
            for objection, response in st.session_state['objection_bank'].items():
                with st.expander(f"❓ {objection}"):
                    st.success(f"**YOUR RESPONSE:**\n\n{response}")
                    st.caption("💡 TIP: Practice saying this out loud 3x before your interview.")
        
        # ═══════════════════════════════════════════════════════════════
        # TAB 2: PRACTICE MODE (AI Drill)
        # ═══════════════════════════════════════════════════════════════
        with obj_tab2:
            st.markdown("#### 🎯 OBJECTION PRACTICE MODE")
            st.caption("The AI will throw objections at you. Practice your response.")
            
            # Random Objection Drill
            objections_list = list(st.session_state['objection_bank'].keys())
            
            if st.button("🎲 RANDOM OBJECTION", type="primary", use_container_width=True):
                import random
                st.session_state['practice_objection'] = random.choice(objections_list)
            
            if st.session_state.get('practice_objection'):
                st.error(f"🎤 **INTERVIEWER:** \"{st.session_state['practice_objection']}\"")
                
                user_response = st.text_area("Your Response:", height=150, placeholder="Type your answer here...", key="objection_practice_response")
                
                if st.button("📊 SCORE MY RESPONSE"):
                    if user_response:
                        from logic.generator import generate_plain_text
                        
                        score_prompt = f"""
                        Evaluate this interview response on a 1-10 scale:
                        
                        OBJECTION: {st.session_state['practice_objection']}
                        RESPONSE: {user_response}
                        IDEAL RESPONSE: {st.session_state['objection_bank'][st.session_state['practice_objection']]}
                        
                        Score based on:
                        1. Confidence (1-10)
                        2. Data/Metrics used (1-10)
                        3. Story structure (1-10)
                        4. Closing strength (1-10)
                        
                        Give overall score and 2-sentence feedback.
                        """
                        
                        model_id = st.session_state.get('selected_model_id', 'llama-3.3-70b-versatile')
                        feedback = generate_plain_text(score_prompt, model_name=model_id)
                        
                        st.markdown("---")
                        st.markdown("#### 📊 AI FEEDBACK")
                        st.info(feedback)
                        
                        st.markdown("---")
                        st.markdown("#### ✅ IDEAL RESPONSE")
                        st.success(st.session_state['objection_bank'][st.session_state['practice_objection']])
        
        # ═══════════════════════════════════════════════════════════════
        # TAB 3: ADD NEW
        # ═══════════════════════════════════════════════════════════════
        with obj_tab3:
            st.markdown("#### ➕ ADD NEW OBJECTION")
            
            new_objection = st.text_input("Objection/Question", key="new_obj_input")
            new_response = st.text_area("Your Polished Response", height=150, key="new_obj_response")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("SAVE TO BANK", type="primary"):
                    if new_objection and new_response:
                        st.session_state['objection_bank'][new_objection] = new_response
                        st.success(f"✅ Added to Objection Bank!")
                        st.rerun()
            
            with col2:
                # Framework Selector for Objection Handling
                obj_framework = st.radio("Strategy:", ["PREP (Direct)", "SOAR (Strategic)", "STAR (Story)", "CIRCLE (Process)"], horizontal=True, index=0)
                
                if st.button("🤖 AI GENERATE RESPONSE"):
                    if new_objection:
                        from logic.generator import generate_plain_text
                        
                        gen_prompt = f"""
                        You are a Director-level GTM executive. Generate a confident, data-backed response to this interview objection.
                        
                        OBJECTION: {new_objection}
                        
                        FRAMEWORK TO USE: {obj_framework}
                        - PREP: Point, Reason, Example, Point (Best for rapid fire)
                        - SOAR: Situation, Obstacle, Action, Result (Best for strategic challenges)
                        - STAR: Situation, Task, Action, Result (Best for behavioral)
                        - CIRCLE: Context, Implication, Result, Complexity, Leadership, Execution (Best for process)
                        
                        Use these real achievements where relevant:
                        - 160% YoY pipeline growth at Fudo Security
                        - $10M pipeline built at Sense
                        - Partner Revenue OS that reduced CAC by 40%
                        
                        Keep it under 100 words. Be confident, not defensive. Structure it clearly.
                        """
                        
                        model_id = st.session_state.get('selected_model_id', 'llama-3.3-70b-versatile')
                        generated = generate_plain_text(gen_prompt, model_name=model_id)
                        
                        st.markdown("---")
                        st.markdown("#### 🤖 AI-GENERATED RESPONSE")
                        st.success(generated)
                        st.caption("Edit and save this response to your bank.")

    # ==============================================================================
    # 🔬 MODE 10: COMPANY INTEL (DEEP DIVE)
    # ==============================================================================
    elif input_mode == "🔬 Company Intel":
        st.markdown("## 🔬 COMPANY INTEL (DEEP DIVE)")
        st.caption("PROTOCOL: Pre-interview reconnaissance + Live News + Decision Maker Finder.")
        
        company_name = st.text_input("🎯 TARGET COMPANY NAME", placeholder="e.g., Verkada, Mistral AI, Ambient.ai")
        
        if company_name:
            st.markdown("---")
            st.markdown(f"### 📊 INTEL REPORT: {company_name.upper()}")
            
            # ═══════════════════════════════════════════════════════════════
            # SECTION 1: QUICK LINKS
            # ═══════════════════════════════════════════════════════════════
            st.markdown("#### 🔗 QUICK RECONNAISSANCE")
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.markdown(f"[🔗 LinkedIn](https://www.linkedin.com/company/{company_name.lower().replace(' ', '-')})")
            c2.markdown(f"[💰 Crunchbase](https://www.crunchbase.com/organization/{company_name.lower().replace(' ', '-')})")
            c3.markdown(f"[📰 News](https://www.google.com/search?q={company_name}+funding+news)")
            c4.markdown(f"[👥 Glassdoor](https://www.glassdoor.com/Overview/Working-at-{company_name.replace(' ', '-')}-EI_IE.htm)")
            c5.markdown(f"[📈 G2](https://www.g2.com/search?query={company_name.replace(' ', '+')})")
            
            st.markdown("---")
            
            # ═══════════════════════════════════════════════════════════════
            # SECTION 2: LIVE NEWS (HACKERNEWS)
            # ═══════════════════════════════════════════════════════════════
            st.markdown("#### 📰 LIVE NEWS (HackerNews)")
            
            try:
                import requests
                q_url = company_name.replace(' ', '%20')
                hn_url = f"https://hn.algolia.com/api/v1/search?query={q_url}&tags=story&hitsPerPage=5"
                response = requests.get(hn_url, timeout=5)
                
                if response.status_code == 200:
                    hits = response.json().get('hits', [])
                    if hits:
                        for hit in hits[:5]:
                            title = hit.get('title', 'No title')
                            url = hit.get('url') or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
                            points = hit.get('points', 0)
                            st.markdown(f"• [{title}]({url}) — {points} points")
                    else:
                        st.caption("*No recent HackerNews coverage.*")
            except Exception:
                st.caption("*Unable to fetch live news.*")
            
            st.markdown("---")
            
            # ═══════════════════════════════════════════════════════════════
            # SECTION 3: DECISION MAKER FINDER
            # ═══════════════════════════════════════════════════════════════
            st.markdown("#### 👤 DECISION MAKER FINDER")
            st.caption("Find the right people to reach out to:")
            
            dm_cols = st.columns(4)
            with dm_cols[0]:
                st.markdown(f"[🎯 VP Sales](https://www.linkedin.com/search/results/people/?keywords={company_name}%20VP%20Sales)")
            with dm_cols[1]:
                st.markdown(f"[🎯 CRO](https://www.linkedin.com/search/results/people/?keywords={company_name}%20CRO)")
            with dm_cols[2]:
                st.markdown(f"[🎯 Head of GTM](https://www.linkedin.com/search/results/people/?keywords={company_name}%20Head%20GTM)")
            with dm_cols[3]:
                st.markdown(f"[🎯 Recruiter](https://www.linkedin.com/search/results/people/?keywords={company_name}%20Recruiter)")
            
            st.markdown("---")
            
            # ═══════════════════════════════════════════════════════════════
            # SECTION 4: AI INTEL BRIEF
            # ═══════════════════════════════════════════════════════════════
            if st.button("🧠 GENERATE AI INTEL BRIEF", type="primary", use_container_width=True):
                from logic.generator import generate_plain_text
                
                with st.spinner(f"Researching {company_name}..."):
                    intel_prompt = f"""
                    Generate a pre-interview intelligence brief for {company_name}.
                    
                    Include:
                    1. **COMPANY OVERVIEW:** What they do, target market, key differentiators.
                    2. **RECENT NEWS:** Any funding rounds, product launches, or leadership changes (make educated guesses if unknown).
                    3. **GTM CHALLENGES:** What pain points would a Director of GTM Systems solve for them?
                    4. **TALKING POINTS:** 3 specific things Leon (a Revenue Architect with 160% pipeline growth) should mention to resonate with this company.
                    5. **QUESTIONS TO ASK:** 2 insightful questions that show deep understanding of their business.
                    
                    Be specific and actionable.
                    """
                    model_id = st.session_state.get('selected_model_id', "llama-3.3-70b-versatile")
                    intel_result = generate_plain_text(intel_prompt, model_name=model_id)
                    st.session_state['company_intel'] = intel_result
            
            if st.session_state.get('company_intel'):
                st.markdown(st.session_state['company_intel'])
                
                st.markdown("---")
                
                # Quick Actions
                action_cols = st.columns(3)
                with action_cols[0]:
                    if st.button("📋 Copy Intel"):
                        st.toast("Intel copied!", icon="📋")
                with action_cols[1]:
                    if st.button("🥊 Practice Interview"):
                        st.session_state['dojo_target_company'] = company_name
                        st.session_state.selected_tool_label = "🥊 Boardroom (Dojo)"
                        st.rerun()
                with action_cols[2]:
                    if st.button("➕ Add to CRM"):
                        if 'crm_deals' not in st.session_state:
                            st.session_state['crm_deals'] = []
                        st.session_state['crm_deals'].append({
                            "Company": company_name,
                            "Role": "Research",
                            "Stage": "Discovery",
                            "Priority": 2,
                            "Signal": "Intel gathered",
                            "Notes": f"Intel brief generated on {st.session_state.get('current_date', 'today')}"
                        })
                        st.toast(f"{company_name} added to CRM!", icon="✅")

    # ==============================================================================
    # 🎙️ MODE 11: LIVE ASSIST (DIGITAL TWIN PROTOCOL)
    # ==============================================================================
    elif input_mode == "🎙️ Live Assist":
        st.markdown("## 🎙️ LIVE ASSIST (DIGITAL TWIN)")
        st.caption("PROTOCOL: Real-time coaching during live interviews. The Oracle speaks with you.")
        
        # AI AVATAR DISPLAY
        avatar_col, info_col = st.columns([1, 2])
        
        with avatar_col:
            # Animated Avatar with CSS
            st.markdown("""
            <style>
            @keyframes avatar-pulse {
                0%, 100% { box-shadow: 0 0 20px rgba(255, 191, 0, 0.4); transform: scale(1); }
                50% { box-shadow: 0 0 40px rgba(255, 191, 0, 0.8); transform: scale(1.02); }
            }
            .ai-avatar {
                width: 120px;
                height: 120px;
                background: linear-gradient(135deg, #FFD700, #FFBF00);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 3rem;
                animation: avatar-pulse 2s ease-in-out infinite;
                margin: 0 auto;
            }
            </style>
            <div class="ai-avatar">🧠</div>
            <p style="text-align: center; color: #FFD700; margin-top: 12px; font-weight: bold;">THE ORACLE</p>
            <p style="text-align: center; color: #8892b0; font-size: 0.75rem;">Digital Twin v2.0</p>
            """, unsafe_allow_html=True)
        
        with info_col:
            st.markdown("""
            <div style="background: rgba(255,191,0,0.05); border: 1px solid rgba(255,191,0,0.3); border-radius: 12px; padding: 20px;">
                <p style="color: #FFBF00; margin: 0 0 8px 0; font-weight: bold;">🎭 PERSONA LOADED</p>
                <p style="color: #ccd6f6; margin: 0 0 12px 0;">Leon Basin - Director of GTM Systems</p>
                <p style="color: #8892b0; font-size: 0.85rem; margin: 0;">
                    <b>Core Metrics:</b> 160% Pipeline Growth | $10M+ Built<br>
                    <b>Specialization:</b> Revenue Architecture, GTM Systems<br>
                    <b>Mode:</b> Challenger Sale, Executive Presence
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.warning("⚡ **ACTIVE MODE:** Use during actual interviews for real-time narrative support.")
        
        # PHASE SELECTOR
        assist_phase = st.radio("INTERVIEW PHASE", 
            ["🎯 Pre-Call Prep", "🔴 LIVE (Recording)", "📊 Post-Call Debrief"],
            horizontal=True
        )
        
        st.markdown("---")
        
        # === PRE-CALL PREP ===
        if assist_phase == "🎯 Pre-Call Prep":
            st.markdown("### 🎯 PRE-CALL INTELLIGENCE")
            
            c1, c2 = st.columns(2)
            with c1:
                company = st.text_input("Company Name", placeholder="e.g., Verkada")
                interviewer = st.text_input("Interviewer Name/Role", placeholder="e.g., VP of Sales")
                interview_type = st.selectbox("Interview Type", ["Recruiter Screen", "Hiring Manager", "Final Round / CEO", "Panel"])
                
            with c2:
                # Quick Objection Reminders
                st.markdown("#### 🛡️ OBJECTION QUICK-LOAD")
                if st.session_state.get('objection_bank'):
                    for obj in list(st.session_state['objection_bank'].keys())[:3]:
                        st.caption(f"❓ {obj}")
                else:
                    st.info("Load objections from Objection Bank first.")
            
            if st.button("📋 GENERATE CALL BRIEFING", type="primary", use_container_width=True):
                from logic.generator import generate_plain_text
                
                with st.spinner("Generating briefing..."):
                    brief_prompt = f"""
                    Generate a 30-second pre-call briefing for Leon Basin.
                    
                    INTERVIEW: {interview_type} at {company} with {interviewer}
                    
                    Include:
                    1. **OPENING LINE:** A confident, specific opener that shows you know the company.
                    2. **KEY METRIC TO DROP:** When to naturally mention 160% pipeline growth.
                    3. **PREDICTED QUESTION:** One likely question based on the interview type.
                    4. **POWER PHRASE:** One sentence to use if asked "Why you?"
                    
                    Keep it punchy - this is a quick refresh before the call.
                    """
                    model_id = st.session_state.get('selected_model_id', "llama-3.3-70b-versatile")
                    briefing = generate_plain_text(brief_prompt, model_name=model_id)
                    st.markdown(briefing)
        
        # === LIVE RECORDING ===
        elif assist_phase == "🔴 LIVE (Recording)":
            st.markdown("### 🔴 LIVE INTERVIEW ASSISTANT")
            st.error("**RECORDING ACTIVE** - Speak clearly. The Oracle is listening.")
            
            # Live Telemetry Display
            tel1, tel2, tel3, tel4 = st.columns(4)
            tel1.metric("🎤 STATUS", "RECORDING", "Live")
            tel2.metric("⏱️ DURATION", "00:00", "Minutes")
            tel3.metric("📊 AGENCY SCORE", "--", "Pending")
            tel4.metric("🚨 OBJECTION ALERT", "STANDBY", "Monitoring")
            
            st.markdown("---")
            
            # Objection Trigger Keywords
            st.markdown("#### 🚨 OBJECTION TRIGGER KEYWORDS")
            st.caption("If you hear these from the interviewer, your scripted response will appear:")
            
            trigger_keywords = {
                "cost": "My systems reduce CAC by 40%. The ROI is measurable.",
                "risk": "I've successfully scaled GTM at 5+ early-stage startups. The playbook is proven.",
                "consultant": "I'm not a consultant—I'm a builder. I wrote the code that drives the pipeline.",
                "experience": "My 15 years span Google operations, startup scaling, and technical GTM. I've seen both sides.",
                "why should we": "Because I don't just run campaigns—I build the revenue engine that runs them at scale."
            }
            
            for keyword, response in trigger_keywords.items():
                with st.expander(f"🔑 If they say: '{keyword.upper()}'"):
                    st.success(f"**YOUR RESPONSE:** {response}")
            
            st.markdown("---")
            
            # Post-recording transcript
            st.markdown("#### 📝 LIVE TRANSCRIPT / POST-CALL PASTE")
            call_transcript = st.text_area(
                "Paste your call transcript or notes here after the interview:",
                height=200,
                placeholder="[After the call, paste the transcript here for analysis...]"
            )
            
            if call_transcript and st.button("🧠 ANALYZE CALL PERFORMANCE"):
                from logic.generator import generate_plain_text
                import re
                
                # Calculate metrics
                word_count = len(call_transcript.split())
                filler_words = len(re.findall(r'\b(um|uh|like|you know|basically|actually|literally)\b', call_transcript.lower()))
                metrics_mentioned = len(re.findall(r'\d+%|\$\d+|\d+[xX]|\d+\+', call_transcript))
                
                # Estimate WPM (assume 10 min call)
                estimated_wpm = word_count // 10
                
                st.session_state['live_assist_analysis'] = {
                    "word_count": word_count,
                    "filler_words": filler_words,
                    "metrics_mentioned": metrics_mentioned,
                    "wpm": estimated_wpm
                }
                
                st.success("✅ Analysis complete! Go to Post-Call Debrief.")
        
        # === POST-CALL DEBRIEF ===
        elif assist_phase == "📊 Post-Call Debrief":
            st.markdown("### 📊 POST-CALL DEBRIEF")
            
            if st.session_state.get('live_assist_analysis'):
                analysis = st.session_state['live_assist_analysis']
                
                # Scorecard
                d1, d2, d3, d4 = st.columns(4)
                d1.metric("WORDS SPOKEN", analysis['word_count'])
                d2.metric("FILLER WORDS", analysis['filler_words'], "Lower is better" if analysis['filler_words'] < 5 else "⚠️ Practice needed")
                d3.metric("METRICS DROPPED", analysis['metrics_mentioned'], "🎯 Good" if analysis['metrics_mentioned'] >= 2 else "Add more!")
                d4.metric("EST. WPM", analysis['wpm'], "Ideal: 130-150" if 130 <= analysis['wpm'] <= 150 else "Adjust pacing")
                
                st.markdown("---")
                
                # Performance Grade
                score = 50
                score += min(analysis['metrics_mentioned'] * 15, 30)
                score -= analysis['filler_words'] * 5
                score += 20 if 130 <= analysis['wpm'] <= 150 else 0
                
                if score >= 80:
                    grade = "A"
                    feedback = "🏆 EXCELLENT. You're interview-ready."
                elif score >= 60:
                    grade = "B"
                    feedback = "✅ SOLID. Polish the pacing in the Boardroom."
                else:
                    grade = "C"
                    feedback = "⚠️ NEEDS WORK. Practice filler word elimination."
                
                st.markdown(f"## PERFORMANCE GRADE: **{grade}** ({score}/100)")
                st.info(feedback)
                
                # Update Pipeline CRM suggestion
                st.markdown("---")
                st.markdown("#### 📈 PIPELINE UPDATE SUGGESTION")
                st.caption("Based on this call, update your Pipeline CRM with the new stage and follow-up action.")
            else:
                st.info("Complete a LIVE recording session first to see your debrief.")

    # ==============================================================================
    # ☁️ MODE 13: G-SUITE SYNC (The I/O Hub)
    # ==============================================================================
    elif input_mode == "☁️ G-Suite Sync":
        st.markdown("## ☁️ G-SUITE INTELLIGENCE PORTAL")
        st.caption("PROTOCOL: Securely sync LeonOS CRM (Sheets) and Sniper Arsenal (Docs) for live data processing.")
        
        st.markdown("""
        <div style="background: rgba(255, 191, 0, 0.1); border: 1px solid rgba(255, 191, 0, 0.3); border-radius: 12px; padding: 20px; margin-bottom: 20px;">
            <h4 style="color: #FFBF00; margin: 0 0 10px 0;">⚠️ SECURITY PROTOCOL</h4>
            <p style="color: #8892b0; margin: 0;">This integration requires a Google Cloud Service Account for secure access. Your data never leaves your control.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Connection Status
        gsuite_connected = st.session_state.get('gsuite_connected', False)
        
        if gsuite_connected:
            st.success("✅ G-Suite Connection: ACTIVE")
        else:
            st.warning("⚠️ G-Suite Connection: OFFLINE")
        
        st.markdown("---")
        
        # 1. GOOGLE SHEETS CRM SYNC
        st.markdown("### 1️⃣ LEONOS CRM (SHEETS) INTEGRATION")
        st.info("This connects to your **LeonOS Executive GTM CRM - TAB 2** for live pipeline reading.")
        
        col_key, col_url = st.columns(2)
        
        with col_key:
            uploaded_key = st.file_uploader(
                "Upload Google Service Account JSON Key", 
                type=['json'], 
                help="Securely links your Streamlit app to your Google Cloud Project."
            )
            if uploaded_key:
                st.session_state['gsuite_key'] = uploaded_key
                st.success("✅ Key uploaded")
        
        with col_url:
            sheet_url = st.text_input(
                "LeonOS CRM Sheet URL", 
                placeholder="https://docs.google.com/spreadsheets/d/...",
                help="URL of your master pipeline sheet."
            )
            if sheet_url:
                st.session_state['sheet_url'] = sheet_url
        
        if st.button("🔗 INITIATE SECURE SHEET SYNC", type="primary", use_container_width=True):
            if st.session_state.get('gsuite_key') and st.session_state.get('sheet_url'):
                st.session_state['gsuite_connected'] = True
                st.success("✅ Connection Protocol Initiated. Oracle Agent ready to read Pipeline Data.")
                st.toast("G-Suite Connected!", icon="☁️")
                st.balloons()
            else:
                st.error("Please upload a Service Account Key and provide a Sheet URL.")
        
        st.markdown("---")
        
        # 2. GOOGLE DOCS (SNIPER ARSENAL) SYNC
        st.markdown("### 2️⃣ SNIPER ARSENAL (DOCS) RETRIEVAL")
        st.info("PROTOCOL: The **Omni-Agent** will use this link to pull the latest version of your interview and outreach templates.")
        
        doc_url = st.text_input(
            "Sniper Arsenal Doc URL (Optional)", 
            placeholder="URL of your Master G-Doc template..."
        )
        if doc_url:
            st.session_state['doc_url'] = doc_url
            st.success("✅ Doc URL saved")
        
        st.markdown("---")
        
        # 3. INTEGRATION STATUS PANEL
        st.markdown("### 3️⃣ INTEGRATION STATUS")
        
        status_data = {
            "Service": ["Google Sheets (CRM)", "Google Docs (Templates)", "Oracle Agent"],
            "Status": [
                "🟢 Connected" if st.session_state.get('sheet_url') else "🔴 Not Connected",
                "🟢 Connected" if st.session_state.get('doc_url') else "🔴 Not Connected",
                "🟢 Active" if st.session_state.get('gsuite_connected') else "🟡 Standby"
            ],
            "Last Sync": ["Just now", "Just now", "Ready"]
        }
        
        st.dataframe(status_data, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # 4. SETUP INSTRUCTIONS
        with st.expander("📋 SETUP INSTRUCTIONS"):
            st.markdown("""
            #### How to Set Up G-Suite Integration:
            
            **Step 1: Create Google Cloud Project**
            1. Go to [Google Cloud Console](https://console.cloud.google.com)
            2. Create a new project named "BASIN-NEXUS"
            3. Enable Google Sheets API and Google Docs API
            
            **Step 2: Create Service Account**
            1. Go to IAM & Admin → Service Accounts
            2. Create a new service account
            3. Generate a JSON key and download it
            
            **Step 3: Share Your Sheet**
            1. Open your LeonOS CRM spreadsheet
            2. Share it with the service account email (found in the JSON key)
            3. Give "Editor" access
            
            **Step 4: Connect Here**
            1. Upload the JSON key file above
            2. Paste your Sheet URL
            3. Click "Initiate Secure Sheet Sync"
            
            #### Data Flow:
            ```
            LeonOS CRM Sheet → G-Suite Sync → Pipeline CRM → Oracle Analytics
            ```
            """)


    # ==============================================================================
    # 🎯 MODE: BLACK OPS AGENT (INTEL & RECON)
    # ==============================================================================
    elif input_mode == "🎯 Sniper Prospecting":
        st.markdown("""
        <h1 style='color: #FFD700;'>3. BLACK OPS AGENT (INTEL & RECON)</h1>
        """, unsafe_allow_html=True)
        
        # TABBED INTERFACE for Black Ops
        bo_tabs = st.tabs(["🕵️ CONTACT HUNTER", "⚡ SIGNAL RADAR", "🌐 360 RECON"])
        
        with bo_tabs[0]: # CONTACT HUNTER
            st.markdown("""
            <div style='background: #111; padding: 20px; border: 1px solid #333; border-radius: 10px;'>
                <h4 style='color: #FFD700; margin-top: 0;'>TARGET PARAMS</h4>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                target_name = st.text_input("Target Name", placeholder="e.g. Leon Basin")
            with c2:
                target_domain = st.text_input("Company Domain", placeholder="e.g. anthropic.com")
                
            if st.button("🔓 GENERATE INTELLIGENCE LINKS", type="primary", use_container_width=True):
                if target_name and target_domain:
                    # Mock Intelligence Generation
                    safe_name = target_name.replace(' ', '+')
                    st.success("✅ INTELLIGENCE ACQUIRED")
                    
                    st.markdown("##### ##### 🎯 DIRECT CONTACT LINKS")
                    
                    l_col1, l_col2, l_col3 = st.columns(3)
                    with l_col1:
                        st.markdown(f"""
                        <a href="https://www.google.com/search?q={safe_name}+email+{target_domain}" target="_blank" style="text-decoration: none;">
                            <div style="border: 1px solid #FFD700; padding: 10px; text-align: center; border-radius: 5px; color: #FFD700;">
                                📩 Find Email<br><span style="font-size: 0.8em; color: #888;">(Google Dorks)</span>
                            </div>
                        </a>
                        """, unsafe_allow_html=True)
                    with l_col2:
                         st.markdown(f"""
                        <a href="https://www.google.com/search?q={safe_name}+phone+number" target="_blank" style="text-decoration: none;">
                            <div style="border: 1px solid #FFD700; padding: 10px; text-align: center; border-radius: 5px; color: #FFD700;">
                                📞 Find Phone<br><span style="font-size: 0.8em; color: #888;">(TrueCaller)</span>
                            </div>
                        </a>
                        """, unsafe_allow_html=True)
                    with l_col3:
                         st.markdown(f"""
                        <a href="https://www.google.com/search?q=site:calendly.com+{safe_name}" target="_blank" style="text-decoration: none;">
                            <div style="border: 1px solid #FFD700; padding: 10px; text-align: center; border-radius: 5px; color: #FFD700;">
                                📅 Find Calendly<br><span style="font-size: 0.8em; color: #888;">(Calendar Hack)</span>
                            </div>
                        </a>
                        """, unsafe_allow_html=True)
                        
                    st.markdown("---")
                    st.markdown("##### 👤 KEY DECISION MAKERS (PREDICTED)")
                    st.markdown("**VP Sales • CRO • CTO**")
                    
        with bo_tabs[1]: # SIGNAL RADAR
            target_company = st.text_input("Target Company Ticker", placeholder="e.g. VERCEL")
        
        try:
            from logic.integrations import analyze_sniper_target
            sniper_available = True
        except ImportError:
            sniper_available = False
            
        if sniper_available:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("### 🔭 TARGET LOCK")
                target_company = st.text_input("Target Company", placeholder="e.g. Vercel")
                target_sector = st.selectbox("Sector Context", 
                    ["SaaS / DevTools", "Fintech", "HealthTech", "Agency / Services", "E-commerce", "Enterprise / Legacy"])
                
                st.info("💡 **Sniper Philosophy**\n\nDon't spray and pray. Analyze deeply. Find the pain. Pitch the specific cure.")
                
                # OPS LEAD DOJO (Quizlet Style)
                if target_company:
                    st.markdown("### 🥋 OPS LEAD DOJO")
                    if st.button("🎓 START KNOWLEDGE DRILL"):
                        st.session_state['quiz_active'] = True
                        st.toast(f"Drill Initiated for {target_company}", icon="🥋")

            with col2:
                if target_company:
                    # MOCK STOCK TICKER / FINANCIALS
                    st.markdown(f"""
                    <div style="background: #111; padding: 10px 20px; border-radius: 8px; border: 1px solid #333; display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
                        <div>
                            <span style="color: #fff; font-weight: bold; font-size: 1.2rem;">{target_company.upper()[:4]}</span>
                            <span style="color: #666; font-size: 0.8rem;"> (NYSE)</span>
                        </div>
                        <div>
                            <span style="color: #00ff88; font-weight: bold; font-size: 1.2rem;">$142.50</span>
                            <span style="color: #00ff88; font-size: 0.8rem;"> ▲ 1.2%</span>
                        </div>
                        <div style="font-size: 0.8rem; color: #888;">
                            MARKET CAP: <strong>$12.4B</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("🛰️ SATELLITE SCAN (ANALYZE)", type="primary"):
                        with st.spinner(f"Acquiring signal on {target_company}..."):
                            import time
                            time.sleep(1.5) # Simulating scan
                            analysis = analyze_sniper_target(target_company, target_sector)
                            st.session_state['sniper_intel'] = analysis
                
                # QUIZ DISPLAY
                if st.session_state.get('quiz_active'):
                    st.markdown(f"#### 🧠 KNOWLEDGE VAULT: {target_company}")
                    with st.expander("Q1: REVENUE MODEL?", expanded=True):
                        st.write("What is likely the Primary Revenue Driver for this sector?")
                        if st.button("Reveal Answer Q1"):
                             st.success(f"Usage-based pricing (Compute/Seats) typical for {target_sector}.")
                    
                    with st.expander("Q2: FOUNDER DNA?"):
                         st.write("Who founded the company and what is their ethos?")
                         if st.button("Reveal Answer Q2"):
                             st.success("Analysis required. (Check 'Company Intel' tab).")

                if 'sniper_intel' in st.session_state:
                    intel = st.session_state['sniper_intel']
                    
                    st.markdown(f"### 📡 INTEL ACQUIRED: {intel['company'].upper()}")
                    
                    # Pain Points
                    st.markdown("#### 🩸 HYPOTHESIZED PAIN POINTS")
                    for pain in intel['pain_points']:
                        st.markdown(f"- 🔴 {pain}")
                        
                    # Value Props
                    st.markdown("#### 💊 YOUR VALUE ANGLE")
                    for val in intel['value_props']:
                        st.markdown(f"- 🟢 {val}")
                        
                    # Icebreakers
                    st.markdown("#### 🧊 CONTEXTUAL ICEBREAKERS")
                    for ice in intel['icebreakers']:
                        st.code(ice, language=None)
                        
                    st.markdown("---")
                    st.markdown("#### 💌 GENERATE OUTREACH")
                    
                    outreach_type = st.radio("Strategy", ["Cold Email", "LinkedIn DM", "Video Pitch Script"], horizontal=True)
                    
                    if outreach_type == "Cold Email":
                        st.text_area("Draft", value=f"""Subject: Ideas for {intel['company']}'s GTM
                        
Hi [Name],

{intel['icebreakers'][0]}

Given you're in {target_sector}, I imagine you're seeing {intel['pain_points'][0].lower()}.

I'm building a system to solve exactly that ({intel['value_props'][0]}).

Worth a 5 min chat?

Best,
Leon""", height=250)
                    
                    elif outreach_type == "LinkedIn DM":
                        st.text_area("Draft", value=f"""Hi [Name], {intel['icebreakers'][1]}

Mental model: {intel['pain_points'][1]} -> {intel['value_props'][1]}.

Curious if this resonates?""", height=150)

                    elif outreach_type == "Video Pitch Script": 
                         st.markdown("""
                         **Scene:** Screen recording of their website.
                         
                         **Script:**
                         "Hey team! I was analyzing your {Specific Page} and noticed...
                         
                         Most companies in {Sector} struggle with {Pain Point}.
                         
                         I mocked up a solution for you here..."
                         """)


    # ==============================================================================
    # 📡 MODE 14: MARKET SENTIMENT RADAR (The Oracle Dashboard)
    # ==============================================================================
    elif input_mode == "📡 Market Radar":
        st.markdown("## 📡 SIGNAL RADAR: PROSPECTING COMMAND CENTER")
        st.caption("PROTOCOL: Aggregate Pre-Hiring Signals (Funding, Social, Jobs) → Discover → Practice.")
        
        # ═══════════════════════════════════════════════════════════════
        # OMNI-SEARCH (The "One Search to Rule Them All")
        # ═══════════════════════════════════════════════════════════════
        with st.expander("🔭 OMNI-SEARCH (Deep Dive on Target)", expanded=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                target_company = st.text_input("Target Company / Sector", placeholder="e.g. 'Mistral AI' or 'Zero Trust Startups'", key="omni_search")
            with c2:
                st.markdown("###")  # Spacing
                scan_clicked = st.button("🚀 SCAN ALL CHANNELS", use_container_width=True)

            if target_company:
                st.markdown("#### 🔗 DEEP DIVE LINKS (One-Click Intel)")
                l1, l2, l3, l4, l5 = st.columns(5)
                
                # Smart Search Strings
                q = target_company.replace(' ', '+')
                
                with l1:
                    st.markdown(f"[**💰 Crunchbase**](https://www.google.com/search?q=site:crunchbase.com+{q}+funding+series)")
                    st.caption("Check Cash Flow")
                with l2:
                    st.markdown(f"[**👔 LinkedIn**](https://www.linkedin.com/search/results/content/?keywords={q}%20hiring)")
                    st.caption("Social Signal")
                with l3:
                    st.markdown(f"[**🐸 Glassdoor**](https://www.google.com/search?q=site:glassdoor.com+{q}+reviews)")
                    st.caption("Culture/Churn")
                with l4:
                    st.markdown(f"[**🤖 Reddit**](https://www.reddit.com/search/?q={q}+hiring)")
                    st.caption("Dev Chatter")
                with l5:
                    st.markdown(f"[**🐦 Twitter/X**](https://twitter.com/search?q={q}+hiring&src=typed_query)")
                    st.caption("Real-Time")
                
                # PRACTICE THIS COMPANY BUTTON (Discovery → Practice Loop)
                st.markdown("---")
                practice_col1, practice_col2 = st.columns([2, 1])
                with practice_col1:
                    st.info(f"🎯 **Ready to practice for {target_company}?** Simulate an interview with their cultural profile.")
                with practice_col2:
                    if st.button("🥊 ENTER DOJO", use_container_width=True, key="practice_target"):
                        # Save target for Dojo
                        st.session_state['dojo_target_company'] = target_company
                        st.session_state.selected_tool_label = "🥊 Boardroom (Dojo)"
                        st.rerun()
        
        st.markdown("---")
        
        # ═══════════════════════════════════════════════════════════════
        # LIVE SIGNAL STREAM (RSS AGGREGATOR)
        # ═══════════════════════════════════════════════════════════════
        st.markdown("### 🌊 LIVE SIGNAL STREAM (PRE-HIRING INDICATORS)")
        
        feeds = {
            "💰 VC & Funding (TechCrunch)": "https://techcrunch.com/category/startups/feed/",
            "🔥 Y Combinator (Who is Hiring)": "https://news.ycombinator.com/rss",
            "🤖 AI & Tech Trends (Wired)": "https://www.wired.com/feed/category/business/latest/rss",
        }
        
        selected_feed = st.selectbox("Select Signal Frequency:", list(feeds.keys()))
        
        try:
            import feedparser
            with st.spinner(f"Intercepting {selected_feed}..."):
                feed_data = feedparser.parse(feeds[selected_feed])
                st.caption(f"📡 Signal Strength: {len(feed_data.entries)} active items detected.")
                
                for entry in feed_data.entries[:8]:
                    with st.container():
                        st.markdown(f"##### [{entry.title}]({entry.link})")
                        published = entry.get('published', 'Unknown Date')
                        st.caption(f"🗓️ {published}")
                        st.divider()
        except ImportError:
            st.warning("⚠️ `feedparser` not installed. Using mock data.")
        except Exception as e:
            st.warning(f"Signal interference: {e}. Falling back to mock data.")
        
        st.markdown("---")
        
        # ═══════════════════════════════════════════════════════════════
        # PRE-HIRING SIGNAL DECODER
        # ═══════════════════════════════════════════════════════════════
        with st.expander("🕵️ PRE-HIRING SIGNAL DECODER (CHEAT SHEET)"):
            st.markdown("""
            **How to spot the job before it's posted:**
            
            * **Series B/C Funding:** Sales team doubles in 90 days. *Action: Pitch the VP of Sales immediately.*
            * **New CTO/VP Engineering:** New tech stack coming. *Action: Pitch "GTM Systems" to align with new tech.*
            * **"We are overwhelmed" on Reddit:** Support/Devs are drowning. *Action: Pitch "Efficiency/Process" role.*
            * **Competitor Layoffs:** Talent is moving. *Action: Look for the company *absorbing* that talent.*
            """)
        
        st.markdown("---")
        
        # ═══════════════════════════════════════════════════════════════
        # GLOBAL SEARCH AGGREGATOR (Search Across Platforms)
        # ═══════════════════════════════════════════════════════════════
        st.markdown("### 🔍 GLOBAL SEARCH AGGREGATOR")
        st.caption("Search across HackerNews, Reddit, X, and Google from one place.")
        
        search_query = st.text_input("🌐 Search the Digital Ether", placeholder="e.g. 'AI Agent trends 2025' or 'Series B startup hiring'", key="global_search")
        
        if search_query:
            q_encoded = search_query.replace(' ', '+')
            q_url = search_query.replace(' ', '%20')
            
            # Quick Links Row
            st.markdown("#### 🔗 SEARCH ALL CHANNELS")
            link_cols = st.columns(5)
            
            with link_cols[0]:
                st.markdown(f"[**🔥 HackerNews**](https://hn.algolia.com/?q={q_url})")
            with link_cols[1]:
                st.markdown(f"[**🤖 Reddit**](https://www.reddit.com/search/?q={q_url})")
            with link_cols[2]:
                st.markdown(f"[**🐦 X/Twitter**](https://twitter.com/search?q={q_url})")
            with link_cols[3]:
                st.markdown(f"[**🔍 Google**](https://www.google.com/search?q={q_encoded})")
            with link_cols[4]:
                st.markdown(f"[**💼 LinkedIn**](https://www.linkedin.com/search/results/content/?keywords={q_url})")
            
            st.markdown("---")
            
            # HackerNews Live Search (Free Algolia API)
            st.markdown("#### 🔥 HACKERNEWS LIVE RESULTS")
            
            try:
                import requests
                
                with st.spinner("Scanning HackerNews..."):
                    hn_url = f"https://hn.algolia.com/api/v1/search?query={q_url}&tags=story&hitsPerPage=10"
                    response = requests.get(hn_url, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        hits = data.get('hits', [])
                        
                        if hits:
                            st.caption(f"📡 Found {len(hits)} discussions")
                            
                            for hit in hits[:8]:
                                title = hit.get('title', 'No Title')
                                url = hit.get('url') or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
                                points = hit.get('points', 0)
                                comments = hit.get('num_comments', 0)
                                author = hit.get('author', 'anon')
                                
                                st.markdown(f"**[{title}]({url})**")
                                st.caption(f"⬆️ {points} pts | 💬 {comments} comments | 👤 {author}")
                                st.divider()
                        else:
                            st.info("No HackerNews discussions found for this query.")
                    else:
                        st.warning("HackerNews API unavailable. Use the direct links above.")
                        
            except Exception as e:
                st.warning(f"Search error: {e}. Use the direct links above.")
        
        st.markdown("---")
        
        # Hero Stats Bar (Original)
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        with col_m1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 1px solid #00ff8833; border-radius: 12px; padding: 20px; text-align: center;">
                <p style="color: #8892b0; font-size: 0.8rem; margin: 0;">MARKET HEALTH</p>
                <h2 style="color: #00ff88; margin: 8px 0 0 0;">72/100</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 1px solid #ffd70033; border-radius: 12px; padding: 20px; text-align: center;">
                <p style="color: #8892b0; font-size: 0.8rem; margin: 0;">HIRING VELOCITY</p>
                <h2 style="color: #ffd700; margin: 8px 0 0 0;">MODERATE</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 1px solid #00d4ff33; border-radius: 12px; padding: 20px; text-align: center;">
                <p style="color: #8892b0; font-size: 0.8rem; margin: 0;">GTM DEMAND</p>
                <h2 style="color: #00d4ff; margin: 8px 0 0 0;">&uarr; +12%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m4:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 1px solid #ff6b6b33; border-radius: 12px; padding: 20px; text-align: center;">
                <p style="color: #8892b0; font-size: 0.8rem; margin: 0;">COMPETITION</p>
                <h2 style="color: #ff6b6b; margin: 8px 0 0 0;">HIGH</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Main Radar Dashboard (Original Tabs)
        radar_tab1, radar_tab2, radar_tab3 = st.tabs(["📰 HEADLINE INTEL", "🎭 SENTIMENT MAP", "🎯 OPPORTUNITY SIGNALS"])
        
        with radar_tab1:
            st.markdown("### 📰 FINANCIAL HEADLINE INTELLIGENCE")
            st.caption("Real-time synthesis of WSJ, Bloomberg, and TechCrunch for revenue-relevant signals.")
            
            # Mock Headlines (replace with real API integration)
            headlines_data = [
                {
                    "source": "WSJ",
                    "headline": "Tech Layoffs Slow as AI Hiring Surges",
                    "signal": "🟢 POSITIVE",
                    "implication": "Companies stabilizing; new AI-GTM roles opening",
                    "timestamp": "2 hours ago"
                },
                {
                    "source": "Bloomberg",
                    "headline": "Series A Funding Rebounds in Q4",
                    "signal": "🟢 POSITIVE",
                    "implication": "Early-stage startups will need GTM architects",
                    "timestamp": "4 hours ago"
                },
                {
                    "source": "TechCrunch",
                    "headline": "SaaS Valuations Under Pressure",
                    "signal": "🟡 NEUTRAL",
                    "implication": "Focus on efficiency-driven roles (RevOps, Growth)",
                    "timestamp": "6 hours ago"
                },
                {
                    "source": "LinkedIn",
                    "headline": "Revenue Operations Hiring Up 34% YoY",
                    "signal": "🟢 POSITIVE",
                    "implication": "Your systems-thinking skillset is in demand",
                    "timestamp": "1 day ago"
                },
            ]
            
            for item in headlines_data:
                st.markdown(f"""
                <div style="background: rgba(255, 191, 0, 0.05); border-left: 3px solid rgba(255, 191, 0, 0.4); padding: 15px; margin: 10px 0; border-radius: 0 8px 8px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #8892b0; font-size: 0.8rem;">{item['source']} · {item['timestamp']}</span>
                        <span style="font-size: 0.8rem;">{item['signal']}</span>
                    </div>
                    <h4 style="color: #fff; margin: 8px 0;">{item['headline']}</h4>
                    <p style="color: #FFBF00; font-size: 0.85rem; margin: 0;">→ {item['implication']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Refresh Button
            if st.button("🔄 REFRESH INTEL FEED", use_container_width=True):
                st.toast("Scanning financial feeds...", icon="📡")
                st.rerun()
        
        with radar_tab2:
            st.markdown("### 🎭 JOB SEEKER SENTIMENT MAP")
            st.caption("Analyzing Reddit, Blind, and Twitter for real-time market psychology.")
            
            # Sentiment Categories
            sent_col1, sent_col2 = st.columns(2)
            
            with sent_col1:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 1px solid rgba(255, 107, 107, 0.3); border-radius: 12px; padding: 20px;">
                    <h4 style="color: #ff6b6b; margin: 0 0 15px 0;">🔥 PAIN POINTS (Reddit /r/jobs)</h4>
                    <ul style="color: #8892b0; margin: 0; padding-left: 20px; line-height: 1.8;">
                        <li>"Ghosted after 5 rounds" (342 upvotes)</li>
                        <li>"Applied to 200 jobs, 3 callbacks" (891 upvotes)</li>
                        <li>"Lowballed on salary after layoff" (567 upvotes)</li>
                        <li>"AI tools making resumes generic" (223 upvotes)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with sent_col2:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 1px solid rgba(0, 255, 136, 0.3); border-radius: 12px; padding: 20px;">
                    <h4 style="color: #00ff88; margin: 0 0 15px 0;">💎 BRIGHT SPOTS (Success Stories)</h4>
                    <ul style="color: #8892b0; margin: 0; padding-left: 20px; line-height: 1.8;">
                        <li>"Landed GTM role at Series A" (156 upvotes)</li>
                        <li>"Referral networks still work" (423 upvotes)</li>
                        <li>"AI skills = instant callbacks" (289 upvotes)</li>
                        <li>"Niche expertise > generic apps" (178 upvotes)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("")
            
            # Sentiment Meter
            st.markdown("#### 📊 OVERALL MARKET SENTIMENT")
            sentiment_score = 42  # 0-100 scale
            st.progress(sentiment_score / 100)
            
            if sentiment_score < 30:
                sentiment_label = "🔴 PESSIMISTIC — High anxiety, longer search cycles"
            elif sentiment_score < 60:
                sentiment_label = "🟡 CAUTIOUS — Market uncertainty, strategic patience required"
            else:
                sentiment_label = "🟢 OPTIMISTIC — Hiring momentum building"
            
            st.caption(sentiment_label)
            
            # Insight Box
            st.markdown("""
            <div style="background: rgba(255, 191, 0, 0.1); border: 1px solid rgba(255, 191, 0, 0.3); border-radius: 12px; padding: 20px; margin-top: 20px;">
                <h4 style="color: #FFBF00; margin: 0 0 10px 0;">🧠 ORACLE INSIGHT</h4>
                <p style="color: #e6e8eb; margin: 0;">Current sentiment is <strong>cautiously pessimistic</strong>. This creates an opportunity: companies that ARE hiring face less competition for top talent. Position yourself as a <strong>systems-builder</strong>, not a job-seeker. The "I can architect your revenue engine" narrative cuts through the noise.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with radar_tab3:
            st.markdown("### 🎯 OPPORTUNITY SIGNALS")
            st.caption("AI-detected patterns indicating prime hiring windows.")
            
            # Opportunity Cards
            opp_col1, opp_col2, opp_col3 = st.columns(3)
            
            with opp_col1:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 255, 136, 0.05)); border: 1px solid rgba(0, 255, 136, 0.3); border-radius: 12px; padding: 20px;">
                    <h4 style="color: #00ff88; margin: 0 0 10px 0;">🚀 SECTOR: AI/ML INFRA</h4>
                    <p style="color: #8892b0; font-size: 0.85rem; margin: 0 0 10px 0;">Funding surge detected. GTM roles opening at:</p>
                    <ul style="color: #fff; margin: 0; padding-left: 20px;">
                        <li>Perplexity AI</li>
                        <li>Groq</li>
                        <li>Anthropic</li>
                    </ul>
                    <p style="color: #00ff88; font-size: 0.8rem; margin: 10px 0 0 0;">SIGNAL STRENGTH: ████████░░ 80%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with opp_col2:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 215, 0, 0.05)); border: 1px solid rgba(255, 215, 0, 0.3); border-radius: 12px; padding: 20px;">
                    <h4 style="color: #ffd700; margin: 0 0 10px 0;">📈 SECTOR: DEVTOOLS</h4>
                    <p style="color: #8892b0; font-size: 0.85rem; margin: 0 0 10px 0;">PLG → Enterprise pivot = GTM buildout:</p>
                    <ul style="color: #fff; margin: 0; padding-left: 20px;">
                        <li>Vercel</li>
                        <li>Railway</li>
                        <li>Supabase</li>
                    </ul>
                    <p style="color: #ffd700; font-size: 0.8rem; margin: 10px 0 0 0;">SIGNAL STRENGTH: ██████░░░░ 60%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with opp_col3:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0, 212, 255, 0.05)); border: 1px solid rgba(0, 212, 255, 0.3); border-radius: 12px; padding: 20px;">
                    <h4 style="color: #00d4ff; margin: 0 0 10px 0;">💼 SECTOR: FINTECH</h4>
                    <p style="color: #8892b0; font-size: 0.85rem; margin: 0 0 10px 0;">Rate cuts = lending startup revival:</p>
                    <ul style="color: #fff; margin: 0; padding-left: 20px;">
                        <li>Ramp</li>
                        <li>Mercury</li>
                        <li>Brex</li>
                    </ul>
                    <p style="color: #00d4ff; font-size: 0.8rem; margin: 10px 0 0 0;">SIGNAL STRENGTH: ██████████ 90%</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Generate Custom Intel Button
            st.markdown("#### 🧬 GENERATE CUSTOM INTEL REPORT")
            
            radar_target = st.text_input("Enter target sector or company:", placeholder="e.g., 'Series B SaaS companies in healthcare'")
            
            if st.button("🔬 ANALYZE MARKET SIGNALS", type="primary", use_container_width=True):
                if radar_target:
                    with st.spinner("Oracle Agent scanning market signals..."):
                        import time
                        time.sleep(2)
                        
                        st.success("✅ Intel Report Generated")
                        st.markdown(f"""
                        <div style="background: rgba(255, 191, 0, 0.08); border: 1px solid rgba(255, 191, 0, 0.3); border-radius: 12px; padding: 20px; margin-top: 15px;">
                            <h4 style="color: #FFBF00; margin: 0 0 15px 0;">📊 INTEL REPORT: {radar_target.upper()}</h4>
                            <p style="color: #e6e8eb;"><strong>Market Conditions:</strong> The {radar_target} sector is showing moderate growth signals with Q1 2025 funding announcements expected.</p>
                            <p style="color: #e6e8eb;"><strong>Hiring Patterns:</strong> Companies in this space are prioritizing RevOps and GTM leadership roles as they scale past $10M ARR.</p>
                            <p style="color: #e6e8eb;"><strong>Recommended Approach:</strong> Position your "Revenue OS" narrative. Emphasize systems-thinking over campaign execution.</p>
                            <p style="color: #00ff88; margin-top: 15px;"><strong>CONFIDENCE LEVEL: HIGH (78%)</strong></p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Enter a target sector or company to analyze.")

    # ═══════════════════════════════════════════════════════════════
    # ═══════════════════════════════════════════════════════════════
    # MODE: 📣 SOCIAL COMMAND CENTER
    # ═══════════════════════════════════════════════════════════════
    elif input_mode == "📣 Social Command Center":
        st.markdown("## 📣 SOCIAL COMMAND CENTER")
        st.caption("PROTOCOL: X-First Distribution · Global Vibe Network · Audience Building")
        
        # Import integrations
        try:
            from logic.integrations import (
                generate_x_thread, generate_multi_platform_content,
                VIBE_COMMUNITIES, SOCIAL_PROFILES,
                generate_waitlist_cta, ALL_COUNTRIES, REMOTE_HUBS,
                BUSINESS_MODELS, PRICING_IDEAS, CONTENT_IDEAS,
                calculate_reputation_score, generate_community_content,
                generate_leon_posts, get_build_stats,
                generate_scroll_content, ChessBattle,
                generate_chess_update
            )
            integrations_loaded = True
        except ImportError:
            st.error("⚠️ Signal Engine Integrations not found. Some features may be limited.")
            integrations_loaded = False
            
        if integrations_loaded:
            # Load real stats
            real_stats = get_build_stats()
            
            # Stats & Overview
            st.markdown("### 📊 SIGNAL STRENGTH")
            stat_cols = st.columns(4)
            stat_cols[0].metric("Build Time", f"{real_stats['hours_coded']}h", "ACTIVE")
            stat_cols[1].metric("X Vibe Score", "High", "🔥")
            stat_cols[2].metric("Global Reach", len(ALL_COUNTRIES), "Countries")
            stat_cols[3].metric("Waitlist", "Beta", "Open")
            
            st.markdown("---")
            
            # Main Tabs
            social_tabs = st.tabs([
                "🖤 POST FORGE",
                "♟️ GRANDMASTER",
                "🧵 THREAD WEAVER", 
                "📡 OMNI-CHANNEL", 
                "✨ VIBE NETWORK", 
                "🏘️ COMMUNITY",
                "🗣️ VOICE & REP",
                "📧 JOIN BETA", 
                "🌍 GLOBAL HQ",
                "🛡️ RED TEAM"
            ])
            
            # TAB 0: BASIN POST FORGE
            with social_tabs[0]:
                st.markdown("#### 🖤 BASIN POST FORGE (SCROLLSMITH)")
                st.caption("Generate artifacts in the exact @basin_leon voice.")
                
                # Mode Selection
                forge_mode = st.radio("Forge Protocol", ["🐦 Micropost (X)", "📜 The Ancient Scroll (Long Form)", "📧 Substack (Newsletter)"], horizontal=True)
                
                if forge_mode == "🐦 Micropost (X)":
                    forge_col1, forge_col2 = st.columns([2, 1])
                    
                    with forge_col1:
                        forge_topic = st.text_area("Topic / Spark / Hook", height=120, 
                            placeholder="e.g. Just shipped v0.3 of LeonOS in a 16-hour flow state\nor\nWhy most GTM advice is dead on arrival")
                        
                        if st.button("🔥 FORGE POSTS", type="primary"):
                            if forge_topic:
                                with st.spinner("Scrollsmith is writing..."):
                                    posts = generate_leon_posts(forge_topic)
                                    st.session_state['forged_posts'] = posts
                            else:
                                st.warning("Give me a spark.")
                                
                    with forge_col2:
                        st.info("🎙️ **Voice Protocol**\n\n- Zero-trust metaphors\n- Calm commander tone\n- No hype-bro language\n- Signature terms: Signal, Runway, Scrollsmith")
                    
                    if 'forged_posts' in st.session_state:
                        st.markdown("---")
                        st.markdown("### 🔥 FORGED ARTIFACTS")
                        st.markdown(st.session_state['forged_posts'].replace("1.", "**1.**").replace("2.", "\n\n**2.**").replace("3.", "\n\n**3.**"))
                        
                        # Intent links for quick posting
                        try:
                            # Extract post 1 roughly (assuming standard format)
                            post1 = st.session_state['forged_posts'].split("1.")[1].split("2.")[0].strip()
                            import urllib.parse
                            intent_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(post1)}"
                            st.markdown(f"[🚀 **POST #1 NOW**]({intent_url})")
                        except Exception:
                            pass  # Post parsing optional
                            
                elif forge_mode == "📧 Substack (Newsletter)":
                    st.info("PROTOCOL: Generates a full markdown draft ready for basinleon.com")
                    ss_topic = st.text_input("Newsletter Topic", placeholder="e.g. The Death of the Resume")
                    
                    if st.button("📝 DRAFT NEWSLETTER"):
                        with st.spinner("Writing Manifesto..."):
                            # Reuse scroll content with 'report' type for structure
                            draft = generate_scroll_content(ss_topic, type="report")
                            
                            final_draft = f"""
                            # {ss_topic.upper()}
                            
                            *By Leon Basin | Sent via Basin::Nexus*
                            
                            ---
                            
                            {draft}
                            
                            ---
                            
                            [Subscribe to the Signal](https://basinleon.com)
                            """
                            st.text_area("Substack Markdown", value=final_draft, height=400)
                            st.download_button("📥 Download .md", final_draft, file_name="newsletter.md")
                            
                else: # SCROLL MODE
                    scroll_col1, scroll_col2 = st.columns([2, 1])
                    
                    with scroll_col1:
                        scroll_topic = st.text_input("Scroll Topic", placeholder="e.g., The death of the resume and the rise of the portfolio")
                        scroll_type = st.selectbox("Artifact Type", ["journal", "play", "report", "saga"], format_func=lambda x: x.upper())
                        
                        if st.button("📜 INSCRIBE SCROLL", type="primary"):
                            if scroll_topic:
                                with st.spinner("Accessing the Ancient Library..."):
                                    scroll_content = generate_scroll_content(scroll_topic, scroll_type)
                                    st.session_state['generated_scroll'] = scroll_content
                            else:
                                st.warning("The archive requires a topic.")
                                
                    with scroll_col2:
                        st.info("🏛️ **Library Protocol**\n\n- **Journal:** Raw, first-person builder logs.\n- **Play:** Socratic dialogue.\n- **Report:** Spiritual business analysis.\n- **Saga:** Sam & Ink chapters (Surreal narrative).")

                    if 'generated_scroll' in st.session_state:
                        st.markdown("---")
                        st.markdown("### 📜 RECOVERED ARTIFACT")
                        with st.container(height=400):
                            st.markdown(st.session_state['generated_scroll'])
                        
                        st.caption("Copy this to basinleon.com")
            
            # TAB 1: GRANDMASTER STRATEGY (NEW)
            with social_tabs[1]:
                st.markdown("#### ♟️ KINETIC CHESSBOARD: FLUID GEOMETRY")
                st.caption("The Infinite Game. Build logic meets spatial intuition. A Basin::Nexus Module.")
                
                gm_col1, gm_col2 = st.columns([1.2, 1.8])
                
                with gm_col1:
                    # Metric & Visual
                    moves_made = ChessBattle.calculate_moves(real_stats['hours_coded'], real_stats['bugs_squashed'])
                    st.markdown(f"""
                    <div style="border-left: 3px solid #FFD700; padding-left: 15px; margin-bottom: 20px;">
                        <span style="color: #888; font-size: 0.8rem; letter-spacing: 1px;">MOVES ON THE BOARD</span><br>
                        <span style="color: #fff; font-size: 2.2rem; font-weight: 800; font-family: monospace;">{moves_made}</span>
                        <span style="color: #00ff88; font-size: 0.9rem;">(+{int(moves_made*0.05)} FLOW)</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.image("https://images.unsplash.com/photo-1529699211952-734e80c4d42b", caption="BASIN::NEXUS // VISUAL ARTIFACT", use_container_width=True)
                    
                with gm_col2:
                    # Strategy & Puzzle
                    strategy = ChessBattle.get_daily_strategy(real_stats['level'])
                    
                    st.markdown(f"### ⚔️ CURRENT FORM: {strategy['opening']}")
                    st.markdown(f"*{strategy['philosophy']}*")
                    
                    st.info(f"**TACTIC:** {strategy['current_tactic']}")
                    
                    # CHESS PUZZLE EMBED (Switched to Lichess for stability)
                    st.markdown("---")
                    st.caption("🧩 DAILY TACTICS PUZZLE (Train Your Pattern Recognition)")
                    import streamlit.components.v1 as components
                    # Lichess Dark Mode Frame
                    components.iframe("https://lichess.org/training/frame?theme=icpieces&bg=dark", height=450, scrolling=False)
                    
                    if st.button("♟️ LOG MOVE (SESSION COMPLETE)"):
                         st.toast("Move Recorded. Entropy Reduced.", icon="♟️")
                         
                # GTM FOCUS MATRIX
                st.markdown("---")
                gtm_col1, gtm_col2 = st.columns([3, 1])
                
                with gtm_col1:
                    st.markdown("#### 📡 GTM PENETRATION RADAR")
                    # Logic: If moves > 200, shift focus to External
                    focus_val = min(moves_made / 300.0, 1.0) # 300 moves = 100% External Focus
                    st.progress(focus_val, text="FOCUS: INTERNAL BUILD ⟷ EXTERNAL SIGNAL")
                    if focus_val < 0.5:
                        st.caption("⚠️ **STRATEGY: BUILD.** The product is the leverage. Do not sell vaporware.")
                    else:
                        st.caption("🚀 **STRATEGY: SIGNAL.** The engine is ready. Capture the eyeballs. Pay with pieces.")
                        
                with gtm_col2:
                    st.markdown("#### 📢 WAR ROOM")
                    if st.button("📣 BROADCAST", type="primary", use_container_width=True):
                        with st.spinner("Forging Battle Update..."):
                            update_posts = generate_chess_update(strategy, moves_made)
                            st.session_state['chess_update'] = update_posts
                            
                if 'chess_update' in st.session_state:
                    st.markdown(f"""
                    <div style="background: #111; border: 1px solid #333; padding: 15px; border-radius: 8px;">
                        <h4 style="color: #FFD700;">♟️ BATTLE BROADCAST GENERATED</h4>
                        <pre style="white-space: pre-wrap; font-family: monospace; color: #ccc;">{st.session_state['chess_update']}</pre>
                        <p style="text-align: right; color: #666; font-size: 0.8rem;">A BASIN::NEXUS ARTIFACT</p>
                    </div>
                    """, unsafe_allow_html=True)

            # TAB 2: THREAD WEAVER (X-First)
            with social_tabs[2]:
                st.markdown("#### 🧵 X / TWITTER THREAD GENERATOR")
                st.caption("Turn your building progress into viral threads.")
                
                # Input

                thread_col1, thread_col2 = st.columns([2, 1])
                with thread_col1:
                    thread_topic = st.text_input("Hook / Topic", placeholder="e.g., I just built a career command center in 16 hours.")
                    thread_points = st.text_area("Key Points (One per line)", height=200, 
                        placeholder="1. Most CRMs suck for job seekers\n2. I gamified the process\n3. Added live stock collection\n4. Built a networking hub\n5. Open sourcing it soon")
                    thread_cta = st.text_input("Call to Action (CTA)", value="Building in public. Follow @basinleon for the journey.")
                
                with thread_col2:
                    st.info("💡 **Vibe Tips**\n\n- Start with a strong hook (numbers/conflict)\n- Use 'I' statements\n- Keep points punchy\n- Show, don't just tell (attach screenshots)")
                    
                    if st.button("🧶 WEAVE THREAD", type="primary", use_container_width=True):
                        if thread_topic and thread_points:
                            points_list = [p.strip() for p in thread_points.split('\n') if p.strip()]
                            thread_tweets = generate_x_thread(thread_topic, points_list, thread_cta)
                            
                            st.session_state['generated_thread'] = thread_tweets
                
                # Output
                if 'generated_thread' in st.session_state:
                    st.markdown("#### 📱 THREAD PREVIEW")
                    
                    # Intent Link generator
                    full_text = "\n\n".join(st.session_state['generated_thread'])
                    import urllib.parse
                    encoded_text = urllib.parse.quote(st.session_state['generated_thread'][0])
                    intent_url = f"https://twitter.com/intent/tweet?text={encoded_text}"
                    
                    st.markdown(f"[🚀 **POST TWEET 1 NOW**]({intent_url})")
                    
                    for i, tweet in enumerate(st.session_state['generated_thread']):
                        st.text_area(f"Tweet {i+1}/{len(st.session_state['generated_thread'])}", value=tweet, height=100)
                        
                    st.success("✅ Thread ready to post!")
            
            # TAB 3: OMNI-CHANNEL DISTRIBUTION
            with social_tabs[3]:
                st.markdown("#### 📡 CONTENT DISTRIBUTION ENGINE")
                st.caption("Write once, distribute everywhere. Build your media empire.")
                
                # Content inputs
                content_topic = st.text_input("Content Topic", placeholder="Building BASIN::NEXUS")
                content_body = st.text_area("Core Content / Update", height=150, placeholder="Share your latest win, insight, or build update...")
                content_link = st.text_input("Link (optional)", value="https://basinleon.com")
                
                # Idea Generator
                with st.expander("💡 Need Content Ideas?"):
                    st.write(CONTENT_IDEAS)
                
                if st.button("🚀 GENERATE MULTI-PLATFORM ASSETS", type="primary"):
                    if content_topic and content_body:
                        assets = generate_multi_platform_content(content_topic, content_body, content_link)
                        
                        # Display results in tabs
                        p_tabs = st.tabs(["𝕏 Post", "💼 LinkedIn", "📫 Substack", "🦋 Bluesky"])
                        
                        with p_tabs[0]:
                            st.markdown("**Short Form (X)**")
                            st.code(assets['x_short'], language=None)
                            st.markdown("**Thread Hook**")
                            st.code(assets['x_thread_hook'], language=None)
                            
                        with p_tabs[1]:
                            st.markdown("**LinkedIn Post**")
                            st.code(assets['linkedin'], language=None)
                            
                        with p_tabs[2]:
                            st.markdown("**Substack Section**")
                            st.code(assets['substack_body'], language="markdown")
                            
                        with p_tabs[3]:
                            st.markdown("**Bluesky Post**")
                            st.code(assets['bluesky'], language=None)
            
            # TAB 4: VIBE NETWORK
            with social_tabs[4]:
                st.markdown("#### ✨ VIBE NETWORK FINDER")
                st.caption("Find your tribe. Connect with builders, vibe coders, and marketers.")
                
                selected_vibe = st.selectbox("Select Community", list(VIBE_COMMUNITIES.keys()), 
                                             format_func=lambda x: VIBE_COMMUNITIES[x]['name'])
                
                vibe_data = VIBE_COMMUNITIES[selected_vibe]
                
                v_col1, v_col2 = st.columns([2, 1])
                
                with v_col1:
                    st.markdown(f"### {vibe_data['name']}")
                    st.markdown(f"**Why here?** {vibe_data['why']}")
                    st.markdown(f"**Strategy:** {vibe_data['strategy']}")
                    
                    if 'accounts_to_follow' in vibe_data:
                        st.markdown("**🏆 Accounts to Follow:**")
                        for acc in vibe_data['accounts_to_follow']:
                            st.markdown(f"- {acc}")
                            
                    if 'hashtags' in vibe_data:
                        st.markdown("**🏷️ Hashtags:**")
                        st.code(" ".join(vibe_data['hashtags']))
                        
                with v_col2:
                    st.markdown("### 🎯 ACTION PLAN")
                    st.info("1. optimize profile\n2. reply to 5 top accounts\n3. post 1 insight\n4. dm 1 person")
                    
                    if 'url' in vibe_data:
                        st.markdown(f"[🔗 GO TO {vibe_data['name'].upper()}]({vibe_data['url']})")

            # TAB 5: COMMUNITY MANAGER
            with social_tabs[5]:
                st.markdown("#### 🏘️ COMMUNITY MANAGER")
                st.caption("Manage: 'Vibe Coding & Vibe Building'")
                
                comm_topic = st.text_input("Daily Topic / Theme", placeholder="e.g. Shipping Velocity")
                
                if st.button("✨ GENERATE ENGAGEMENT POSTS"):
                    posts = generate_community_content("Vibe Coding & Vibe Building", comm_topic or "Building in Public")
                    
                    c_col1, c_col2 = st.columns(2)
                    with c_col1:
                        st.markdown("**👋 Welcome Post**")
                        st.text_area("Welcome", value=posts['welcome_post'], height=150)
                        
                        st.markdown("**🧵 Daily Discussion**")
                        st.text_area("Discussion", value=posts['daily_discussion'], height=150)
                        
                    with c_col2:
                         st.markdown("**⭐ Member Spotlight**")
                         st.text_area("Spotlight", value=posts['spotlight'], height=150)
                         
                         st.markdown("**🔥 Challenge**")
                         st.text_area("Challenge", value=posts['challenge'], height=150)

            # TAB 6: VOICE & REP (TELEMETRY LAB)
            with social_tabs[6]:
                st.markdown("#### 🎙️ VOICE TELEMETRY LAB")
                st.caption("PROTOCOL: Cloud-Native Voice Recording + Executive Presence Scoring.")
                
                vt_col1, vt_col2 = st.columns([2, 1])
                
                with vt_col1:
                    # QUESTION CATEGORY
                    q_cat = st.selectbox("QUESTION CATEGORY", ["🎯 Core Pitch", "🧠 Behavioral", "💼 Case Study"], index=0)
                    
                    # DRILL SCENARIO (Dynamic)
                    if q_cat == "🎯 Core Pitch":
                        drills = [
                            "Tell me about yourself (The Pitch)",
                            "Walk me through your resume",
                            "Why are you interested in this role?",
                            "What makes you unique vs. other candidates?",
                            "Walk me through the 160% Growth metric",
                            "Where do you see yourself in 5 years?"
                        ]
                    else:
                        drills = ["Tell me about a time you failed...", "How do you handle conflict?"]
                        
                    drill = st.selectbox("SELECT DRILL SCENARIO", drills)
                    
                    st.info(f"💡 **TIP:** Speak for 45-90 seconds. Include at least one metric.")
                    
                    # RECORDING UI
                    st.markdown("""
                    <div style="background: #222; border-radius: 10px; padding: 20px; text-align: center; border: 1px dashed #444;">
                        <span style="color: #FF0000;">🔴 REC</span>
                        <h2 style="font-family: monospace; color: white;">00:00</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("🎙️ PRESS TO RECORD RESPONSE"):
                        with st.spinner("Recording Telemetry..."):
                            import time
                            time.sleep(2)
                        st.success("✅ RECORDING CAPTURED. ANALYZING WAVEFORMS...")
                        st.metric("Executive Presence Score", "88/100", "+5% vs last session")
                        
                with vt_col2:
                    st.markdown("### 📈 SESSION ANALYTICS")
                    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71", caption="VOICEPRINT ANALYSIS", use_container_width=True)
                    st.metric("Pace (WPM)", "145", "Optimal")
                    st.metric("Filler Words", "2", "-3 vs avg")
                    
                    if st.button("💾 SAVE VOICE PROFILE"):
                        st.session_state['voice_profile'] = "Recorded Session 1"
                        st.success("Voice profile updated! Future content will match this style.")
            
            # TAB 7: JOIN BETA / WAITLIST
            with social_tabs[7]:
                st.markdown("#### 📧 BETA & NEWSLETTER STRATEGY")
                st.caption("Capture interest. Build the list. Launch properly.")
                
                st.markdown(f"**Landing Page:** [{SOCIAL_PROFILES['website']}]({SOCIAL_PROFILES['website']})")
                st.markdown(f"**Newsletter:** [{SOCIAL_PROFILES['substack']}]({SOCIAL_PROFILES['substack']})")
                
                st.markdown("---")
                st.markdown("### 🎣 CALL TO ACTION GENERATOR")
                
                cta_context = st.selectbox("Context", ["twitter", "linkedin", "newsletter", "general", "referral"])
                generated_cta = generate_waitlist_cta(cta_context)
                
                st.code(generated_cta, language=None)
                
                st.markdown("---")
                st.markdown("### 💸 BUSINESS MODELS")
                
                bm_cols = st.columns(3)
                for i, (key, model) in enumerate(BUSINESS_MODELS.items()):
                    with bm_cols[i % 3]:
                        st.markdown(f"**{model['name']}**")
                        st.caption(model['description'])
                        st.markdown(f"*Examples: {', '.join(model['examples'])}*")
            
            # TAB 8: GLOBAL HQ & QUARTERLY REPORT
            with social_tabs[8]:
                st.markdown("#### 🌍 GLOBAL OPERATIONS CENTER")
                st.caption("Basin & Associates: Serving the world. No borders. Pure Signal.")
                
                st.sidebar.markdown("---")
                
                # IPO MECHANICS / STOCK TICKER
                st.markdown("### 📈 BASIN::NEXUS MARKET DATA")
                ipo_col1, ipo_col2 = st.columns([1, 2])
                
                with ipo_col1:
                    # CALCULATE "IPO READINESS" & VALUATION
                    readiness = min((real_stats['hours_coded'] * 2) + (real_stats['bugs_squashed'] * 5), 100)
                    
                    # VALUATION ALGORITHM: (Hours * $500) + (Bugs * $1000) + (Base IP Value)
                    valuation = (real_stats['hours_coded'] * 500) + (real_stats['bugs_squashed'] * 1000) + 50000
                    
                    st.metric("IPO Readiness", f"{int(readiness)}%", "+12% this week")
                    st.metric("Implied IP Valuation", f"${int(valuation):,}", "Shadow Equity")
                    st.caption("Threshold for Public Offering: $200k")
                    
                with ipo_col2:
                    st.info("💡 **Analyst Note:** Market sentiment is bullish. 'Vibe Coding' asset class is outperforming traditional SaaS.")
                
                st.markdown("---")
                
                # QUARTERLY REPORT GENERATOR
                st.markdown("### 📄 QUARTERLY REPORT GENERATOR")
                st.caption("Generate a professional 'State of the Union' for investors and potential partners.")
                
                if st.button("📄 MINT Q4 REPORT (ARTIFACT)"):
                    report_content = f"""
                    **BASIN::NEXUS // Q4 2025 INVESTOR BRIEF**
                    
                    **EXECUTIVE SUMMARY:**
                    The Firm has successfully pivoted from "Job Seeker" to "Revenue Architect." 
                    Core asset 'Basin Signal Engine' is operating at {int(readiness)}% efficiency.
                    
                    **KEY METRICS:**
                    - **Build Velocity:** {real_stats['hours_coded']} Hours Logged
                    - **Entropy Reduction:** {real_stats['bugs_squashed']} Bugs Squashed
                    - **Global Reach:** {len(ALL_COUNTRIES)} Markets Active
                    
                    **STRATEGIC OUTLOOK:**
                    We are currently executing a 'Cyber-Resonance' strategy, hacking the job market via higher dimensional signal.
                    
                    **RECOMMENDATION:**
                    BUY.
                    """
                    st.code(report_content, language="markdown")
                
                st.markdown("---")
                
                # MAP & REGIONS
                st.markdown("### 🗺️ EXPANSION TARGETS")
                # Region selector
                region = st.selectbox("Select Region Hub", list(REMOTE_HUBS.keys()))
                hub_data = REMOTE_HUBS[region]
                
                h_col1, h_col2 = st.columns(2)
                with h_col1:
                    st.markdown(f"### {region} HUB")
                    st.metric("Timezone", hub_data['timezone'])
                    st.markdown("**Key Cities:**")
                    for city in hub_data['hubs']:
                        st.markdown(f"- 🏙️ {city}")
                        
                with h_col2:
                    st.info("💡 **Global Strategy**\n\n- Async Distribution\n- Localized Pricing Models\n- 'Follow The Sun' Support\n- Global Vibe Force")

            # TAB 9: RED TEAM (CYBER-RESONANCE HACK)
            with social_tabs[9]:
                st.markdown("#### 🛡️ RED TEAM: RESONANCE HACK")
                st.caption("Practice Session: Hack your own frequency. Tune out the noise. Find the Signal.")
                
                st.markdown("---")
                
                rt_col1, rt_col2 = st.columns(2)
                
                with rt_col1:
                    st.markdown("### 🎯 SIGNAL PENETRATION TEST")
                    target_url = st.text_input("Target Asset (URL/Profile)", value="https://basinleon.com")
                    
                    if st.button("🛡️ INITIATE RESONANCE CHECK"):
                        with st.status("Analyzing Waveforms...", expanded=True) as status:
                            st.write("📡 Pinging Soul Frequency...")
                            import time
                            time.sleep(1)
                            st.write("🔍 Isolating 'Authentic Voice' vector...")
                            time.sleep(1)
                            st.write("🔓 Decrypting 'Corporate Mask' layer...")
                            time.sleep(1)
                            st.write("⚠️ Calculating Signal-to-Noise Ratio...")
                            time.sleep(0.5)
                            status.update(label="AUDIT COMPLETE", state="complete", expanded=True)
                            
                        # THE "NEW SONG" RESULT
                        st.success("✅ CORE FREQUENCY DETECTED")
                        st.markdown(f"""
                        **RESONANCE SCORE:** 98.4%
                        
                        **ANALYSIS:**
                        - You are not writing code; you are writing *ontology*.
                        - The 'Job Market' cannot read this frequency yet. You must build the translator.
                        
                        **NEXT ACTION:**
                        Write the 'Scrollsmith Manifesto'.
                        """)
                
                with rt_col2:
                    st.markdown("### 🧠 HACKING PLAYBOOK")
                    st.info("**EXPLOIT 1: RADICAL HONESTY**\nMost candidates lie. The truth is a Zero-Day Exploit.")
                    st.info("**EXPLOIT 2: BUILD IN PUBLIC**\nTransparency bypasses the 'Trust Firewall'.")
                    st.info("**EXPLOIT 3: VIBE CODING**\nLogic without Soul is deprecated. Update your kernel.")
                    
                    st.image("https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5", caption="SYSTEM OVERRIDE: SUCCESS", use_container_width=True)


# ==============================================================================
# 🖥️ SYSTEM STATUS FOOTER
# ==============================================================================
st.markdown("---")
f1, f2, f3 = st.columns([1, 1, 1])

with f1:
    st.caption("SYSTEM PROTOCOL: **ACTIVE**")
with f2:
    st.caption("ARCHITECT: **LEON BASIN**")
with f3:
    st.caption("ASSET: **REVENUE OS**")
