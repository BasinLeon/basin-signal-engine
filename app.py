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

with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")
    
    # System Status
    col_status1, col_status2 = st.columns(2)
    with col_status1:
        if MOCK_MODE:
            st.markdown('<span class="status-badge mock">🔧 MOCK</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-badge">🟢 LIVE</span>', unsafe_allow_html=True)
    with col_status2:
        st.markdown('<span class="status-badge voice">🎤 VOICE</span>', unsafe_allow_html=True)
    
    st.markdown("")
    
    # Model Selection FIRST (to determine which API key is needed)
    model_options = get_model_options()
    selected_model = st.selectbox(
        "🤖 LLM Model",
        options=[m[1] for m in model_options],
        format_func=lambda x: next((m[0] for m in model_options if m[1] == x), x),
        help="Choose between OpenAI GPT or Google Gemini models."
    )
    
    # Determine provider
    is_groq = selected_model.startswith("groq:")
    is_ollama = selected_model.startswith("ollama:")
    is_gemini = selected_model.startswith("gemini")
    is_openai = selected_model.startswith("gpt")
    
    st.markdown("")
    
    # API Key Input - Dynamic based on model
    if is_ollama:
        st.success("✓ Local Model - No API Key Needed!")
        st.caption("Running on your Mac via Ollama")
    elif is_groq:
        st.markdown("##### ⚡ Groq API Key (FREE)")
        api_key_input = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="Get FREE key at console.groq.com",
            label_visibility="collapsed"
        )
        if api_key_input:
            os.environ["GROQ_API_KEY"] = api_key_input
            st.success("✓ Groq API Key Set")
        elif os.environ.get("GROQ_API_KEY"):
            st.success("✓ Groq API Key Loaded")
        elif not MOCK_MODE:
            st.warning("⚠ Groq API Key Required")
            st.caption("[Get FREE Key →](https://console.groq.com)")
    elif is_gemini:
        st.markdown("##### 🔑 Google API Key")
        api_key_input = st.text_input(
            "Google API Key",
            type="password",
            placeholder="AIza...",
            help="Get your key at https://aistudio.google.com/apikey",
            label_visibility="collapsed"
        )
        if api_key_input:
            os.environ["GOOGLE_API_KEY"] = api_key_input
            st.success("✓ Google API Key Set")
        elif os.environ.get("GOOGLE_API_KEY"):
            st.success("✓ Google API Key Loaded")
        elif not MOCK_MODE:
            st.warning("⚠ Google API Key Required")
            st.caption("[Get API Key →](https://aistudio.google.com/apikey)")
    else:
        st.markdown("##### 🔑 OpenAI API Key")
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-proj-...",
            help="Required for GPT-4o, Whisper, and TTS.",
            label_visibility="collapsed"
        )
        if api_key_input:
            os.environ["OPENAI_API_KEY"] = api_key_input
            st.success("✓ OpenAI API Key Set")
        elif os.environ.get("OPENAI_API_KEY"):
            st.success("✓ OpenAI API Key Loaded")
        elif not MOCK_MODE:
            st.warning("⚠ OpenAI API Key Required")
    
    st.markdown("---")
    
    # Voice Selection for TTS
    voice_options = get_voice_options()
    selected_voice = st.selectbox(
        "TTS Voice",
        options=[v[1] for v in voice_options],
        format_func=lambda x: next((v[0] for v in voice_options if v[1] == x), x),
        help="Voice for audio cover letter generation."
    )
    
    st.markdown("---")
    
    # Philosophy Reminder
    st.markdown("### 📐 The Basin Protocol")
    st.markdown("""
    - **Systems > Hires**
    - **Signal > Noise**
    - **Architecture > Activity**
    """)
    
    st.markdown("---")
    st.caption("Basin & Associates © 2024")
    st.caption("Voice-First Career Intelligence")


# ═══════════════════════════════════════════════════════════════
# MAIN INTERFACE
# ═══════════════════════════════════════════════════════════════

