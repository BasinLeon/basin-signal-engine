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

# --- SIDEBAR: MISSION CONTROL (FLUID EXECUTIVE LIBRARY) ---
with st.sidebar:
    # 1. HEADER & SYSTEM STATUS
    st.markdown("### ⚡ BASIN::NEXUS")
    st.caption("v4.2 | REVENUE ARCHITECT OS")
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
    
    # Simplified Model Selector
    st.selectbox("LLM ENGINE", ["Llama 3.3 70B (Speed)", "Mixtral 8x7B (Logic)"], label_visibility="collapsed")
    
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
            ["Omni-Agent (Intel)", "Black Ops (Hunt)", "Analytics (Scoreboard)"],
            label_visibility="collapsed")
            
    elif "EXECUTION OPS" in mission_phase:
        st.caption("Focus: Scaling the Narrative & Team")
        selected_tool_label = st.radio("Select Tool:", 
            ["Practice (Dojo)", "Voice", "Talent Signal (Recruiter)"],
            label_visibility="collapsed")
            
    elif "ARCHITECT DECK" in mission_phase:
        st.caption("Focus: High-Level Strategy & Governance")
        selected_tool_label = st.radio("Select Tool:", 
            ["First 90 Days (Closer)", "Analytics (Scoreboard)", "Talent Signal (Recruiter)"],
            label_visibility="collapsed")

    # MAPPING TO SYSTEM KERNEL (Connecting UX to Logic)
    # This maps the "Cool Executive Names" to the internal "Functional Names"
    tool_map = {
        "Omni-Agent (Intel)": "📄 Intel",
        "Black Ops (Hunt)": "🎯 Hunt",
        "Analytics (Scoreboard)": "📊 Analytics",
        "Practice (Dojo)": "🥊 Practice (Dojo)",
        "Voice": "🎤 Voice",
        "Talent Signal (Recruiter)": "🔍 Talent Signal",
        "First 90 Days (Closer)": "🚀 First 90 Days"
    }
    
    input_mode = tool_map.get(selected_tool_label, "📄 Intel")

    st.markdown("---")

    # 4. FINAL FOOTER
    st.markdown("`OPERATOR: LEON BASIN`")
    st.markdown("`STATUS: ONLINE`")


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
    # Input Mode Controlled by Sidebar
    st.info(f"🧬 SYSTEM MODE: **{input_mode}**")
    
    st.markdown("")
    
    # ─────────────────────────────────────────────────────────────
    # INTEL MODE (Text/File Input)
    # ─────────────────────────────────────────────────────────────
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
    # 🎯 MODE 2: HUNT (TARGET ACQUISITION SYSTEM)
    # ==============================================================================
    elif input_mode == "🎯 Hunt":
        st.markdown("## TARGET ACQUISITION SYSTEM")
        st.caption("PROTOCOL: Generate high-precision search vectors. Bypass noise.")
        
        # 1. THE FREQUENCY SELECTOR
        tab_linked, tab_xray, tab_social, tab_blackops = st.tabs(["LINKEDIN VECTORS", "ATS X-RAY", "SOCIAL SIGNAL", "🏴‍☠️ BLACK OPS"])
        
        # ------------------------------------------------------------------
        # TAB 1: LINKEDIN VECTORS (THE MASTER KEY)
        # ------------------------------------------------------------------
        with tab_linked:
            st.markdown("#### 1. CONFIGURE SEARCH VECTOR")
            
            c1, c2 = st.columns(2)
            with c1:
                # Strategies from your "Master Boolean Library"
                search_strategy = st.selectbox("STRATEGY PROTOCOL", 
                    ["The 'HR Tech' Strike (Home Turf)", 
                     "The 'GTM Operations' Strike (Builder)", 
                     "The 'Partnerships' Strike (Ecosystem)", 
                     "The 'Chief of Staff' Strike (Wildcard)"])
            with c2:
                geo_lock = st.selectbox("GEOGRAPHIC LOCK", ["Remote", "San Francisco Bay Area", "New York", "Global"])

            st.markdown("#### 2. SIGNAL REFINEMENT")
            k1, k2 = st.columns([3, 1])
            with k1:
                keywords = st.text_input("MUST-HAVE KEYWORDS", placeholder="e.g. 'Zero Trust' OR 'Python'")
            with k2:
                exclude_noise = st.checkbox("NOISE FILTER", value=True, help="Removes Interns/Entry Level")

            # LOGIC ENGINE
            if st.button("GENERATE SEARCH STRING", type="primary", use_container_width=True):
                
                base_string = ""
                
                # LOGIC MAP
                if "HR Tech" in search_strategy:
                    base_string = '("Head of" OR "Senior Manager" OR "Director") AND ("Partnerships" OR "GTM" OR "Business Development" OR "Alliances") AND ("HR Tech" OR "Workforce" OR "Payroll" OR "People Ops" OR "Compliance")'
                elif "GTM Operations" in search_strategy:
                    base_string = '("GTM Operations" OR "Revenue Operations" OR "Sales Strategy" OR "Go-to-Market Strategy") AND ("Manager" OR "Head of" OR "Lead") AND ("SaaS" OR "Tech")'
                    base_string += ' AND NOT ("Account Executive" OR "SDR" OR "Cold Call")'
                elif "Partnerships" in search_strategy:
                    base_string = '("Head of Partnerships" OR "Senior Partner Manager" OR "Head of Channel" OR "Strategic Alliances") AND ("SaaS" OR "Cybersecurity" OR "AI")'
                elif "Chief of Staff" in search_strategy:
                    base_string = '("Chief of Staff") AND ("Revenue" OR "Sales" OR "CRO" OR "GTM" OR "Strategy") AND ("Tech" OR "Startup")'

                if geo_lock != "Global":
                    base_string += f' AND ("{geo_lock}")'

                if exclude_noise:
                    base_string += ' AND NOT ("Intern" OR "Entry Level" OR "Part Time")'

                if keywords:
                    base_string += f' AND ({keywords})'

                st.markdown("---")
                st.caption("🎯 PRECISION VECTOR GENERATED")
                st.code(base_string, language="text")
                
                encoded_string = base_string.replace('"', '%22').replace(' ', '%20').replace('(', '%28').replace(')', '%29')
                st.markdown(f"[🚀 **EXECUTE MISSION (OPEN LINKEDIN)**](https://www.linkedin.com/jobs/search/?keywords={encoded_string})", unsafe_allow_html=True)

        # ------------------------------------------------------------------
        # TAB 2: ATS X-RAY
        # ------------------------------------------------------------------
        with tab_xray:
            st.markdown("#### ☢️ DATABASE PENETRATION (GOOGLE)")
            st.caption("PROTOCOL: Direct query of ATS subdomains. Bypasses LinkedIn algorithm.")
            
            x1, x2 = st.columns([2, 1])
            with x1:
                ats_role = st.text_input("TARGET ROLE", value="Director of GTM", label_visibility="collapsed", placeholder="Role Title")
            with x2:
                ats_target = st.multiselect("TARGET SYSTEM", ["Lever", "Greenhouse", "Ashby"], default=["Lever", "Greenhouse", "Ashby"], label_visibility="collapsed")
            
            if st.button("INITIATE X-RAY SCAN", use_container_width=True):
                sites = []
                if "Lever" in ats_target: sites.append("site:lever.co")
                if "Greenhouse" in ats_target: sites.append("site:greenhouse.io")
                if "Ashby" in ats_target: sites.append("site:ashbyhq.com")
                
                site_logic = " OR ".join(sites)
                query = f'{site_logic} "{ats_role}"'
                
                st.code(query, language="text")
                st.markdown(f"[🚀 **EXECUTE GOOGLE SEARCH**](https://www.google.com/search?q={query.replace(' ', '+').replace('"', '%22')})", unsafe_allow_html=True)

        # ------------------------------------------------------------------
        # TAB 3: SOCIAL SIGNAL
        # ------------------------------------------------------------------
        with tab_social:
            st.markdown("#### 🐦 SIGNAL INTERCEPT (X/TWITTER)")
            st.caption("PROTOCOL: Detect 'Hiring' signals before job boards.")
            
            s1, s2 = st.columns([3, 1])
            with s1:
                social_role = st.text_input("ROLE KEYWORD", value="Revenue Operations", label_visibility="collapsed")
            with s2:
                min_likes = st.number_input("MIN SIGNAL (LIKES)", value=5, label_visibility="collapsed")
                
            if st.button("GENERATE SIGNAL STRING", use_container_width=True):
                query = f'("{social_role}") AND ("hiring" OR "join my team" OR "dm me") min_faves:{min_likes} -filter:retweets'
                st.code(query, language="text")
                st.markdown(f"[🚀 **EXECUTE INTERCEPT**](https://twitter.com/search?q={query.replace(' ', '%20')}&src=typed_query)", unsafe_allow_html=True)

        # ------------------------------------------------------------------
        # TAB 4: BLACK OPS (THE INDUSTRY BACKBONE)
        # ------------------------------------------------------------------
        with tab_blackops:
            st.markdown("#### 🏴‍☠️ SILICON VALLEY BACKCHANNELS")
            st.caption("PROTOCOL: Tap into VC Portfolios and Engineering Aggregators.")
            
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown("##### 🏦 VC PORTFOLIOS (THE MONEY)")
                st.markdown("*Direct access to portfolio job boards. High signal, low noise.*")
                
                if st.button("🍊 Y COMBINATOR (Work at a Startup)"):
                    st.markdown("[🚀 **OPEN YC JOBS**](https://www.workatastartup.com/companies?roles=Sales&roles=Operations)", unsafe_allow_html=True)
                
                if st.button("🌲 SEQUOIA CAPITAL (Portfolio)"):
                    st.markdown("[🚀 **OPEN SEQUOIA JOBS**](https://jobs.sequoiacap.com/jobs)", unsafe_allow_html=True)
                
                if st.button("🚀 ANDREESSEN HOROWITZ (Portfolio)"):
                    st.markdown("[🚀 **OPEN A16Z JOBS**](https://jobs.a16z.com/)", unsafe_allow_html=True)

            with c2:
                st.markdown("##### 🕵️ STEALTH AGGREGATORS")
                st.markdown("*Where the engineers and founders hang out.*")
                
                if st.button("👾 HACKER NEWS ('Who is Hiring')"):
                    hn_query = "hiring GTM OR Sales OR Operations"
                    st.markdown(f"[🚀 **SCAN HACKER NEWS**](https://hn.algolia.com/?q={hn_query.replace(' ', '+')})", unsafe_allow_html=True)
                
                if st.button("✌️ WELLFOUND (AngelList)"):
                    st.markdown("[🚀 **SCAN STARTUPS**](https://wellfound.com/jobs)", unsafe_allow_html=True)

    # ==============================================================================
    # 📊 MODE 6: COMMAND CENTER (CAREER OS)
    # ==============================================================================
    elif input_mode == "📊 Analytics":
        st.markdown("## CAREER OPERATIONS CENTER")
        st.caption("PROTOCOL: PIPELINE FORECASTING & REVENUE INTELLIGENCE")
        
        # --- 1. GLOBAL TELEMETRY (THE NUMBERS) ---
        st.markdown("#### 1. PIPELINE TELEMETRY")
        
        # User Inputs (Simulating CRM Data Entry)
        with st.expander("📝 UPDATE WEEKLY METRICS", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                apps = st.number_input("APPLICATIONS SENT", value=42, step=1, help="Total outbound volume")
            with c2:
                screens = st.number_input("RECRUITER SCREENS", value=6, step=1, help="Top of Funnel conversion")
            with c3:
                hms = st.number_input("MANAGER INTERVIEWS", value=2, step=1, help="Mid Funnel conversion")
            with c4:
                finals = st.number_input("FINAL ROUNDS", value=1, step=1, help="Bottom Funnel conversion")

        # METRIC CALCULATIONS
        screen_rate = (screens / apps) * 100 if apps > 0 else 0.0
        hm_rate = (hms / screens) * 100 if screens > 0 else 0.0
        close_rate = (finals / hms) * 100 if hms > 0 else 0.0
        
        # PIPELINE VALUE (The "Apollo" Feature)
        avg_salary = 220000 # Your Target OTE
        pipeline_value = (screens * 0.1 * avg_salary) + (hms * 0.3 * avg_salary) + (finals * 0.6 * avg_salary)
        
        st.markdown("---")
        
        # --- 2. THE DASHBOARD (VISUALS) ---
        
        # ROW 1: HEALTH METRICS
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("PIPELINE VELOCITY", f"{screens} Leads/Wk", "Active Signal")
        k2.metric("FORECASTED REVENUE", f"${pipeline_value/1000:,.0f}k", "Weighted Value")
        k3.metric("CONVERSION (APP > SCREEN)", f"{screen_rate:.1f}%", f"{screen_rate-10:.1f}% vs Benchmark")
        k4.metric("OFFER PROBABILITY", f"{min(finals*25, 95)}%", "Based on Finals")
        
        # ROW 2: FUNNEL DIAGNOSTICS (THE COACH)
        st.markdown("#### 2. SYSTEM DIAGNOSTICS")
        
        d1, d2 = st.columns([2, 1])
        
        with d1:
            # LOGIC ENGINE: WHERE IS THE LEAK?
            if screen_rate < 10:
                status_color = "error"
                diagnosis = "CRITICAL FAILURE: TOP OF FUNNEL"
                fix = "Your Resume/Outreach is not converting. The Market is rejecting your 'Signal'."
                action = "GO TO 'INTEL MODE' -> RUN 'OMNI-SCAN' TO FIX KEYWORDS."
            elif hm_rate < 30:
                status_color = "warning"
                diagnosis = "WARNING: MID-FUNNEL LEAK"
                fix = "You are passing the Recruiter but failing the Hiring Manager. Your narrative lacks 'Builder' authority."
                action = "GO TO 'PRACTICE MODE' -> DRILL 'THE SKEPTIC' PERSONA."
            elif finals > 0:
                status_color = "success"
                diagnosis = "SYSTEM OPTIMIZED: CLOSING MODE"
                fix = "You are in the kill zone. Focus entirely on the 'First 90 Days' plan."
                action = "GO TO 'FIRST 90 DAYS' -> GENERATE EXECUTION PLAN."
            else:
                status_color = "info"
                diagnosis = "SYSTEM CALIBRATING..."
                fix = "Increase outbound volume to generate statistically significant data."
                action = "GO TO 'HUNT MODE' -> EXECUTE 'BLACK OPS' SEARCH."

            # RENDER DIAGNOSTIC CARD
            if status_color == "error":
                st.error(f"**DIAGNOSIS:** {diagnosis}")
            elif status_color == "warning":
                st.warning(f"**DIAGNOSIS:** {diagnosis}")
            elif status_color == "success":
                st.success(f"**DIAGNOSIS:** {diagnosis}")
            else:
                st.info(f"**DIAGNOSIS:** {diagnosis}")
                
            st.markdown(f"**ROOT CAUSE:** {fix}")
            st.caption(f"**RECOMMENDED PROTOCOL:** {action}")

        with d2:
            # MOMENTUM GAUGE
            st.markdown("**MOMENTUM SCORE**")
            momentum = min((apps * 1) + (screens * 5) + (hms * 10), 100)
            st.progress(momentum / 100)
            st.caption(f"Current Load: {momentum}% Capacity")
            
            # TIME TO OFFER ESTIMATOR
            needed_screens = max(0, 15 - screens) # Assume 15 screens = 1 offer
            weeks_left = needed_screens / 2 # Assume 2 screens/week velocity
            if finals > 0:
                st.metric("EST. TIME TO OFFER", "2 Weeks", "In Final Rounds")
            else:
                st.metric("EST. TIME TO OFFER", f"{weeks_left:.1f} Weeks", "Based on Velocity")

        # --- 3. STRATEGIC ACTIONS ---
        st.markdown("---")
        st.markdown("#### 3. DEPLOY COUNTER-MEASURES")
        
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("🚀 LAUNCH 'BLACK OPS' HUNT", use_container_width=True):
                st.toast("Redirecting to Search Arrays...")
        with b2:
            if st.button("🧬 RUN RESUME DIAGNOSTIC", use_container_width=True):
                st.toast("Loading Omni-Agent...")
        with b3:
            if st.button("⚔️ ENTER THE DOJO", use_container_width=True):
                st.toast("Initializing Combat Simulator...")

    
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
    



# ==============================================================================
# 🖥️ SYSTEM STATUS FOOTER
# ==============================================================================
st.markdown("---")
f1, f2, f3 = st.columns([1, 1, 2])

with f1:
    st.caption("SYSTEM STATUS: **ONLINE**")
with f2:
    st.caption("OPERATOR: **LEON BASIN**")
with f3:
    st.caption("BUILD: **BASIN::NEXUS v4.1 (Revenue Architect Edition)**")
