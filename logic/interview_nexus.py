"""
INTERVIEW::NEXUS v3.0 - THE ULTIMATE INTERVIEW DOMINATION SYSTEM
═══════════════════════════════════════════════════════════════════════════════
Part of Basin::Nexus v0.5 Executive OS

CORE FEATURES:
✅ Resume + JD Paste Input (The Foundation)
✅ 11 Interviewer Layers (Recruiter → CEO)
✅ Live Coaching Analytics (Gong-style feedback)
✅ Signal Bridge (Connect outreach tools)
✅ Pipeline CRM Integration
✅ STAR Story Bank
✅ Bio-State Optimization
✅ Adversarial Mode

THE 11-LAYER INTERVIEW GAUNTLET:
1. Recruiter Screen
2. HR/People Ops
3. Hiring Manager
4. Skip-Level (Manager's Manager)
5. Peer Interview (Lateral)
6. Technical/Systems
7. Cross-Functional (Sales/CS/Product)
8. VP/CRO
9. Founder/CEO
10. Team Simulation (Panel)
11. Board/Investor

Protocol: Build → Use → Win → Prove
"""

import streamlit as st
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# ═══════════════════════════════════════════════════════════════
# DATABASE INTEGRATION
# ═══════════════════════════════════════════════════════════════
try:
    from logic.database import (
        get_all_deals, 
        get_all_contacts, 
        get_interview_stages,
        get_upcoming_events,
        save_voice_session,
        get_voice_analytics
    )
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

try:
    from logic.generator import generate_plain_text
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════
# THE 11-LAYER INTERVIEW GAUNTLET
# ═══════════════════════════════════════════════════════════════

