# Basin::Nexus v5.1 - Core Modules

This directory contains the production code that implements the **Bifurcated GTM Operating Model**.

---

## Directory Structure

```
core/
├── ingestion/       Phase 1 (Machine): Signal detection & collection
├── scoring/         Phase 2 (The Gate): LLM-powered ICP scoring  
└── execution/       Phase 3 (Human): High-Signal SDR orchestration
```

---

## Module Overview

### `/ingestion` - The Signal Ledger
**Purpose:** Detect buyer intent signals from multiple channels in real-time

**Channels:**
- GitHub webhooks (repo activity, stars, commits)
- LinkedIn scraper (job posts, exec hires, company updates)
- Funding APIs (Crunchbase, PitchBook)
- Job board scrapers (hiring velocity signals)

**Output:** `RawSignal` objects ready for scoring

**Key File:** `engine.py` - Multi-source ingestion coordinator

---

### `/scoring` - The LLM Gate
**Purpose:** Apply the 0.8 threshold that bifurcates Machine from Human work

**Logic:**
- Score >= 0.8 → **HOT** → High-Signal SDR (Executive Ghostwriting)
- Score 0.5-0.8 → **WARM** → Automated nurture sequence
- Score < 0.5 → **COLD** → Archive to Data Jail (CRM)

**Output:** `ScoringDecision` with tier and routing instructions

**Key File:** `gate.py` - The decision engine that killed human latency at Fudo

---

### `/execution` - The Handoff
**Purpose:** Route scored signals to appropriate execution channels

**Routes:**
- **HOT signals:** Assigned to High-Signal SDR with 4-hour SLA
- **WARM signals:** Enrolled in LLM-driven nurture (30-day window)
- **COLD signals:** Archived to CRM for quarterly review

**Output:** `ExecutionTask` objects + CRM sync payloads

**Key File:** `engine.py` - The handoff coordinator

---

## The Complete Pipeline

```
Signal Detection → LLM Scoring → Human Handoff → Meeting/Deal
(Ingestion)        (Gate)         (Execution)      (Outcome)
```

**Data Flow:**
1. `ingestion/engine.py` captures signals from GitHub, LinkedIn, etc.
2. `scoring/gate.py` applies LLM-powered ICP matching
3. `execution/engine.py` routes HOT signals to SDRs, WARM to automation

**Result:** 160% pipeline growth with 50% reduction in manual toil (Fudo Security implementation)

---

## Running the Examples

Each module includes a `__main__` block with test data:

```bash
# Test the Scoring Gate
python core/scoring/gate.py

# Test the Ingestion Engine
python core/ingestion/engine.py

# Test the Execution Engine
python core/execution/engine.py
```

---

## Design Philosophy

> **"The CRM is a Data Jail. Intelligence happens upstream."**

This codebase proves that Basin::Nexus isn't a slide deck—it's a production-grade revenue engine that:
- Kills the 24-48 hour "Human Latency" gap
- Gives SDRs 10x leverage by pre-qualifying all signals
- Reduces CAC by 60% while increasing throughput by 3x

**Code is the new revenue capacity.**

---

*Leon Basin | Revenue Architect*  
*Basin::Nexus v5.1*
