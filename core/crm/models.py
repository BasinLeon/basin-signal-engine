"""
Basin::Nexus CRM Models
Pydantic models for War Room, Fractional Pipeline, and Network tracking.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class Priority(str, Enum):
    """Deal priority levels"""
    P1 = "P1"  # Critical - must close
    P2 = "P2"  # Important - active pursuit
    P3 = "P3"  # Normal - nurture
    COLD = "COLD"  # Freezer


class DealStatus(str, Enum):
    """Deal lifecycle status"""
    URGENT = "URGENT"
    ACTIVE = "ACTIVE"
    WAITING = "WAITING"
    REFERRAL = "REFERRAL"
    PROPOSAL = "PROPOSAL"
    SCOPING = "SCOPING"
    LEAD = "LEAD"
    STALLED = "STALLED"
    DEAD = "DEAD"


class WarRoomTarget(BaseModel):
    """Active combat deal in the War Room"""
    id: str
    company: str
    role: str
    priority: Priority
    status: DealStatus
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    next_move: str
    last_activity: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None
    
    @property
    def is_hot(self) -> bool:
        return self.priority == Priority.P1 and self.status in [DealStatus.URGENT, DealStatus.ACTIVE]


class FractionalDeal(BaseModel):
    """Fractional/Octopus revenue deal"""
    id: str
    client: str
    monthly_value: float  # MRR
    probability: float  # 0.0 - 1.0
    status: DealStatus
    next_step: str
    last_activity: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None
    
    @property
    def weighted_value(self) -> float:
        """Probability-adjusted monthly value"""
        return self.monthly_value * self.probability


class FreezerAccount(BaseModel):
    """Stalled/zombie deal in the Freezer"""
    id: str
    company: str
    last_activity: datetime
    stalled_since: datetime
    verdict: str  # "Purge", "Archive", "Hail Mary", "One Final Bump"
    notes: Optional[str] = None
    
    @property
    def days_stalled(self) -> int:
        return (datetime.now() - self.stalled_since).days


class ContactTier(str, Enum):
    """Network contact tier"""
    CHAMPION = "CHAMPION"
    TIER_1 = "TIER_1"
    TIER_2 = "TIER_2"
    REVIVAL = "REVIVAL"


class NetworkContact(BaseModel):
    """Network CRM contact"""
    id: str
    name: str
    company: str
    tier: ContactTier
    relationship: str  # e.g., "Direct Line", "Referral Source", "Champion"
    last_contact: Optional[datetime] = None
    next_action: Optional[str] = None
    notes: Optional[str] = None


class CommandCenterMetrics(BaseModel):
    """Executive Command Center summary metrics"""
    active_war_room: int
    fractional_mrr: float
    weighted_pipeline: float
    network_heat: str  # "High", "Medium", "Low"
    zombie_count: int
    
    # Computed
    @property
    def pipeline_velocity(self) -> str:
        if self.active_war_room >= 3:
            return "Urgent"
        elif self.active_war_room >= 1:
            return "Active"
        return "Cold"


class CRMSnapshot(BaseModel):
    """Full CRM state snapshot"""
    timestamp: datetime = Field(default_factory=datetime.now)
    war_room: List[WarRoomTarget] = []
    fractional: List[FractionalDeal] = []
    freezer: List[FreezerAccount] = []
    network: List[NetworkContact] = []
    
    @property
    def metrics(self) -> CommandCenterMetrics:
        total_mrr = sum(d.monthly_value for d in self.fractional)
        weighted = sum(d.weighted_value for d in self.fractional)
        
        return CommandCenterMetrics(
            active_war_room=len(self.war_room),
            fractional_mrr=total_mrr,
            weighted_pipeline=weighted,
            network_heat="High" if len([c for c in self.network if c.tier == ContactTier.CHAMPION]) >= 3 else "Medium",
            zombie_count=len(self.freezer)
        )
