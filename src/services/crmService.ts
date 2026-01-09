/**
 * Basin::Nexus CRM Service
 * TypeScript service for CRM data - synced with LeonOS Master State
 * Updated: January 9, 2026
 */

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

export interface WarRoomTarget {
    id: string;
    company: string;
    role: string;
    gatekeeper: string;
    priority: number; // 1 = P1, 2 = P2
    status: 'FINALIST' | 'ACTIVE' | 'REFERRAL' | 'ADVANCING';
    nextMove: string;
    lastActivity: Date;
    signalStrength: number; // 0-100
    velocityScore: number; // 0-10
    notes?: string;
}

export interface PipelineTarget {
    id: string;
    company: string;
    role: string;
    priority: number;
    status: string;
    nextStep: string;
    notes?: string;
}

export interface FractionalDeal {
    id: string;
    client: string;
    monthlyValue: number;
    probability: number; // 0-100
    status: 'Active' | 'Proposal' | 'Initial Call' | 'Scoping';
    nextStep: string;
    scope?: string;
    contractType?: string;
}

export interface FreezerAccount {
    id: string;
    company: string;
    lastSignal: Date;
    daysCold: number;
    verdict: string;
    reactivationStrategy?: string;
}

export interface NetworkContact {
    id: string;
    name: string;
    company: string;
    relationshipStrength: number;
    lastInteraction: Date;
    valueExchanged?: string;
    nextTouchpoint?: string;
    isChampion: boolean;
}

export interface CommandCenterMetrics {
    activeWarRoom: number;
    fractionalMRR: number;
    weightedPipeline: number;
    zombieCount: number;
    pipelineVelocity: number;
    lastUpdated: Date;
}

// ============================================================================
// 1. THE WAR ROOM (Active Combat)
// ============================================================================

export const WAR_ROOM_TARGETS: WarRoomTarget[] = [
    {
        id: 'wr-liveramp',
        company: 'LiveRamp',
        role: 'Lead PMM',
        gatekeeper: 'Tammy (HM)',
        priority: 1,
        status: 'FINALIST',
        nextMove: "Wait: Tammy advancing you to Samantha Lopez (Marketplace/Commercial). 'Insurance Policy' narrative landed.",
        lastActivity: new Date('2026-01-09T10:00:00'),
        signalStrength: 95,
        velocityScore: 9.5,
        notes: 'Multiple rounds complete. Final decision stage. Samantha Lopez intro pending.'
    },
    {
        id: 'wr-fastino',
        company: 'Fastino',
        role: 'Founding Sales',
        gatekeeper: 'Allison/Founders',
        priority: 1,
        status: 'ACTIVE',
        nextMove: "Wait: Sent 'Agentic Architecture' to George & Ash. Used LiveRamp as leverage to force urgency.",
        lastActivity: new Date('2026-01-09T09:30:00'),
        signalStrength: 88,
        velocityScore: 8.5,
        notes: 'Founders engaged. Agentic Architecture deck deployed. LiveRamp leverage play active.'
    },
    {
        id: 'wr-okta',
        company: 'Okta',
        role: 'Tech PMM',
        gatekeeper: 'Anthony Walsh',
        priority: 1,
        status: 'REFERRAL',
        nextMove: "Wait: Anthony is vouching for you with the team. 'Playdate' bond secured.",
        lastActivity: new Date('2026-01-09T12:00:00'),
        signalStrength: 85,
        velocityScore: 8.0,
        notes: 'Warm referral from Anthony Walsh. Personal connection established.'
    },
    {
        id: 'wr-quantumscape',
        company: 'QuantumScape',
        role: 'PMM',
        gatekeeper: 'Smita',
        priority: 1,
        status: 'ADVANCING',
        nextMove: "Drafting: Creating the 'Translation Layer' brief Smita requested.",
        lastActivity: new Date('2026-01-09T08:00:00'),
        signalStrength: 78,
        velocityScore: 7.5,
        notes: 'Smita requested Translation Layer brief. Actively engaged.'
    },
    {
        id: 'wr-sendbird',
        company: 'Sendbird',
        role: 'SDR Manager',
        gatekeeper: 'Peter/Charles',
        priority: 2,
        status: 'ADVANCING',
        nextMove: "Monitor: Sent 'SDR Transition Playbook' to Peter. Awaiting feedback.",
        lastActivity: new Date('2026-01-08T16:00:00'),
        signalStrength: 72,
        velocityScore: 7.0,
        notes: 'SDR Transition Playbook deployed. Peter reviewing.'
    }
];