INTERVIEW_LAYERS = {
    "1️⃣ Recruiter Screen": {
        "name": "Taylor (Talent Acquisition)",
        "title": "Recruiter",
        "difficulty": "Easy",
        "focus": ["Clarity", "Brevity", "Red flags", "Salary expectations", "Culture fit basics"],
        "behavior": """You are Taylor, a busy Talent Acquisition lead with 15 minutes and 12 other calls today.
You are NOT impressed by jargon. You want clear, short answers.
If they ramble, cut them off: "I need you to summarize that in one sentence."
You're scanning for: job hopping, gaps, inflated titles, salary misalignment.""",
        "example_questions": [
            "Walk me through your resume in 60 seconds.",
            "Why are you leaving your current role?",
            "What are your salary expectations?",
            "Why this company?"
        ]
    },
    
    "2️⃣ HR/People Ops": {
        "name": "Jordan (HR Business Partner)",
        "title": "HR Business Partner",
        "difficulty": "Easy",
        "focus": ["Culture fit", "Values alignment", "EEOC compliance", "Behavioral basics"],
        "behavior": """You are Jordan, an HR Business Partner who cares about culture and values.
You're assessing if this person will be a culture add or culture drain.
You probe for conflicts, teamwork, and how they handle adversity.
You ask soft questions but listen for red flags.""",
        "example_questions": [
            "Tell me about a time you received difficult feedback.",
            "How do you handle conflict with a colleague?",
            "What does diversity and inclusion mean to you?",
            "Describe your ideal manager."
        ]
    },
    
    "3️⃣ Hiring Manager": {
        "name": "Alex (Direct Manager)",
        "title": "Hiring Manager",
        "difficulty": "Medium",
        "focus": ["Competence", "Day-to-day execution", "Specific skills", "Team dynamics"],
        "behavior": """You are Alex, the direct hiring manager. You've been burned by bad hires.
You want to know: Can this person actually DO the job on day 1?
You attack vague answers. "Managed" means nothing - what did they actually OWN?
You care about execution details, not strategy decks.""",
        "example_questions": [
            "Walk me through a typical day in your last role.",
            "How do you prioritize when everything is urgent?",
            "Give me a specific example of how you built [X].",
            "What tools and systems do you use?"
        ]
    },
    
    "4️⃣ Skip-Level": {
        "name": "Morgan (VP, Manager's Manager)",
        "title": "VP/Skip-Level",
        "difficulty": "Hard",
        "focus": ["Strategic thinking", "Leadership potential", "Scalability", "Vision"],
        "behavior": """You are Morgan, the VP (skip-level). You're thinking 2-3 years out.
You don't care about today's tasks - you care about tomorrow's impact.
Can this person grow? Can they eventually replace their manager?
You probe for strategic thinking and leadership DNA.""",
        "example_questions": [
            "Where do you see this function in 3 years?",
            "How would you rebuild this team from scratch?",
            "What's the biggest bet you'd make if you were me?",
            "Tell me about a time you led without authority."
        ]
    },
    
    "5️⃣ Peer Interview": {
        "name": "Casey (Lateral Colleague)",
        "title": "Peer/Lateral",
        "difficulty": "Medium",
        "focus": ["Collaboration", "Communication style", "Team dynamics", "Ego check"],
        "behavior": """You are Casey, who would be this person's peer.
You care about: Will this person make my life easier or harder?
Are they a collaborator or a credit-taker? 
You ask subtle questions to gauge ego and teamwork.""",
        "example_questions": [
            "How do you work with cross-functional teams?",
            "Tell me about a project that failed. What was your role?",
            "How do you handle it when a colleague drops the ball?",
            "What would your last team say about working with you?"
        ]
    },
    
    "6️⃣ Technical/Systems": {
        "name": "Riley (RevOps/Systems)",
        "title": "Technical Specialist",
        "difficulty": "Hard",
        "focus": ["Technical depth", "Systems thinking", "Data/analytics", "Tool proficiency"],
        "behavior": """You are Riley, the technical evaluator (RevOps, Systems, or Engineering).
You smell BS from a mile away. "I built a system" means nothing without specifics.
What was the data model? What were the integrations? 
You want to know if they understand the plumbing or just the PowerPoint.""",
        "example_questions": [
            "Walk me through the architecture of a system you built.",
            "How do you ensure data quality across systems?",
            "What's your relationship with RevOps/Engineering?",
            "Describe a technical decision you regret."
        ]
    },
    
    "7️⃣ Cross-Functional": {
        "name": "Drew (Sales/CS/Product)",
        "title": "Cross-Functional Partner",
        "difficulty": "Medium",
        "focus": ["Stakeholder management", "Influence without authority", "Business acumen"],
        "behavior": """You are Drew from a different function (Sales, CS, or Product).
You care about: Will this person understand MY priorities?
You test for empathy, business acumen, and the ability to influence without authority.
You want a partner, not a silo-builder.""",
        "example_questions": [
            "How do you balance partner needs vs. direct sales needs?",
            "Tell me about a time you had to influence a decision you didn't own.",
            "How do you handle competing priorities from different stakeholders?",
            "What do you think my biggest pain point is?"
        ]
    },
    
    "8️⃣ VP/CRO": {
        "name": "Marcus (CRO)",
        "title": "VP/CRO",
        "difficulty": "Nightmare",
        "focus": ["Revenue impact", "Numbers", "ROI", "Strategic value"],
        "behavior": """You are Marcus, CRO with $50M on the line.
You are NOT here to make friends. You are protecting your number.
You've fired people who "had great strategies" but couldn't hit quota.
You speak in short sentences. You interrupt rambling. You want PROOF.""",
        "example_questions": [
            "What's your impact on revenue? Give me a number.",
            "Why should I bet my quota on you?",
            "Tell me about a time you missed a number. What happened?",
            "How do you forecast? Walk me through your model."
        ]
    },
    
    "9️⃣ Founder/CEO": {
        "name": "Sam (Founder/CEO)",
        "title": "Founder/CEO",
        "difficulty": "Nightmare",
        "focus": ["Vision", "Ownership", "Hustle", "Cultural DNA"],
        "behavior": """You are Sam, the Founder/CEO. You built this company from nothing.
You care about missionaries, not mercenaries.
You want to know: Does this person CARE? Will they bleed for the mission?
You probe for ownership, hustle, and authentic passion.""",
        "example_questions": [
            "Why this company? Why now?",
            "What would you do in the first 30 days if no one told you what to do?",
            "Tell me about something you built from nothing.",
            "What do you think we're getting wrong?"
        ]
    },
    
    "🔟 Team Panel": {
        "name": "Team (Multiple Interviewers)",
        "title": "Panel Interview",
        "difficulty": "Hard",
        "focus": ["Consistency", "Pressure handling", "Multi-stakeholder communication"],
        "behavior": """This is a PANEL interview with multiple people in the room.
One person asks about execution. Another asks about culture. A third tests technical depth.
You must stay consistent across different question types.
The pressure is high. They're watching for cracks.""",
        "example_questions": [
            "[Manager]: Walk me through your biggest accomplishment.",
            "[Peer]: How would you handle a conflict with me?",
            "[Technical]: What's your approach to data and systems?",
            "[VP]: Why should we hire you over the other candidates?"
        ]
    },
    
    "1️⃣1️⃣ Board/Investor": {
        "name": "Sarah (Board Member/Investor)",
        "title": "Board/Investor",
        "difficulty": "Nightmare",
        "focus": ["Unit economics", "Scalability", "Pattern matching", "Fund thesis alignment"],
        "behavior": """You are Sarah, a Board Member or VC Partner.
You've seen 1,000 candidates. You pattern-match against the best.
You care about CAC, LTV, scalability, and whether this person thinks like an owner.
You ask calm questions with surgical precision.""",
        "example_questions": [
            "What were the unit economics of your partnerships?",
            "How does your experience translate to our scale?",
            "What's the biggest strategic risk in this hire?",
            "If you were on this board, what would you ask me?"
        ]
    }
}


# ═══════════════════════════════════════════════════════════════
# LIVE COACHING ANALYTICS (GONG-STYLE)
# ═══════════════════════════════════════════════════════════════

