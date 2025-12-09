"""
BASIN::NEXUS - Networking CRM Module
═══════════════════════════════════════════════════════════════════════════════

Part of Basin::Nexus v1.0 Executive OS

FEATURES:
✅ People Database (Contacts with relationship stages)
✅ Outreach Tracker (Log every touch)
✅ Follow-Up Triggers (Automated reminders)
✅ Conversion Analytics (Response rates, funnel)
✅ X/LinkedIn Integration (Track by source)

THE RELATIONSHIP FUNNEL:
1. COLD → First touch (connect request, cold DM)
2. WARM → They responded or engaged
3. HOT → Active conversation, meeting scheduled
4. CHAMPION → They're helping you (referral, intro, advocate)

Protocol: Signal → Connect → Nurture → Convert
"""

import streamlit as st
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# ═══════════════════════════════════════════════════════════════
# RELATIONSHIP STAGES
# ═══════════════════════════════════════════════════════════════

RELATIONSHIP_STAGES = {
    "❄️ COLD": {
        "color": "#808080",
        "description": "No interaction yet",
        "next_action": "Send initial outreach"
    },
    "🌡️ WARM": {
        "color": "#fbbf24",
        "description": "They responded or engaged",
        "next_action": "Continue conversation, add value"
    },
    "🔥 HOT": {
        "color": "#f87171",
        "description": "Active conversation, meeting scheduled",
        "next_action": "Convert to opportunity"
    },
    "⭐ CHAMPION": {
        "color": "#4ade80",
        "description": "They're actively helping you",
        "next_action": "Maintain, reciprocate"
    }
}

SOURCES = [
    "🐦 X (Twitter)",
    "💼 LinkedIn",
    "📧 Cold Email",
    "🤝 Referral",
    "🎤 Event/Conference",
    "💬 Slack/Discord",
    "📞 Call",
    "🌐 Website",
    "📱 Other"
]

OUTREACH_TYPES = [
    "🐦 X DM",
    "🐦 X Reply/Comment",
    "🐦 X Like/Retweet",
    "💼 LinkedIn DM",
    "💼 LinkedIn Connect Request",
    "💼 LinkedIn Comment",
    "📧 Cold Email",
    "📧 Follow-Up Email",
    "📞 Call",
    "🎥 Video Message",
    "📝 Other"
]

RESPONSE_STATUS = [
    "📤 Sent",
    "👀 Viewed",
    "💬 Replied",
    "📅 Meeting Booked",
    "🚫 No Response",
    "❌ Rejected"
]


# ═══════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════

def init_network_state():
    """Initialize session state for networking CRM."""
    if 'network_contacts' not in st.session_state:
        st.session_state.network_contacts = []
    if 'outreach_log' not in st.session_state:
        st.session_state.outreach_log = []


def add_contact(name: str, company: str, title: str, source: str, 
                linkedin_url: str = "", twitter_handle: str = "", 
                email: str = "", notes: str = "") -> Dict:
    """Add a new contact to the network."""
    contact = {
        "id": len(st.session_state.network_contacts) + 1,
        "name": name,
        "company": company,
        "title": title,
        "source": source,
        "stage": "❄️ COLD",
        "linkedin_url": linkedin_url,
        "twitter_handle": twitter_handle,
        "email": email,
        "notes": notes,
        "created_at": datetime.now().isoformat(),
        "last_touch": None,
        "next_touch": (datetime.now() + timedelta(days=3)).isoformat(),
        "touch_count": 0
    }
    st.session_state.network_contacts.append(contact)
    return contact


def add_outreach(contact_id: int, outreach_type: str, content: str, 
                 response_status: str = "📤 Sent") -> Dict:
    """Log an outreach touch."""
    outreach = {
        "id": len(st.session_state.outreach_log) + 1,
        "contact_id": contact_id,
        "type": outreach_type,
        "content": content,
        "status": response_status,
        "sent_at": datetime.now().isoformat(),
        "response": None,
        "response_at": None
    }
    st.session_state.outreach_log.append(outreach)
    
    # Update contact's last touch
    for contact in st.session_state.network_contacts:
        if contact["id"] == contact_id:
            contact["last_touch"] = datetime.now().isoformat()
            contact["touch_count"] += 1
            contact["next_touch"] = (datetime.now() + timedelta(days=3)).isoformat()
            break
    
    return outreach


