"""
BASIN::NEXUS - Data Bridge Module
═══════════════════════════════════════════════════════════════════════════════

Bridges data between Streamlit (Python) and React (TypeScript) versions.

EXPORT: Streamlit → JSON → React
IMPORT: React → JSON → Streamlit

Protocol: Build once, use everywhere.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import streamlit as st

# ═══════════════════════════════════════════════════════════════
# EXPORT FUNCTIONS (Streamlit → JSON)
# ═══════════════════════════════════════════════════════════════

def export_all_data() -> Dict:
    """Export all Basin::Nexus data as a unified JSON structure."""
    
    export_data = {
        "version": "5.0",
        "exported_at": datetime.now().isoformat(),
        "source": "streamlit_python",
        "contacts": st.session_state.get('network_contacts', []),
        "outreach_log": st.session_state.get('outreach_log', []),
        "deals": st.session_state.get('crm_deals', []),
        "crm_contacts": st.session_state.get('crm_contacts', []),
        "interview_log": st.session_state.get('interview_log', []),
        "story_bank": st.session_state.get('story_bank', []),
        "resume_text": st.session_state.get('resume_text', ''),
        "jd_text": st.session_state.get('jd_text', ''),
        "target_company": st.session_state.get('target_company', ''),
        "target_role": st.session_state.get('target_role', ''),
    }
    
    return export_data


def export_to_file(filepath: str = "data/nexus_export.json") -> str:
    """Export all data to a JSON file."""
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    data = export_all_data()
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    
    return filepath


def export_for_website() -> Dict:
    """Export a public-safe subset for basinleon.com."""
    
    contacts = st.session_state.get('network_contacts', [])
    
    # Only export non-sensitive fields
    public_contacts = []
    for c in contacts[-10:]:  # Last 10 only
        public_contacts.append({
            "name": c.get('name', 'Anonymous'),
            "company": c.get('company', 'Unknown'),
            "stage": c.get('stage', '❄️ COLD'),
            "date": c.get('created_at', '')[:10] if c.get('created_at') else ''
        })
    
    return {
        "version": "5.0",
        "updated_at": datetime.now().isoformat(),
        "contacts": public_contacts,
        "stats": {
            "total_contacts": len(contacts),
            "total_sessions": len(st.session_state.get('interview_log', [])),
            "active_deals": len(st.session_state.get('crm_deals', []))
        }
    }


# ═══════════════════════════════════════════════════════════════
# IMPORT FUNCTIONS (JSON → Streamlit)
# ═══════════════════════════════════════════════════════════════

def import_from_json(data: Dict) -> bool:
    """Import data from JSON into session state."""
    
    try:
        # Validate version
        version = data.get('version', '0')
        source = data.get('source', 'unknown')
        
        # Import contacts
        if 'contacts' in data:
            existing = st.session_state.get('network_contacts', [])
            imported = data['contacts']
            
            # Merge by name (avoid duplicates)
            existing_names = {c['name'].lower() for c in existing}
            for contact in imported:
                if contact.get('name', '').lower() not in existing_names:
                    existing.append(contact)
            
            st.session_state.network_contacts = existing
        
        # Import deals
        if 'deals' in data:
            existing = st.session_state.get('crm_deals', [])
            imported = data['deals']
            
            existing_companies = {d.get('company', '').lower() for d in existing}
            for deal in imported:
                if deal.get('company', '').lower() not in existing_companies:
                    existing.append(deal)
            
            st.session_state.crm_deals = existing
        
        # Import interview sessions
        if 'interview_log' in data or 'sessions' in data:
            sessions = data.get('interview_log', data.get('sessions', []))
            existing = st.session_state.get('interview_log', [])
            existing.extend(sessions)
            st.session_state.interview_log = existing
        
        # Import resume/JD if present
        if data.get('resume_text'):
            st.session_state.resume_text = data['resume_text']
        if data.get('jd_text'):
            st.session_state.jd_text = data['jd_text']
        
        return True
        
    except Exception as e:
        print(f"Import error: {e}")
        return False


def import_from_file(filepath: str) -> bool:
    """Import data from a JSON file."""
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return import_from_json(data)
    except Exception as e:
        print(f"File import error: {e}")
        return False


# ═══════════════════════════════════════════════════════════════
# STREAMLIT UI COMPONENT
# ═══════════════════════════════════════════════════════════════

def render_data_bridge():
    """Render the data bridge UI in Streamlit."""
    
    st.subheader("🔗 Data Bridge")
    st.caption("Sync data between Streamlit and React versions of Basin::Nexus")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📤 Export")
        
        if st.button("📥 Export All Data", type="primary"):
            data = export_all_data()
            json_str = json.dumps(data, indent=2, default=str)
            
            st.download_button(
                label="⬇️ Download nexus_export.json",
                data=json_str,
                file_name="nexus_export.json",
                mime="application/json"
            )
            st.success("✅ Data ready for download!")
        
        if st.button("🌐 Export for Website"):
            data = export_for_website()
            json_str = json.dumps(data, indent=2, default=str)
            
            st.code(json_str, language="json")
            st.caption("Copy this to your website's data folder")
    
    with col2:
        st.markdown("### 📥 Import")
        
        uploaded_file = st.file_uploader(
            "Upload JSON from React",
            type=['json'],
            key="import_json"
        )
        
        if uploaded_file:
            try:
                data = json.load(uploaded_file)
                
                st.markdown("**Preview:**")
                st.json({
                    "version": data.get('version'),
                    "source": data.get('source'),
                    "contacts": len(data.get('contacts', [])),
                    "deals": len(data.get('deals', [])),
                    "sessions": len(data.get('sessions', data.get('interview_log', [])))
                })
                
                if st.button("✅ Import This Data"):
                    if import_from_json(data):
                        st.success("✅ Data imported successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Import failed")
            except Exception as e:
                st.error(f"Invalid JSON: {e}")
    
    # Sync status
    st.markdown("---")
    st.markdown("### 📊 Current Data Status")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Contacts", len(st.session_state.get('network_contacts', [])))
    col2.metric("Deals", len(st.session_state.get('crm_deals', [])))
    col3.metric("Sessions", len(st.session_state.get('interview_log', [])))
    col4.metric("Outreach", len(st.session_state.get('outreach_log', [])))