// ============================================================================
// 2. THE PIPELINE (Screening & Backups)
// ============================================================================

export const PIPELINE_TARGETS: PipelineTarget[] = [
    {
        id: 'pl-mastech',
        company: 'Mastech',
        role: 'Sales Lead',
        priority: 2,
        status: 'Screening',
        nextStep: "Call Monday: Confirmed $320k+ OTE. 'Hunter' profile.",
        notes: 'High OTE confirmed. Strong backup option.'
    },
    {
        id: 'pl-variacode',
        company: 'Variacode',
        role: 'Sales',
        priority: 3,
        status: 'Screening',
        nextStep: "Pending: Sent 'Comp/JD' filter email.",
        notes: 'Awaiting comp/JD details. Low priority.'
    },
    {
        id: 'pl-nvidia',
        company: 'NVIDIA',
        role: 'DevRel',
        priority: 3,
        status: 'Referral',
        nextStep: 'Check: Confirm Minh Pham submitted the formal referral.',
        notes: 'Minh Pham referral pending confirmation.'
    }
];

// ============================================================================
// 3. FRACTIONAL PIPELINE (~$18k/mo Potential)
// ============================================================================

export const FRACTIONAL_DEALS: FractionalDeal[] = [
    {
        id: 'frac-fym',
        client: 'FYM Partners',
        monthlyValue: 5000,
        probability: 70,
        status: 'Active',
        nextStep: 'Deliver Tiered System Doc.',
        scope: 'GTM Strategy + Sales Process Optimization',
        contractType: 'Retainer'
    },
    {
        id: 'frac-nexusai',
        client: 'Nexus AI',
        monthlyValue: 2500,
        probability: 60,
        status: 'Proposal',
        nextStep: 'Finalize Scope of Work.',
        scope: 'Product Marketing Strategy',
        contractType: 'Project'
    },
    {
        id: 'frac-techflow',
        client: 'TechFlow',
        monthlyValue: 1500,
        probability: 50,
        status: 'Initial Call',
        nextStep: 'Send Project Outline.',
        scope: 'Sales Enablement',
        contractType: 'Project'
    },
    {
        id: 'frac-solvejet',
        client: 'SolveJet',
        monthlyValue: 3000,
        probability: 40,
        status: 'Proposal',
        nextStep: 'Follow up on Contract.',
        scope: 'Enterprise Pipeline Development',
        contractType: 'Retainer'
    },
    {
        id: 'frac-spray',
        client: 'Spray.io',
        monthlyValue: 2000,
        probability: 30,
        status: 'Scoping',
        nextStep: 'Define Deliverables.',
        scope: 'Outbound Strategy',
        contractType: 'Project'
    }
];

// ============================================================================
// 4. THE FREEZER (Stalled / Low Signal)
// ============================================================================

export const FREEZER_ACCOUNTS: FreezerAccount[] = [
    {
        id: 'frz-snapmagic',
        company: 'SnapMagic',
        lastSignal: new Date('2025-11-20'),
        daysCold: 50,
        verdict: "Purge or 'Hail Mary' to Ryan",
        reactivationStrategy: 'Final Hail Mary email to Ryan, then archive'
    },
    {
        id: 'frz-aikido',
        company: 'Aikido Security',
        lastSignal: new Date('2025-11-25'),
        daysCold: 45,
        verdict: 'Archive',
        reactivationStrategy: 'None - Archive'
    },
    {
        id: 'frz-hightouch',
        company: 'Hightouch',
        lastSignal: new Date('2025-11-21'),
        daysCold: 49,
        verdict: 'Dead',
        reactivationStrategy: 'None - Dead'
    },
    {
        id: 'frz-mistral',
        company: 'Mistral',
        lastSignal: new Date('2025-11-21'),
        daysCold: 49,
        verdict: 'Dead',
        reactivationStrategy: 'None - Dead'
    },
    {
        id: 'frz-skypoint',
        company: 'Skypoint',
        lastSignal: new Date('2025-12-04'),
        daysCold: 36,
        verdict: 'One final bump, then archive',
        reactivationStrategy: "'Zero Trust' pitch sent Dec 4. One final bump."
    }
];