def update_contact_stage(contact_id: int, new_stage: str):
    """Update a contact's relationship stage."""
    for contact in st.session_state.network_contacts:
        if contact["id"] == contact_id:
            contact["stage"] = new_stage
            break


def get_due_followups() -> List[Dict]:
    """Get contacts that need follow-up."""
    due = []
    now = datetime.now()
    for contact in st.session_state.network_contacts:
        if contact.get("next_touch"):
            next_touch = datetime.fromisoformat(contact["next_touch"])
            if next_touch <= now:
                due.append(contact)
    return due


def get_analytics() -> Dict:
    """Calculate networking analytics."""
    contacts = st.session_state.network_contacts
    outreach = st.session_state.outreach_log
    
    if not contacts:
        return {
            "total_contacts": 0,
            "by_stage": {},
            "by_source": {},
            "response_rate": 0,
            "avg_touches": 0
        }
    
    # By stage
    by_stage = {}
    for contact in contacts:
        stage = contact["stage"]
        by_stage[stage] = by_stage.get(stage, 0) + 1
    
    # By source
    by_source = {}
    for contact in contacts:
        source = contact["source"]
        by_source[source] = by_source.get(source, 0) + 1
    
    # Response rate
    replied_count = len([o for o in outreach if o["status"] in ["💬 Replied", "📅 Meeting Booked"]])
    response_rate = (replied_count / len(outreach) * 100) if outreach else 0
    
    # Average touches
    avg_touches = sum(c["touch_count"] for c in contacts) / len(contacts) if contacts else 0
    
    return {
        "total_contacts": len(contacts),
        "by_stage": by_stage,
        "by_source": by_source,
        "total_outreach": len(outreach),
        "replied_count": replied_count,
        "response_rate": response_rate,
        "avg_touches": avg_touches,
        "meetings_booked": len([o for o in outreach if o["status"] == "📅 Meeting Booked"])
    }