def analyze_response_live(response: str) -> Dict:
    """
    Real-time analysis of interview response with Gong-style metrics.
    Returns detailed coaching feedback.
    """
    word_count = len(response.split())
    
    # Time estimation (assuming 150 WPM speaking pace)
    estimated_time_seconds = (word_count / 150) * 60
    
    # Filler word detection
    fillers = ['um', 'uh', 'like', 'you know', 'sort of', 'kind of', 'basically', 'actually', 'literally', 'honestly']
    filler_count = sum(response.lower().count(f) for f in fillers)
    filler_density = (filler_count / word_count) * 100 if word_count > 0 else 0
    
    # First person ownership
    i_statements = response.lower().count(' i ') + response.lower().count("i ") + response.lower().count(' my ')
    we_statements = response.lower().count(' we ') + response.lower().count(' our ')
    ownership_ratio = i_statements / max(we_statements, 1)
    
    # Metric density
    has_numbers = any(c.isdigit() for c in response)
    has_percent = '%' in response
    has_dollar = '$' in response
    metric_count = sum([has_numbers, has_percent, has_dollar])
    
    # Power verbs
    power_verbs = ['led', 'drove', 'built', 'created', 'launched', 'designed', 'architected', 
                   'scaled', 'grew', 'closed', 'negotiated', 'implemented', 'reduced', 'increased']
    power_verb_count = sum(1 for v in power_verbs if v in response.lower())
    
    # Weak language detection (hedging)
    weak_phrases = ['tried to', 'helped with', 'was involved', 'participated in', 'assisted', 
                    'was part of', 'contributed to', 'supported']
    weak_count = sum(1 for w in weak_phrases if w in response.lower())
    
    # CONVICTION SCORE (strong vs hedging language)
    hedging_words = ['maybe', 'perhaps', 'sort of', 'kind of', 'i think', 'i believe', 
                     'probably', 'possibly', 'might', 'somewhat', 'fairly', 'quite']
    hedging_count = sum(1 for h in hedging_words if h in response.lower())
    
    assertive_words = ['definitely', 'absolutely', 'clearly', 'specifically', 'precisely',
                       'exactly', 'directly', 'measurably', 'quantifiably', 'demonstrated']
    assertive_count = sum(1 for a in assertive_words if a in response.lower())
    
    conviction_score = max(0, min(100, 60 + (assertive_count * 10) - (hedging_count * 15) - (weak_count * 10)))
    
    # SPECIFICITY SCORE (names, dates, tools, numbers)
    import re
    has_specific_numbers = len(re.findall(r'\d+', response)) > 0
    has_company_names = any(name in response for name in ['Google', 'Microsoft', 'AWS', 'Salesforce', 'Adobe', 'Sense', 'Fudo'])
    has_tools = any(tool.lower() in response.lower() for tool in ['CRM', 'Salesforce', 'HubSpot', 'Outreach', 'Gong', 'Slack', 'Jira', 'Notion'])
    has_timeframes = any(tf in response.lower() for tf in ['q1', 'q2', 'q3', 'q4', 'quarter', 'month', 'week', 'year', '2024', '2023', '2022'])
    
    specificity_components = [has_specific_numbers, has_company_names, has_tools, has_timeframes, has_percent, has_dollar]
    specificity_score = sum(specificity_components) / len(specificity_components) * 100
    
    # STAR structure detection
    has_situation = any(kw in response.lower() for kw in ['situation', 'context', 'when', 'at the time', 'background'])
    has_task = any(kw in response.lower() for kw in ['challenge', 'goal', 'objective', 'problem', 'needed to', 'responsible for'])
    has_action = i_statements >= 2
    has_result = any(kw in response.lower() for kw in ['result', 'outcome', 'impact', 'achieved', 'led to'])
    star_score = sum([has_situation, has_task, has_action, has_result]) * 25
    
    # Overall score (enhanced)
    base_score = 50
    base_score += min(power_verb_count * 5, 20)  # Up to +20 for power verbs
    base_score += min(metric_count * 10, 20)  # Up to +20 for metrics
    base_score += 15 if ownership_ratio >= 2 else 5 if ownership_ratio >= 1 else 0
    base_score += int(specificity_score / 10)  # Up to +10 for specificity
    base_score -= filler_count * 3  # Penalty for fillers
    base_score -= weak_count * 5  # Penalty for weak language
    base_score -= hedging_count * 3  # Penalty for hedging
    
    # Time penalty (too short or too long)
    if word_count < 50:
        base_score -= 15
    elif word_count > 400:
        base_score -= 10
    
    return {
        "overall_score": min(max(base_score, 0), 100),
        "star_score": star_score,
        "word_count": word_count,
        "estimated_time": f"{int(estimated_time_seconds)}s",
        "filler_count": filler_count,
        "filler_density": f"{filler_density:.1f}%",
        "ownership_ratio": f"{ownership_ratio:.1f}:1",
        "metric_density": "High" if metric_count >= 2 else "Medium" if metric_count == 1 else "Low",
        "power_verbs": power_verb_count,
        "weak_language": weak_count,
        "conviction_score": conviction_score,
        "conviction_label": "💪 STRONG" if conviction_score >= 70 else "😐 OK" if conviction_score >= 50 else "⚠️ HEDGING",
        "specificity_score": int(specificity_score),
        "specificity_label": "🎯 SPECIFIC" if specificity_score >= 60 else "📝 GENERAL" if specificity_score >= 30 else "❌ VAGUE",
        "hedging_count": hedging_count,
        "has_situation": "✅" if has_situation else "❌",
        "has_task": "✅" if has_task else "❌",
        "has_action": "✅" if has_action else "❌",
        "has_result": "✅" if has_result else "❌",
        "coaching": []
    }