# Header - BASIN::NEXUS Command Center
st.markdown('<h1 class="nexus-header">⚡ BASIN::NEXUS</h1>', unsafe_allow_html=True)
st.markdown('<p class="nexus-subtitle">Director of GTM Systems & Revenue Architecture • I Build the "Revenue OS"</p>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Two-column layout
col1, col2 = st.columns([1, 1], gap="large")


# ═══════════════════════════════════════════════════════════════
# INPUT COLUMN
# ═══════════════════════════════════════════════════════════════

with col1:
    st.markdown("### 📥 Ingest Data (The Signal)")
    
    # Input Mode Toggle - FULL ARSENAL
    input_mode = st.radio(
        "Mission Mode",
        ["📄 Intel", "🎯 Hunt", "🔍 Talent Signal", "🎤 Voice", "🥊 Practice (Dojo)", "🚀 First 90 Days"],
        horizontal=True,
        help="Intel (Recon), Hunt (Search), Signal (Screen), Voice (Audio), Dojo (Interview), 90 Days (Plan)"
    )
    
    st.markdown("")
    
    # ─────────────────────────────────────────────────────────────
    # INTEL MODE (Text/File Input)
    # ─────────────────────────────────────────────────────────────
    # ─────────────────────────────────────────────────────────────
    # INTEL MODE (The Data Center HUD)
    # ─────────────────────────────────────────────────────────────
    if input_mode == "📄 Intel":
        st.markdown("### 🧬 STRATEGIC ALIGNMENT HUD")
        
        # 1. DATA INGESTION (THE FEED)
        with st.expander("📂 SOURCE DATA (Resume & Target)", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                resume_text = st.text_area(
                    "Your Signal (Resume)", 
                    height=150, 
                    value=st.session_state.get('resume_text', ''),
                    placeholder="Paste your Master Resume...", 
                    help="The Asset",
                    key="hud_resume"
                )
                st.session_state.resume_text = resume_text
            with c2:
                jd_text = st.text_area(
                    "Target Signal (JD)", 
                    height=150, 
                    value=st.session_state.get('jd_text', ''),
                    placeholder="Paste the Job Description...", 
                    help="The Mission",
                    key="hud_jd"
                )
                st.session_state.jd_text = jd_text

        # 2. THE ANALYSIS ENGINE
        if st.button("🚀 RUN SIGNAL DIAGNOSTICS", type="primary", use_container_width=True):
            if resume_text and jd_text:
                with st.spinner("Encrypting connection... Analyzing Signal Strength..."):
                    
                    from logic.generator import generate_plain_text
                    import json
                    
                    # THE LLM PROMPT (STRUCTURED JSON OUTPUT)
                    prompt = f"""
                    ACT AS: BASIN::NEXUS Intelligence Engine.
                    INPUT: RESUME vs JD.
                    
                    TASK: Perform a deep gap analysis.
                    
                    OUTPUT JSON FORMAT ONLY:
                    {{
                        "match_score": (Integer 0-100),
                        "ats_probability": (Integer 0-100, estimate of passing automated screen),
                        "market_temperature": ("Cold", "Warm", "Hot" based on urgency of JD),
                        "missing_keywords": ["keyword1", "keyword2", "keyword3"],
                        "key_strengths": ["strength1", "strength2"],
                        "bleeding_neck": "The #1 expensive problem detailed in the JD",
                        "hiring_manager_persona": "Description of the buyer psychology",
                        "salary_estimate": "Estimated range based on level/title"
                    }}
                    
                    RESUME: {resume_text[:3000]}
                    JD: {jd_text[:3000]}
                    """
                    
                    raw_result = generate_plain_text(prompt, model_name=selected_model)
                    
                    # Clean the output (strip markdown code blocks if present)
                    clean_result = raw_result.replace("```json", "").replace("```", "").strip()
                    
                    try:
                        response = json.loads(clean_result)
                    except Exception as e:
                        st.warning(f"⚠️ Signal Interference (JSON Parse Error). Using Simulation protocols. Error: {e}")
                        # Fallback Mock Data
                        response = {
                            "match_score": 85,
                            "ats_probability": 90,
                            "market_temperature": "Warm",
                            "missing_keywords": ["Strategic Planning", "P&L Management", "Team Building"],
                            "key_strengths": ["Technical Architecture", "System Design"],
                            "bleeding_neck": "Operational inefficiency and lack of scalable systems.",
                            "hiring_manager_persona": "Results-oriented leader seeking immediate impact.",
                            "salary_estimate": "$160k - $220k"
                        }

                    # 3. THE VISUAL DASHBOARD (THE DATA CENTER)
                    st.markdown("---")
                    
                    # ROW 1: TOP LEVEL TELEMETRY
                    m1, m2, m3, m4 = st.columns(4)
                    with m1:
                        st.metric("SIGNAL MATCH", f"{response.get('match_score', 0)}%", "Executive Fit")
                    with m2:
                        st.metric("ATS PROBABILITY", f"{response.get('ats_probability', 0)}%", "High Pass Rate")
                    with m3:
                        st.metric("MARKET TEMP", response.get('market_temperature', 'N/A'), "Urgent Hire", delta_color="inverse")
                    with m4:
                        st.metric("EST. SALARY", response.get('salary_estimate', 'N/A'))
                    
                    # ROW 2: THE GAP VISUALIZER
                    st.markdown("#### 🚨 SIGNAL INTERFERENCE (Missing Keywords)")
                    
                    # CSS for "Chips"
                    st.markdown("""
                    <style>
                    .keyword-chip {
                        display: inline-block;
                        padding: 5px 12px;
                        margin: 5px;
                        border-radius: 15px;
                        background-color: #1E1E1E;
                        border: 1px solid #FF4B4B; 
                        color: #FF4B4B;
                        font-family: monospace;
                        font-weight: bold;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # Generate Chips
                    chips_html = ""
                    for kw in response.get('missing_keywords', []):
                        chips_html += f"<span class='keyword-chip'>⚠ {kw}</span>"
                    st.markdown(chips_html, unsafe_allow_html=True)
                    
                    st.caption("Fix: Add these exact keywords to your 'Core Competencies' or 'Summary'.")

                    st.markdown("---")

                    # ROW 3: DEEP RECON DOSSIER
                    c1_dash, c2_dash = st.columns([2, 1])
                    
                    with c1_dash:
                        st.subheader("🚩 THE BLEEDING NECK")
                        st.error(f"**DIAGNOSIS:** {response.get('bleeding_neck', 'N/A')}")
                        st.markdown(f"**STRATEGY:** Leverage your strengths ({', '.join(response.get('key_strengths', [])[:2])}) to solve this.")
                    
                    with c2_dash:
                        st.subheader("👤 BUYER PSYCHOLOGY")
                        st.info(f"**TARGET:** {response.get('hiring_manager_persona', 'N/A')}")
                        st.caption("Tone Strategy: Be direct.")

            else:
                st.warning("⚠ WAITING FOR SIGNAL INPUT...")
    
    # ─────────────────────────────────────────────────────────────
    # HUNT MODE - THE HEADHUNTER
    # ─────────────────────────────────────────────────────────────
    # ─────────────────────────────────────────────────────────────
    # HUNT MODE - THE RADAR ARRAY
    # ─────────────────────────────────────────────────────────────
    elif input_mode == "🎯 Hunt":
        st.markdown("### 🔭 GLOBAL TARGETING RADAR")
        
        # TABS FOR DIFFERENT "RADAR FREQUENCIES"
        tab1, tab2, tab3 = st.tabs(["🔍 LINKEDIN (Sonar)", "☢️ GOOGLE (X-Ray)", "🐦 SOCIAL (Whisper)"])
        
        with tab1:
            st.markdown("#### 🧱 BOOLEAN ARCHITECT")
            c1, c2, c3 = st.columns(3)
            with c1:
                role_select = st.selectbox("Role", ["Director of GTM", "Head of Partnerships", "RevOps Leader", "Founding Sales"])
            with c2:
                sector_select = st.selectbox("Sector", ["HR Tech (Deel)", "Cyber (Zero Trust)", "AI / DevTools", "General SaaS"])
            with c3:
                seniority = st.multiselect("Level", ["Manager", "Director", "VP", "Head of"], default=["Director", "Head of"])
            
            # DYNAMIC STRING BUILDER
            base_string = f'("{role_select}" OR "{role_select.replace("Director", "Head")}")'
            sector_string = f'AND ("{sector_select.split()[0]}" OR "SaaS" OR "B2B")'
            noise_filter = 'AND NOT ("Intern" OR "SDR" OR "Entry Level")'
            
            if seniority:
                 seniority_string = 'AND (' + ' OR '.join([f'"{s}"' for s in seniority]) + ')'
            else:
                 seniority_string = ""
            
            final_boolean = f"{base_string} {sector_string} {seniority_string} {noise_filter}"
            
            st.code(final_boolean, language="text")
            st.caption("📋 Copy/Paste into LinkedIn Search")
            
        with tab2:
            st.markdown("#### ☢️ ATS BREAKER (Bypass LinkedIn)")
            st.markdown("Directly ping the databases of Lever, Greenhouse, and Ashby.")
            xray_string = f'site:lever.co OR site:greenhouse.io OR site:ashbyhq.com {base_string} {sector_string}'
            st.code(xray_string, language="text")
            st.markdown(f"[🚀 LAUNCH GOOGLE X-RAY](https://www.google.com/search?q={xray_string.replace(' ', '+').replace('\"', '%22')})")

        with tab3:
            st.markdown("#### 🐦 THE WHISPER (Hidden Market)")
            st.info("Find leaders tweeting about hiring before they post the job.")
            whisper_query = f'("{role_select.split()[0]}") AND ("hiring" OR "join my team" OR "dm me") min_faves:5'
            st.code(whisper_query, language="text")
            st.markdown(f"[🚀 LAUNCH X SEARH](https://twitter.com/search?q={whisper_query.replace(' ', '%20').replace('\"', '%22')}&src=typed_query)")

    
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

    elif input_mode == "🥊 Practice (Dojo)":
        st.markdown("####  INTERVIEW ANALYTICS & SCOREBOARD")
        st.info("💡 **PROTOCOL:** Use your system Mic (Office/Mac Dictation) to speak into the text box. We measure speech patterns.")
        
        col_dojo1, col_dojo2 = st.columns([1, 1])
        
        with col_dojo1:
            opponent = st.selectbox("Choose Interviewer Persona", 
                ["💀 The Skeptic (CFO - Wants ROI)", 
                 "🚀 The Founder (Series A - Wants Speed)", 
                 "🛡️ The Gatekeeper (HR - Wants Keywords)"])
            
            q_type = st.selectbox("Question Type", ["Behavioral (Conflict)", "Strategic (GTM)", "Operational (Failure)"])
            
            # Setup context from other modes
            jd_context = st.session_state.get('jd_text', "")
            resume_context = st.session_state.get('resume_text', "")
            
        with col_dojo2:
             if st.button("🔥 GENERATE PRESSURE QUESTION", use_container_width=True, type="primary"):
                # Use plain text generator
                from logic.generator import generate_plain_text
                
                with st.spinner(f"{opponent} is preparing the interrogation..."):
                    q_prompt = f"""
                    ACT AS: {opponent}.
                    CONTEXT: Interviewing a candidate for a Director of Revenue Architecture role.
                    JD CONTEXT: {jd_context[:500]}
                    RESUME CONTEXT: {resume_context[:500]}
                    TASK: Generate one HARD {q_type} interview question. Keep it short and punchy.
                    """
                    question = generate_plain_text(q_prompt)
                    st.session_state['war_room_q'] = question
                    st.session_state['dojo_transcript'] = "" # Reset transcript
                    st.session_state['dojo_score'] = None
        
        # Display Question & Input
        if st.session_state.get('war_room_q'):
            st.markdown("---")
            st.markdown(f"### 🗣️ {st.session_state['war_room_q']}")
            
            st.markdown("##### 🎙️ SPEAK YOUR ANSWER (Dictation)")
            user_transcript = st.text_area(
                "Activate Mic (Fn+Fn on Mac) then speak...", 
                height=150,
                key="dojo_voice_input",
                placeholder="[System Dictation] Speak here..."
            )
            
            if st.button("� ANALYZE PERFORMANCE", use_container_width=True):
                if user_transcript and len(user_transcript) > 5:
                    from logic.generator import generate_plain_text
                    
                    with st.spinner("Calculating Telemetry..."):
                        # ANALYTICS LOGIC
                        word_count = len(user_transcript.split())
                        
                        prompt = f"""
                        ACT AS: A Speech Coach and GTM Executive.
                        CONTEXT: Question: "{st.session_state['war_room_q']}".
                        TRANSCRIPT: "{user_transcript}"
                        
                        TASK: Analyze this spoken answer.
                        
                        OUTPUT MARKDOWN FORMAT:
                        # 📊 THE SCOREBOARD
                        - **🏆 SCORE:** [0-100]
                        - **🗣️ CONFIDENCE:** [Low/Med/High]
                        - **🧱 METRIC DENSITY:** [Low/High - did they use numbers?]
                        - **⭐ STAR ALIGNMENT:** [Yes/No]
                        
                        ### 🚩 THE DIAGNOSIS
                        [One sentence on what went wrong or right]
                        
                        ### ✅ THE FIX
                        [Rewrite the 'Action' part of the answer to be more Executive]
                        """
                        result = generate_plain_text(prompt)
                        st.session_state['dojo_score'] = result
                        st.session_state['dojo_word_count'] = word_count
                else:
                    st.warning("Please dictate an answer first.")
                    
            # Result Display
            if st.session_state.get('dojo_score'):
                st.markdown("---")
                st.markdown(st.session_state['dojo_score'])
                
                # Simple Metrics
                wc = st.session_state.get('dojo_word_count', 0)
                st.info(f"**Word Count:** {wc} (Target: 150-250)")
                if wc > 300:
                    st.warning("⚠️ Rambling detected. Tighten the narrative.")
                elif wc < 50:
                    st.warning("⚠️ Too thin. Add more context.")

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
    
    st.markdown("")
    



# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.caption("**Mode:** Voice-First Intelligence")

with footer_col2:
    st.caption("**Protocol:** Zero-to-One")

with footer_col3:
    st.caption("**Status:** Multimodal Ready")
