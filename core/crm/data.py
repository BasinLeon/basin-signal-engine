"""
LeonOS GTM CRM: Master State Data
Updated: January 9, 2026

This module contains the seeded CRM data synchronized with LeonOS.
Contains War Room targets, Pipeline screening, Fractional deals,
Freezer accounts, and Network contacts.
"""

from datetime import datetime, date
from typing import List
from .models import (
    WarRoomTarget, PipelineTarget, FractionalDeal, 
    FreezerAccount, NetworkContact, CRMSnapshot, CommandCenterMetrics
)


# ============================================================================
# 1. THE WAR ROOM (Active Combat)
# Focus: P1 Opportunities with "High Velocity" status
# ============================================================================

WAR_ROOM_TARGETS: List[WarRoomTarget] = [
    WarRoomTarget(
        id="wr-liveramp",
        company="LiveRamp",
        role="Lead PMM",
        gatekeeper="Tammy (HM)",
        priority=1,  # P1 - FINALIST
        status="FINALIST",
        next_move="Wait: Tammy advancing you to Samantha Lopez (Marketplace/Commercial). 'Insurance Policy' narrative landed.",
        last_activity=datetime(2026, 1, 9, 10, 0),
        signal_strength=95,
        velocity_score=9.5,
        notes="Multiple rounds complete. Final decision stage. Samantha Lopez intro pending."
    ),
    WarRoomTarget(
        id="wr-fastino",
        company="Fastino",
        role="Founding Sales",
        gatekeeper="Allison/Founders",
        priority=1,  # P1 - ACTIVE
        status="ACTIVE",
        next_move="Wait: Sent 'Agentic Architecture' to George & Ash. Used LiveRamp as leverage to force urgency.",
        last_activity=datetime(2026, 1, 9, 9, 30),
        signal_strength=88,
        velocity_score=8.5,
        notes="Founders engaged. Agentic Architecture deck deployed. LiveRamp leverage play active."
    ),
    WarRoomTarget(
        id="wr-okta",
        company="Okta",
        role="Tech PMM",
        gatekeeper="Anthony Walsh",
        priority=1,  # P1 - NEW REFERRAL
        status="REFERRAL",
        next_move="Wait: Anthony is vouching for you with the team. 'Playdate' bond secured.",
        last_activity=datetime(2026, 1, 9, 12, 0),
        signal_strength=85,
        velocity_score=8.0,
        notes="Warm referral from Anthony Walsh. Personal connection established. Awaiting team intro."
    ),
    WarRoomTarget(
        id="wr-quantumscape",
        company="QuantumScape",
        role="PMM",
        gatekeeper="Smita",
        priority=1,  # P1 - ADVANCING
        status="ADVANCING",
        next_move="Drafting: Creating the 'Translation Layer' brief Smita requested.",
        last_activity=datetime(2026, 1, 9, 8, 0),
        signal_strength=78,
        velocity_score=7.5,
        notes="Smita requested Translation Layer brief. Actively engaged."
    ),
    WarRoomTarget(
        id="wr-sendbird",
        company="Sendbird",
        role="SDR Manager",
        gatekeeper="Peter/Charles",
        priority=2,  # P2 - ADVANCING
        status="ADVANCING",
        next_move="Monitor: Sent 'SDR Transition Playbook' to Peter. Awaiting feedback.",
        last_activity=datetime(2026, 1, 8, 16, 0),
        signal_strength=72,
        velocity_score=7.0,
        notes="SDR Transition Playbook deployed. Peter reviewing."
    ),
]


# ============================================================================
# 2. THE PIPELINE (Screening & Backups)
# Focus: Insurance policies and "Safety Net" interviews
# ============================================================================

