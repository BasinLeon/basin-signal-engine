/**
 * Basin::Nexus CRM Service
 * TypeScript service for managing War Room, Fractional Pipeline, and Network data
 */

// Types matching Python models
export interface WarRoomTarget {
    id: string;
    company: string;
    role: string;
    priority: 'P1' | 'P2' | 'P3' | 'COLD';
    status: 'URGENT' | 'ACTIVE' | 'WAITING' | 'REFERRAL' | 'PROPOSAL' | 'SCOPING' | 'LEAD' | 'STALLED' | 'DEAD';
    contactName?: string;
    contactPhone?: string;
    nextMove: string;
    lastActivity: string;
    notes?: string;
}

export interface FractionalDeal {
    id: string;
    client: string;
    monthlyValue: number;
    probability: number; // 0.0 - 1.0
    status: string;
    nextStep: string;
    lastActivity: string;
    notes?: string;
}

export interface FreezerAccount {
    id: string;
    company: string;
    lastActivity: string;
    stalledSince: string;
    verdict: string;
    notes?: string;
}

export interface NetworkContact {
    id: string;
    name: string;
    company: string;
    tier: 'CHAMPION' | 'TIER_1' | 'TIER_2' | 'REVIVAL';
    relationship: string;
    lastContact?: string;
    nextAction?: string;
    notes?: string;
}

export interface CommandCenterMetrics {
    activeWarRoom: number;
    fractionalMRR: number;
    weightedPipeline: number;
    networkHeat: 'High' | 'Medium' | 'Low';
    zombieCount: number;
    pipelineVelocity: 'Urgent' | 'Active' | 'Cold';
}

// Seeded data matching Python core/crm/data.py - REAL-TIME as of Jan 9, 2026
export const WAR_ROOM_TARGETS: WarRoomTarget[] = [
    {
        id: 'wr-001',
        company: 'LiveRamp',
        role: 'Lead PMM',
        priority: 'P1',
        status: 'URGENT',
        contactName: 'Samantha Lopez',
        nextMove: "Execute 'Insurance Policy' - awaiting schedule with Samantha",
        lastActivity: new Date().toISOString(),
        notes: 'FINALIST STAGE - Career-defining opportunity.'
    },
    {
        id: 'wr-002',
        company: 'Fastino',
        role: 'Founding Sales',
        priority: 'P1',
        status: 'ACTIVE',
        contactName: 'Allison → George/Ash (Founders)',
        nextMove: "Sent 'Agentic Architecture' to Allison for Founders",
        lastActivity: new Date().toISOString(),
        notes: 'Founder sync pending. High priority.'
    },
    {
        id: 'wr-003',
        company: 'QuantumScape',
        role: 'PMM',
        priority: 'P1',
        status: 'ACTIVE',
        contactName: 'Smita',
        contactPhone: '408-849-2907',
        nextMove: "Draft 'Translation Layer' brief requested by Smita",
        lastActivity: new Date().toISOString(),
        notes: 'ADVANCING - Spoke Jan 8, discussed Internal Agent concept.'
    },
    {
        id: 'wr-004',
        company: 'Sendbird',
        role: 'SDR Manager',
        priority: 'P2',
        status: 'ACTIVE',
        contactName: 'Peter / Charles',
        nextMove: "Monitor: Sent 'SDR Transition Playbook' to Peter",
        lastActivity: new Date().toISOString(),
        notes: 'ADVANCING - Awaiting feedback on PDF artifacts.'
    },
];

export const FRACTIONAL_DEALS: FractionalDeal[] = [
    { id: 'frac-001', client: 'FYM Partners', monthlyValue: 5000, probability: 0.70, status: 'ACTIVE', nextStep: 'Deliver Tiered System Doc', lastActivity: new Date().toISOString(), notes: 'High confidence close' },
    { id: 'frac-002', client: 'Nexus AI', monthlyValue: 2500, probability: 0.60, status: 'PROPOSAL', nextStep: 'Finalize Scope of Work', lastActivity: new Date().toISOString() },
    { id: 'frac-003', client: 'TechFlow', monthlyValue: 1500, probability: 0.50, status: 'SCOPING', nextStep: 'Send Project Outline', lastActivity: new Date().toISOString(), notes: 'Initial call completed' },
    { id: 'frac-004', client: 'SolveJet', monthlyValue: 3000, probability: 0.40, status: 'PROPOSAL', nextStep: 'Follow up on Contract', lastActivity: new Date().toISOString() },
    { id: 'frac-005', client: 'Spray.io', monthlyValue: 2000, probability: 0.30, status: 'SCOPING', nextStep: 'Define Deliverables', lastActivity: new Date().toISOString() },
    { id: 'frac-006', client: 'AlphaCorp', monthlyValue: 4000, probability: 0.20, status: 'LEAD', nextStep: 'Schedule Discovery', lastActivity: new Date().toISOString() },
];

