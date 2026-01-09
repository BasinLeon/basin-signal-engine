"""Basin::Nexus v5.1 - Core package initialization"""

from core.ingestion.engine import (
    IngestionEngine,
    IngestionChannel,
    RawSignal,
    GitHubSignal,
    LinkedInSignal,
    FundingSignal
)

from core.scoring.gate import (
    nexus_scoring_gate,
    GTMSignal,
    ScoringDecision,
    SignalSource,
    SignalTier
)

from core.execution.engine import (
    ExecutionEngine,
    ExecutionTask,
    SDRTier,
    OutreachTemplate,
    route_to_sdr,
    sync_to_crm
)

__version__ = "5.1.0"
__all__ = [
    # Ingestion
    "IngestionEngine",
    "IngestionChannel",
    "RawSignal",
    "GitHubSignal",
    "LinkedInSignal",
    "FundingSignal",
    
    # Scoring
    "nexus_scoring_gate",
    "GTMSignal",
    "ScoringDecision",
    "SignalSource",
    "SignalTier",
    
    # Execution
    "ExecutionEngine",
    "ExecutionTask",
    "SDRTier",
    "OutreachTemplate",
    "route_to_sdr",
    "sync_to_crm",
]
