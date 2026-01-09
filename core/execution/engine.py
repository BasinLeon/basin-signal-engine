"""
Basin::Nexus v5.1 - Execution Engine
Phase 3: The Human Handoff - High-Signal SDR orchestration

This module handles the transition from Machine to Human:
- Routes HOT signals (score >= 0.8) to Senior SDRs
- Triggers exec ghostwriting workflows
- Manages the "High-Leverage" activities
"""

from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

from core.scoring.gate import ScoringDecision, SignalTier


class SDRTier(str, Enum):
    """SDR specialization tiers in the Bifurcated Model"""
    HIGH_SIGNAL = "high_signal_sdr"      # Handles score >= 0.8 (executive accounts)
    MID_MARKET = "mid_market_sdr"         # Handles score 0.6-0.79 (growth accounts)
    AUTOMATED = "automated_sequence"      # Handles score < 0.6 (nurture only)


class OutreachTemplate(str, Enum):
    """Human-in-the-loop messaging strategies"""
    EXEC_GHOSTWRITE = "executive_ghostwriting"
    TECH_PEER = "technical_peer_outreach"
    WARM_INTRO = "mutual_connection_intro"
    MULTI_THREAD = "champion_plus_economic_buyer"


class ExecutionTask(BaseModel):
    """A task routed to a High-Signal SDR"""
    task_id: str
    company: str
    signal_score: float
    assigned_to: SDRTier
    template: OutreachTemplate
    context: Dict[str, any]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    due_at: Optional[datetime] = None


class CRMSyncPayload(BaseModel):
    """Payload for syncing to the 'Data Jail' (Salesforce/HubSpot)"""
    company: str
    contact_email: Optional[EmailStr] = None
    signal_tier: SignalTier
    enrichment_data: Dict[str, any]
    next_action: str
    sync_timestamp: datetime = Field(default_factory=datetime.utcnow)


def route_to_sdr(decision: ScoringDecision) -> ExecutionTask:
    """
    The Handoff Logic: Converts a Scoring Decision into an SDR task.
    
    This is the "Bifurcation Point" - where the machine hands off to humans.
    
    HOT signals (>= 0.8): High-Signal SDR + Executive Ghostwriting
    WARM signals (0.5-0.79): Automated sequence (no human touch)
    COLD signals (< 0.5): Archive to CRM (Data Jail)
    """
    
    task_id = f"TASK_{decision.company}_{datetime.utcnow().timestamp()}"
    
    if decision.tier == SignalTier.HOT:
        # High-leverage human activity
        return ExecutionTask(
            task_id=task_id,
            company=decision.company,
            signal_score=decision.score,
            assigned_to=SDRTier.HIGH_SIGNAL,
            template=OutreachTemplate.EXEC_GHOSTWRITE,
            context={
                "reasoning": decision.reasoning,
                "action": "Draft executive-level messaging for key decision-makers",
                "sla": "4 hours",  # Fudo standard: same-day outreach for HOT signals
                "talking_points": [
                    "Reference specific signal (GitHub repo, funding round, etc.)",
                    "Position as peer-to-peer technical conversation",
                    "Offer specific value (not generic pitch)"
                ]
            }
        )
    
    elif decision.tier == SignalTier.WARM:
        # Automated nurture (no human required)
        return ExecutionTask(
            task_id=task_id,
            company=decision.company,
            signal_score=decision.score,
            assigned_to=SDRTier.AUTOMATED,
            template=OutreachTemplate.TECH_PEER,
            context={
                "reasoning": decision.reasoning,
                "action": "Enroll in 30-day LLM-driven nurture sequence",
                "cadence": "3 emails over 30 days",
                "re_score_date": "30 days from now"
            }
        )
    
    else:  # SignalTier.COLD
        # Archive to CRM (no immediate action)
        return ExecutionTask(
            task_id=task_id,
            company=decision.company,
            signal_score=decision.score,
            assigned_to=SDRTier.AUTOMATED,
            template=OutreachTemplate.TECH_PEER,
            context={
                "reasoning": decision.reasoning,
                "action": "Archive to Data Jail (CRM) for quarterly review",
                "next_review": "Q2 2026"
            }
        )