export const FREEZER_ACCOUNTS: FreezerAccount[] = [
    { id: 'freeze-001', company: 'SnapMagic', lastActivity: '2025-11-20', stalledSince: '2025-11-20', verdict: "Purge or 'Hail Mary' to Ryan" },
    { id: 'freeze-002', company: 'Aikido Security', lastActivity: '2025-11-15', stalledSince: '2025-11-15', verdict: 'Archive' },
    { id: 'freeze-003', company: 'Hightouch', lastActivity: '2025-11-21', stalledSince: '2025-11-21', verdict: 'Dead' },
    { id: 'freeze-004', company: 'Mistral', lastActivity: '2025-11-21', stalledSince: '2025-11-21', verdict: 'Dead' },
    { id: 'freeze-005', company: 'Andromeda', lastActivity: '2025-11-21', stalledSince: '2025-11-21', verdict: 'Dead' },
    { id: 'freeze-006', company: 'Skypoint', lastActivity: '2025-12-04', stalledSince: '2025-12-04', verdict: 'One final bump, then archive' },
    { id: 'freeze-007', company: 'Verkada', lastActivity: '2025-11-10', stalledSince: '2025-11-10', verdict: 'Archive' },
    { id: 'freeze-008', company: 'LinkedIn', lastActivity: '2025-11-08', stalledSince: '2025-11-08', verdict: 'Archive' },
];

export const NETWORK_CONTACTS: NetworkContact[] = [
    { id: 'net-001', name: 'Ryan Richardson', company: 'SnapMagic / Source', tier: 'CHAMPION', relationship: 'Referral Source', notes: 'Top champion' },
    { id: 'net-002', name: 'Minh Pham', company: 'NVIDIA', tier: 'CHAMPION', relationship: 'Direct Referral', nextAction: 'Confirm referral submitted', notes: 'NVIDIA pathway' },
    { id: 'net-003', name: 'Oliver Perry', company: 'Trust in Soda', tier: 'CHAMPION', relationship: 'Strategic Partner', notes: 'Successfully re-engaged' },
    { id: 'net-004', name: 'Ed Carr', company: 'Elite Cyber GTM', tier: 'REVIVAL', relationship: 'Revival', notes: 'Re-engaged with Reg + AI pitch' },
    { id: 'net-005', name: 'Samantha Lopez', company: 'LiveRamp', tier: 'TIER_1', relationship: 'Decision Maker', nextAction: 'Execute Insurance Policy play', notes: 'Critical relationship for P1 deal' },
];

// Computed metrics
export function getCommandCenterMetrics(): CommandCenterMetrics {
    const totalMRR = FRACTIONAL_DEALS.reduce((acc, d) => acc + d.monthlyValue, 0);
    const weightedPipeline = FRACTIONAL_DEALS.reduce((acc, d) => acc + (d.monthlyValue * d.probability), 0);
    const champions = NETWORK_CONTACTS.filter(c => c.tier === 'CHAMPION').length;

    return {
        activeWarRoom: WAR_ROOM_TARGETS.length,
        fractionalMRR: totalMRR,
        weightedPipeline: weightedPipeline,
        networkHeat: champions >= 3 ? 'High' : 'Medium',
        zombieCount: FREEZER_ACCOUNTS.length,
        pipelineVelocity: WAR_ROOM_TARGETS.length >= 3 ? 'Urgent' : WAR_ROOM_TARGETS.length >= 1 ? 'Active' : 'Cold'
    };
}

// Format helpers
export function formatCurrency(value: number): string {
    return `$${value.toLocaleString()}`;
}

export function formatMRR(value: number): string {
    return `$${value.toLocaleString()}/mo`;
}

export function getPriorityColor(priority: string): string {
    switch (priority) {
        case 'P1': return '#ef4444'; // red
        case 'P2': return '#f59e0b'; // amber  
        case 'P3': return '#10b981'; // green
        default: return '#64748b';   // slate
    }
}

export function getStatusColor(status: string): string {
    switch (status) {
        case 'URGENT': return '#ef4444';
        case 'ACTIVE': return '#10b981';
        case 'WAITING': return '#f59e0b';
        case 'REFERRAL': return '#8b5cf6';
        case 'PROPOSAL': return '#00E5FF';
        default: return '#64748b';
    }
}
