"""
Basin::Nexus CRM Data
Seeded from LeonOS CRM export - January 2026
"""

from datetime import datetime
from core.crm.models import (
    Priority,
    DealStatus,
    WarRoomTarget,
    FractionalDeal,
    FreezerAccount,
    ContactTier,
    NetworkContact,
    CRMSnapshot
)


# =============================================================================
# WAR ROOM - Active Combat (4 High-Value Targets)
# =============================================================================

WAR_ROOM_TARGETS = [
    WarRoomTarget(
        id="wr-001",
        company="LiveRamp",
        role="Lead PMM",
        priority=Priority.P1,
        status=DealStatus.URGENT,
        contact_name="Samantha Lopez",
        next_move="Execute 'Insurance Policy' play - secure next round",
        notes="Finalist Stage - RED ZONE. Career-defining opportunity."
    ),
    WarRoomTarget(
        id="wr-002",
        company="QuantumScape",
        role="PMM",
        priority=Priority.P1,
        status=DealStatus.ACTIVE,
        contact_name="Smita",
        contact_phone="408-849-2907",
        next_move="Call Smita directly - lock the screen",
        notes="Direct line available. High urgency."
    ),
    WarRoomTarget(
        id="wr-003",
        company="Sendbird",
        role="SDR Manager",
        priority=Priority.P2,
        status=DealStatus.WAITING,
        contact_name="Peter / Charles",
        next_move="Bump Peter - check for 'Agentic Framework' feedback",
        notes="Waiting on internal feedback."
    ),
    WarRoomTarget(
        id="wr-004",
        company="NVIDIA",
        role="DevRel",
        priority=Priority.P2,
        status=DealStatus.REFERRAL,
        contact_name="Minh Pham",
        next_move="Confirm formal referral submission",
        notes="Referral pathway - confirm Minh has submitted."
    ),
]


# =============================================================================
# FRACTIONAL PIPELINE - The "Octopus" Revenue
# =============================================================================
# Total Monthly Potential: ~$16,000/mo
# Weighted Pipeline (Probability Adjusted): ~$8,350/mo

FRACTIONAL_DEALS = [
    FractionalDeal(
        id="frac-001",
        client="FYM Partners",
        monthly_value=5000.0,
        probability=0.70,
        status=DealStatus.ACTIVE,
        next_step="Deliver Tiered System Doc",
        notes="High confidence close"
    ),
    FractionalDeal(
        id="frac-002",
        client="Nexus AI",
        monthly_value=2500.0,
        probability=0.60,
        status=DealStatus.PROPOSAL,
        next_step="Finalize Scope of Work",
        notes=""
    ),
    FractionalDeal(
        id="frac-003",
        client="TechFlow",
        monthly_value=1500.0,
        probability=0.50,
        status=DealStatus.SCOPING,
        next_step="Send Project Outline",
        notes="Initial call completed"
    ),
    FractionalDeal(
        id="frac-004",
        client="SolveJet",
        monthly_value=3000.0,
        probability=0.40,
        status=DealStatus.PROPOSAL,
        next_step="Follow up on Contract",
        notes=""
    ),
    FractionalDeal(
        id="frac-005",
        client="Spray.io",
        monthly_value=2000.0,
        probability=0.30,
        status=DealStatus.SCOPING,
        next_step="Define Deliverables",
        notes=""
    ),
    FractionalDeal(
        id="frac-006",
        client="AlphaCorp",
        monthly_value=4000.0,
        probability=0.20,
        status=DealStatus.LEAD,
        next_step="Schedule Discovery",
        notes=""
    ),
]


# =============================================================================
# FREEZER - Stalled / Low Signal (Do not spend Prime Time here)
# =============================================================================