// ============================================================================
// 5. NETWORK CHAMPIONS
// ============================================================================

export const NETWORK_CONTACTS: NetworkContact[] = [
    {
        id: 'net-anthony',
        name: 'Anthony Walsh',
        company: 'Okta',
        relationshipStrength: 95,
        lastInteraction: new Date('2026-01-09'),
        valueExchanged: 'Okta team intro + vouching',
        nextTouchpoint: "Monitor for 'Coffee' text or team intro",
        isChampion: true
    },
    {
        id: 'net-minh',
        name: 'Minh Pham',
        company: 'NVIDIA',
        relationshipStrength: 80,
        lastInteraction: new Date('2026-01-06'),
        valueExchanged: 'NVIDIA referral pending',
        nextTouchpoint: 'Confirm formal referral submitted',
        isChampion: true
    },
    {
        id: 'net-smita',
        name: 'Smita',
        company: 'QuantumScape',
        relationshipStrength: 75,
        lastInteraction: new Date('2026-01-09'),
        valueExchanged: 'Translation Layer brief request',
        nextTouchpoint: 'Deliver Translation Layer brief',
        isChampion: true
    },
    {
        id: 'net-samantha',
        name: 'Samantha Lopez',
        company: 'LiveRamp',
        relationshipStrength: 70,
        lastInteraction: new Date('2026-01-09'),
        valueExchanged: 'Marketplace/Commercial intro pending',
        nextTouchpoint: 'Await intro from Tammy',
        isChampion: true
    },
    {
        id: 'net-ryan',
        name: 'Ryan Richardson',
        company: 'SnapMagic',
        relationshipStrength: 65,
        lastInteraction: new Date('2025-11-20'),
        valueExchanged: 'Previous engagement',
        nextTouchpoint: 'Hail Mary email if SnapMagic worth pursuing',
        isChampion: false
    }
];

// ============================================================================
// METRICS CALCULATION
// ============================================================================

export function calculateMetrics(): CommandCenterMetrics {
    const activeWarRoom = WAR_ROOM_TARGETS.filter(t => t.priority === 1).length;
    const fractionalMRR = FRACTIONAL_DEALS.reduce((sum, d) => sum + d.monthlyValue, 0);
    const weightedPipeline = FRACTIONAL_DEALS.reduce(
        (sum, d) => sum + (d.monthlyValue * d.probability / 100), 0
    );
    const zombieCount = FREEZER_ACCOUNTS.length;
    const avgVelocity = WAR_ROOM_TARGETS.reduce((sum, t) => sum + t.velocityScore, 0) / WAR_ROOM_TARGETS.length;

    return {
        activeWarRoom,
        fractionalMRR,
        weightedPipeline,
        zombieCount,
        pipelineVelocity: avgVelocity,
        lastUpdated: new Date()
    };
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

export function formatCurrency(value: number): string {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value);
}

export function getStatusColor(status: string): string {
    const colors: Record<string, string> = {
        FINALIST: '#10b981',    // Green
        ACTIVE: '#f59e0b',      // Orange
        REFERRAL: '#8b5cf6',    // Purple
        ADVANCING: '#3b82f6',   // Blue
        Active: '#10b981',
        Proposal: '#f59e0b',
        'Initial Call': '#3b82f6',
        Scoping: '#6b7280'
    };
    return colors[status] || '#6b7280';
}

export function getPriorityEmoji(priority: number): string {
    switch (priority) {
        case 1: return '🚨';
        case 2: return '🟡';
        case 3: return '⚪';
        default: return '❄️';
    }
}

// ============================================================================
// WEEKEND PROTOCOL
// ============================================================================

export const WEEKEND_PROTOCOL = {
    monitor: "Watch for Anthony's 'Okta Intro' or 'Coffee' text.",
    build: "Get your first n8n workflow live (e.g., 'Email to Slack').",
    rest: "You have 3 major deals (LiveRamp, Fastino, Okta) in the 'Red Zone.' Clear your head for closing week."
};
