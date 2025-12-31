"""
BASIN::NEXUS - Streamlit Landing Page
Redirects to the main React app while providing a quick demo
"""
import streamlit as st

st.set_page_config(
    page_title="BASIN::NEXUS v9.0",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #020617 0%, #1e293b 100%);
        padding: 2rem;
        border-radius: 10px;
        color: #D4AF37;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #0f172a;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #D4AF37;
        text-align: center;
    }
    .gold { color: #D4AF37; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎯 BASIN::NEXUS v9.0</h1>
    <p style="font-size: 1.2rem;">Executive Career Intelligence OS</p>
</div>
""", unsafe_allow_html=True)

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Lines of Code", "10,500+", delta="Python + TypeScript")
with col2:
    st.metric("Modules", "21", delta="Integrated Systems")
with col3:
    st.metric("Pipeline Generated", "$10M+", delta="GTM Impact")
with col4:
    st.metric("Career Hits", "19,451", delta="Signal Engine")

st.divider()

# About
st.markdown("""
## 👤 About the Builder

**Leon Basin** — Revenue Architect | AI Builder | 15+ Years GTM

> "I don't just sell technology. I build it."

This platform represents my approach to GTM: **systems over playbooks, signals over spam**.

---

## 🏗️ Architecture

| Module | Description |
|--------|-------------|
| **War Room** | Executive dashboard with AI market signals |
| **Pipeline Tracker** | Kanban board for opportunity management |
| **Network CRM** | Contact intelligence with relationship scoring |
| **The Dojo** | Interview simulation with AI |
| **Identity Engine** | 22-layer professional knowledge base |
| **Agent Hub** | Autonomous AI research agents |

---

## 🔗 Explore More
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.link_button("📦 View Source Code", "https://github.com/BasinLeon/basin-signal-engine", use_container_width=True)

with col2:
    st.link_button("🌐 Portfolio", "https://basinleon.github.io", use_container_width=True)

with col3:
    st.link_button("�� LinkedIn", "https://linkedin.com/in/leonbasin", use_container_width=True)

st.divider()
st.caption("Built by Leon Basin | Revenue Architect | Python + AI Builder")
