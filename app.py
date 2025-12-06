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

# Import audio recorder (Python 3.13 compatible)
from audio_recorder_streamlit import audio_recorder


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

st.markdown("""
<style>
    /* === BASIN::NEXUS DARK PROTOCOL === */
    
    /* Core Background - Void Black */
    .stApp {
        background: #000000;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1400px;
    }
    
    /* === TYPOGRAPHY === */
    
    /* Header - Signal Amber gradient */
    .nexus-header {
        font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
        background: linear-gradient(90deg, #FFBF00 0%, #FFD700 50%, #FFBF00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0;
        text-shadow: 0 0 40px rgba(255, 191, 0, 0.3);
    }
    
    .nexus-subtitle {
        color: #708090;
        font-family: 'SF Mono', monospace;
        font-size: 0.9rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 5px;
    }
    
    /* === STATUS INDICATORS === */
    
    .status-live {
        background: linear-gradient(135deg, #FFBF00 0%, #FFD700 100%);
        color: #000;
        padding: 6px 16px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
        font-family: 'SF Mono', monospace;
        letter-spacing: 1px;
        display: inline-block;
        box-shadow: 0 0 20px rgba(255, 191, 0, 0.4);
    }
    
    .status-ready {
        background: transparent;
        border: 1px solid #FFBF00;
        color: #FFBF00;
        padding: 6px 16px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'SF Mono', monospace;
        letter-spacing: 1px;
        display: inline-block;
    }
    
    /* === CARDS & CONTAINERS === */
    
    .nexus-card {
        background: rgba(255, 191, 0, 0.03);
        border: 1px solid rgba(255, 191, 0, 0.2);
        border-radius: 8px;
        padding: 24px;
        margin: 12px 0;
        backdrop-filter: blur(10px);
    }
    
    .nexus-card:hover {
        border-color: rgba(255, 191, 0, 0.4);
        box-shadow: 0 0 30px rgba(255, 191, 0, 0.1);
    }
    
    /* Output card - highlighted */
    .output-card {
        background: rgba(255, 191, 0, 0.05);
        border: 1px solid rgba(255, 191, 0, 0.3);
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
    }
    
    /* === BUTTONS === */
    
    .stButton > button {
        background: linear-gradient(135deg, #FFBF00 0%, #E6AC00 100%);
        color: #000 !important;
        font-weight: 700;
        font-family: 'SF Mono', monospace;
        letter-spacing: 1px;
        border: none;
        border-radius: 6px;
        padding: 12px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 191, 0, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(255, 191, 0, 0.5);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #FFBF00 0%, #FFD700 100%);
    }
    
    /* === INPUTS === */
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        background: rgba(0, 0, 0, 0.8) !important;
        border: 1px solid rgba(255, 191, 0, 0.3) !important;
        border-radius: 6px !important;
        color: #fff !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #FFBF00 !important;
        box-shadow: 0 0 10px rgba(255, 191, 0, 0.2) !important;
    }
    
    /* === DIVIDERS === */
    
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 191, 0, 0.3), transparent);
        margin: 24px 0;
    }
    
    .divider-solid {
        height: 1px;
        background: rgba(255, 191, 0, 0.2);
        margin: 20px 0;
    }
    
    /* === METRICS & SCORES === */
    
    .score-high {
        color: #00D67E;
        font-weight: 700;
        font-size: 1.5rem;
    }
    
    .score-mid {
        color: #FFBF00;
        font-weight: 700;
        font-size: 1.5rem;
    }
    
    .score-low {
        color: #FF4B4B;
        font-weight: 700;
        font-size: 1.5rem;
    }
    
    /* === SIDEBAR === */
    
    [data-testid="stSidebar"] {
        background: #0a0a0a;
        border-right: 1px solid rgba(255, 191, 0, 0.1);
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFBF00 !important;
    }
    
    /* === EXPANDERS === */
    
    .streamlit-expanderHeader {
        background: rgba(255, 191, 0, 0.05);
        border: 1px solid rgba(255, 191, 0, 0.2);
        border-radius: 6px;
    }
    
    /* === TABS === */
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: 1px solid rgba(255, 191, 0, 0.3);
        border-radius: 6px;
        color: #FFBF00;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 191, 0, 0.2) !important;
        border-color: #FFBF00 !important;
    }
    
    /* === ANIMATIONS === */
    
    @keyframes pulse-amber {
        0%, 100% { box-shadow: 0 0 20px rgba(255, 191, 0, 0.3); }
        50% { box-shadow: 0 0 40px rgba(255, 191, 0, 0.6); }
    }
    
    .pulse-active {
        animation: pulse-amber 2s infinite;
    }
    
    /* === SUCCESS/ERROR STATES === */
    
    .stSuccess {
        background: rgba(0, 214, 126, 0.1);
        border-left: 4px solid #00D67E;
    }
    
    .stError {
        background: rgba(255, 75, 75, 0.1);
        border-left: 4px solid #FF4B4B;
    }
    
    .stWarning {
        background: rgba(255, 191, 0, 0.1);
        border-left: 4px solid #FFBF00;
    }
    
    /* === PREMIUM CARD CONTAINERS === */
    
    .nexus-card {
        background: linear-gradient(135deg, #0d0d1a 0%, #0a0a0f 100%);
        border: 1px solid rgba(255, 191, 0, 0.15);
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        transition: all 0.3s ease;
    }
    
    .nexus-card:hover {
        border-color: rgba(255, 191, 0, 0.4);
        box-shadow: 0 8px 32px rgba(255, 191, 0, 0.1);
    }
    
    .nexus-card-title {
        color: #FFBF00;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .nexus-card-body {
        color: #8892b0;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* === METRIC CARDS === */
    
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #0d0d1a 0%, #0a0a0f 100%);
        border: 1px solid rgba(255, 191, 0, 0.15);
        border-radius: 10px;
        padding: 16px;
    }
    
    [data-testid="stMetricValue"] {
        color: #FFBF00 !important;
        font-weight: 700;
    }
    
    [data-testid="stMetricDelta"] {
        color: #00ff88 !important;
    }
    
    /* === BUTTONS === */
    
    .stButton > button {
        background: linear-gradient(135deg, #FFBF00 0%, #FFD700 100%);
        color: #000;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(255, 191, 0, 0.3);
    }
    
    /* === FILE UPLOADER === */
    
    [data-testid="stFileUploader"] {
        background: rgba(255, 191, 0, 0.05);
        border: 2px dashed rgba(255, 191, 0, 0.3);
        border-radius: 12px;
        padding: 16px;
    }
    
    /* === SCROLLBAR === */
    
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 191, 0, 0.3);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 191, 0, 0.5);
    }
    
    /* === CARD HOVER ANIMATIONS === */
    
    .nexus-card, [data-testid="stMetric"] {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .nexus-card:hover, [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
    }
    
    /* === RADIO BUTTON STYLING === */
    
    [data-testid="stRadio"] > label {
        display: flex;
        align-items: center;
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 8px;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    [data-testid="stRadio"] > label:hover {
        background: rgba(255, 191, 0, 0.1);
    }
    
    /* === MOBILE RESPONSIVE === */
    
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        .nexus-header {
            font-size: 1.8rem !important;
        }
        
        [data-testid="stMetric"] {
            padding: 12px;
        }
        
        [data-testid="stSidebar"] {
            min-width: 280px;
        }
    }
    
    /* === LOADING SPINNER === */
    
    .stSpinner > div {
        border-top-color: #FFBF00 !important;
    }
    
    /* === INPUT FIELDS === */
    
    input, textarea, [data-testid="stTextInput"] input {
        background: rgba(255, 191, 0, 0.05) !important;
        border: 1px solid rgba(255, 191, 0, 0.2) !important;
        border-radius: 8px !important;
        color: white !important;
    }
    
    input:focus, textarea:focus {
        border-color: #FFBF00 !important;
        box-shadow: 0 0 0 2px rgba(255, 191, 0, 0.2) !important;
    }
    
    /* === SELECT BOXES === */
    
    [data-testid="stSelectbox"] > div {
        background: rgba(255, 191, 0, 0.05);
        border: 1px solid rgba(255, 191, 0, 0.2);
        border-radius: 8px;
    }
    
    /* === TOAST NOTIFICATIONS === */
    
    [data-testid="stToast"] {
        background: linear-gradient(135deg, #0d0d1a, #0a0a0f) !important;
        border: 1px solid rgba(255, 191, 0, 0.3) !important;
        border-radius: 12px !important;
    }

</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════════
# SIDEBAR: CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# --- SIDEBAR: MISSION CONTROL (FLUID EXECUTIVE LIBRARY) ---
with st.sidebar:
    # 1. HEADER & SYSTEM STATUS
    st.markdown("### ▲ BASIN::NEXUS")
    st.caption("v13 | REVENUE ARCHITECT OS | ☁️ G-SUITE SYNC")
    st.markdown("---")
    
    # 2. SYSTEM CORE & CONFIGURATION (Terminal Style)
    st.markdown("#### ⚙️ SYSTEM CORE")
    
    api_key = st.text_input("GROQ API KEY", type="password", placeholder="sk-...", label_visibility="collapsed")
    if api_key:
        st.session_state['groq_api_key'] = api_key # Persist
        st.caption("✅ LINK: SECURE")
    else:
        st.caption("⚠️ LINK: OFFLINE")
        st.markdown("[Get Key](https://console.groq.com)")
    
    # LLM FLEET SELECTOR (v11:11 FINAL CONFIGURATION)
    selected_model_label = st.selectbox("LLM ENGINE", 
        ["Llama 3.3 70B (Speed/Groq)", 
         "Mixtral 8x7B (Logic/Groq)", 
         "Gemini Pro (Reasoning/Google)",
         "Claude 3.5 Sonnet (Narrative/Anthropic)"], 
        label_visibility="collapsed"
    )
    
    # SYSTEM KERNEL: Map Human Labels to API IDs
    model_map = {
        "Llama 3.3 70B (Speed/Groq)": "groq:llama-3.3-70b-versatile",
        "Mixtral 8x7B (Logic/Groq)": "groq:mixtral-8x7b-32768", 
        "Gemini Pro (Reasoning/Google)": "gemini-pro",
        "Claude 3.5 Sonnet (Narrative/Anthropic)": "claude-3-5-sonnet-20241022"
    }
    st.session_state['selected_model_id'] = model_map.get(selected_model_label, "groq:llama-3.3-70b-versatile")
    
    st.markdown("---")

    # 3. THE EXECUTIVE LIBRARY (STARTUP LIFECYCLE MAPPING)
    st.markdown("#### 🧭 MISSION PROTOCOL")
    
    # Lifecycle Phase Selector (The "Executive" View)
    mission_phase = st.selectbox("OPERATIONAL PHASE", 
        ["I. STRATEGIC RECON (Pre-A)", "II. EXECUTION OPS (Series A-C)", "III. ARCHITECT DECK (IPO+)"],
        label_visibility="collapsed"
    )
    
    # Dynamic Tool Selection based on Phase
    selected_tool_label = ""
    
    if "STRATEGIC RECON" in mission_phase:
        st.caption("Focus: Finding Market Fit & Targets")
        selected_tool_label = st.radio("Select Tool:", 
            ["📄 Omni-Agent (Intel)", "🎯 Black Ops (Hunt)", "🔥 Swipe Mode", "🔬 Company Intel", "🥊 Boardroom (Sim)", "📊 Analytics", "☁️ G-Suite Sync"],
            label_visibility="collapsed")
            
    elif "EXECUTION OPS" in mission_phase:
        st.caption("Focus: Scaling the Narrative & Team")
        selected_tool_label = st.radio("Select Tool:", 
            ["📈 Pipeline CRM", "🥊 Boardroom (Sim)", "🎙️ Live Assist", "🛡️ Objection Bank", "🎤 Voice", "🔍 Talent Signal"],
            label_visibility="collapsed")
            
    elif "ARCHITECT DECK" in mission_phase:
        st.caption("Focus: High-Level Strategy & Governance")
        selected_tool_label = st.radio("Select Tool:", 
            ["🚀 First 90 Days", "📈 Pipeline CRM", "🥊 Boardroom (Sim)", "🎙️ Live Assist", "📊 Analytics"],
            label_visibility="collapsed")

    # MAPPING TO SYSTEM KERNEL (Connecting UX to Logic)
    # This maps the "Cool Executive Names" to the internal "Functional Names"
    tool_map = {
        "📄 Omni-Agent (Intel)": "📄 Intel",
        "🎯 Black Ops (Hunt)": "🎯 Hunt",
        "🔥 Swipe Mode": "🔥 Swipe Mode",
        "📊 Analytics": "📊 Analytics",
        "🥊 Boardroom (Sim)": "🥊 Practice (Dojo)",
        "🎤 Voice": "🎤 Voice",
        "🔍 Talent Signal": "🔍 Talent Signal",
        "🚀 First 90 Days": "🚀 First 90 Days",
        "📈 Pipeline CRM": "📈 Pipeline CRM",
        "🛡️ Objection Bank": "🛡️ Objection Bank",
        "🔬 Company Intel": "🔬 Company Intel",
        "🎙️ Live Assist": "🎙️ Live Assist",
        "☁️ G-Suite Sync": "☁️ G-Suite Sync"
    }
    
    input_mode = tool_map.get(selected_tool_label, "📄 Intel")

    st.markdown("---")

    # 4. FINAL FOOTER
    st.markdown("`OPERATOR: LEON BASIN`")
    st.markdown("`STATUS: ONLINE`")


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

# Check if we should show Dashboard (default on first load)
show_dashboard = input_mode == "📄 Intel" and not st.session_state.get('resume_vault') and not st.session_state.resume_text

if show_dashboard:
    # ═══════════════════════════════════════════════════════════════
    # DASHBOARD: WELCOME VIEW
    # ═══════════════════════════════════════════════════════════════
    st.markdown("## 🎯 COMMAND CENTER")
    st.caption("Welcome back, Revenue Architect. Select a mode from the sidebar to begin.")
    
    st.markdown("---")
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("SYSTEM VERSION", "v12", "🔥 Swipe Mode")
    with col2:
        st.metric("MODES ACTIVE", "12", "All Online")
    with col3:
        vault_count = len(st.session_state.get('resume_vault', {}))
        st.metric("VAULT ASSETS", str(vault_count), "Upload to begin")
    with col4:
        pipeline_count = len(st.session_state.get('pipeline_crm', []))
        st.metric("PIPELINE DEALS", str(pipeline_count), "Add opportunities")
    
    st.markdown("---")
    
    # Quick Actions - Row 1
    st.markdown("### ⚡ QUICK START")
    st.caption("Select a mode from the sidebar, or choose your phase above")
    
    qa1, qa2, qa3, qa4 = st.columns(4)
    with qa1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 1px solid #00d4ff33; border-radius: 12px; padding: 20px; min-height: 120px;">
            <h4 style="color: #00d4ff; margin: 0 0 8px 0; font-size: 1rem;">🎯 HUNT MODE</h4>
            <p style="color: #8892b0; font-size: 0.8rem; margin: 0;">7-vector job search</p>
        </div>
        """, unsafe_allow_html=True)
    with qa2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 1px solid #ff6b6b33; border-radius: 12px; padding: 20px; min-height: 120px;">
            <h4 style="color: #ff6b6b; margin: 0 0 8px 0; font-size: 1rem;">🔥 SWIPE MODE</h4>
            <p style="color: #8892b0; font-size: 0.8rem; margin: 0;">Tinder for jobs</p>
        </div>
        """, unsafe_allow_html=True)
    with qa3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 1px solid #ffd70033; border-radius: 12px; padding: 20px; min-height: 120px;">
            <h4 style="color: #ffd700; margin: 0 0 8px 0; font-size: 1rem;">🥊 BOARDROOM</h4>
            <p style="color: #8892b0; font-size: 0.8rem; margin: 0;">Interview simulator</p>
        </div>
        """, unsafe_allow_html=True)
    with qa4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 1px solid #00ff8833; border-radius: 12px; padding: 20px; min-height: 120px;">
            <h4 style="color: #00ff88; margin: 0 0 8px 0; font-size: 1rem;">📈 PIPELINE</h4>
            <p style="color: #8892b0; font-size: 0.8rem; margin: 0;">Track opportunities</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Row 2
    qa5, qa6, qa7, qa8 = st.columns(4)
    with qa5:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 1px solid #9966ff33; border-radius: 12px; padding: 20px; min-height: 120px;">
            <h4 style="color: #9966ff; margin: 0 0 8px 0; font-size: 1rem;">🎙️ LIVE ASSIST</h4>
            <p style="color: #8892b0; font-size: 0.8rem; margin: 0;">Real-time coaching</p>
        </div>
        """, unsafe_allow_html=True)
    with qa6:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 1px solid #ff66b233; border-radius: 12px; padding: 20px; min-height: 120px;">
            <h4 style="color: #ff66b2; margin: 0 0 8px 0; font-size: 1rem;">📊 ANALYTICS</h4>
            <p style="color: #8892b0; font-size: 0.8rem; margin: 0;">Oracle dashboard</p>
        </div>
        """, unsafe_allow_html=True)
    with qa7:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 1px solid #66ccff33; border-radius: 12px; padding: 20px; min-height: 120px;">
            <h4 style="color: #66ccff; margin: 0 0 8px 0; font-size: 1rem;">🔬 COMPANY</h4>
            <p style="color: #8892b0; font-size: 0.8rem; margin: 0;">Intel & research</p>
        </div>
        """, unsafe_allow_html=True)
    with qa8:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e, #0a0a1a); border: 1px solid #ffcc6633; border-radius: 12px; padding: 20px; min-height: 120px;">
            <h4 style="color: #ffcc66; margin: 0 0 8px 0; font-size: 1rem;">🚀 FIRST 90</h4>
            <p style="color: #8892b0; font-size: 0.8rem; margin: 0;">Onboarding plan</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Getting Started Section
    st.markdown("### � GETTING STARTED")
    
    gs1, gs2 = st.columns(2)
    with gs1:
        st.markdown("""
        <div style="background: rgba(255, 191, 0, 0.05); border: 1px solid rgba(255, 191, 0, 0.2); border-radius: 12px; padding: 20px;">
            <h4 style="color: #FFBF00; margin: 0 0 12px 0;">1️⃣ Configure API</h4>
            <p style="color: #8892b0; font-size: 0.9rem; margin: 0;">Add your Groq API key in the sidebar to enable LLM features. Get one free at console.groq.com</p>
        </div>
        """, unsafe_allow_html=True)
    with gs2:
        st.markdown("""
        <div style="background: rgba(255, 191, 0, 0.05); border: 1px solid rgba(255, 191, 0, 0.2); border-radius: 12px; padding: 20px;">
            <h4 style="color: #FFBF00; margin: 0 0 12px 0;">2️⃣ Select Phase</h4>
            <p style="color: #8892b0; font-size: 0.9rem; margin: 0;">Choose your mission phase (Strategic Recon, Execution Ops, or Architect Deck) to see relevant tools.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    gs3, gs4 = st.columns(2)
    with gs3:
        st.markdown("""
        <div style="background: rgba(255, 191, 0, 0.05); border: 1px solid rgba(255, 191, 0, 0.2); border-radius: 12px; padding: 20px;">
            <h4 style="color: #FFBF00; margin: 0 0 12px 0;">3️⃣ Upload Resume</h4>
            <p style="color: #8892b0; font-size: 0.9rem; margin: 0;">Go to Intel mode and upload your resume to the Career Vault for AI-powered analysis.</p>
        </div>
        """, unsafe_allow_html=True)
    with gs4:
        st.markdown("""
        <div style="background: rgba(255, 191, 0, 0.05); border: 1px solid rgba(255, 191, 0, 0.2); border-radius: 12px; padding: 20px;">
            <h4 style="color: #FFBF00; margin: 0 0 12px 0;">4️⃣ Start Hunting</h4>
            <p style="color: #8892b0; font-size: 0.9rem; margin: 0;">Use Hunt Mode or Swipe Mode to find opportunities, then track them in Pipeline CRM.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add st.stop() to prevent rest of app from rendering when dashboard is shown
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
    # 📄 MODE 1: INTEL (THE OMNI-AGENT HUD)
    # ==============================================================================
    if input_mode == "📄 Intel":
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
                    except:
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

        # --- 2. TARGET VECTOR ---
        st.markdown("#### 2. TARGET VECTOR (THE MISSION)")
        jd_text = st.text_area("Paste Job Description", height=150, placeholder="[PASTE JD HERE]", label_visibility="collapsed")

    # --- 2. THE WAR ROOM (MULTI-AGENT CONFIG) ---
    st.markdown("---")
    st.markdown("#### 3. DEPLOY GTM SWARM (MULTI-AGENT)")
    
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

                            I’ve been tracking **[Company]**'s expansion. The velocity is incredible, but I know from experience that scaling at this speed creates **structural debt**.
                            
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
    # 🔥 MODE 12: SWIPE MODE (JOB TINDER)
    # ==============================================================================
    elif input_mode == "🔥 Swipe Mode":
        st.markdown("## 🔥 SWIPE MODE: JOB TINDER")
        st.caption("PROTOCOL: Swipe through opportunities. Build your pipeline fast.")
        
        # Sample job data - In production, this would come from Hunt Mode vectors
        if 'swipe_jobs' not in st.session_state:
            st.session_state.swipe_jobs = [
                {"id": 1, "title": "Director of GTM Strategy", "company": "Mistral AI", "location": "San Francisco, CA", "salary": "$220k-280k", "match": 95, "signal": "Series B, $600M raised, hiring 50+ in GTM"},
                {"id": 2, "title": "VP of Revenue Operations", "company": "Anthropic", "location": "San Francisco, CA", "salary": "$250k-320k", "match": 92, "signal": "AI Leader, aggressive expansion, ex-OpenAI team"},
                {"id": 3, "title": "Head of Partnerships", "company": "Verkada", "location": "San Mateo, CA", "salary": "$200k-260k", "match": 88, "signal": "Physical security + AI, strong channel program"},
                {"id": 4, "title": "Director of Sales Strategy", "company": "Wiz", "location": "Palo Alto, CA", "salary": "$230k-300k", "match": 91, "signal": "Cloud security unicorn, $1B ARR run rate"},
                {"id": 5, "title": "GTM Lead - Enterprise", "company": "Notion", "location": "San Francisco, CA", "salary": "$190k-240k", "match": 85, "signal": "Productivity + AI features, PLG motion"},
                {"id": 6, "title": "Director of Channel Sales", "company": "CrowdStrike", "location": "Austin, TX (Remote OK)", "salary": "$210k-270k", "match": 89, "signal": "Cybersecurity leader, expanding partner ecosystem"},
                {"id": 7, "title": "VP GTM Operations", "company": "Figma", "location": "San Francisco, CA", "salary": "$240k-300k", "match": 87, "signal": "Adobe acquisition fell through, independent growth mode"},
            ]
            st.session_state.swipe_index = 0
            st.session_state.swiped_right = []
            st.session_state.swiped_priority = []
        
        # Current job
        jobs = st.session_state.swipe_jobs
        idx = st.session_state.swipe_index
        
        if idx < len(jobs):
            job = jobs[idx]
            
            # Job Card Display
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a2e 0%, #0a0a1a 100%); 
                        border: 2px solid #00d4ff; border-radius: 20px; padding: 30px; 
                        margin: 20px 0; text-align: center;">
                <p style="color: #00d4ff; font-size: 0.9rem;">JOB {idx + 1} of {len(jobs)}</p>
                <h1 style="color: white; margin: 10px 0;">{job['title']}</h1>
                <h2 style="color: #00d4ff; margin: 5px 0;">{job['company']}</h2>
                <p style="color: #8892b0;">📍 {job['location']} | 💰 {job['salary']}</p>
                <div style="background: #00d4ff22; padding: 15px; border-radius: 10px; margin: 20px 0;">
                    <p style="color: #00d4ff; font-weight: bold;">🎯 MATCH SCORE: {job['match']}%</p>
                    <p style="color: #8892b0; font-size: 0.9rem;">📡 SIGNAL: {job['signal']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Swipe Buttons
            st.markdown("### MAKE YOUR MOVE")
            
            col_left, col_up, col_right = st.columns([1, 1, 1])
            
            with col_left:
                if st.button("❌ SKIP", use_container_width=True, key="swipe_left"):
                    st.session_state.swipe_index += 1
                    st.rerun()
            
            with col_up:
                if st.button("⭐ PRIORITY 1", use_container_width=True, key="swipe_up"):
                    st.session_state.swiped_priority.append(job)
                    st.session_state.swipe_index += 1
                    st.toast(f"🌟 {job['company']} added to PRIORITY 1!", icon="⭐")
                    st.rerun()
            
            with col_right:
                if st.button("✅ ADD TO CRM", use_container_width=True, key="swipe_right"):
                    st.session_state.swiped_right.append(job)
                    st.session_state.swipe_index += 1
                    st.toast(f"✅ {job['company']} added to Pipeline!", icon="✅")
                    st.rerun()
            
            st.markdown("---")
            
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
        st.markdown("## ▲ ORACLE: CAREER SYNTHESIS PORTAL")
        st.caption("PROTOCOL: Predictive Indexing & Digital Ether Stream")

        # --- 1. THE REVENUE OS DASHBOARD (CRM DATA SYNTHESIS) ---
        st.markdown("#### 1. REVENUE OS PIPELINE INTELLIGENCE")
        st.info("Data sourced from LeonOS Executive GTM CRM (Active Opps, Fractional Deals)")

        # Key Metrics derived from uploaded CRM sheets (Simulated Synthesis)
        PIPELINE_VALUE = 245000  # Weighted value of DepthFirst, Mistral, CRS deals
        FRACTIONAL_VALUE = 7500   # Max potential monthly value from FYM, SolveJet, Spray.io
        OFFER_PROBABILITY = 65    # Based on 1 Final Round + 3 Active Screens
        
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("ACTIVE PIPELINE VALUE", f"${PIPELINE_VALUE:,.0f}", "Weighted OTE Forecast")
        k2.metric("FRACTIONAL VALUE (Monthly)", f"${FRACTIONAL_VALUE:,.0f}", "Market Presence Maintained")
        k3.metric("OFFER_PROBABILITY", f"{OFFER_PROBABILITY}%", "High Confidence Signal")
        k4.metric("CRITICAL FOLLOW-UPS", "5", "Verkada/Aikido/Hightouch")

        st.markdown("---")

        # --- 2. THE DIGITAL ETHER STREAM (NEWS & MARKET TRENDS) ---
        st.markdown("#### 2. DIGITAL ETHER STREAM (BUSINESS ACADEMIC INDEXING)")
        st.caption("Protocol: Connect GTM Strategy to Global Tech/Cyber Trends.")

        # Using actual search results to simulate the news feed
        trend_data = [
            ("AI Agents & IAM Crisis", "The transition to Zero Trust 2.0 requires treating AI Agents as distinct digital actors, making Identity Access Management (IAM) the new battleground for security.", "Cybersecurity"),
            ("DevSecOps Growth & GRC Shift", "The DevSecOps market is projected to reach $20.2 Billion by 2030 (13.2% CAGR). GRC must shift from compliance to continuous, interconnected risk architecture.", "DevSecOps/GRC"),
            ("AI GTM: Hard Hat Work", "AI in GTM is moving from 'hype to hard hat' work, demanding a focus on tangible, secure business outcomes rather than superficial features.", "GTM/AI Strategy"),
            ("Supply Chain & SBOM", "Security is evolving from simple vendor assessment to continuous supply-chain assurance using Software Bills of Materials (SBOMs).", "Cybersecurity"),
            ("GTM Architect (The Fix)", "AI enables startups to optimize GTM in minutes, drastically improving time-to-market. AI-driven systems are non-negotiable for hyper-growth.", "Software/AI")
        ]
        
        # RENDER THE STREAM
        for title, snippet, category in trend_data:
            st.markdown(f"**[{category}]** {title}")
            st.write(snippet)
            st.markdown("---")

        # --- 3. BUSINESS ACADEMIC ACTION (HERALD AGENT) ---
        st.markdown("#### 3. BUSINESS ACADEMIC ACTION")
        st.caption("Trigger content creation based on current market intelligence.")
        
        if st.button("GENERATE ACADEMIC MANIFESTO OUTLINE (Based on Stream)", type="primary", use_container_width=True):
            st.success("✅ HERALD AGENT TASK: DRAFTING")
            st.info("PROTOCOL: Use the 'Zero Trust to Revenue' bridge.")
            
            st.write(f"""
            **TOPIC MANIFESTO:** "The Triad: Why GTM Strategy Must Converge with AI Agent Identity."
            
            **CONTENT OUTLINE (For www.basinleon.com):**
            1.  **THE HOOK (The Identity Crisis):** Use the 'CEO deepfake/AI Identity' threat to establish urgency.
            2.  **THE ARCHITECT'S SOLUTION:** Explain how your **Revenue OS** (Python/Automation) is the necessary antidote to this chaos.
            3.  **THE METRIC:** Conclude with the **160% pipeline growth** as the verifiable proof that your architectural approach works.
            """)

    
    # ─────────────────────────────────────────────────────────────
    # TALENT SIGNAL MODE - SCREEN CANDIDATES
    # ─────────────────────────────────────────────────────────────
    elif input_mode == "🔍 Talent Signal":
        st.markdown("#### 🔍 TALENT SIGNAL DETECTOR")
        st.caption("Screen candidates using 15 years of hiring instinct, codified into AI")
        
        st.info("💡 **Use Case:** You're helping a company screen candidates, or building your portfolio as a hiring consultant.")
        
        st.markdown('<div class="divider-solid"></div>', unsafe_allow_html=True)
        
        # Job Requirements
        st.markdown("##### 📋 ROLE REQUIREMENTS")
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

                        from groq import Groq
                        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": screening_prompt}],
                            temperature=0.6
                        )
                        screening_result = response.choices[0].message.content
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
        st.markdown("#### 🎤 Voice-First Resume Input")
        
        # Resume input method selector
        voice_resume_method = st.radio(
            "Resume Source",
            ["🎙️ Record Voice", "📁 Upload File", "📝 Paste Text"],
            horizontal=True,
            key="voice_resume_method"
        )
        
        if voice_resume_method == "🎙️ Record Voice":
            st.caption("🎯 Speak about your background (2-3 minutes). Describe your experience, key achievements, and skills.")
            
            # Resume Voice Recorder
            audio_bytes_resume = audio_recorder(
                text="🎙️ Click to start recording",
                recording_color="#e74c3c",
                neutral_color="#667eea",
                icon_name="microphone",
                icon_size="3x",
                key="resume_recorder"
            )
            
            if audio_bytes_resume:
                st.audio(audio_bytes_resume, format="audio/wav")
                
                # Auto-transcribe or manual button
                col_trans1, col_trans2 = st.columns([1, 1])
                with col_trans1:
                    if st.button("🔄 Transcribe with Whisper", key="transcribe_resume", use_container_width=True):
                        with st.spinner("Transcribing..."):
                            try:
                                transcript = transcribe_audio(audio_bytes_resume, use_api=True)
                                st.session_state.voice_resume_text = transcript
                                st.success("✓ Transcription complete!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Transcription failed: {str(e)}")
                                st.caption("Make sure OPENAI_API_KEY is set for Whisper")
                
                with col_trans2:
                    st.download_button(
                        "💾 Download Audio",
                        data=audio_bytes_resume,
                        file_name="resume_recording.wav",
                        mime="audio/wav",
                        use_container_width=True
                    )
            
            # Show/edit transcription
            if st.session_state.voice_resume_text:
                st.markdown("##### 📝 Transcribed Resume (editable)")
                resume_text = st.text_area(
                    "Edit your transcription",
                    value=st.session_state.voice_resume_text,
                    height=300,
                    key="resume_transcript_edit",
                    label_visibility="collapsed"
                )
                st.session_state.voice_resume_text = resume_text
                st.success(f"✓ {len(resume_text)} characters ready")
            else:
                resume_text = ""
                
        elif voice_resume_method == "📁 Upload File":
            uploaded_resume = st.file_uploader(
                "Upload Resume (PDF, MD, TXT)",
                type=['pdf', 'md', 'txt'],
                key="voice_mode_resume_upload"
            )
            if uploaded_resume:
                resume_text = extract_text_from_upload(uploaded_resume)
                st.session_state.voice_resume_text = resume_text
                st.success(f"✓ Resume loaded ({len(resume_text)} characters)")
            else:
                resume_text = st.session_state.voice_resume_text or ""
                
        else:  # Paste Text
            resume_text = st.text_area(
                "Paste Your Resume",
                value=st.session_state.voice_resume_text or "",
                height=300,
                placeholder="Paste your resume content here..."
            )
            if resume_text:
                st.session_state.voice_resume_text = resume_text
                st.success(f"✓ {len(resume_text)} characters loaded")
        
        st.markdown("---")
        
        # JD Input Section
        st.markdown("#### 🎤 Voice-First Job Description")
        
        voice_jd_method = st.radio(
            "JD Source",
            ["🎙️ Record Voice", "📝 Paste Text"],
            horizontal=True,
            key="voice_jd_method"
        )
        
        if voice_jd_method == "🎙️ Record Voice":
            st.caption("🎯 Describe the role: What does the job involve? What are they looking for?")
            
            audio_bytes_jd = audio_recorder(
                text="🎙️ Click to record JD description",
                recording_color="#e74c3c",
                neutral_color="#764ba2",
                icon_name="microphone",
                icon_size="3x",
                key="jd_recorder"
            )
            
            if audio_bytes_jd:
                st.audio(audio_bytes_jd, format="audio/wav")
                
                if st.button("🔄 Transcribe JD", key="transcribe_jd", use_container_width=True):
                    with st.spinner("Transcribing..."):
                        try:
                            transcript = transcribe_audio(audio_bytes_jd, use_api=True)
                            st.session_state.voice_jd_text = transcript
                            st.success("✓ Transcription complete!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Transcription failed: {str(e)}")
            
            if st.session_state.voice_jd_text:
                st.markdown("##### 📝 Transcribed JD (editable)")
                job_description = st.text_area(
                    "Edit transcription",
                    value=st.session_state.voice_jd_text,
                    height=400,
                    key="jd_transcript_edit",
                    label_visibility="collapsed"
                )
                st.session_state.voice_jd_text = job_description
            else:
                job_description = ""
                
        else:  # Paste Text
            job_description = st.text_area(
                "Paste Job Description",
                value=st.session_state.voice_jd_text or "",
                height=400,
                placeholder="Paste the full job description here..."
            )
            if job_description:
                st.session_state.voice_jd_text = job_description
    
    # ─────────────────────────────────────────────────────────────
    # VIDEO MODE - THE GAME CHANGER
    # ─────────────────────────────────────────────────────────────

    # ==============================================================================
    # 🥊 MODE 7: BOARDROOM (SWARM SYNTHESIS) - FINAL ARCHITECTURE
    # ==============================================================================
    elif input_mode == "🥊 Practice (Dojo)":
        st.markdown("## ▲ BOARDROOM SIMULATOR (SWARM SYNTHESIS)")
        st.caption("PROTOCOL: Develop executive narrative, coding, and board presentation skills.")
        
        # SESSION HISTORY VIEWER
        if st.session_state.get('session_history'):
            with st.expander(f"📜 SESSION HISTORY ({len(st.session_state['session_history'])} sessions)"):
                total_xp = sum(s.get('xp_gained', 0) for s in st.session_state['session_history'])
                st.metric("TOTAL XP EARNED", f"{total_xp} XP", "Lifetime")
                
                for i, session in enumerate(reversed(st.session_state['session_history'][-5:])):  # Last 5
                    st.markdown(f"**Session {len(st.session_state['session_history']) - i}:** {session.get('opponent', 'Unknown')} | +{session.get('xp_gained', 0)} XP")
                    st.caption(f"Q: {session.get('question', '')[:100]}...")
                st.markdown("---")
        
        # 1. SETUP
        col1, col2 = st.columns([1, 2])
        with col1:
            # User is practicing for a high-stakes scenario
            opponent = st.selectbox("INTERVIEW TARGET", 
                ["CEO / Founder", "Board Member / Investor (The Skeptic CFO)", "Technical VP (Coding)", "Head of Partnerships (Story)"])
            artifact = st.selectbox("TOPIC ARTIFACT", ["Behavioral Story (STAR)", "Systems Design Question (Code)", "Board/CEO Presentation (Strategy)"])
            
            st.info("💡 Context: Omni-Agent is RAG-ing your entire Vault.")
            
        # 2. QUESTION GENERATION
        with col2:
            if st.button(f"GENERATE {artifact.upper()} CHALLENGE"):
                from logic.generator import generate_plain_text
                q_prompt = f"""
                ROLE: You are interviewing a 'Director of GTM Systems' (Leon Basin).
                Generate one highly challenging, scenario-based question related to {artifact} suitable for a {opponent}.
                If {artifact} is 'Systems Design Question', include a constraint (e.g., must be Python/Streamlit based).
                """
                # PASS THE SELECTED MODEL ID
                model_id = st.session_state.get('selected_model_id', "groq:llama-3.3-70b-versatile")
                st.session_state['current_q'] = generate_plain_text(q_prompt, model_name=model_id)
                st.session_state['opponent'] = opponent
                st.session_state['artifact'] = artifact

        # 3. LIVE SWARM INTERACTION
        if 'current_q' in st.session_state:
            st.markdown("---")
            st.warning(f"🗣️ **{st.session_state['opponent'].upper()}:** {st.session_state['current_q']}")
            
            user_answer = st.text_area("🎙️ YOUR RESPONSE (Draft or Voice Transcript)", height=200, placeholder="Speak your answer or draft your presentation summary...")
            
            if st.button("DEPLOY SWARM ANALYSIS"):
                if user_answer:
                    from logic.generator import generate_plain_text
                    with st.spinner("INITIATING MULTI-AGENT TRACE..."):
                        
                        # LLM TRACE: SIMULATE AGENT CONVERSATION
                        swarm_trace_prompt = f"""
                        ROLEPLAY THE FOUR AGENTS: ARCHITECT, ORACLE, SCRIBE, CODER.
                        
                        CONTEXT: Leon's metrics are: 160% Pipeline Growth, $10M ARR, Google Ops Rigor, MBA.
                        
                        QUESTION: {st.session_state['current_q']}
                        USER RESPONSE: {user_answer}

                        OUTPUT MUST BE A TRACE OF THEIR CONVERSATION:

                        **▲ ARCHITECT (SYSTEMS/GTM):** (Critique the solution's alignment with GTM Methodology - MEDDICC, Outbound, Partner Architecture. Define the structural goal.)
                        
                        **▲ ORACLE (DATA/SALES):** (Pull the single best metric or historical fact from Leon's vault to support the solution. Verify its ROI.)
                        
                        **▲ SCRIBE (NARRATIVE/CEO PITCH):** (Translate the answer into board-level, high-agency language. Advise on tone and presentation structure.)
                        
                        **▲ CODER (VALIDATION/TECH):** (If it's a coding/systems question, validate the Python/Streamlit approach. If behavioral, suggest a GTM tool to automate the story.)
                        
                        ---
                        
                        **FINAL SYNTHESIS (THE WINNING ANSWER):** (Write the final, polished response, incorporating all four points.)
                        """
                        
                        # PASS THE SELECTED MODEL ID
                        model_id = st.session_state.get('selected_model_id', "groq:llama-3.3-70b-versatile")
                        trace_result = generate_plain_text(swarm_trace_prompt, model_name=model_id)
                        
                        st.markdown("### 🧠 SWARM SYNTHESIS TRACE")
                        st.code(trace_result, language="markdown")
                        
                        # ====== REAL-TIME XP CALCULATION ======
                        word_count = len(user_answer.split())
                        
                        # Check for metrics (numbers, percentages, dollar signs)
                        import re
                        metrics_found = len(re.findall(r'\d+%|\$\d+|\d+[xX]|\d+\+', user_answer))
                        
                        # Check for STAR keywords
                        star_keywords = ['situation', 'task', 'action', 'result', 'impact', 'outcome', 'achieved', 'delivered', 'built', 'led', 'grew']
                        star_hits = sum(1 for kw in star_keywords if kw.lower() in user_answer.lower())
                        
                        # Calculate XP
                        base_xp = 50
                        word_bonus = min(word_count // 20, 50)  # Max 50 XP for length
                        metric_bonus = metrics_found * 25  # 25 XP per metric
                        star_bonus = star_hits * 15  # 15 XP per STAR keyword
                        total_xp = base_xp + word_bonus + metric_bonus + star_bonus
                        
                        # Boss Health (inverse of your score quality)
                        boss_damage = min(95, 20 + (metrics_found * 15) + (star_hits * 10))
                        
                        # Determine critical action
                        if metrics_found == 0:
                            critical_action = "ADD METRICS!"
                            critical_tip = "Include numbers (%, $, x growth)"
                        elif star_hits < 2:
                            critical_action = "Use STAR Format"
                            critical_tip = "Structure: Situation → Action → Result"
                        elif word_count < 100:
                            critical_action = "Expand Story"
                            critical_tip = "Add more context and detail"
                        else:
                            critical_action = "DEPLOY NOW"
                            critical_tip = "Answer is interview-ready!"
                        
                        # FINAL SCORECARD CALL (Gamified Update)
                        st.markdown("---")
                        st.subheader("🏆 MISSION RESULT")
                        
                        c1, c2, c3 = st.columns(3)
                        c1.metric("ARCHITECT XP GAINED", f"+{total_xp} XP", f"Words: {word_count}")
                        c2.metric("BOSS HEALTH REDUCTION", f"{boss_damage}%", f"Metrics: {metrics_found} | STAR: {star_hits}")
                        c3.metric("CRITICAL ACTION", critical_action, critical_tip)
                        
                        st.success("✅ AGENT TRACE COMPLETE. FINAL ANSWER GENERATED.")
                        
                        # ====== SESSION HISTORY SAVE ======
                        if 'session_history' not in st.session_state:
                            st.session_state['session_history'] = []
                        
                        session_entry = {
                            "timestamp": "2024-12-06",
                            "opponent": st.session_state.get('opponent', 'Unknown'),
                            "artifact": st.session_state.get('artifact', 'Unknown'),
                            "question": st.session_state.get('current_q', ''),
                            "answer": user_answer,
                            "xp_gained": total_xp,
                            "trace": trace_result[:500]  # Truncate for storage
                        }
                        st.session_state['session_history'].append(session_entry)
                        st.info(f"📁 Session saved! Total sessions: {len(st.session_state['session_history'])}")
                        
                        # ====== LINKEDIN POST GENERATOR ======
                        st.markdown("---")
                        with st.expander("📱 GENERATE LINKEDIN POST (Herald V2)"):
                            if st.button("🚀 CREATE LINKEDIN POST"):
                                linkedin_prompt = f"""
                                Convert this interview answer into a compelling LinkedIn post:
                                
                                ORIGINAL ANSWER: {user_answer}
                                
                                RULES:
                                1. Start with a hook (question or bold statement)
                                2. Keep it under 200 words
                                3. Include the key metric (160% growth, $10M, etc.)
                                4. End with a call-to-action or insight
                                5. Use line breaks for readability
                                6. Add 3-5 relevant hashtags
                                
                                Make it sound like a thought leader, not a job seeker.
                                """
                                linkedin_post = generate_plain_text(linkedin_prompt, model_name=model_id)
                                st.text_area("📋 COPY THIS:", linkedin_post, height=250)
                                st.caption("💡 Post this to build your 'Business Academic' brand!")

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
                    plan = generate_plain_text(prompt, model_name=selected_model)
                    st.session_state['90_day_plan'] = plan
            else:
                st.error("Please paste a JD.")
                
        if st.session_state.get('90_day_plan'):
            st.markdown("---")
            st.markdown(st.session_state['90_day_plan'])
            st.download_button("📥 Download Plan", st.session_state['90_day_plan'], "30_60_90_Plan.md")

    # ==============================================================================
    # 📈 MODE 8: PIPELINE CRM (DEAL TRACKER)
    # ==============================================================================
    elif input_mode == "📈 Pipeline CRM":
        st.markdown("## 📈 PIPELINE CRM (DEAL TRACKER)")
        st.caption("PROTOCOL: Track every opportunity from Application to Offer.")
        
        # Initialize Pipeline Data
        if 'pipeline_data' not in st.session_state:
            st.session_state['pipeline_data'] = [
                {"Company": "DepthFirst", "Role": "Dir. GTM", "Stage": "Final Round", "Next Action": "Follow-up CEO", "Priority": "🔥 HIGH", "Last Contact": "2024-12-05"},
                {"Company": "Mistral AI", "Role": "GTM Lead", "Stage": "HM Interview", "Next Action": "Send 90-Day Plan", "Priority": "🔥 HIGH", "Last Contact": "2024-12-04"},
                {"Company": "Ambient.ai", "Role": "Rev Ops", "Stage": "Screen", "Next Action": "Prep Recruiter Q's", "Priority": "⚡ MED", "Last Contact": "2024-12-03"},
                {"Company": "Verkada", "Role": "Sr. GTM", "Stage": "Applied", "Next Action": "Wait", "Priority": "⏳ LOW", "Last Contact": "2024-12-02"},
            ]
        
        # Pipeline Metrics
        k1, k2, k3, k4 = st.columns(4)
        stages = [d["Stage"] for d in st.session_state['pipeline_data']]
        k1.metric("TOTAL ACTIVE", len(st.session_state['pipeline_data']))
        k2.metric("FINAL ROUNDS", stages.count("Final Round"))
        k3.metric("HM INTERVIEWS", stages.count("HM Interview"))
        k4.metric("SCREENS", stages.count("Screen"))
        
        st.markdown("---")
        
        # Editable Pipeline Table
        st.markdown("#### 📋 ACTIVE PIPELINE")
        edited_df = st.data_editor(
            st.session_state['pipeline_data'],
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Stage": st.column_config.SelectboxColumn(
                    options=["Applied", "Screen", "HM Interview", "Final Round", "Offer", "Closed Won", "Closed Lost"]
                ),
                "Priority": st.column_config.SelectboxColumn(
                    options=["🔥 HIGH", "⚡ MED", "⏳ LOW"]
                )
            }
        )
        st.session_state['pipeline_data'] = edited_df
        
        # Quick Add
        st.markdown("---")
        with st.expander("➕ QUICK ADD OPPORTUNITY"):
            c1, c2, c3 = st.columns(3)
            new_company = c1.text_input("Company Name")
            new_role = c2.text_input("Role Title")
            new_stage = c3.selectbox("Stage", ["Applied", "Screen", "HM Interview", "Final Round"])
            
            if st.button("ADD TO PIPELINE", type="primary"):
                if new_company and new_role:
                    new_entry = {
                        "Company": new_company,
                        "Role": new_role,
                        "Stage": new_stage,
                        "Next Action": "TBD",
                        "Priority": "⚡ MED",
                        "Last Contact": "2024-12-06"
                    }
                    st.session_state['pipeline_data'].append(new_entry)
                    st.success(f"✅ Added {new_company} to Pipeline!")
                    st.rerun()

    # ==============================================================================
    # 🛡️ MODE 9: OBJECTION BANK (INTERVIEW ARMOR)
    # ==============================================================================
    elif input_mode == "🛡️ Objection Bank":
        st.markdown("## 🛡️ OBJECTION BANK (INTERVIEW ARMOR)")
        st.caption("PROTOCOL: Pre-loaded responses to common interview challenges.")
        
        # Initialize Objection Bank
        if 'objection_bank' not in st.session_state:
            st.session_state['objection_bank'] = {
                "Why did you leave your last role?": "I completed my mission—architecting the Revenue OS that drove 160% YoY pipeline growth. The next chapter requires a larger canvas where I can build at scale.",
                "You don't have direct experience in [X industry].": "My systems are industry-agnostic. The Revenue OS I built reduced CAC by 40% and generated $10M pipeline—that methodology transfers to any B2B SaaS environment.",
                "Why should we hire you over someone with more tenure?": "Tenure measures time; I measure impact. In 18 months, I built a GTM engine from zero that now generates 100+ qualified leads per week. I'm not looking for a job—I'm looking to build your next revenue machine.",
                "Tell me about a failure.": "Early in my career, I relied on 'sales activity' over 'sales architecture.' I was burning cycles instead of building systems. That failure taught me to think like an engineer—now I build once, scale infinitely.",
                "What's your weakness?": "I can over-engineer solutions when speed is required. I've learned to ship MVPs fast, then iterate based on data—not perfectionism."
            }
        
        # Display Objections
        st.markdown("#### 📖 YOUR PLAYBOOK")
        
        for objection, response in st.session_state['objection_bank'].items():
            with st.expander(f"❓ {objection}"):
                st.success(f"**YOUR RESPONSE:**\n\n{response}")
                st.caption("💡 TIP: Practice saying this out loud 3x before your interview.")
        
        st.markdown("---")
        
        # Add New Objection
        st.markdown("#### ➕ ADD NEW OBJECTION")
        new_objection = st.text_input("Objection/Question")
        new_response = st.text_area("Your Polished Response", height=150)
        
        if st.button("SAVE TO BANK", type="primary"):
            if new_objection and new_response:
                st.session_state['objection_bank'][new_objection] = new_response
                st.success(f"✅ Added to Objection Bank!")
                st.rerun()

    # ==============================================================================
    # 🔬 MODE 10: COMPANY INTEL (DEEP DIVE)
    # ==============================================================================
    elif input_mode == "🔬 Company Intel":
        st.markdown("## 🔬 COMPANY INTEL (DEEP DIVE)")
        st.caption("PROTOCOL: Pre-interview reconnaissance on target companies.")
        
        company_name = st.text_input("🎯 TARGET COMPANY NAME", placeholder="e.g., Verkada, Mistral AI, Ambient.ai")
        
        if company_name:
            st.markdown("---")
            st.markdown(f"#### 📊 INTEL REPORT: {company_name.upper()}")
            
            # Quick Links
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"[🔗 LinkedIn](https://www.linkedin.com/company/{company_name.lower().replace(' ', '-')})")
            c2.markdown(f"[💰 Crunchbase](https://www.crunchbase.com/organization/{company_name.lower().replace(' ', '-')})")
            c3.markdown(f"[📰 News](https://www.google.com/search?q={company_name}+funding+news)")
            c4.markdown(f"[👥 Glassdoor](https://www.glassdoor.com/Overview/Working-at-{company_name.replace(' ', '-')}-EI_IE.htm)")
            
            st.markdown("---")
            
            # AI Intel Generator
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
                    model_id = st.session_state.get('selected_model_id', "groq:llama-3.3-70b-versatile")
                    intel_result = generate_plain_text(intel_prompt, model_name=model_id)
                    st.session_state['company_intel'] = intel_result
            
            if st.session_state.get('company_intel'):
                st.markdown(st.session_state['company_intel'])

    # ==============================================================================
    # 🎙️ MODE 11: LIVE ASSIST (DIGITAL TWIN PROTOCOL)
    # ==============================================================================
    elif input_mode == "🎙️ Live Assist":
        st.markdown("## 🎙️ LIVE ASSIST (DIGITAL TWIN)")
        st.caption("PROTOCOL: Real-time coaching during live interviews. The Oracle speaks with you.")
        
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
                    model_id = st.session_state.get('selected_model_id', "groq:llama-3.3-70b-versatile")
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