PIPELINE_TARGETS: List[PipelineTarget] = [
    PipelineTarget(
        id="pl-mastech",
        company="Mastech",
        role="Sales Lead",
        priority=2,  # P2
        status="Screening",
        next_step="Call Monday: Confirmed $320k+ OTE. 'Hunter' profile. Good leverage/backup.",
        last_activity=datetime(2026, 1, 9, 11, 0),
        notes="High OTE confirmed. Strong backup option."
    ),
    PipelineTarget(
        id="pl-variacode",
        company="Variacode",
        role="Sales",
        priority=3,  # P3
        status="Screening",
        next_step="Pending: Sent 'Comp/JD' filter email. Low tier until proven otherwise.",
        last_activity=datetime(2026, 1, 7, 14, 0),
        notes="Awaiting comp/JD details. Low priority."
    ),
    PipelineTarget(
        id="pl-nvidia",
        company="NVIDIA",
        role="DevRel",
        priority=3,  # P3
        status="Referral",
        next_step="Check: Confirm Minh Pham submitted the formal referral.",
        last_activity=datetime(2026, 1, 6, 10, 0),
        notes="Minh Pham referral pending confirmation."
    ),
]


# ============================================================================
# 3. FRACTIONAL PIPELINE (The "Octopus" Revenue)
# Focus: Cash Flow Stabilization (~$18k/mo Potential)
# ============================================================================

FRACTIONAL_DEALS: List[FractionalDeal] = [
    FractionalDeal(
        id="frac-fym",
        client="FYM Partners",
        monthly_value=5000,
        probability=70,
        status="Active",
        next_step="Deliver Tiered System Doc.",
        last_contact=date(2026, 1, 9),
        scope="GTM Strategy + Sales Process Optimization",
        contract_type="Retainer"
    ),
    FractionalDeal(
        id="frac-nexusai",
        client="Nexus AI",
        monthly_value=2500,
        probability=60,
        status="Proposal",
        next_step="Finalize Scope of Work.",
        last_contact=date(2026, 1, 8),
        scope="Product Marketing Strategy",
        contract_type="Project"
    ),
    FractionalDeal(
        id="frac-techflow",
        client="TechFlow",
        monthly_value=1500,
        probability=50,
        status="Initial Call",
        next_step="Send Project Outline.",
        last_contact=date(2026, 1, 7),
        scope="Sales Enablement",
        contract_type="Project"
    ),
    FractionalDeal(
        id="frac-solvejet",
        client="SolveJet",
        monthly_value=3000,
        probability=40,
        status="Proposal",
        next_step="Follow up on Contract.",
        last_contact=date(2026, 1, 6),
        scope="Enterprise Pipeline Development",
        contract_type="Retainer"
    ),
    FractionalDeal(
        id="frac-spray",
        client="Spray.io",
        monthly_value=2000,
        probability=30,
        status="Scoping",
        next_step="Define Deliverables.",
        last_contact=date(2026, 1, 5),
        scope="Outbound Strategy",
        contract_type="Project"
    ),
]


# ============================================================================
# 4. THE FREEZER (Stalled / Low Signal)
# Verdict: Do not spend "Prime Time" energy here
# ============================================================================

FREEZER_ACCOUNTS: List[FreezerAccount] = [
    FreezerAccount(
        id="frz-snapmagic",
        company="SnapMagic",
        last_signal=date(2025, 11, 20),
        days_cold=50,
        verdict="Purge or 'Hail Mary' to Ryan",
        potential_value=0,
        reactivation_strategy="Final Hail Mary email to Ryan, then archive"
    ),
    FreezerAccount(
        id="frz-aikido",
        company="Aikido Security",
        last_signal=date(2025, 11, 25),
        days_cold=45,
        verdict="Archive",
        potential_value=0,
        reactivation_strategy="None - Archive"
    ),
    FreezerAccount(
        id="frz-hightouch",
        company="Hightouch",
        last_signal=date(2025, 11, 21),
        days_cold=49,
        verdict="Dead",
        potential_value=0,
        reactivation_strategy="None - Dead"
    ),
    FreezerAccount(
        id="frz-mistral",
        company="Mistral",
        last_signal=date(2025, 11, 21),
        days_cold=49,
        verdict="Dead",
        potential_value=0,
        reactivation_strategy="None - Dead"
    ),
    FreezerAccount(
        id="frz-skypoint",
        company="Skypoint",
        last_signal=date(2025, 12, 4),
        days_cold=36,
        verdict="One final bump, then archive",
        potential_value=0,
        reactivation_strategy="'Zero Trust' pitch sent Dec 4. One final bump."
    ),
]


# ============================================================================
# 5. NETWORK CHAMPIONS
# Key contacts and referral sources
# ============================================================================

