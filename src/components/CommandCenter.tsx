import React, { useMemo } from 'react';
import {
    WAR_ROOM_TARGETS,
    FRACTIONAL_DEALS,
    NETWORK_CONTACTS,
    FREEZER_ACCOUNTS,
    calculateMetrics,
    formatCurrency,
    getPriorityEmoji,
    getStatusColor
} from '../services/crmService';
import {
    Target, Users, Snowflake, Zap, ArrowRight,
    TrendingUp, AlertTriangle, Activity
} from 'lucide-react';

interface CommandCenterProps {
    addNotification: (type: 'SUCCESS' | 'ERROR' | 'INFO' | 'WARNING', msg: string, sub?: string) => void;
}

export const CommandCenter: React.FC<CommandCenterProps> = ({ addNotification }) => {
    const metrics = useMemo(() => calculateMetrics(), []);

    const getVelocityLabel = (velocity: number): string => {
        if (velocity >= 8) return 'Urgent';
        if (velocity >= 6) return 'Active';
        return 'Cold';
    };

    const getVelocityClass = (velocity: number): string => {
        if (velocity >= 8) return 'bg-red-500/20 text-red-400 border border-red-500/50';
        if (velocity >= 6) return 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/50';
        return 'bg-slate-500/20 text-slate-400 border border-slate-500/50';
    };

    const getPriorityColor = (priority: number): string => {
        switch (priority) {
            case 1: return '#ef4444';
            case 2: return '#f59e0b';
            case 3: return '#6b7280';
            default: return '#3b82f6';
        }
    };

    return (
        <div className="p-8 h-full flex flex-col bg-[#020617] relative animate-in fade-in duration-700 overflow-y-auto custom-scrollbar">
            {/* Header */}
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h2 className="text-5xl font-black text-white leading-none tracking-tighter uppercase">
                        Command <span className="text-[#D4AF37]">Center</span>
                    </h2>
                    <p className="text-[10px] text-slate-500 font-mono uppercase tracking-[0.5em] mt-3">
                        Executive GTM Operations // LeonOS CRM v11
                    </p>
                </div>
                <div className="flex gap-4">
                    <div className={`px-4 py-2 rounded-full text-xs font-black uppercase ${getVelocityClass(metrics.pipelineVelocity)}`}>
                        <Activity size={12} className="inline mr-2" />
                        {getVelocityLabel(metrics.pipelineVelocity)} Velocity
                    </div>
                </div>
            </div>

            {/* Metrics Row */}
            <div className="grid grid-cols-4 gap-4 mb-8">
                <div className="glass-panel p-6 rounded-2xl border border-slate-800">
                    <div className="flex items-center gap-3 mb-2">
                        <Target size={18} className="text-red-500" />
                        <span className="text-[9px] text-slate-500 uppercase font-black tracking-widest">War Room</span>
                    </div>
                    <div className="text-3xl font-mono font-bold text-white">{metrics.activeWarRoom}</div>
                    <div className="text-[10px] text-slate-600 mt-1">P1 Targets</div>
                </div>
                <div className="glass-panel p-6 rounded-2xl border border-[#D4AF37]/30 bg-[#D4AF37]/5">
                    <div className="flex items-center gap-3 mb-2">
                        <TrendingUp size={18} className="text-[#D4AF37]" />
                        <span className="text-[9px] text-[#D4AF37] uppercase font-black tracking-widest">Fractional MRR</span>
                    </div>
                    <div className="text-3xl font-mono font-bold text-[#D4AF37]">{formatCurrency(metrics.fractionalMRR)}</div>
                    <div className="text-[10px] text-slate-600 mt-1">Total Potential</div>
                </div>
                <div className="glass-panel p-6 rounded-2xl border border-emerald-500/30 bg-emerald-500/5">
                    <div className="flex items-center gap-3 mb-2">
                        <Zap size={18} className="text-emerald-400" />
                        <span className="text-[9px] text-emerald-400 uppercase font-black tracking-widest">Weighted</span>
                    </div>
                    <div className="text-3xl font-mono font-bold text-emerald-400">{formatCurrency(metrics.weightedPipeline)}</div>
                    <div className="text-[10px] text-slate-600 mt-1">Probability Adjusted</div>
                </div>
                <div className="glass-panel p-6 rounded-2xl border border-slate-800">
                    <div className="flex items-center gap-3 mb-2">
                        <Snowflake size={18} className="text-blue-400" />
                        <span className="text-[9px] text-slate-500 uppercase font-black tracking-widest">Freezer</span>
                    </div>
                    <div className="text-3xl font-mono font-bold text-slate-400">{metrics.zombieCount}</div>
                    <div className="text-[10px] text-slate-600 mt-1">Stalled Accounts</div>
                </div>
            </div>

            {/* Main Content */}
            <div className="flex-1 grid grid-cols-2 gap-6">
                {/* War Room */}
                <div className="glass-panel rounded-3xl border border-red-500/20 overflow-hidden">
                    <div className="p-6 border-b border-slate-800 bg-red-500/10 flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <Target size={20} className="text-red-500" />
                            <h3 className="text-lg font-black text-white uppercase tracking-tight">War Room</h3>
                        </div>
                        <span className="text-[9px] text-red-400 font-mono uppercase">Active Combat</span>
                    </div>
                    <div className="p-4 space-y-3 max-h-[400px] overflow-y-auto custom-scrollbar">
                        {WAR_ROOM_TARGETS.map(target => (
                            <div
                                key={target.id}
                                className="p-4 bg-slate-900/60 rounded-xl border border-slate-800 hover:border-slate-600 transition-all cursor-pointer group"
                                onClick={() => addNotification('INFO', `${target.company}`, target.nextMove)}
                            >
                                <div className="flex justify-between items-start mb-3">
                                    <div className="flex items-center gap-2">
                                        <span
                                            className="px-2 py-0.5 rounded text-[8px] font-black"
                                            style={{ backgroundColor: `${getPriorityColor(target.priority)}20`, color: getPriorityColor(target.priority), border: `1px solid ${getPriorityColor(target.priority)}50` }}
                                        >
                                            {getPriorityEmoji(target.priority)} P{target.priority}
                                        </span>
                                        <span
                                            className="px-2 py-0.5 rounded text-[8px] font-black"
                                            style={{ backgroundColor: `${getStatusColor(target.status)}20`, color: getStatusColor(target.status) }}
                                        >
                                            {target.status}
                                        </span>
                                    </div>
                                </div>
                                <h4 className="text-sm font-black text-white uppercase tracking-tight mb-1">{target.company}</h4>
                                <p className="text-[10px] text-[#D4AF37] font-mono mb-1">{target.role}</p>
                                <p className="text-[9px] text-slate-500 mb-2">Gatekeeper: {target.gatekeeper}</p>
                                <div className="flex items-center gap-2 text-[10px] text-slate-500">
                                    <ArrowRight size={10} className="text-emerald-500" />
                                    <span className="truncate">{target.nextMove}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Fractional Pipeline */}
                <div className="glass-panel rounded-3xl border border-[#D4AF37]/20 overflow-hidden">
                    <div className="p-6 border-b border-slate-800 bg-[#D4AF37]/10 flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <TrendingUp size={20} className="text-[#D4AF37]" />
                            <h3 className="text-lg font-black text-white uppercase tracking-tight">Fractional Pipeline</h3>
                        </div>
                        <span className="text-[9px] text-[#D4AF37] font-mono uppercase">~$18k/mo Potential</span>
                    </div>
                    <div className="p-4 space-y-3 max-h-[400px] overflow-y-auto custom-scrollbar">
                        {FRACTIONAL_DEALS.map(deal => (
                            <div
                                key={deal.id}
                                className="p-4 bg-slate-900/60 rounded-xl border border-slate-800 hover:border-slate-600 transition-all"
                            >
                                <div className="flex justify-between items-start mb-3">
                                    <h4 className="text-sm font-black text-white uppercase tracking-tight">{deal.client}</h4>
                                    <span className="text-lg font-mono font-bold text-[#D4AF37]">{formatCurrency(deal.monthlyValue)}/mo</span>
                                </div>
                                <div className="flex items-center justify-between mb-3">
                                    <span className="text-[9px] text-slate-500 uppercase font-black">{deal.status}</span>
                                    <span className="text-xs font-mono text-slate-400">{deal.probability}% prob</span>
                                </div>
                                {/* Progress bar */}
                                <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden mb-2">
                                    <div
                                        className="h-full bg-gradient-to-r from-[#D4AF37] to-yellow-500 rounded-full transition-all"
                                        style={{ width: `${deal.probability}%` }}
                                    />
                                </div>
                                <div className="flex items-center gap-2 text-[10px] text-slate-500">
                                    <ArrowRight size={10} className="text-emerald-500" />
                                    <span>{deal.nextStep}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Network Champions */}
                <div className="glass-panel rounded-3xl border border-purple-500/20 overflow-hidden">
                    <div className="p-6 border-b border-slate-800 bg-purple-500/10 flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <Users size={20} className="text-purple-400" />
                            <h3 className="text-lg font-black text-white uppercase tracking-tight">Network Champions</h3>
                        </div>
                        <span className="text-[9px] text-purple-400 font-mono uppercase">{NETWORK_CONTACTS.filter(c => c.isChampion).length} Champions</span>
                    </div>
                    <div className="p-4 space-y-2">
                        {NETWORK_CONTACTS.filter(c => c.isChampion).map(contact => (
                            <div
                                key={contact.id}
                                className="p-3 bg-slate-900/60 rounded-xl border border-slate-800 flex items-center justify-between"
                            >
                                <div>
                                    <h4 className="text-sm font-bold text-white">{contact.name}</h4>
                                    <p className="text-[10px] text-slate-500">{contact.company} • {contact.valueExchanged}</p>
                                </div>
                                <div className="text-right">
                                    <span className="px-2 py-0.5 rounded text-[8px] font-black bg-purple-500/20 text-purple-400">
                                        ⭐ CHAMPION
                                    </span>
                                    <p className="text-[9px] text-slate-600 mt-1">{contact.relationshipStrength}% strength</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Freezer Summary */}
                <div className="glass-panel rounded-3xl border border-blue-500/20 overflow-hidden">
                    <div className="p-6 border-b border-slate-800 bg-blue-500/10 flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <Snowflake size={20} className="text-blue-400" />
                            <h3 className="text-lg font-black text-white uppercase tracking-tight">Freezer</h3>
                        </div>
                        <span className="text-[9px] text-blue-400 font-mono uppercase flex items-center gap-2">
                            <AlertTriangle size={10} /> Do Not Spend Prime Time
                        </span>
                    </div>
                    <div className="p-4 space-y-2 max-h-[200px] overflow-y-auto custom-scrollbar">
                        {FREEZER_ACCOUNTS.map(account => (
                            <div
                                key={account.id}
                                className="p-3 bg-slate-900/60 rounded-xl border border-slate-800 flex items-center justify-between opacity-60"
                            >
                                <div>
                                    <h4 className="text-sm font-bold text-slate-400">{account.company}</h4>
                                    <p className="text-[9px] text-slate-600">{account.daysCold} days cold</p>
                                </div>
                                <span className="text-[8px] text-slate-500 uppercase font-mono">{account.verdict}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};