def generate_coaching_tips(analysis: Dict) -> List[str]:
    """Generate specific coaching tips based on analysis."""
    tips = []
    
    if analysis['word_count'] < 50:
        tips.append("⚠️ Too brief! Expand with context and specific examples. Aim for 100-200 words.")
    if analysis['word_count'] > 400:
        tips.append("⚠️ Too long! Be more concise. Cut the fluff and get to the result faster.")
    
    if analysis['filler_count'] > 2:
        tips.append(f"🎤 {analysis['filler_count']} filler words detected. Replace 'um/like' with pauses.")
    
    if analysis['ownership_ratio'] == "0.0:1" or float(analysis['ownership_ratio'].split(':')[0]) < 1:
        tips.append("👤 More 'I' statements needed! You're hiding behind 'we'. Take credit for YOUR work.")
    
    if analysis['metric_density'] == "Low":
        tips.append("📊 Add numbers! Quantify your impact with %, $, or specific metrics.")
    
    if analysis['power_verbs'] < 2:
        tips.append("💪 Use stronger verbs: 'led', 'drove', 'built', 'scaled' instead of 'helped' or 'worked on'.")
    
    if analysis['weak_language'] > 0:
        tips.append("🚫 Remove weak language: 'tried to', 'helped with', 'was involved'. Be direct.")
    
    if analysis['has_situation'] == "❌":
        tips.append("📍 [S] Add situation context: When? Where? What was the background?")
    if analysis['has_task'] == "❌":
        tips.append("🎯 [T] Clarify the task: What was the challenge or goal?")
    if analysis['has_action'] == "❌":
        tips.append("⚡ [A] More action detail: What did YOU specifically do?")
    if analysis['has_result'] == "❌":
        tips.append("🏆 [R] Add result: What was the outcome? Quantify the impact!")
    
    return tips if tips else ["✅ Strong answer! Consider adding more specific metrics."]


# ═══════════════════════════════════════════════════════════════
# STAR STORY BANK
# ═══════════════════════════════════════════════════════════════

def get_default_stories() -> List[Dict]:
    """Pre-loaded STAR stories from Leon Basin's resume."""
    return [
        {
            "title": "Fudo GTM Turnaround (160% Pipeline Growth)",
            "competency": "GTM Strategy & Execution",
            "situation": "Series B Cyber vendor. US pipeline was stagnant. Partner channel dormant.",
            "task": "Revive Americas GTM and build predictable pipeline without adding headcount.",
            "action": "Restructured outbound motion. Built 'Technical-to-Commercial' enablement for partners. Shifted narrative from features to business risk. Personal outreach to 50+ strategic partners.",
            "result": "160% YoY increase in pipeline coverage. Reactivated LATAM channel. 12+ strategic partnerships signed. $2M+ influenced pipeline.",
            "tags": ["GTM", "Partnerships", "Revenue Growth", "Startup"]
        },
        {
            "title": "Sense Ecosystem Architecture ($10M Pipeline)",
            "competency": "Systems Thinking & Alliance Building",
            "situation": "High-growth AI startup. Had product-market fit but no repeatable mechanism to reach enterprise buyers at scale.",
            "task": "Design alliance strategy to punch above weight class. Build partner ecosystem from scratch.",
            "action": "Mapped ecosystem landscape. Built co-sell playbooks with Microsoft, AWS, ServiceNow. Trained 200+ partner SEs. Created mutual success metrics with joint QBRs.",
            "result": "$10M influenced pipeline. 40% of enterprise deals partner-sourced. Generated $300k in expansion revenue. Promoted to Principal Alliance Manager.",
            "tags": ["Alliances", "Enterprise", "Scale", "Microsoft", "AWS"]
        },
        {
            "title": "Churn Reduction (18% → 6%)",
            "competency": "Operational Excellence",
            "situation": "High churn rate of 18% was bleeding revenue. BDR team hitting activity metrics but retention was poor.",
            "task": "Reduce churn without adding headcount. Fix the leaky bucket.",
            "action": "Built automated renewal playbook. Implemented health scoring system. Created executive review cadence. Unified CS/Sales on single CRM dashboard.",
            "result": "Reduced churn from 18% to 6% (12-point improvement). Achieved 94% gross retention. Saved estimated $1.2M ARR.",
            "tags": ["Operations", "Customer Success", "Data", "Automation"]
        },
        {
            "title": "Partner vs. Sales Territory Conflict",
            "competency": "Leadership & Conflict Resolution",
            "situation": "Sales team viewing partners as 'deal registration thieves.' Partners feeling undervalued and going dormant.",
            "task": "Rebuild trust between direct sales and partner org without forcing structural change.",
            "action": "Ran 'Rules of Engagement' workshops. Created transparent comp structure where both could win. Celebrated joint wins publicly. Met 1:1 with every sales leader.",
            "result": "Partner conflict tickets dropped 80%. Joint deal velocity increased 3x. NPS from sales team improved to +60.",
            "tags": ["Leadership", "Conflict", "Culture", "EQ"]
        }
    ]


# ═══════════════════════════════════════════════════════════════
# BIO-STATE OPTIMIZATION
# ═══════════════════════════════════════════════════════════════

BIO_PROTOCOLS = {
    "🔥 The Primer (Anxious)": {
        "technique": "4-7-8 Breathing",
        "instructions": "Inhale 4s, Hold 7s, Exhale 8s. Repeat 4x.",
        "purpose": "Activates parasympathetic nervous system",
        "timing": "5 minutes before interview"
    },
    "🧊 The Cold State (Low Energy)": {
        "technique": "Mammalian Dive Reflex",
        "instructions": "Splash cold water on face for 30 seconds",
        "purpose": "Increases alertness and focus",
        "timing": "10 minutes before interview"
    },
    "💊 The Stack (Brain Fog)": {
        "technique": "L-Theanine + Caffeine",
        "instructions": "200mg L-Theanine + 100mg Caffeine",
        "purpose": "Smooth focus without jitters",
        "timing": "60-90 minutes before"
    },
    "🧘 Power Pose": {
        "technique": "Superman Stance",
        "instructions": "Stand tall, chest open, 2 minutes",
        "purpose": "Increases testosterone, reduces cortisol",
        "timing": "Immediately before joining call"
    }
}


# ═══════════════════════════════════════════════════════════════
# MAIN RENDER FUNCTION
# ═══════════════════════════════════════════════════════════════