FREEZER_ACCOUNTS = [
    FreezerAccount(
        id="freeze-001",
        company="SnapMagic",
        last_activity=datetime(2025, 11, 20),
        stalled_since=datetime(2025, 11, 20),
        verdict="Purge or 'Hail Mary' to Ryan",
        notes="Stalled since 11/20"
    ),
    FreezerAccount(
        id="freeze-002",
        company="Aikido Security",
        last_activity=datetime(2025, 11, 15),
        stalled_since=datetime(2025, 11, 15),
        verdict="Archive",
        notes="No movement"
    ),
    FreezerAccount(
        id="freeze-003",
        company="Hightouch",
        last_activity=datetime(2025, 11, 21),
        stalled_since=datetime(2025, 11, 21),
        verdict="Dead",
        notes="Stalled Nov 21"
    ),
    FreezerAccount(
        id="freeze-004",
        company="Mistral",
        last_activity=datetime(2025, 11, 21),
        stalled_since=datetime(2025, 11, 21),
        verdict="Dead",
        notes="Stalled Nov 21"
    ),
    FreezerAccount(
        id="freeze-005",
        company="Andromeda",
        last_activity=datetime(2025, 11, 21),
        stalled_since=datetime(2025, 11, 21),
        verdict="Dead",
        notes="Stalled Nov 21"
    ),
    FreezerAccount(
        id="freeze-006",
        company="Skypoint",
        last_activity=datetime(2025, 12, 4),
        stalled_since=datetime(2025, 12, 4),
        verdict="One final bump, then archive",
        notes="Zero Trust pitch sent Dec 4"
    ),
    FreezerAccount(
        id="freeze-007",
        company="Verkada",
        last_activity=datetime(2025, 11, 10),
        stalled_since=datetime(2025, 11, 10),
        verdict="Archive",
        notes=""
    ),
    FreezerAccount(
        id="freeze-008",
        company="LinkedIn",
        last_activity=datetime(2025, 11, 8),
        stalled_since=datetime(2025, 11, 8),
        verdict="Archive",
        notes=""
    ),
]


# =============================================================================
# NETWORK PULSE - Champions and Revivals
# =============================================================================

NETWORK_CONTACTS = [
    NetworkContact(
        id="net-001",
        name="Ryan Richardson",
        company="SnapMagic / Source",
        tier=ContactTier.CHAMPION,
        relationship="Referral Source",
        notes="Top champion"
    ),
    NetworkContact(
        id="net-002",
        name="Minh Pham",
        company="NVIDIA",
        tier=ContactTier.CHAMPION,
        relationship="Direct Referral",
        next_action="Confirm referral submitted",
        notes="NVIDIA pathway"
    ),
    NetworkContact(
        id="net-003",
        name="Oliver Perry",
        company="Trust in Soda",
        tier=ContactTier.CHAMPION,
        relationship="Strategic Partner",
        notes="Successfully re-engaged"
    ),
    NetworkContact(
        id="net-004",
        name="Ed Carr",
        company="Elite Cyber GTM",
        tier=ContactTier.REVIVAL,
        relationship="Revival",
        notes="Re-engaged with Reg + AI pitch"
    ),
    NetworkContact(
        id="net-005",
        name="Samantha Lopez",
        company="LiveRamp",
        tier=ContactTier.TIER_1,
        relationship="Decision Maker",
        next_action="Execute Insurance Policy play",
        notes="Critical relationship for P1 deal"
    ),
]


# =============================================================================
# COMMAND CENTER SNAPSHOT
# =============================================================================

def get_current_snapshot() -> CRMSnapshot:
    """Get current CRM state as a snapshot"""
    return CRMSnapshot(
        war_room=WAR_ROOM_TARGETS,
        fractional=FRACTIONAL_DEALS,
        freezer=FREEZER_ACCOUNTS,
        network=NETWORK_CONTACTS
    )


def get_metrics_summary() -> dict:
    """Get formatted metrics for display"""
    snapshot = get_current_snapshot()
    metrics = snapshot.metrics
    
    return {
        "active_war_room": metrics.active_war_room,
        "fractional_mrr": f"${metrics.fractional_mrr:,.0f}/mo",
        "weighted_pipeline": f"${metrics.weighted_pipeline:,.0f}/mo",
        "pipeline_velocity": metrics.pipeline_velocity,
        "network_heat": metrics.network_heat,
        "zombie_count": metrics.zombie_count
    }


# Quick access for templates
METRICS_SUMMARY = {
    "active_war_room": 4,
    "fractional_mrr": "$16,000/mo",
    "weighted_pipeline": "$8,350/mo",
    "pipeline_velocity": "Urgent",
    "network_heat": "High",
    "zombie_count": 8
}
