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
    page_title="Basin Signal Engine",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ═══════════════════════════════════════════════════════════════
# CUSTOM STYLING
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<style>
    /* Dark mode optimizations */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0;
    }
    
    .sub-header {
        color: #888;
        font-style: italic;
        margin-top: 0;
    }
    
    /* Status badge */
    .status-badge {
        background: linear-gradient(135deg, #00c853 0%, #00e676 100%);
        color: #000;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-badge.mock {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
    }
    
    .status-badge.voice {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff;
    }
    
    /* Card styling */
    .output-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    /* Voice indicator */
    .voice-active {
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        margin: 20px 0;
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

# Header
st.markdown('<h1 class="main-header">🏗️ Basin Signal Engine</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Voice-First Career Intelligence Platform</p>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Two-column layout
col1, col2 = st.columns([1, 1], gap="large")


# ═══════════════════════════════════════════════════════════════
# INPUT COLUMN
# ═══════════════════════════════════════════════════════════════

with col1:
    st.markdown("### 📥 Ingest Data (The Signal)")
    
    # Input Mode Toggle - NOW WITH VIDEO!
    input_mode = st.radio(
        "Input Mode",
        ["📄 Text/File", "🎤 Voice", "📹 Video"],
        horizontal=True,
        help="Choose: Text/File, Voice recording, or Video pitch analysis."
    )
    
    st.markdown("")
    
    # ─────────────────────────────────────────────────────────────
    # TEXT/FILE MODE
    # ─────────────────────────────────────────────────────────────
    if input_mode == "📄 Text/File":
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
        
        # B. The Target (Job Description) - EXPANDED
        job_description = st.text_area(
            "Paste Job Description / Context",
            height=400,  # Increased from 200 to fit longer JDs
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
    # VOICE MODE
    # ─────────────────────────────────────────────────────────────
    elif input_mode == "🎤 Voice":
        st.markdown("#### 🎤 Voice Resume Input")
        st.caption("Click to record your career background (2-3 minutes)")
        
        # Resume Voice Recorder
        audio_bytes_resume = audio_recorder(
            text="Click to record resume",
            recording_color="#e74c3c",
            neutral_color="#667eea",
            icon_name="microphone",
            icon_size="2x",
            key="resume_recorder"
        )
        
        if audio_bytes_resume:
            st.audio(audio_bytes_resume, format="audio/wav")
            st.caption(f"📊 Recording captured ({len(audio_bytes_resume)} bytes)")
            
            # Transcribe button
            if st.button("🔄 Transcribe Resume", key="transcribe_resume"):
                with st.spinner("Transcribing with Whisper..."):
                    try:
                        transcript = transcribe_audio(audio_bytes_resume, use_api=True)
                        st.session_state.voice_resume_text = transcript
                        st.success("✓ Transcription complete!")
                    except Exception as e:
                        st.error(f"Transcription failed: {str(e)}")
            
            # Show transcription
            if st.session_state.voice_resume_text:
                resume_text = st.text_area(
                    "Transcribed Resume (edit if needed)",
                    value=st.session_state.voice_resume_text,
                    height=150,
                    key="resume_transcript_display"
                )
                st.session_state.voice_resume_text = resume_text
            else:
                resume_text = ""
        else:
            resume_text = st.session_state.voice_resume_text or ""
            if resume_text:
                st.info("Previous transcription available")
                st.text_area(
                    "Previous Transcription",
                    value=resume_text,
                    height=100,
                    disabled=True
                )
        
        st.markdown("---")
        
        st.markdown("#### 🎤 Voice JD Input")
        st.caption("Click to describe the role requirements")
        
        # JD Voice Recorder
        audio_bytes_jd = audio_recorder(
            text="Click to record JD",
            recording_color="#e74c3c",
            neutral_color="#764ba2",
            icon_name="microphone",
            icon_size="2x",
            key="jd_recorder"
        )
        
        if audio_bytes_jd:
            st.audio(audio_bytes_jd, format="audio/wav")
            st.caption(f"📊 Recording captured ({len(audio_bytes_jd)} bytes)")
            
            if st.button("🔄 Transcribe JD", key="transcribe_jd"):
                with st.spinner("Transcribing with Whisper..."):
                    try:
                        transcript = transcribe_audio(audio_bytes_jd, use_api=True)
                        st.session_state.voice_jd_text = transcript
                        st.success("✓ Transcription complete!")
                    except Exception as e:
                        st.error(f"Transcription failed: {str(e)}")
            
            if st.session_state.voice_jd_text:
                job_description = st.text_area(
                    "Transcribed JD (edit if needed)",
                    value=st.session_state.voice_jd_text,
                    height=150,
                    key="jd_transcript_display"
                )
                st.session_state.voice_jd_text = job_description
            else:
                job_description = ""
        else:
            job_description = st.session_state.voice_jd_text or ""
            if job_description:
                st.info("Previous transcription available")
                st.text_area(
                    "Previous Transcription",
                    value=job_description,
                    height=100,
                    disabled=True
                )
    
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
    
    st.markdown("")
    
    # C. The Persona Selector (always visible for text/voice modes)
    if input_mode != "📹 Video":
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
        target_persona = "The Operator (Process & Efficiency)"  # Default for video mode


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