NETWORK_CONTACTS: List[NetworkContact] = [
    NetworkContact(
        id="net-anthony",
        name="Anthony Walsh",
        company="Okta",
        relationship_strength=95,
        last_interaction=date(2026, 1, 9),
        value_exchanged="Okta team intro + vouching",
        next_touchpoint="Monitor for 'Coffee' text or team intro",
        is_champion=True
    ),
    NetworkContact(
        id="net-ryan",
        name="Ryan Richardson",
        company="SnapMagic",
        relationship_strength=65,
        last_interaction=date(2025, 11, 20),
        value_exchanged="Previous engagement",
        next_touchpoint="Hail Mary email if SnapMagic worth pursuing",
        is_champion=False
    ),
    NetworkContact(
        id="net-minh",
        name="Minh Pham",
        company="NVIDIA",
        relationship_strength=80,
        last_interaction=date(2026, 1, 6),
        value_exchanged="NVIDIA referral pending",
        next_touchpoint="Confirm formal referral submitted",
        is_champion=True
    ),
    NetworkContact(
        id="net-smita",
        name="Smita",
        company="QuantumScape",
        relationship_strength=75,
        last_interaction=date(2026, 1, 9),
        value_exchanged="Translation Layer brief request",
        next_touchpoint="Deliver Translation Layer brief",
        is_champion=True
    ),
    NetworkContact(
        id="net-samantha",
        name="Samantha Lopez",
        company="LiveRamp",
        relationship_strength=70,
        last_interaction=date(2026, 1, 9),
        value_exchanged="Marketplace/Commercial intro pending",
        next_touchpoint="Await intro from Tammy",
        is_champion=True
    ),
]


# ============================================================================
# 6. TECHNICAL PROJECTS (The "Builder" Narrative)
# ============================================================================

TECHNICAL_PROJECTS = {
    "n8n_docker": {
        "name": "n8n on Docker",
        "status": "Deploying",
        "port": 5678,
        "narrative": "'Eating your own dog food' story for Fastino/Okta"
    },
    "basin_nexus": {
        "name": "Basin::Nexus v11",
        "status": "Live",
        "deployments": ["Fastino", "LiveRamp", "Anthony Walsh"],
        "narrative": "PDF deployed to key stakeholders"
    }
}


# ============================================================================
# AGGREGATE METRICS
# ============================================================================

def calculate_metrics() -> CommandCenterMetrics:
    """Calculate real-time Command Center metrics from CRM data."""
    
    # War Room stats
    active_war_room = len([t for t in WAR_ROOM_TARGETS if t.priority == 1])
    
    # Fractional pipeline
    total_mrr = sum(d.monthly_value for d in FRACTIONAL_DEALS)
    weighted_pipeline = sum(
        d.monthly_value * (d.probability / 100) 
        for d in FRACTIONAL_DEALS
    )
    
    # Freezer count
    zombie_count = len(FREEZER_ACCOUNTS)
    
    # Velocity (average of war room targets)
    avg_velocity = sum(t.velocity_score for t in WAR_ROOM_TARGETS) / len(WAR_ROOM_TARGETS) if WAR_ROOM_TARGETS else 0
    
    return CommandCenterMetrics(
        active_war_room=active_war_room,
        fractional_mrr=total_mrr,
        weighted_pipeline=weighted_pipeline,
        zombie_count=zombie_count,
        pipeline_velocity=avg_velocity,
        last_updated=datetime.now()
    )


def get_crm_snapshot() -> CRMSnapshot:
    """Get complete CRM snapshot for dashboard."""
    return CRMSnapshot(
        war_room=WAR_ROOM_TARGETS,
        fractional_pipeline=FRACTIONAL_DEALS,
        freezer=FREEZER_ACCOUNTS,
        network=NETWORK_CONTACTS,
        metrics=calculate_metrics(),
        snapshot_time=datetime.now()
    )


# ============================================================================
# WEEKEND PROTOCOL - NEXT STEPS
# ============================================================================

WEEKEND_PROTOCOL = {
    "monitor": "Watch for Anthony's 'Okta Intro' or 'Coffee' text.",
    "build": "Get your first n8n workflow live (e.g., 'Email to Slack').",
    "rest": "You have 3 major deals (LiveRamp, Fastino, Okta) in the 'Red Zone.' Clear your head for closing week."
}