def sync_to_crm(decision: ScoringDecision, enrichment: Dict[str, any]) -> CRMSyncPayload:
    """
    Push data to the 'Data Jail' (Salesforce/HubSpot).
    
    The CRM is the STORAGE layer, not the INTELLIGENCE layer.
    It receives decisions; it doesn't make them.
    """
    
    if decision.tier == SignalTier.HOT:
        next_action = "Senior SDR assigned - Executive ghostwriting in progress"
    elif decision.tier == SignalTier.WARM:
        next_action = "Automated nurture sequence - 30-day engagement window"
    else:
        next_action = "Archived - Low signal score"
    
    return CRMSyncPayload(
        company=decision.company,
        signal_tier=decision.tier,
        enrichment_data=enrichment,
        next_action=next_action
    )


class ExecutionEngine:
    """
    Phase 3 (Human) coordinator.
    
    Manages the handoff from Machine (scoring) to Human (closing).
    
    This is the "10x SDR" multiplier - one human managing 5x the pipeline
    because they only touch high-probability, pre-qualified signals.
    """
    
    def __init__(self):
        self.pending_tasks: List[ExecutionTask] = []
        self.crm_sync_queue: List[CRMSyncPayload] = []
    
    def execute(self, decision: ScoringDecision, enrichment: Dict[str, any] = None) -> ExecutionTask:
        """
        Execute on a scored signal.
        
        Routes to:
        1. High-Signal SDR (for HOT signals)
        2. Automated sequence (for WARM signals)
        3. Data Jail archive (for COLD signals)
        """
        
        enrichment = enrichment or {}
        
        # Create SDR task
        task = route_to_sdr(decision)
        self.pending_tasks.append(task)
        
        # Sync to CRM
        crm_payload = sync_to_crm(decision, enrichment)
        self.crm_sync_queue.append(crm_payload)
        
        return task
    
    def get_sdr_workload(self, sdr_tier: SDRTier) -> List[ExecutionTask]:
        """Fetch tasks for a specific SDR tier"""
        return [task for task in self.pending_tasks if task.assigned_to == sdr_tier]
    
    def flush_crm_sync(self) -> List[CRMSyncPayload]:
        """Batch sync to CRM (reduce API calls)"""
        payloads = self.crm_sync_queue.copy()
        self.crm_sync_queue.clear()
        return payloads


# Example: The complete Nexus pipeline
if __name__ == "__main__":
    from core.scoring.gate import GTMSignal, SignalSource, nexus_scoring_gate
    
    engine = ExecutionEngine()
    
    # Example 1: HOT signal from NVIDIA
    nvidia_signal = GTMSignal(
        source=SignalSource.GITHUB,
        company="NVIDIA",
        intent_type="New security infrastructure repo",
        raw_score=0.92
    )
    
    decision = nexus_scoring_gate(nvidia_signal)
    task = engine.execute(decision, enrichment={
        "tech_stack": ["Kubernetes", "Python", "Go"],
        "team_size": 500,
        "decision_maker": "VP Engineering"
    })
    
    print(f"\\n🔥 HOT SIGNAL EXECUTION")
    print(f"Task ID: {task.task_id}")
    print(f"Assigned To: {task.assigned_to.value}")
    print(f"Template: {task.template.value}")
    print(f"Action: {task.context['action']}")
    print(f"SLA: {task.context.get('sla', 'N/A')}")
    
    # Example 2: WARM signal from eBay
    ebay_signal = GTMSignal(
        source=SignalSource.JOB_POST,
        company="eBay",
        intent_type="Hiring Security Engineer",
        raw_score=0.67
    )
    
    decision2 = nexus_scoring_gate(ebay_signal)
    task2 = engine.execute(decision2)
    
    print(f"\\n⚡ WARM SIGNAL EXECUTION")
    print(f"Task ID: {task2.task_id}")
    print(f"Assigned To: {task2.assigned_to.value}")
    print(f"Action: {task2.context['action']}")
    print(f"Cadence: {task2.context.get('cadence', 'N/A')}")
    
    # Show SDR workload
    high_signal_tasks = engine.get_sdr_workload(SDRTier.HIGH_SIGNAL)
    print(f"\\n📊 High-Signal SDR Workload: {len(high_signal_tasks)} tasks")
    
    # Flush CRM sync
    crm_syncs = engine.flush_crm_sync()
    print(f"📤 CRM Sync Queue: {len(crm_syncs)} records ready for Data Jail")
