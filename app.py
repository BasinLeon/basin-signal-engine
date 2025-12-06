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
st.markdown('<p class="nexus-subtitle">GTM Intelligence Command Center • January 2026 Protocol</p>', unsafe_allow_html=True)
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
        ["📄 Intel", "🎯 Hunt", "🎤 Voice", "📹 Video", "🥊 Practice"],
        horizontal=True,
        help="Intel (Resume+JD), Hunt (Boolean search), Voice (Audio), Video (Pitch analysis), Practice (Interview sim)"
    )
    
    st.markdown("")
    
    # ─────────────────────────────────────────────────────────────
    # INTEL MODE (Text/File Input)
    # ─────────────────────────────────────────────────────────────
    if input_mode == "📄 Intel":
        # Resume Input Method
        resume_input_method = st.radio(
            "Resume Input",
            ["📁 Upload File", "📝 Paste Text"],
            horizontal=True,
            key="resume_input_method"
        )
        
        if resume_input_method == "📁 Upload File":
            # A. Upload Resume
            uploaded_resume = st.file_uploader(
                "Upload Master Resume",
                type=['pdf', 'md', 'txt'],
                help="Your 'Source of Truth'. PDF, Markdown, or Text format."
            )
            
            if uploaded_resume:
                resume_text = extract_text_from_upload(uploaded_resume)
                validation = validate_resume_content(resume_text)
                
                if validation["valid"]:
                    st.success(f"✓ {validation['message']}")
                    st.session_state.resume_text = resume_text
                else:
                    st.error(f"✗ {validation['message']}")
                    resume_text = ""
            else:
                resume_text = st.session_state.resume_text
        else:
            # B. Paste Resume Text
            resume_text = st.text_area(
                "Paste Your Resume",
                height=200,
                value=st.session_state.resume_text,
                placeholder="""Paste your resume content here...

Include:
- Professional summary
- Key achievements with metrics
- Skills and experience
- Projects and outcomes"""
            )
            if resume_text:
                st.session_state.resume_text = resume_text
                st.success(f"✓ Resume loaded ({len(resume_text)} characters)")
        
        st.markdown("")
        
        # B. The Target (Job Description) - EXPANDED for long JDs
        job_description = st.text_area(
            "Paste Job Description / Context",
            height=500,  # Tall enough for most full JDs
            value=st.session_state.jd_text,
            placeholder="""Paste the full job description here...

The system will:
1. Extract the top 3 Pain Points
2. Map your resume to those pains
3. Generate tailored output

Tip: Include the FULL JD for best results - the more context, the better the output."""
        )
        st.session_state.jd_text = job_description
    
    # ─────────────────────────────────────────────────────────────
    # HUNT MODE - THE HEADHUNTER
    # ─────────────────────────────────────────────────────────────
    elif input_mode == "🎯 Hunt":
        st.markdown("#### 🎯 THE HEADHUNTER")
        st.caption("Generate precision targeting strings for LinkedIn. Find the jobs BEFORE they find you.")
        
        st.markdown('<div class="divider-solid"></div>', unsafe_allow_html=True)
        
        # === ROLE SELECTION ===
        st.markdown("##### 🎖️ TARGET ROLE")
        target_role = st.selectbox(
            "What role are you hunting?",
            [
                "GTM Operations / Revenue Ops",
                "Head of Partnerships / Channel",
                "Chief of Staff (Revenue/GTM)",
                "Founding Sales / First Hire",
                "Sales Strategy & Enablement",
                "Solutions Architect / SE",
                "Product Operations",
                "Custom..."
            ],
            key="hunt_role"
        )
        
        # Custom role option
        if target_role == "Custom...":
            custom_role = st.text_input("Enter custom role keywords", placeholder='e.g., "Director of Growth" OR "VP Marketing"')
        
        st.markdown("")
        
        # === SECTOR SELECTION ===
        st.markdown("##### 🏢 TARGET SECTOR")
        target_sector = st.selectbox(
            "Which industry vertical?",
            [
                "General SaaS / B2B Tech",
                "HR Tech / Future of Work",
                "Cybersecurity / GRC",
                "AI / ML / DevTools",
                "FinTech / Payments",
                "HealthTech / Digital Health",
                "Climate / CleanTech",
                "Custom..."
            ],
            key="hunt_sector"
        )
        
        if target_sector == "Custom...":
            custom_sector = st.text_input("Enter custom sector keywords", placeholder='e.g., "Climate Tech" OR "Sustainability"')
        
        st.markdown("")
        
        # === SENIORITY FILTER ===
        st.markdown("##### 📊 SENIORITY LEVEL")
        seniority = st.multiselect(
            "Select target levels",
            ["Manager", "Senior Manager", "Director", "Head of", "VP", "C-Level"],
            default=["Manager", "Director", "Head of"],
            key="hunt_seniority"
        )
        
        st.markdown("")
        
        # === LOCATION (Optional) ===
        st.markdown("##### 🌍 LOCATION (Optional)")
        location = st.text_input(
            "Add location filter",
            placeholder='e.g., "Remote" OR "San Francisco" OR "New York"',
            key="hunt_location"
        )
        
        st.markdown('<div class="divider-solid"></div>', unsafe_allow_html=True)
        
        # === GENERATE BUTTON ===
        if st.button("⚡ GENERATE HUNTING COORDINATES", use_container_width=True, type="primary"):
            
            # === THE BOOLEAN LOGIC ENGINE ===
            
            # Role strings
            role_strings = {
                "GTM Operations / Revenue Ops": '("GTM Operations" OR "Revenue Operations" OR "RevOps" OR "Sales Operations" OR "Go-to-Market Strategy" OR "Sales Strategy")',
                "Head of Partnerships / Channel": '("Head of Partnerships" OR "Director of Partnerships" OR "Senior Partner Manager" OR "Head of Channel" OR "Channel Sales" OR "Strategic Alliances" OR "Business Development Director")',
                "Chief of Staff (Revenue/GTM)": '("Chief of Staff") AND ("Revenue" OR "Sales" OR "CRO" OR "GTM" OR "Commercial" OR "COO")',
                "Founding Sales / First Hire": '("Founding AE" OR "First Sales Hire" OR "Head of Sales" OR "0 to 1 Sales" OR "First GTM Hire" OR "Founding Sales")',
                "Sales Strategy & Enablement": '("Sales Strategy" OR "Sales Enablement" OR "Revenue Enablement" OR "GTM Enablement" OR "Commercial Strategy")',
                "Solutions Architect / SE": '("Solutions Architect" OR "Solutions Engineer" OR "Pre-Sales Engineer" OR "Technical Account Manager" OR "Solutions Consultant")',
                "Product Operations": '("Product Operations" OR "Product Ops" OR "Business Operations" OR "Growth Operations" OR "Strategy & Operations")',
            }
            
            # Sector strings
            sector_strings = {
                "General SaaS / B2B Tech": 'AND ("SaaS" OR "B2B" OR "Enterprise Software" OR "Cloud" OR "Software")',
                "HR Tech / Future of Work": 'AND ("HR Tech" OR "HRTech" OR "Workforce" OR "Payroll" OR "People Operations" OR "Compliance" OR "Deel" OR "Rippling" OR "Gusto" OR "Remote")',
                "Cybersecurity / GRC": 'AND ("Cybersecurity" OR "Security" OR "Zero Trust" OR "GRC" OR "Compliance" OR "Identity" OR "Vanta" OR "Drata" OR "Snyk" OR "CrowdStrike")',
                "AI / ML / DevTools": 'AND ("Generative AI" OR "GenAI" OR "LLM" OR "Machine Learning" OR "DevTools" OR "Developer Experience" OR "AI Platform" OR "MLOps")',
                "FinTech / Payments": 'AND ("FinTech" OR "Payments" OR "Banking" OR "Lending" OR "Financial Services" OR "Stripe" OR "Plaid" OR "Ramp")',
                "HealthTech / Digital Health": 'AND ("HealthTech" OR "Digital Health" OR "Healthcare" OR "Telehealth" OR "Medical" OR "Health Tech")',
                "Climate / CleanTech": 'AND ("Climate Tech" OR "CleanTech" OR "Sustainability" OR "Clean Energy" OR "Carbon" OR "ESG")',
            }
            
            # Noise filter - CRITICAL
            noise_filter = 'AND NOT ("Intern" OR "Entry Level" OR "Junior" OR "SDR" OR "BDR" OR "Account Executive" OR "Door to Door" OR "Commission Only" OR "Cold Calling")'
            
            # Build the string
            if target_role == "Custom...":
                role_part = f'({custom_role})'
            else:
                role_part = role_strings.get(target_role, "")
            
            if target_sector == "Custom...":
                sector_part = f'AND ({custom_sector})'
            else:
                sector_part = sector_strings.get(target_sector, "")
            
            # Seniority
            if seniority:
                seniority_part = 'AND (' + ' OR '.join([f'"{s}"' for s in seniority]) + ')'
            else:
                seniority_part = ""
            
            # Location
            if location:
                location_part = f'AND ({location})'
            else:
                location_part = ""
            
            # COMBINE
            boolean_string = f"{role_part} {sector_part} {seniority_part} {location_part} {noise_filter}"
            boolean_string = boolean_string.strip()
            
            # Store in session
            st.session_state.hunt_result = boolean_string
        
        # === DISPLAY RESULTS ===
        if "hunt_result" in st.session_state and st.session_state.hunt_result:
            st.markdown('<div class="divider-solid"></div>', unsafe_allow_html=True)
            st.markdown("##### ⚡ HUNTING COORDINATES GENERATED")
            
            # Display the string
            st.code(st.session_state.hunt_result, language="text")
            
            # Copy instruction
            st.info("📋 **Copy the string above** and paste into LinkedIn's search bar for precision targeting.")
            
            # Quick links
            col_link1, col_link2 = st.columns(2)
            with col_link1:
                st.markdown("[🔗 Open LinkedIn Jobs](https://www.linkedin.com/jobs/search/)")
            with col_link2:
                st.markdown("[🔗 Open LinkedIn People](https://www.linkedin.com/search/results/people/)")
            
            st.markdown("")
            
            # Pro tips
            with st.expander("💡 PRO TIPS FOR HUNTING"):
                st.markdown("""
                **LinkedIn Search Hacks:**
                
                1. **Jobs Search**: Paste the string, then filter by "Date Posted: Past Week"
                2. **People Search**: Find hiring managers with: `"Head of" AND "HR Tech" AND "hiring"`
                3. **Saved Searches**: Save your search for daily alerts
                4. **Boolean in Messages**: Use keywords when reaching out
                
                **The Sniper Approach:**
                - Find the job → Find the hiring manager → Send a DM
                - Don't just apply - **architect the connection**
                
                **Refining Results:**
                - Too many results? Add more specific sectors
                - Too few results? Remove seniority filters
                """)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # ═══════════════════════════════════════════════════════════════
        # THE WHISPER SEARCH - Stealth Job Detection
        # ═══════════════════════════════════════════════════════════════
        st.markdown("#### 🕵️ THE WHISPER SEARCH")
        st.caption("Detect stealth jobs, first hires, and opportunities before they go public")
        
        whisper_keywords = st.text_input(
            "Target keywords (companies, leaders, signals)",
            placeholder='e.g., "Rippling" OR "Matt MacInnis" OR "first GTM hire"',
            key="whisper_keywords"
        )
        
        col_whisper1, col_whisper2, col_whisper3 = st.columns(3)
        
        with col_whisper1:
            if st.button("🔥 X/Twitter Search", use_container_width=True):
                if whisper_keywords:
                    twitter_query = f'{whisper_keywords} ("hiring" OR "looking for" OR "join my team" OR "scaling" OR "first hire")'
                    twitter_url = f"https://twitter.com/search?q={twitter_query.replace(' ', '%20')}&f=live"
                    st.session_state.whisper_twitter = twitter_url
                    st.markdown(f"[🔗 Open Twitter Search]({twitter_url})")
        
        with col_whisper2:
            if st.button("💼 LinkedIn <24h", use_container_width=True):
                if whisper_keywords:
                    # LinkedIn recent jobs
                    linkedin_url = f"https://www.linkedin.com/jobs/search/?keywords={whisper_keywords.replace(' ', '%20')}&f_TPR=r86400"
                    st.markdown(f"[🔗 LinkedIn Jobs (Last 24h)]({linkedin_url})")
        
        with col_whisper3:
            if st.button("🚀 Wellfound Startups", use_container_width=True):
                if whisper_keywords:
                    wellfound_url = f"https://wellfound.com/jobs?q={whisper_keywords.replace(' ', '%20')}"
                    st.markdown(f"[🔗 Wellfound Startup Jobs]({wellfound_url})")
        
        st.markdown("")
        
        # Stealth detection presets
        st.markdown("**⚡ Quick Whisper Presets:**")
        col_preset1, col_preset2, col_preset3 = st.columns(3)
        
        with col_preset1:
            if st.button("🥷 Stealth Startups", use_container_width=True):
                st.code('"stealth mode" OR "stealth startup" AND ("GTM" OR "Operations" OR "Partnerships") AND "hiring"', language="text")
        
        with col_preset2:
            if st.button("🎯 First Hires", use_container_width=True):
                st.code('"first hire" OR "founding" OR "0 to 1" AND ("GTM" OR "Sales" OR "Revenue") AND NOT "intern"', language="text")
        
        with col_preset3:
            if st.button("💸 Just Raised", use_container_width=True):
                st.code('"just raised" OR "Series A" OR "Series B" AND "hiring" AND ("GTM" OR "Growth" OR "Ops")', language="text")
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # ═══════════════════════════════════════════════════════════════
        # THE HEADHUNTER CRITIQUE - AI Recruiter Feedback
        # ═══════════════════════════════════════════════════════════════
        st.markdown("#### 🎭 THE HEADHUNTER CRITIQUE")
        st.caption("Get ruthless feedback as if you were being screened by a top recruiter")
        
        critique_company = st.selectbox(
            "Simulate recruiter from:",
            ["Deel (Global Payroll)", "Rippling (HR Tech)", "Vanta (Security)", "OpenAI (AI)", "Stripe (Payments)", "Custom..."],
            key="critique_company"
        )
        
        if critique_company == "Custom...":
            custom_company = st.text_input("Enter company name and focus", placeholder="e.g., Anthropic (AI Safety)")
        
        critique_role = st.text_input(
            "Role you're applying for:",
            placeholder="e.g., Head of GTM Operations",
            key="critique_role"
        )
        
        critique_resume = st.text_area(
            "Paste your resume/summary to critique:",
            height=150,
            placeholder="Paste the first 500 chars of your resume or professional summary...",
            key="critique_resume"
        )
        
        if st.button("🔥 GET BRUTALLY HONEST FEEDBACK", use_container_width=True):
            if critique_resume and critique_role:
                with st.spinner("The Headhunter is reviewing your materials..."):
                    try:
                        company_context = custom_company if critique_company == "Custom..." else critique_company
                        
                        critique_prompt = f"""You are a ruthless Head of Talent at {company_context}. 
You are screening candidates for the role of {critique_role}.

CANDIDATE'S RESUME/SUMMARY:
{critique_resume[:1500]}

Be BRUTALLY honest. You only have 6 seconds to review this. 
Give feedback in this format:

**VERDICT**: [PASS TO INTERVIEW / MAYBE / REJECT]

**6-SECOND SCAN**: What I noticed in the first 6 seconds

**KILLER MISTAKE**: The ONE thing that would make me reject this

**MISSING SIGNAL**: What keyword/proof is missing for {company_context}?

**THE FIX**: Exactly how to rewrite the first 2 sentences to get my attention

**INSIDER TIP**: What would actually make me excited about this candidate?

Be harsh. Be specific. No fluff."""

                        # Use Groq for speed
                        from groq import Groq
                        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": critique_prompt}],
                            temperature=0.7
                        )
                        critique_result = response.choices[0].message.content
                        st.session_state.critique_result = critique_result
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        if "critique_result" in st.session_state and st.session_state.critique_result:
            st.markdown("---")
            st.markdown("##### 🎯 HEADHUNTER VERDICT")
            st.markdown(st.session_state.critique_result)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # ═══════════════════════════════════════════════════════════════
        # TELEPROMPTER SCRIPT GENERATOR
        # ═══════════════════════════════════════════════════════════════
        st.markdown("#### 📹 TELEPROMPTER SCRIPT")
        st.caption("Generate a 60-second video pitch script to send via Loom")
        
        script_context = st.text_area(
            "Paste the JD or describe the role:",
            height=100,
            placeholder="Paste the job description or describe: 'Head of Partnerships at Series B HR Tech startup...'",
            key="script_context"
        )
        
        script_tone = st.radio(
            "Tone:",
            ["🎯 Executive (Confident)", "🤝 Collaborative (Warm)", "⚡ Startup (High Energy)"],
            horizontal=True,
            key="script_tone"
        )
        
        if st.button("🎬 GENERATE TELEPROMPTER SCRIPT", use_container_width=True):
            if script_context:
                with st.spinner("Writing your 60-second script..."):
                    try:
                        tone_instruction = {
                            "🎯 Executive (Confident)": "Sound like a peer, not a candidate. Use 'I built' not 'I helped'. No filler words.",
                            "🤝 Collaborative (Warm)": "Be approachable but credible. Show you've done your research on THEM.",
                            "⚡ Startup (High Energy)": "Show urgency and hunger. Use action verbs. Sound like a builder."
                        }
                        
                        script_prompt = f"""Write a 60-second video pitch script for someone applying to this role:

ROLE/CONTEXT:
{script_context[:1000]}

TONE: {script_tone}
INSTRUCTION: {tone_instruction.get(script_tone, "")}

FORMAT YOUR OUTPUT AS:

**[0-10 sec] THE HOOK**
(Grab attention immediately. Start with a result, not your name.)

**[10-30 sec] THE PROOF**
(One specific story that shows you can do THIS job. Use numbers.)

**[30-50 sec] THE BRIDGE**
(Why THIS company, THIS role? Show you've researched them.)

**[50-60 sec] THE CLOSE**
(Clear next step. Don't ask 'if' - assume the meeting.)

Keep each section to 2-3 sentences max. Write it exactly as they should SAY it out loud."""

                        from groq import Groq
                        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": script_prompt}],
                            temperature=0.7
                        )
                        script_result = response.choices[0].message.content
                        st.session_state.script_result = script_result
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        if "script_result" in st.session_state and st.session_state.script_result:
            st.markdown("---")
            st.markdown("##### 🎬 YOUR 60-SECOND SCRIPT")
            st.markdown(st.session_state.script_result)
            st.info("💡 **Pro tip:** Record this in Loom and send directly to the hiring manager's LinkedIn DM.")
        
        # Set empty values for Intel mode compatibility
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
    elif input_mode == "📹 Video":
        st.markdown("#### 📹 Video Pitch Analysis")
        st.caption("Upload a video of your elevator pitch or mock interview")
        
        # Initialize video session state
        if "video_analysis" not in st.session_state:
            st.session_state.video_analysis = None
        
        # Video upload
        uploaded_video = st.file_uploader(
            "Upload Video (MP4, MOV, WebM)",
            type=['mp4', 'mov', 'webm', 'avi'],
            help="Max 100MB. Record yourself delivering your pitch."
        )
        
        if uploaded_video:
            video_bytes = uploaded_video.read()
            validation = validate_video(video_bytes)
            
            if validation["valid"]:
                st.success(f"✓ {validation['message']}")
                
                # Show video preview
                st.video(video_bytes)
                
                # Context for analysis
                video_context = st.text_area(
                    "Context for Analysis (optional)",
                    placeholder="e.g., 'Elevator pitch for Senior PM role at Adobe' or 'Mock interview answer for GTM question'",
                    height=80
                )
                
                # Analyze button
                if st.button("🎬 Analyze My Pitch", type="primary", use_container_width=True):
                    with st.spinner("🔍 Gemini is analyzing your delivery, content, and presence..."):
                        try:
                            result = analyze_video_pitch(video_bytes, context=video_context)
                            
                            if result["success"]:
                                st.session_state.video_analysis = result["analysis"]
                                st.success("✅ Analysis Complete!")
                            else:
                                st.error(f"Analysis failed: {result['error']}")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                
                # Show analysis results
                if st.session_state.video_analysis:
                    st.markdown("---")
                    st.markdown("### 🎯 Pitch Analysis Results")
                    st.markdown(st.session_state.video_analysis)
                    
                    # Copy analysis
                    st.download_button(
                        "📥 Download Analysis",
                        data=st.session_state.video_analysis,
                        file_name="pitch_analysis.md",
                        mime="text/markdown"
                    )
            else:
                st.error(f"✗ {validation['message']}")
        
        else:
            st.info("💡 **Tips for a great pitch video:**")
            st.markdown("""
            - **Duration**: 60-90 seconds is ideal
            - **Lighting**: Face a window or light source
            - **Framing**: Head and shoulders, eyes at top third
            - **Background**: Clean, professional
            - **Audio**: Quiet environment, speak clearly
            """)
        
        # Set placeholder values for video mode
        resume_text = st.session_state.resume_text or "[Video Mode - Resume not required]"
        job_description = video_context if uploaded_video else ""
    
    # ─────────────────────────────────────────────────────────────
    # PRACTICE MODE - INTERVIEW ROLEPLAY
    # ─────────────────────────────────────────────────────────────
    elif input_mode == "🥊 Practice":
        st.markdown("#### 🥊 THE WAR ROOM")
        st.caption("Practice with AI-powered interview questions. Get scored on your performance.")
        
        # Initialize practice session state
        if "practice_messages" not in st.session_state:
            st.session_state.practice_messages = []
        if "practice_started" not in st.session_state:
            st.session_state.practice_started = False
        if "practice_resume" not in st.session_state:
            st.session_state.practice_resume = ""
        if "practice_jd" not in st.session_state:
            st.session_state.practice_jd = ""
        
        # Step 1: Load Resume
        st.markdown("##### 📄 Step 1: Load Your Resume")
        practice_resume_method = st.radio(
            "Resume source",
            ["📁 Upload", "📝 Paste", "🔄 Use from Text/File mode"],
            horizontal=True,
            key="practice_resume_method"
        )
        
        if practice_resume_method == "📁 Upload":
            practice_resume_file = st.file_uploader(
                "Upload resume", 
                type=['pdf', 'md', 'txt'],
                key="practice_resume_upload"
            )
            if practice_resume_file:
                st.session_state.practice_resume = extract_text_from_upload(practice_resume_file)
                st.success(f"✓ Resume loaded ({len(st.session_state.practice_resume)} chars)")
        elif practice_resume_method == "📝 Paste":
            st.session_state.practice_resume = st.text_area(
                "Paste resume",
                value=st.session_state.practice_resume,
                height=200,
                key="practice_resume_paste"
            )
        else:  # Use from Text/File mode
            if st.session_state.resume_text:
                st.session_state.practice_resume = st.session_state.resume_text
                st.success(f"✓ Using resume from Text/File mode ({len(st.session_state.practice_resume)} chars)")
            else:
                st.warning("No resume found. Upload one in Text/File mode first.")
        
        # Step 2: Load JD
        st.markdown("##### 📋 Step 2: Target Job Description")
        st.session_state.practice_jd = st.text_area(
            "Paste Job Description",
            value=st.session_state.practice_jd or st.session_state.jd_text,
            height=200,
            placeholder="Paste the job description to practice for...",
            key="practice_jd_input"
        )
        
        st.markdown("---")
        
        # Step 3: Practice Options
        st.markdown("##### 🎭 Step 3: Practice Type")
        practice_type = st.selectbox(
            "What would you like to practice?",
            [
                "🎤 Behavioral Questions (STAR method)",
                "💼 Technical/Role Questions",
                "🤝 Tell me about yourself",
                "💡 Why this company/role?",
                "🔥 Tough Questions (weaknesses, gaps, failures)",
                "💰 Salary Negotiation",
                "❓ Random Mix"
            ],
            key="practice_type"
        )
        
        # Start Practice Session
        col_start, col_reset = st.columns(2)
        with col_start:
            if st.button("🚀 Start Practice Session", use_container_width=True, type="primary"):
                if st.session_state.practice_resume and st.session_state.practice_jd:
                    st.session_state.practice_started = True
                    st.session_state.practice_messages = []
                    
                    # Generate first question
                    system_prompt = f"""You are an expert interview coach conducting a mock interview.

CANDIDATE'S RESUME:
{st.session_state.practice_resume[:3000]}

TARGET JOB DESCRIPTION:
{st.session_state.practice_jd[:2000]}

PRACTICE TYPE: {practice_type}

Your role:
1. Ask ONE interview question at a time
2. After the candidate responds, provide brief feedback (1-2 sentences)
3. Then ask a follow-up or new question
4. Be encouraging but honest
5. Reference specific details from their resume and the JD
6. For STAR questions, prompt for Situation, Task, Action, Result if they miss parts

Start by introducing yourself as the interviewer and asking your first question."""

                    st.session_state.practice_messages.append({
                        "role": "system",
                        "content": system_prompt
                    })
                    
                    # Get first AI question
                    try:
                        from logic.generator import generate_signal_output, get_provider
                        import google.generativeai as genai
                        from groq import Groq
                        
                        if selected_model.startswith("groq:"):
                            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
                            response = client.chat.completions.create(
                                model=selected_model.replace("groq:", ""),
                                messages=st.session_state.practice_messages,
                                temperature=0.8
                            )
                            ai_response = response.choices[0].message.content
                        elif selected_model.startswith("ollama:"):
                            import ollama
                            response = ollama.chat(
                                model=selected_model.replace("ollama:", ""),
                                messages=st.session_state.practice_messages
                            )
                            ai_response = response['message']['content']
                        else:
                            from openai import OpenAI
                            client = OpenAI()
                            response = client.chat.completions.create(
                                model=selected_model,
                                messages=st.session_state.practice_messages
                            )
                            ai_response = response.choices[0].message.content
                        
                        st.session_state.practice_messages.append({
                            "role": "assistant",
                            "content": ai_response
                        })
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error starting practice: {str(e)}")
                else:
                    st.warning("Please load your resume and job description first!")
        
        with col_reset:
            if st.button("🔄 Reset Session", use_container_width=True):
                st.session_state.practice_started = False
                st.session_state.practice_messages = []
                st.rerun()
        
        # Display conversation
        if st.session_state.practice_started and st.session_state.practice_messages:
            st.markdown("---")
            st.markdown("##### 💬 Interview Conversation")
            
            # Show messages (skip system prompt)
            for msg in st.session_state.practice_messages[1:]:
                if msg["role"] == "assistant":
                    st.markdown(f"**🎯 Interviewer:** {msg['content']}")
                else:
                    st.markdown(f"**👤 You:** {msg['content']}")
                st.markdown("")
            
            # User input
            user_response = st.text_area(
                "Your response:",
                height=150,
                placeholder="Type your answer here... Be specific, use examples from your experience.",
                key="practice_user_input"
            )
            
            if st.button("📤 Send Response", use_container_width=True):
                if user_response:
                    st.session_state.practice_messages.append({
                        "role": "user",
                        "content": user_response
                    })
                    
                    # Get AI follow-up
                    try:
                        if selected_model.startswith("groq:"):
                            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
                            response = client.chat.completions.create(
                                model=selected_model.replace("groq:", ""),
                                messages=st.session_state.practice_messages,
                                temperature=0.8
                            )
                            ai_response = response.choices[0].message.content
                        elif selected_model.startswith("ollama:"):
                            import ollama
                            response = ollama.chat(
                                model=selected_model.replace("ollama:", ""),
                                messages=st.session_state.practice_messages
                            )
                            ai_response = response['message']['content']
                        else:
                            from openai import OpenAI
                            client = OpenAI()
                            response = client.chat.completions.create(
                                model=selected_model,
                                messages=st.session_state.practice_messages
                            )
                            ai_response = response.choices[0].message.content
                        
                        st.session_state.practice_messages.append({
                            "role": "assistant",
                            "content": ai_response
                        })
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        # Set values for the rest of the app
        resume_text = st.session_state.practice_resume or ""
        job_description = st.session_state.practice_jd or ""
    
    st.markdown("")
    
    # C. The Persona Selector (only for Intel mode)
    if input_mode == "� Intel":
        persona_options = get_persona_options()
        target_persona = st.selectbox(
            "Target Persona (The Lens)",
            options=persona_options,
            help="Tunes the output style for the hiring manager's mindset."
        )
        
        st.caption(get_persona_description(target_persona))
        
        st.markdown("")
        
        # Token estimation
        if resume_text and job_description:
            messages = construct_basin_prompt(resume_text, job_description, target_persona)
            estimated_tokens = estimate_tokens(messages)
            st.caption(f"📊 Estimated input: ~{estimated_tokens:,} tokens")
    else:
        target_persona = "The Operator (Process & Efficiency)"  # Default for video/practice mode