# ═══════════════════════════════════════════════════════════════
# RENDER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def render_network_crm():
    """Main entry point for Networking CRM."""
    init_network_state()
    
    st.markdown("## 🌐 NETWORK CRM | Relationship Intelligence")
    st.caption("Track connections, log outreach, and convert relationships into opportunities")
    
    # Quick stats
    analytics = get_analytics()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Contacts", analytics["total_contacts"])
    col2.metric("Outreach Sent", analytics["total_outreach"])
    col3.metric("Response Rate", f"{analytics['response_rate']:.0f}%")
    col4.metric("Meetings Booked", analytics["meetings_booked"])
    
    st.markdown("---")
    
    # Navigation
    crm_mode = st.radio(
        "Mode",
        ["👤 People", "📬 Log Outreach", "✍️ Content Factory", "🔔 Follow-Ups", "📊 Analytics"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if crm_mode == "👤 People":
        render_people_mode()
    elif crm_mode == "📬 Log Outreach":
        render_outreach_mode()
    elif crm_mode == "✍️ Content Factory":
        render_content_factory()
    elif crm_mode == "🔔 Follow-Ups":
        render_followups_mode()
    elif crm_mode == "📊 Analytics":
        render_analytics_mode()


def generate_linkedin_post(name: str, role: str, company: str, topic: str, insight: str) -> str:
    """Generate a LinkedIn post from a conversation."""
    return f"""🚀 Just had a massive signal download with {name} ({role} at {company}).

We went deep on {topic}. The biggest takeaway?

💡 "{insight}"

Most people are still playing the old game. The real operators are shifting to {topic}.

Are you seeing this in your org? 👇

#GTM #RevenueArchitecture #BasinNexus"""


def generate_x_post(name: str, topic: str, insight: str) -> str:
    """Generate an X/Twitter post from a conversation."""
    return f"""Just spoke with {name} about {topic}.

The alpha: {insight}

Stop ignoring this. The market is shifting. 📉📈

#GTM #Sales #RevenueOps"""


def generate_next_step(name: str, company: str, topic: str, stage: str) -> dict:
    """Generate a strategic recommended next step based on relationship stage."""
    import random
    
    next_steps = {
        "❄️ COLD": [
            {"action": f"Send {name} a relevant article about {topic} to warm up the relationship", "type": "value_add"},
            {"action": f"Comment on {name}'s recent LinkedIn post before sending a DM", "type": "engagement"},
            {"action": f"Find a mutual connection who can provide a warm intro to {name}", "type": "intro"},
        ],
        "🌡️ WARM": [
            {"action": f"Share a specific case study showing {topic} impact at a similar company", "type": "value_add"},
            {"action": f"Ask {name} for their perspective on {topic} to deepen the conversation", "type": "engagement"},
            {"action": f"Offer to send a 2-minute Loom video with a personalized insight for {company}", "type": "value_add"},
        ],
        "🔥 HOT": [
            {"action": f"Propose a 15-minute call to discuss how {topic} applies to {company}", "type": "meeting"},
            {"action": f"Send a tailored one-pager on implementing {topic} at {company}", "type": "whitepaper"},
            {"action": f"Introduce {name} to someone in your network who solved this problem", "type": "intro"},
        ],
        "⭐ CHAMPION": [
            {"action": f"Ask {name} for a referral to another leader dealing with {topic}", "type": "referral"},
            {"action": f"Co-create content with {name} about your {topic} conversation", "type": "collab"},
            {"action": f"Invite {name} to an exclusive event or community discussion", "type": "community"},
        ]
    }
    
    options = next_steps.get(stage, next_steps["❄️ COLD"])
    selected = random.choice(options)
    
    return {
        "action": selected["action"],
        "type": selected["type"],
        "stage": stage
    }


def render_content_factory():
    """Content Factory - Turn conversations into gravity."""
    st.subheader("✍️ Content Factory")
    st.caption("Turn every conversation into LinkedIn/X content that creates gravity.")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0a0a1a, #1a1a2e); border: 1px solid #D4AF37; 
                border-radius: 8px; padding: 15px; margin-bottom: 20px;">
        <p style="color: #D4AF37; margin: 0; font-weight: bold;">THE FLYWHEEL</p>
        <p style="color: #888; margin: 5px 0 0 0; font-size: 0.85rem;">
            Conversation → Log → Content → Engagement → More Conversations → Repeat
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input form
    st.markdown("### 📝 Log Conversation & Generate Content")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Who did you talk to?", placeholder="John Smith")
        role = st.text_input("Their Role", placeholder="VP of Sales")
        company = st.text_input("Company", placeholder="Tebra")
        source = st.selectbox("Where?", ["LinkedIn", "X (Twitter)", "Zoom/Call", "IRL Event", "Slack"])
    
    with col2:
        topic = st.text_input("Topic discussed", placeholder="AI SDRs replacing humans")
        insight = st.text_area("Key Insight / Alpha", 
                              placeholder="Most companies are still cold calling when AI can pre-qualify leads...",
                              height=130)
    
    if st.button("🚀 Generate Content", type="primary"):
        if name and insight:
            # Store in session for display
            st.session_state['content_gen'] = {
                "name": name,
                "role": role,
                "company": company,
                "topic": topic,
                "insight": insight,
                "source": source
            }
            
            # Also add to contacts if new
            existing = [c for c in st.session_state.network_contacts if c['name'].lower() == name.lower()]
            if not existing:
                add_contact(name, company, role, f"💼 {source}")
                st.success(f"✅ Added {name} to your Network!")
            
            st.success("✅ Content generated!")
        else:
            st.error("Name and Insight are required")
    
    # Display generated content
    if st.session_state.get('content_gen'):
        data = st.session_state['content_gen']
        
        st.markdown("---")
        st.markdown("### 📱 Generated Content")
        
        col_li, col_x = st.columns(2)
        
        with col_li:
            st.markdown("##### 💼 LinkedIn Draft")
            li_post = generate_linkedin_post(
                data['name'], data['role'], data['company'], 
                data['topic'], data['insight']
            )
            st.code(li_post, language="text")
            if st.button("📋 Copy LinkedIn", key="copy_li"):
                st.info("Copy the text above!")
        
        with col_x:
            st.markdown("##### 🐦 X (Twitter) Draft")
            x_post = generate_x_post(data['name'], data['topic'], data['insight'])
            st.code(x_post, language="text")
            if st.button("📋 Copy X", key="copy_x"):
                st.info("Copy the text above!")
        
        # RECOMMENDED NEXT STEP
        st.markdown("---")
        
        # Get or generate next step
        if 'current_next_step' not in st.session_state or st.session_state.get('refresh_next_step'):
            # Determine stage (default to COLD if not set)
            stage = "❄️ COLD"
            existing = [c for c in st.session_state.network_contacts if c['name'].lower() == data['name'].lower()]
            if existing:
                stage = existing[0].get('stage', '❄️ COLD')
            
            next_step = generate_next_step(
                data['name'], 
                data['company'], 
                data['topic'], 
                stage
            )
            st.session_state.current_next_step = next_step
            st.session_state.refresh_next_step = False
        
        next_step = st.session_state.current_next_step
        
        # Display next step
        step_color = {
            "value_add": "#4ade80",
            "engagement": "#fbbf24", 
            "intro": "#60a5fa",
            "meeting": "#f87171",
            "whitepaper": "#a78bfa",
            "referral": "#D4AF37",
            "collab": "#ec4899",
            "community": "#14b8a6"
        }.get(next_step['type'], "#888")
        
        st.markdown(f"""
        <div style="background: #0f0f15; border: 1px solid {step_color}; border-radius: 8px; padding: 20px; margin: 10px 0;">
            <p style="color: {step_color}; margin: 0 0 10px 0; font-weight: bold;">🎯 Recommended Next Step</p>
            <p style="color: #f0e6d3; margin: 0; font-size: 1rem; line-height: 1.5;">
                {next_step['action']}
            </p>
            <p style="color: #666; margin: 10px 0 0 0; font-size: 0.75rem;">
                Type: {next_step['type'].upper()} | Stage: {next_step['stage']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("✅ Mark Complete", key="complete_step"):
                st.success("🎉 Great work! Step logged.")
                st.session_state.refresh_next_step = True
                st.rerun()
        with col_btn2:
            if st.button("🔄 Get Another", key="refresh_step"):
                st.session_state.refresh_next_step = True
                st.rerun()
    
    # Recent conversations for content
    st.markdown("---")
    st.markdown("### 📂 Recent Conversations → Content Ideas")
    
    contacts = st.session_state.network_contacts
    recent = [c for c in contacts if c.get('notes') and len(c['notes']) > 10][-5:]
    
    if recent:
        for contact in reversed(recent):
            with st.expander(f"💬 {contact['name']} - {contact['company']}"):
                st.markdown(f"**Notes:** {contact['notes']}")
                if st.button(f"✍️ Turn into Content", key=f"content_{contact['id']}"):
                    st.session_state['content_gen'] = {
                        "name": contact['name'],
                        "role": contact['title'],
                        "company": contact['company'],
                        "topic": "GTM Strategy",
                        "insight": contact['notes'][:200],
                        "source": contact['source']
                    }
                    st.rerun()
    else:
        st.info("Add contacts with notes to see content ideas here.")
    
    # Export for website
    st.markdown("---")
    st.markdown("### 📤 Export for basinleon.com")
    st.caption("Use this JSON on your website to show a 'Who I'm Talking To' ticker.")
    
    export_data = []
    for contact in st.session_state.network_contacts[-10:]:
        export_data.append({
            "name": contact['name'],
            "company": contact['company'],
            "stage": contact['stage'],
            "date": contact['created_at'][:10] if contact.get('created_at') else "2024-12-01"
        })
    
    if export_data:
        import json
        st.code(json.dumps(export_data, indent=2), language="json")
        st.caption("💡 Copy this to `data/network.json` on your website")


def render_people_mode():
    """Manage contacts."""
    st.subheader("👤 Your Network")
    
    # Add new contact
    with st.expander("➕ Add New Contact"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name*", placeholder="John Smith")
            company = st.text_input("Company*", placeholder="Tebra")
            title = st.text_input("Title", placeholder="VP of Sales")
        with col2:
            source = st.selectbox("Source*", SOURCES)
            linkedin = st.text_input("LinkedIn URL", placeholder="linkedin.com/in/...")
            twitter = st.text_input("X Handle", placeholder="@handle")
        
        email = st.text_input("Email", placeholder="john@company.com")
        notes = st.text_area("Notes", placeholder="Met at SaaStr conference...")
        
        if st.button("💾 Add Contact", type="primary"):
            if name and company:
                add_contact(name, company, title, source, linkedin, twitter, email, notes)
                st.success(f"✅ Added {name} to your network!")
                st.rerun()
            else:
                st.error("Name and Company are required")
    
    # Display contacts
    contacts = st.session_state.network_contacts
    
    if not contacts:
        st.info("No contacts yet. Add your first connection above!")
        return
    
    # Filter
    filter_stage = st.selectbox("Filter by Stage", ["All"] + list(RELATIONSHIP_STAGES.keys()))
    
    for contact in reversed(contacts):
        if filter_stage != "All" and contact["stage"] != filter_stage:
            continue
        
        stage_info = RELATIONSHIP_STAGES.get(contact["stage"], {})
        stage_color = stage_info.get("color", "#888")
        
        st.markdown(f"""
        <div style="background: #0f0f15; border: 1px solid {stage_color}; border-radius: 8px; 
                    padding: 15px; margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="color: {stage_color}; font-weight: bold;">{contact['name']}</span>
                    <span style="color: #888;"> — {contact['company']}</span>
                    <span style="color: #666; font-size: 0.8rem;"> ({contact['title']})</span>
                </div>
                <span style="background: {stage_color}22; color: {stage_color}; padding: 4px 10px; 
                             border-radius: 4px; font-size: 0.75rem;">
                    {contact['stage']}
                </span>
            </div>
            <div style="margin-top: 8px; color: #666; font-size: 0.75rem;">
                Source: {contact['source']} | Touches: {contact['touch_count']} | 
                Last: {contact['last_touch'][:10] if contact['last_touch'] else 'Never'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Actions
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            new_stage = st.selectbox(
                "Stage",
                list(RELATIONSHIP_STAGES.keys()),
                index=list(RELATIONSHIP_STAGES.keys()).index(contact["stage"]),
                key=f"stage_{contact['id']}"
            )
            if new_stage != contact["stage"]:
                update_contact_stage(contact["id"], new_stage)
                st.rerun()
        with col2:
            if st.button("📬 Log Touch", key=f"touch_{contact['id']}"):
                st.session_state[f"logging_for_{contact['id']}"] = True
                st.rerun()


def render_outreach_mode():
    """Log outreach activities."""
    st.subheader("📬 Log Outreach")
    
    contacts = st.session_state.network_contacts
    
    if not contacts:
        st.info("Add contacts first before logging outreach!")
        return
    
    contact_options = {f"{c['name']} ({c['company']})": c["id"] for c in contacts}
    
    selected = st.selectbox("Select Contact", list(contact_options.keys()))
    contact_id = contact_options[selected]
    
    outreach_type = st.selectbox("Outreach Type", OUTREACH_TYPES)
    content = st.text_area("Content/Message", placeholder="Hey John, saw your post about...")
    status = st.selectbox("Status", RESPONSE_STATUS)
    
    if st.button("📤 Log This Outreach", type="primary"):
        if content:
            add_outreach(contact_id, outreach_type, content, status)
            st.success("✅ Outreach logged!")
            
            # Auto-update stage based on status
            if status in ["💬 Replied", "📅 Meeting Booked"]:
                update_contact_stage(contact_id, "🔥 HOT")
            st.rerun()
        else:
            st.error("Add content/message")
    
    # Recent outreach
    st.markdown("---")
    st.markdown("### 📋 Recent Outreach")
    
    for outreach in reversed(st.session_state.outreach_log[-10:]):
        contact = next((c for c in contacts if c["id"] == outreach["contact_id"]), None)
        if contact:
            st.markdown(f"""
            **{contact['name']}** ({contact['company']}) — {outreach['type']}
            
            {outreach['content'][:100]}...
            
            *Status: {outreach['status']} | {outreach['sent_at'][:10]}*
            """)
            st.markdown("---")


def render_followups_mode():
    """Show due follow-ups."""
    st.subheader("🔔 Follow-Up Triggers")
    
    due = get_due_followups()
    
    if not due:
        st.success("🎉 You're all caught up! No follow-ups due.")
    else:
        st.warning(f"⚠️ {len(due)} contacts need attention!")
        
        for contact in due:
            stage_info = RELATIONSHIP_STAGES.get(contact["stage"], {})
            stage_color = stage_info.get("color", "#888")
            
            days_overdue = (datetime.now() - datetime.fromisoformat(contact["next_touch"])).days
            
            st.markdown(f"""
            <div style="background: #1a0a0a; border: 1px solid #f87171; border-radius: 8px; 
                        padding: 15px; margin: 10px 0;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #f0e6d3; font-weight: bold;">{contact['name']}</span>
                    <span style="color: #f87171; font-size: 0.8rem;">
                        ⏰ {days_overdue} days overdue
                    </span>
                </div>
                <p style="color: #888; margin: 5px 0 0 0; font-size: 0.85rem;">
                    {contact['company']} | {stage_info.get('next_action', 'Follow up')}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"📬 Log Touch for {contact['name']}", key=f"followup_{contact['id']}"):
                st.session_state[f"logging_for_{contact['id']}"] = True
                st.rerun()
    
    # Upcoming
    st.markdown("---")
    st.markdown("### 📅 Upcoming (Next 7 Days)")
    
    upcoming = []
    now = datetime.now()
    for contact in st.session_state.network_contacts:
        if contact.get("next_touch"):
            next_touch = datetime.fromisoformat(contact["next_touch"])
            if now < next_touch <= now + timedelta(days=7):
                upcoming.append((contact, next_touch))
    
    if not upcoming:
        st.info("No upcoming follow-ups in the next 7 days.")
    else:
        for contact, due_date in sorted(upcoming, key=lambda x: x[1]):
            days_until = (due_date - now).days
            st.markdown(f"• **{contact['name']}** ({contact['company']}) — in {days_until} days")


def render_analytics_mode():
    """Show networking analytics."""
    st.subheader("📊 Network Analytics")
    
    analytics = get_analytics()
    
    if analytics["total_contacts"] == 0:
        st.info("Add contacts and log outreach to see analytics!")
        return
    
    # Funnel visualization
    st.markdown("### 🔱 Relationship Funnel")
    
    for stage, info in RELATIONSHIP_STAGES.items():
        count = analytics["by_stage"].get(stage, 0)
        pct = (count / analytics["total_contacts"] * 100) if analytics["total_contacts"] else 0
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 8px 0;">
            <span style="width: 120px; color: {info['color']}; font-weight: bold;">{stage}</span>
            <div style="flex: 1; background: #1a1a2e; border-radius: 4px; height: 24px; overflow: hidden;">
                <div style="width: {pct}%; background: {info['color']}; height: 100%;"></div>
            </div>
            <span style="width: 60px; text-align: right; color: #888; margin-left: 10px;">{count}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # By source
    st.markdown("### 📡 By Source")
    
    for source, count in sorted(analytics["by_source"].items(), key=lambda x: -x[1]):
        pct = count / analytics["total_contacts"] * 100
        st.markdown(f"**{source}**: {count} ({pct:.0f}%)")
    
    st.markdown("---")
    
    # Key metrics
    st.markdown("### 📈 Key Metrics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background: #0f0f15; border: 1px solid #D4AF37; border-radius: 8px; padding: 20px; text-align: center;">
            <p style="color: #888; margin: 0;">Response Rate</p>
            <h2 style="color: {'#4ade80' if analytics['response_rate'] > 30 else '#fbbf24'}; margin: 10px 0;">
                {analytics['response_rate']:.1f}%
            </h2>
            <p style="color: #666; font-size: 0.75rem;">{analytics['replied_count']}/{analytics['total_outreach']} replied</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #0f0f15; border: 1px solid #D4AF37; border-radius: 8px; padding: 20px; text-align: center;">
            <p style="color: #888; margin: 0;">Avg Touches per Contact</p>
            <h2 style="color: #D4AF37; margin: 10px 0;">{analytics['avg_touches']:.1f}</h2>
            <p style="color: #666; font-size: 0.75rem;">Across {analytics['total_contacts']} contacts</p>
        </div>
        """, unsafe_allow_html=True)
