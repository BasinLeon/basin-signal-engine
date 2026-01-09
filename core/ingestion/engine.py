"""
Basin::Nexus v5.1 - Ingestion Engine
Multi-source signal detection that powers the Bifurcated GTM Model.

This module handles Phase 1 (Machine): Signal detection from GitHub, LinkedIn,
funding databases, and job boards.
"""

from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import json


class IngestionChannel(str, Enum):
    """Active signal sources for the Unified Signal Ledger"""
    GITHUB_WEBHOOKS = "github_webhooks"
    LINKEDIN_SCRAPER = "linkedin_scraper"
    FUNDING_API = "funding_api"
    JOB_BOARD_SCRAPER = "job_board_scraper"
    TECH_STACK_MONITOR = "tech_stack_monitor"


class RawSignal(BaseModel):
    """
    Unprocessed signal before LLM scoring.
    This is the input to the Scoring Gate.
    """
    channel: IngestionChannel
    company_name: str
    signal_type: str
    raw_data: Dict[str, Any]
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    source_url: Optional[HttpUrl] = None


class GitHubSignal(BaseModel):
    """GitHub webhook payload structure"""
    repo_name: str
    action: str  # "star", "fork", "new_repo", "commit"
    actor: str
    org: Optional[str] = None
    tech_stack: List[str] = []


class LinkedInSignal(BaseModel):
    """LinkedIn intent signal structure"""
    company: str
    signal_type: str  # "job_post", "exec_hire", "funding_announcement"
    content: str
    url: str
    detected_keywords: List[str] = []


class FundingSignal(BaseModel):
    """Funding database signal (Crunchbase, PitchBook)"""
    company: str
    round_type: str  # "Series A", "Series B", "IPO"
    amount: Optional[float] = None
    lead_investor: Optional[str] = None
    announced_date: datetime


def ingest_github_webhook(payload: Dict[str, Any]) -> RawSignal:
    """
    Process GitHub webhook for organizational signals.
    
    Detects:
    - New repository creation (potential new initiative)
    - Stars on security/infra repos (buying intent)
    - Engineering hiring velocity (team growth)
    
    This is how we detected NVIDIA's expansion at Fudo.
    """
    
    github_signal = GitHubSignal(
        repo_name=payload.get("repository", {}).get("name", "unknown"),
        action=payload.get("action", "unknown"),
        actor=payload.get("sender", {}).get("login", "unknown"),
        org=payload.get("organization", {}).get("login"),
        tech_stack=_extract_tech_stack(payload)
    )
    
    return RawSignal(
        channel=IngestionChannel.GITHUB_WEBHOOKS,
        company_name=github_signal.org or github_signal.actor,
        signal_type=f"GitHub {github_signal.action}",
        raw_data=github_signal.dict(),
        source_url=payload.get("repository", {}).get("html_url")
    )


def ingest_linkedin_signal(scraped_data: Dict[str, Any]) -> RawSignal:
    """
    Process LinkedIn scraper output for executive signals.
    
    Detects:
    - Job postings (hiring = budget availability)
    - Executive hires (new decision-makers)
    - Company updates (growth signals)
    
    This is the "Human Latency Killer" - detects intent 24-48 hrs
    before manual SDRs would notice it.
    """
    
    linkedin_signal = LinkedInSignal(
        company=scraped_data.get("company", "unknown"),
        signal_type=scraped_data.get("post_type", "general"),
        content=scraped_data.get("content", ""),
        url=scraped_data.get("url", ""),
        detected_keywords=_extract_intent_keywords(scraped_data.get("content", ""))
    )
    
    return RawSignal(
        channel=IngestionChannel.LINKEDIN_SCRAPER,
        company_name=linkedin_signal.company,
        signal_type=f"LinkedIn {linkedin_signal.signal_type}",
        raw_data=linkedin_signal.dict(),
        source_url=linkedin_signal.url
    )


def ingest_funding_alert(funding_data: Dict[str, Any]) -> RawSignal:
    """
    Process funding database alerts.
    
    Detects:
    - Series A/B rounds (new budget cycles)
    - IPO announcements (enterprise readiness)
    - Strategic acquisitions (new pain points)
    
    Funding = Intent. This is the highest-signal channel.
    """
    
    funding_signal = FundingSignal(
        company=funding_data.get("company", "unknown"),
        round_type=funding_data.get("round", "unknown"),
        amount=funding_data.get("amount"),
        lead_investor=funding_data.get("lead_investor"),
        announced_date=datetime.fromisoformat(funding_data.get("date", datetime.utcnow().isoformat()))
    )
    
    return RawSignal(
        channel=IngestionChannel.FUNDING_API,
        company_name=funding_signal.company,
        signal_type=f"Funding: {funding_signal.round_type}",
        raw_data=funding_signal.dict()
    )


