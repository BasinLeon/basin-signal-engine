"""
Basin::Nexus CRM Models
Pydantic models for War Room, Pipeline, Fractional, Freezer, and Network tracking.
Updated: January 9, 2026
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class Priority(str, Enum):
    """Deal priority levels"""
    P1 = "P1"  # Critical - must close
    P2 = "P2"  # Important - active pursuit
    P3 = "P3"  # Normal - nurture
    COLD = "COLD"  # Freezer


class WarRoomTarget(BaseModel):
    """Active combat deal in the War Room"""
    id: str
    company: str
    role: str
    gatekeeper: str
    priority: int  # 1 = P1, 2 = P2, 3 = P3
    status: str  # FINALIST, ACTIVE, REFERRAL, ADVANCING
    next_move: str
    last_activity: datetime = Field(default_factory=datetime.now)
    signal_strength: int = 50  # 0-100
    velocity_score: float = 5.0  # 0-10
    notes: Optional[str] = None
    
    @property
    def is_hot(self) -> bool:
        return self.priority == 1 and self.status in ["FINALIST", "ACTIVE", "REFERRAL"]


class PipelineTarget(BaseModel):
    """Screening/backup pipeline target"""
    id: str
    company: str
    role: str
    priority: int  # 2 = P2, 3 = P3
    status: str  # Screening, Referral
    next_step: str
    last_activity: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None


class FractionalDeal(BaseModel):
    """Fractional/Octopus revenue deal"""
    id: str
    client: str
    monthly_value: float  # MRR in dollars
    probability: int  # 0-100 percentage
    status: str  # Active, Proposal, Initial Call, Scoping
    next_step: str
    last_contact: date = Field(default_factory=date.today)
    scope: Optional[str] = None
    contract_type: Optional[str] = None  # Retainer, Project
    
    @property
    def weighted_value(self) -> float:
        """Probability-adjusted monthly value"""
        return self.monthly_value * (self.probability / 100)


class FreezerAccount(BaseModel):
    """Stalled/zombie deal in the Freezer"""
    id: str
    company: str
    last_signal: date
    days_cold: int
    verdict: str  # "Purge", "Archive", "Dead", "One final bump"
    potential_value: float = 0
    reactivation_strategy: Optional[str] = None


class NetworkContact(BaseModel):
    """Network CRM contact / Champion"""
    id: str
    name: str
    company: str
    relationship_strength: int  # 0-100
    last_interaction: date = Field(default_factory=date.today)
    value_exchanged: Optional[str] = None
    next_touchpoint: Optional[str] = None
    is_champion: bool = False


class CommandCenterMetrics(BaseModel):
    """Executive Command Center summary metrics"""
    active_war_room: int
    fractional_mrr: float
    weighted_pipeline: float
    zombie_count: int
    pipeline_velocity: float  # Average velocity score
    last_updated: datetime = Field(default_factory=datetime.now)


class CRMSnapshot(BaseModel):
    """Full CRM state snapshot"""
    war_room: List[WarRoomTarget] = []
    fractional_pipeline: List[FractionalDeal] = []
    freezer: List[FreezerAccount] = []
    network: List[NetworkContact] = []
    metrics: Optional[CommandCenterMetrics] = None
    snapshot_time: datetime = Field(default_factory=datetime.now)