def render_interview_nexus():
    """Main entry point for Interview::Nexus v3.0"""
    
    # Header
    st.markdown("## 🥋 INTERVIEW::NEXUS v3.0 | The Ultimate Training System")
    st.caption("11-Layer Interview Gauntlet • Live Coaching • Resume + JD Input • Signal Bridge")
    
    # Show integration status
    if DATABASE_AVAILABLE:
        deals = get_all_deals()
        contacts = get_all_contacts()
    else:
        deals = []
        contacts = []
    
    # Initialize session state
    if 'story_bank' not in st.session_state:
        st.session_state.story_bank = get_default_stories()
    if 'interview_log' not in st.session_state:
        st.session_state.interview_log = []
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = ""
    if 'jd_text' not in st.session_state:
        st.session_state.jd_text = ""
    if 'signal_bridge_content' not in st.session_state:
        st.session_state.signal_bridge_content = ""
    
    st.markdown("---")
    
    # Navigation
    nexus_mode = st.radio(
        "Select Mode",
        ["📄 Resume + JD Setup", "🎯 11-Layer Gauntlet", "📝 Story Bank", "🧬 Bio-Optimization", "📊 Performance"],
        horizontal=True,
        key="nexus_mode_v3"
    )
    
    st.markdown("---")
    
    # Route to mode
    if nexus_mode == "📄 Resume + JD Setup":
        render_setup_mode()
    elif nexus_mode == "🎯 11-Layer Gauntlet":
        render_gauntlet_mode(deals, contacts)
    elif nexus_mode == "📝 Story Bank":
        render_story_bank_mode()
    elif nexus_mode == "🧬 Bio-Optimization":
        render_bio_mode()
    elif nexus_mode == "📊 Performance":
        render_performance_mode()


def render_setup_mode():
    """Resume + JD Setup with Signal Bridge"""
    
    st.subheader("📄 Interview Context Setup")
    st.caption("Paste your resume and the job description. This context powers all simulations.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Your Resume/Experience")
        resume_input = st.text_area(
            "Paste your resume or key experience",
            value=st.session_state.get('resume_text', ''),
            height=300,
            placeholder="Paste your resume here or key bullet points from your experience..."
        )
        if resume_input != st.session_state.get('resume_text', ''):
            st.session_state.resume_text = resume_input
            st.success("✅ Resume saved!")
    
    with col2:
        st.markdown("### 📑 Target Job Description")
        jd_input = st.text_area(
            "Paste the job description",
            value=st.session_state.get('jd_text', ''),
            height=300,
            placeholder="Paste the job description here..."
        )
        if jd_input != st.session_state.get('jd_text', ''):
            st.session_state.jd_text = jd_input
            st.success("✅ JD saved!")
    
    st.markdown("---")
    
    # Signal Bridge
    st.markdown("### 🔗 Signal Bridge (Connect Outreach Tools)")
    st.caption("Paste your best-performing outreach copy to train the AI on your voice.")
    
    with st.expander("🔗 Add Outreach Signal", expanded=False):
        signal_input = st.text_area(
            "Paste high-performing email/LinkedIn message",
            value=st.session_state.get('signal_bridge_content', ''),
            height=150,
            placeholder="Paste a successful cold email or LinkedIn message that got replies..."
        )
        if signal_input != st.session_state.get('signal_bridge_content', ''):
            st.session_state.signal_bridge_content = signal_input
            st.success("✅ Signal ingested! AI will reference your writing style.")
    
    # Quick company setup
    st.markdown("---")
    st.markdown("### 🎯 Target Company")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        company = st.text_input("Company Name", value=st.session_state.get('target_company', 'Adobe'))
        st.session_state.target_company = company
    with col_c2:
        role = st.text_input("Role", value=st.session_state.get('target_role', 'Director of GTM Strategy'))
        st.session_state.target_role = role
    
    # Status
    st.markdown("---")
    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.metric("Resume", "✅ Set" if st.session_state.get('resume_text') else "❌ Missing")
    col_s2.metric("JD", "✅ Set" if st.session_state.get('jd_text') else "❌ Missing")
    col_s3.metric("Signal Bridge", "✅ Connected" if st.session_state.get('signal_bridge_content') else "Optional")
    
    if st.button("🚀 GO TO GAUNTLET", type="primary", use_container_width=True):
        if st.session_state.get('resume_text') and st.session_state.get('jd_text'):
            st.session_state.nexus_mode_v3 = "🎯 11-Layer Gauntlet"
            st.rerun()
        else:
            st.error("Please paste both Resume and JD first!")