def ingest_job_posting(job_data: Dict[str, Any]) -> RawSignal:
    """
    Process job board scraper output.
    
    Detects:
    - Security engineer roles (pain point evidence)
    - DevOps/SRE hiring (infrastructure investment)
    - Leadership hires (decision-maker changes)
    
    Job posts = Budget allocated. This validates ICP fit.
    """
    
    return RawSignal(
        channel=IngestionChannel.JOB_BOARD_SCRAPER,
        company_name=job_data.get("company", "unknown"),
        signal_type=f"Job Post: {job_data.get('title', 'unknown')}",
        raw_data=job_data,
        source_url=job_data.get("url")
    )


def _extract_tech_stack(github_payload: Dict[str, Any]) -> List[str]:
    """Extract technology signals from GitHub repo metadata"""
    languages = github_payload.get("repository", {}).get("language")
    topics = github_payload.get("repository", {}).get("topics", [])
    
    stack = []
    if languages:
        stack.append(languages)
    stack.extend(topics)
    
    return stack


def _extract_intent_keywords(content: str) -> List[str]:
    """
    Detect buying intent keywords in LinkedIn content.
    
    High-intent keywords: "hiring", "seeking", "looking for", "expanding",
    "funding", "series", "growth", "security", "infrastructure"
    """
    
    intent_keywords = [
        "hiring", "seeking", "looking for", "expanding", "growth",
        "funding", "series", "raised", "security", "infrastructure",
        "compliance", "enterprise", "scale", "team"
    ]
    
    content_lower = content.lower()
    detected = [kw for kw in intent_keywords if kw in content_lower]
    
    return detected


# Ingestion Engine Orchestrator
class IngestionEngine:
    """
    The Phase 1 (Machine) coordinator.
    
    Aggregates signals from all channels and prepares them for the Scoring Gate.
    This is the "anti-human-latency" layer that runs 24/7.
    """
    
    def __init__(self):
        self.active_channels = list(IngestionChannel)
        self.signal_buffer: List[RawSignal] = []
    
    def process_webhook(self, channel: IngestionChannel, payload: Dict[str, Any]) -> RawSignal:
        """Route incoming webhooks to appropriate ingestion handlers"""
        
        if channel == IngestionChannel.GITHUB_WEBHOOKS:
            signal = ingest_github_webhook(payload)
        elif channel == IngestionChannel.LINKEDIN_SCRAPER:
            signal = ingest_linkedin_signal(payload)
        elif channel == IngestionChannel.FUNDING_API:
            signal = ingest_funding_alert(payload)
        elif channel == IngestionChannel.JOB_BOARD_SCRAPER:
            signal = ingest_job_posting(payload)
        else:
            raise ValueError(f"Unknown channel: {channel}")
        
        self.signal_buffer.append(signal)
        return signal
    
    def flush_to_scoring(self) -> List[RawSignal]:
        """Send accumulated signals to the Scoring Gate"""
        signals = self.signal_buffer.copy()
        self.signal_buffer.clear()
        return signals


# Example usage
if __name__ == "__main__":
    engine = IngestionEngine()
    
    # Simulate GitHub webhook
    github_payload = {
        "action": "created",
        "repository": {
            "name": "kubernetes-security-platform",
            "html_url": "https://github.com/nvidia/k8s-sec",
            "language": "Python",
            "topics": ["security", "kubernetes", "devsecops"]
        },
        "organization": {"login": "NVIDIA"},
        "sender": {"login": "nvidia-security-team"}
    }
    
    signal1 = engine.process_webhook(IngestionChannel.GITHUB_WEBHOOKS, github_payload)
    print(f"\\n🎯 GitHub Signal Ingested:")
    print(f"Company: {signal1.company_name}")
    print(f"Type: {signal1.signal_type}")
    print(f"Tech Stack: {signal1.raw_data.get('tech_stack', [])}")
    
    # Simulate LinkedIn scrape
    linkedin_payload = {
        "company": "eBay",
        "post_type": "job_posting",
        "content": "We're hiring a Senior Security Engineer to expand our infrastructure team",
        "url": "https://linkedin.com/posts/ebay-security"
    }
    
    signal2 = engine.process_webhook(IngestionChannel.LINKEDIN_SCRAPER, linkedin_payload)
    print(f"\\n🎯 LinkedIn Signal Ingested:")
    print(f"Company: {signal2.company_name}")
    print(f"Type: {signal2.signal_type}")
    print(f"Intent Keywords: {signal2.raw_data.get('detected_keywords', [])}")
    
    # Flush to scoring
    ready_for_scoring = engine.flush_to_scoring()
    print(f"\\n✅ {len(ready_for_scoring)} signals ready for Scoring Gate")
