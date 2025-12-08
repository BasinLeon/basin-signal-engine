"""
BASIN::NEXUS // BIO-OS MODULE
The Biological Operating System for the Corporate Athlete.
Manages state, focus, and recovery protocols.
"""

import streamlit as st
import time
from datetime import datetime
import random

# ═══════════════════════════════════════════════════════════════
# STATE MANAGEMENT
# ═══════════════════════════════════════════════════════════════

def init_bio_state():
    """Initialize Bio-OS session state variables."""
    if 'bio_session_start' not in st.session_state:
        st.session_state.bio_session_start = datetime.now()
    if 'bio_battery' not in st.session_state:
        st.session_state.bio_battery = 100
    if 'bio_state' not in st.session_state:
        st.session_state.bio_state = "NEUTRAL"
    if 'deep_work_timer' not in st.session_state:
        st.session_state.deep_work_timer = 0
    if 'protocols_completed' not in st.session_state:
        st.session_state.protocols_completed = []

def get_bio_metrics():
    """Calculate current biological metrics."""
    # Simulate battery drain based on session time
    elapsed = (datetime.now() - st.session_state.bio_session_start).seconds / 60
    drain = elapsed * 0.5  # 0.5% drain per minute of session
    current_battery = max(0, 100 - drain)
    
    # Recovery boost from protocols
    boost = len(st.session_state.protocols_completed) * 5
    current_battery = min(100, current_battery + boost)
    
    return {
        "battery": int(current_battery),
        "elapsed_min": int(elapsed),
        "state": st.session_state.bio_state
    }

# ═══════════════════════════════════════════════════════════════
# PROTOCOLS
# ═══════════════════════════════════════════════════════════════

PROTOCOLS = {
    "NEURO_PRIME": [
        "Hydration (500ml Water + Electrolytes)",
        "Nootropic Stack (Caffeine + L-Theanine)",
        "Binaural Beats (40Hz Gamma)",
        "Phone in Airplane Mode"
    ],
    "DEEP_WORK": [
        "Set Intent (One Single Task)",
        "Clear Visual Field",
        "Block Slack/Email",
        "Start Timer (90 Minutes)"
    ],
    "RECOVERY": [
        "NSDR (Non-Sleep Deep Rest) - 10 min",
        "Optical Flow (Walk/Horizon View)",
        "Cold Exposure / Face Dunk",
        "Box Breathing (4-4-4-4)"
    ]
}

def render_protocol_checklist(protocol_name):
    """Render a checklist for a specific protocol."""
    st.markdown(f"### 🧬 {protocol_name.replace('_', ' ')} PROTOCOL")
    
    completed_count = 0
    items = PROTOCOLS.get(protocol_name, [])
    
    for item in items:
        key = f"proto_{protocol_name}_{item}"
        if st.checkbox(item, key=key):
            completed_count += 1
            if item not in st.session_state.protocols_completed:
                st.session_state.protocols_completed.append(item)
    
    if completed_count == len(items):
        st.success(f"✅ {protocol_name} ACTIVATED")
        st.session_state.bio_state = protocol_name
        return True
    return False

# ═══════════════════════════════════════════════════════════════
# WIDGETS
# ═══════════════════════════════════════════════════════════════

def render_bio_dashboard():
    """Render the main Bio-OS dashboard widget."""
    metrics = get_bio_metrics()
    
    # Battery Visualization
    battery_color = "green" if metrics['battery'] > 70 else "orange" if metrics['battery'] > 30 else "red"
    
    st.markdown(f"""
    <div style="padding: 15px; border: 1px solid #333; border-radius: 10px; background-color: #0e1117;">
        <h3 style="margin-top: 0; color: #FFD700;">🧬 BIO-OS STATUS</h3>
        <p style="font-size: 0.8em; color: #888;">SYSTEM INTEGRITY MONITOR</p>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span>🔋 BATTERY</span>
            <span style="color: {battery_color}; font-weight: bold;">{metrics['battery']}%</span>
        </div>
        <div style="width: 100%; bg-color: #333; height: 10px; border-radius: 5px;">
            <div style="width: {metrics['battery']}%; background-color: {battery_color}; height: 100%; border-radius: 5px;"></div>
        </div>
        <div style="margin-top: 15px; font-family: monospace;">
            <p>⏱️ SESSION: {metrics['elapsed_min']} MIN</p>
            <p>🧠 STATE: <span style="color: #00ff00;">{metrics['state']}</span></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_breathing_guide():
    """Simple visual breathing guide."""
    st.markdown("### 🫁 BOX BREATHING")
    st.caption("Inhale (4s) > Hold (4s) > Exhale (4s) > Hold (4s)")
    
    if st.button("Start Breathing Cycle"):
        placeholder = st.empty()
        phases = [
            ("😤 INHALE", "green"), 
            ("🤐 HOLD", "yellow"), 
            ("😮‍💨 EXHALE", "blue"), 
            ("🤐 HOLD", "yellow")
        ]
        
        for _ in range(3):  # 3 cycles
            for text, color in phases:
                placeholder.markdown(f"<h1 style='text-align: center; color: {color}; transition: all 1s;'>{text}</h1>", unsafe_allow_html=True)
                time.sleep(4)
        
        placeholder.markdown("<h3 style='text-align: center;'>Cycle Complete. Focus Restored.</h3>", unsafe_allow_html=True)