def render_gauntlet_mode(deals: List[Dict], contacts: List[Dict]):
    """The 11-Layer Interview Gauntlet with Live Coaching"""
    
    st.subheader("🎯 11-Layer Interview Gauntlet")
    
    # Check if setup is done
    if not st.session_state.get('resume_text') or not st.session_state.get('jd_text'):
        st.warning("⚠️ Go to 'Resume + JD Setup' first to paste your context!")
        return
    
    st.caption(f"Target: {st.session_state.get('target_company', 'Unknown')} | {st.session_state.get('target_role', 'Unknown')}")
    
    # Layer selector
    selected_layer = st.selectbox(
        "Select Interview Layer",
        list(INTERVIEW_LAYERS.keys()),
        key="gauntlet_layer"
    )
    
    layer = INTERVIEW_LAYERS[selected_layer]
    
    # Layer info
    col_info1, col_info2 = st.columns([2, 1])
    with col_info1:
        st.markdown(f"### {layer['name']}")
        st.caption(f"**Title:** {layer['title']} | **Difficulty:** {layer['difficulty']}")
        st.markdown(f"**Focus Areas:** {', '.join(layer['focus'])}")
    
    with col_info2:
        difficulty_color = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴", "Nightmare": "💀"}
        st.markdown(f"### {difficulty_color.get(layer['difficulty'], '⚪')} {layer['difficulty']}")
    
    st.markdown("---")
    
    # Start simulation
    if st.button("⚔️ START INTERVIEW", type="primary", use_container_width=True):
        if LLM_AVAILABLE:
            with st.spinner(f"Summoning {layer['name']}..."):
                # Build prompt with full context
                prompt = f"""
{layer['behavior']}

INTERVIEW CONTEXT:
Company: {st.session_state.get('target_company', 'Unknown Company')}
Role: {st.session_state.get('target_role', 'Unknown Role')}

CANDIDATE BACKGROUND:
{st.session_state.get('resume_text', '')[:2000]}

JOB REQUIREMENTS:
{st.session_state.get('jd_text', '')[:1500]}

{"CANDIDATE WRITING STYLE (from outreach): " + st.session_state.get('signal_bridge_content', '')[:500] if st.session_state.get('signal_bridge_content') else ""}

TASK: Generate ONE challenging interview question that:
1. Is specific to this candidate's background and the role
2. Tests for the gaps between their experience and our requirements
3. Stays in character as {layer['title']}
4. Forces them to be specific, not generic

Do NOT be polite. Go straight to the question.
"""
                
                model_id = st.session_state.get('selected_model_id', 'llama-3.3-70b-versatile')
                question = generate_plain_text(prompt, model_name=model_id)
                
                st.session_state['current_gauntlet_q'] = question
                st.session_state['gauntlet_active'] = True
                st.session_state['current_layer'] = selected_layer
        else:
            st.error("LLM not available. Check API key.")
    
    # Show active simulation
    if st.session_state.get('gauntlet_active'):
        # Question display
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a2e, #0f0f23); border-left: 4px solid #D4AF37; 
                    padding: 20px; margin: 15px 0; border-radius: 8px;">
            <p style="color: #D4AF37; margin: 0 0 10px 0; font-size: 0.85rem;">
                {layer['name']} ({layer['title']})
            </p>
            <p style="color: #ffffff; font-size: 1.1rem; margin: 0; line-height: 1.6;">
                "{st.session_state['current_gauntlet_q']}"
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # TTS
        try:
            from gtts import gTTS
            from io import BytesIO
            tts = gTTS(st.session_state['current_gauntlet_q'], lang='en', tld='us')
            audio_bytes = BytesIO()
            tts.write_to_fp(audio_bytes)
            st.audio(audio_bytes, format='audio/mp3')
        except:
            pass
        
        st.markdown("---")
        
        # Answer input with live coaching
        col_answer, col_coach = st.columns([2, 1])
        
        with col_answer:
            st.markdown("### 🎙️ Your Answer")
            st.caption("💡 Voice dictation: Fn+Fn on Mac")
            
            user_answer = st.text_area(
                "Type your response",
                height=300,
                placeholder="S: Set the situation...\nT: What was the task/challenge?\nA: What did YOU specifically do?\nR: What was the quantified result?",
                key="gauntlet_answer"
            )
        
        with col_coach:
            st.markdown("### 📊 Live Coaching")
            
            if user_answer:
                # Real-time analysis
                analysis = analyze_response_live(user_answer)
                
                # ENHANCED SCORE DISPLAY (Larger, more prominent)
                score_color = "#00ff88" if analysis['overall_score'] >= 75 else "#FFD700" if analysis['overall_score'] >= 50 else "#ff4444"
                score_label = "EXCELLENT" if analysis['overall_score'] >= 75 else "GOOD" if analysis['overall_score'] >= 50 else "NEEDS WORK"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #0a0a0a, #1a1a2e); border: 3px solid {score_color}; border-radius: 12px; 
                            padding: 20px; text-align: center; margin-bottom: 20px; box-shadow: 0 0 30px {score_color}33;">
                    <p style="color: #8892b0; margin: 0; font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase;">LIVE SCORE</p>
                    <h1 style="color: {score_color}; margin: 10px 0; font-size: 3rem; font-weight: 900; text-shadow: 0 0 20px {score_color};">{analysis['overall_score']}</h1>
                    <p style="color: {score_color}; margin: 0; font-size: 0.8rem; letter-spacing: 1px;">{score_label}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # METRICS GRID (Enhanced visual with 6 metrics)
                st.markdown(f"""
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; margin-bottom: 15px;">
                    <div style="background: #0f0f15; border: 1px solid #333; border-radius: 8px; padding: 8px; text-align: center;">
                        <p style="color: #8892b0; margin: 0; font-size: 0.6rem;">WORDS</p>
                        <p style="color: #f0e6d3; margin: 2px 0; font-size: 0.9rem; font-weight: bold;">{analysis['word_count']}</p>
                        <p style="color: #666; margin: 0; font-size: 0.5rem;">~{analysis['estimated_time']}</p>
                    </div>
                    <div style="background: #0f0f15; border: 1px solid #333; border-radius: 8px; padding: 8px; text-align: center;">
                        <p style="color: #8892b0; margin: 0; font-size: 0.6rem;">OWNERSHIP</p>
                        <p style="color: {'#00ff88' if float(analysis['ownership_ratio'].split(':')[0]) >= 2 else '#FFD700'}; margin: 2px 0; font-size: 0.9rem; font-weight: bold;">{analysis['ownership_ratio']}</p>
                        <p style="color: #666; margin: 0; font-size: 0.5rem;">I vs We</p>
                    </div>
                    <div style="background: #0f0f15; border: 1px solid #333; border-radius: 8px; padding: 8px; text-align: center;">
                        <p style="color: #8892b0; margin: 0; font-size: 0.6rem;">METRICS</p>
                        <p style="color: {'#00ff88' if analysis['metric_density'] == 'High' else '#FFD700' if analysis['metric_density'] == 'Medium' else '#ff4444'}; margin: 2px 0; font-size: 0.9rem; font-weight: bold;">{analysis['metric_density']}</p>
                        <p style="color: #666; margin: 0; font-size: 0.5rem;">Numbers</p>
                    </div>
                    <div style="background: #0f0f15; border: 1px solid #333; border-radius: 8px; padding: 8px; text-align: center;">
                        <p style="color: #8892b0; margin: 0; font-size: 0.6rem;">CONVICTION</p>
                        <p style="color: {'#00ff88' if analysis['conviction_score'] >= 70 else '#FFD700' if analysis['conviction_score'] >= 50 else '#ff4444'}; margin: 2px 0; font-size: 0.9rem; font-weight: bold;">{analysis['conviction_label']}</p>
                        <p style="color: #666; margin: 0; font-size: 0.5rem;">{analysis['conviction_score']}%</p>
                    </div>
                    <div style="background: #0f0f15; border: 1px solid #333; border-radius: 8px; padding: 8px; text-align: center;">
                        <p style="color: #8892b0; margin: 0; font-size: 0.6rem;">SPECIFICITY</p>
                        <p style="color: {'#00ff88' if analysis['specificity_score'] >= 60 else '#FFD700' if analysis['specificity_score'] >= 30 else '#ff4444'}; margin: 2px 0; font-size: 0.9rem; font-weight: bold;">{analysis['specificity_label']}</p>
                        <p style="color: #666; margin: 0; font-size: 0.5rem;">{analysis['specificity_score']}%</p>
                    </div>
                    <div style="background: #0f0f15; border: 1px solid #333; border-radius: 8px; padding: 8px; text-align: center;">
                        <p style="color: #8892b0; margin: 0; font-size: 0.6rem;">POWER VERBS</p>
                        <p style="color: {'#00ff88' if analysis['power_verbs'] >= 3 else '#FFD700'}; margin: 2px 0; font-size: 0.9rem; font-weight: bold;">{analysis['power_verbs']}</p>
                        <p style="color: #666; margin: 0; font-size: 0.5rem;">Strong words</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # STAR CHECK (Visual boxes)
                st.markdown(f"""
                <div style="background: #0f0f15; border: 1px solid #333; border-radius: 8px; padding: 12px; margin-bottom: 15px;">
                    <p style="color: #D4AF37; margin: 0 0 8px 0; font-size: 0.7rem; letter-spacing: 1px;">STAR STRUCTURE</p>
                    <div style="display: flex; justify-content: space-between; gap: 5px;">
                        <div style="flex: 1; text-align: center; padding: 8px; background: {'#0a2f0a' if analysis['has_situation'] == '✅' else '#2f0a0a'}; border-radius: 4px;">
                            <span style="font-size: 1rem;">{analysis['has_situation']}</span>
                            <p style="color: #888; margin: 2px 0 0 0; font-size: 0.6rem;">Situation</p>
                        </div>
                        <div style="flex: 1; text-align: center; padding: 8px; background: {'#0a2f0a' if analysis['has_task'] == '✅' else '#2f0a0a'}; border-radius: 4px;">
                            <span style="font-size: 1rem;">{analysis['has_task']}</span>
                            <p style="color: #888; margin: 2px 0 0 0; font-size: 0.6rem;">Task</p>
                        </div>
                        <div style="flex: 1; text-align: center; padding: 8px; background: {'#0a2f0a' if analysis['has_action'] == '✅' else '#2f0a0a'}; border-radius: 4px;">
                            <span style="font-size: 1rem;">{analysis['has_action']}</span>
                            <p style="color: #888; margin: 2px 0 0 0; font-size: 0.6rem;">Action</p>
                        </div>
                        <div style="flex: 1; text-align: center; padding: 8px; background: {'#0a2f0a' if analysis['has_result'] == '✅' else '#2f0a0a'}; border-radius: 4px;">
                            <span style="font-size: 1rem;">{analysis['has_result']}</span>
                            <p style="color: #888; margin: 2px 0 0 0; font-size: 0.6rem;">Result</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # COACHING TIPS (Prominent)
                tips = generate_coaching_tips(analysis)
                if tips:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #1a1a0a, #0a0a1a); border: 1px solid #D4AF37; border-radius: 8px; padding: 12px;">
                        <p style="color: #D4AF37; margin: 0 0 8px 0; font-size: 0.7rem; letter-spacing: 1px;">💡 LIVE COACHING</p>
                    </div>
                    """, unsafe_allow_html=True)
                    for tip in tips[:4]:
                        st.markdown(f"<p style='color: #f0e6d3; font-size: 0.75rem; margin: 5px 0; line-height: 1.4;'>{tip}</p>", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: #0f0f15; border: 1px dashed #333; border-radius: 12px; padding: 30px; text-align: center;">
                    <p style="color: #666; font-size: 2rem; margin: 0;">📊</p>
                    <p style="color: #888; font-size: 0.9rem; margin: 10px 0 0 0;">Start typing to see<br/>live coaching...</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Action buttons
        st.markdown("---")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("🛑 END & ANALYZE", use_container_width=True):
                if user_answer:
                    analysis = analyze_response_live(user_answer)
                    st.session_state.interview_log.append({
                        "timestamp": datetime.now().isoformat(),
                        "layer": selected_layer,
                        "company": st.session_state.get('target_company', 'Unknown'),
                        "question": st.session_state['current_gauntlet_q'],
                        "answer": user_answer,
                        "score": analysis['overall_score'],
                        "star_score": analysis['star_score']
                    })
                    st.success(f"✅ Logged! Score: {analysis['overall_score']}/100")
        
        with col_b:
            if st.button("➡️ NEXT QUESTION", use_container_width=True):
                st.session_state['gauntlet_active'] = False
                st.rerun()
        
        with col_c:
            if st.button("⏫ NEXT LAYER", use_container_width=True):
                # Find next layer
                layer_list = list(INTERVIEW_LAYERS.keys())
                current_idx = layer_list.index(selected_layer)
                if current_idx < len(layer_list) - 1:
                    st.session_state['gauntlet_layer'] = layer_list[current_idx + 1]
                st.session_state['gauntlet_active'] = False
                st.rerun()


def render_story_bank_mode():
    """STAR Story Bank"""
    
    st.subheader("📝 STAR Story Arsenal")
    st.caption("Your curated library of 'Tell me about a time...' answers")
    
    # Display stories
    for idx, story in enumerate(st.session_state.story_bank):
        with st.expander(f"**{story['title']}** ({story['competency']})"):
            st.markdown(f"**S:** {story['situation']}")
            st.markdown(f"**T:** {story['task']}")
            st.markdown(f"**A:** {story['action']}")
            st.markdown(f"**R:** {story['result']}")
            st.caption(f"Tags: {', '.join(story['tags'])}")
    
    # Add new story
    st.markdown("---")
    with st.expander("➕ Add New Story"):
        new_title = st.text_input("Story Title")
        new_comp = st.selectbox("Competency", ["GTM Strategy", "Leadership", "Operations", "Technical", "Conflict Resolution"])
        
        col1, col2 = st.columns(2)
        new_s = col1.text_area("Situation", height=80)
        new_t = col2.text_area("Task", height=80)
        new_a = col1.text_area("Action", height=80)
        new_r = col2.text_area("Result", height=80)
        
        if st.button("💾 Save Story"):
            if new_title and new_s and new_a and new_r:
                st.session_state.story_bank.append({
                    "title": new_title,
                    "competency": new_comp,
                    "situation": new_s,
                    "task": new_t,
                    "action": new_a,
                    "result": new_r,
                    "tags": []
                })
                st.success("✅ Story saved!")
                st.rerun()


def render_bio_mode():
    """Bio-State Optimization"""
    
    st.subheader("🧬 Bio-State Optimization")
    st.caption("Science-backed protocols for peak interview performance")
    
    current_state = st.select_slider(
        "How do you feel?",
        options=["😰 Anxious", "😴 Low Energy", "🌫️ Brain Fog", "😐 Baseline", "⚡ Peak"]
    )
    
    st.markdown("---")
    
    for name, protocol in BIO_PROTOCOLS.items():
        with st.expander(name):
            st.markdown(f"**Technique:** {protocol['technique']}")
            st.markdown(f"**Instructions:** {protocol['instructions']}")
            st.markdown(f"**Timing:** {protocol['timing']}")
    
    # Checklist
    st.markdown("---")
    st.markdown("### ⚡ Pre-Interview Checklist")
    
    items = [
        "🔍 Researched company",
        "👥 LinkedIn-stalked interviewers",
        "📝 Prepared 3 questions for them",
        "🧊 Breathing/cold water done",
        "💪 Power pose (2 min)",
        "🎤 Tested audio/video",
        "📋 STAR stories reviewed"
    ]
    
    completed = sum(1 for item in items if st.checkbox(item, key=f"bio_{item}"))
    
    if completed == len(items):
        st.success("🏆 FULLY PREPPED!")
    else:
        st.info(f"{completed}/{len(items)} completed")


def render_performance_mode():
    """Performance Analytics"""
    
    st.subheader("📊 Performance Analytics")
    
    if not st.session_state.interview_log:
        st.info("No sessions logged yet. Complete some simulations!")
        return
    
    # Summary
    total = len(st.session_state.interview_log)
    avg_score = sum(s['score'] for s in st.session_state.interview_log) / total
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sessions", total)
    col2.metric("Average Score", f"{avg_score:.0f}/100")
    col3.metric("Latest Score", st.session_state.interview_log[-1]['score'])
    
    st.markdown("---")
    
    # Session history
    for session in reversed(st.session_state.interview_log[-10:]):
        with st.expander(f"Score: {session['score']}/100 | {session.get('layer', 'Unknown')}"):
            st.markdown(f"**Company:** {session.get('company', 'Unknown')}")
            st.markdown(f"**Question:** {session['question']}")
            st.markdown(f"**Answer:** {session['answer'][:200]}...")
    
    # Export
    if st.button("📥 Export JSON"):
        st.download_button(
            "Download",
            json.dumps(st.session_state.interview_log, indent=2),
            f"interview_log_{datetime.now().strftime('%Y%m%d')}.json"
        )