# ═══════════════════════════════════════════════════════════════
# OUTPUT COLUMN
# ═══════════════════════════════════════════════════════════════

with col2:
    st.markdown("### 📤 Architect Output (The Bridge)")
    
    # The Deploy Button
    deploy_clicked = st.button(
        "🚀 Deploy Signal Architecture",
        type="primary",
        use_container_width=True,
        disabled=not (resume_text and job_description)
    )
    
    if deploy_clicked:
        # Determine what API key is needed (if any)
        needs_api_key = True
        has_api_key = False
        
        if selected_model.startswith("ollama:"):
            needs_api_key = False  # Local model, no key needed
            has_api_key = True
        elif selected_model.startswith("groq:"):
            has_api_key = bool(os.environ.get("GROQ_API_KEY"))
        elif selected_model.startswith("gemini"):
            has_api_key = bool(os.environ.get("GOOGLE_API_KEY"))
        else:  # OpenAI
            has_api_key = bool(os.environ.get("OPENAI_API_KEY"))
        
        # Validation
        if not MOCK_MODE and needs_api_key and not has_api_key:
            st.error("⚠ Error: Missing API Key. Please authenticate in the sidebar.")
        elif not resume_text:
            st.warning("⚠ Waiting for Signal: Please provide a resume.")
        elif not job_description:
            st.warning("⚠ Waiting for Signal: Please provide a job description.")
        else:
            # Execute the Basin Protocol
            with st.spinner("Analyzing Pain Points & Architecting Narrative..."):
                try:
                    # 1. Construct the Basin Prompt
                    messages = construct_basin_prompt(resume_text, job_description, target_persona)
                    
                    # 2. Generate Output
                    response = generate_signal_output(messages, model=selected_model)
                    
                    # 3. Display Results
                    st.success("✅ Signal Detected. Architecture Complete.")
                    
                    # Gap Analysis
                    st.markdown("#### 🔍 Gap Analysis")
                    with st.expander("View Pain Point Analysis", expanded=True):
                        st.markdown(response.get("gap_analysis", "No analysis generated."))
                    
                    st.markdown("")
                    
                    # Professional Summary
                    st.markdown("#### 📄 Tailored Professional Summary")
                    summary = response.get("summary", "No summary generated.")
                    st.info(summary)
                    st.code(summary, language=None)
                    
                    st.markdown("")
                    
                    # Sniper Email Blurb
                    st.markdown("#### 🎯 'Sniper' Cover Blurb")
                    email_blurb = response.get("email_blurb", "No blurb generated.")
                    st.text_area(
                        "Ready to copy",
                        value=email_blurb,
                        height=200,
                        label_visibility="collapsed"
                    )
                    
                    # ─────────────────────────────────────────────────
                    # VOICE OUTPUT: Generate Audio Cover Letter
                    # ─────────────────────────────────────────────────
                    st.markdown("")
                    st.markdown("#### 🔊 Audio Cover Letter")
                    
                    if st.button("🎧 Generate Audio Version", key="generate_tts"):
                        with st.spinner("Generating voice message..."):
                            try:
                                audio_data = generate_speech(email_blurb, voice=selected_voice)
                                st.session_state.generated_audio = audio_data
                                st.success("✓ Voice message ready!")
                            except Exception as e:
                                st.error(f"TTS failed: {str(e)}")
                    
                    if st.session_state.generated_audio:
                        st.audio(st.session_state.generated_audio, format="audio/mp3")
                        st.download_button(
                            "📥 Download Audio",
                            data=st.session_state.generated_audio,
                            file_name="cover_letter_audio.mp3",
                            mime="audio/mp3"
                        )
                    
                    st.markdown("")
                    
                    # Key Bullets (if present)
                    key_bullets = response.get("key_bullets", [])
                    if key_bullets:
                        st.markdown("#### 🎯 Key Bullets (Evidence)")
                        for i, bullet in enumerate(key_bullets, 1):
                            st.markdown(f"**{i}.** {bullet}")
                    
                except Exception as e:
                    st.error(f"❌ System Failure: {str(e)}")
                    st.exception(e)
    
    else:
        # Placeholder when not deployed
        st.markdown("""
        <div class="output-card">
            <p style="color: #666; text-align: center;">
                🎤 Record or upload your data, then deploy the Signal Architecture.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick tips
        st.markdown("")
        st.markdown("#### 💡 Voice Mode Tips")
        st.markdown("""
        1. **Voice Resume**: Click the mic, speak, click again to stop
        2. **Voice JD**: Describe the role's key requirements
        3. **Audio Output**: Generate a voice message to send
        """)
        
        st.markdown("")
        st.markdown("#### 📊 Voice Capabilities")
        st.markdown("""
        - 🎤 **Whisper STT**: Accurate speech-to-text
        - 🔊 **OpenAI TTS**: Professional voice synthesis
        - 📁 **Export**: Download audio cover letters
        """)


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
