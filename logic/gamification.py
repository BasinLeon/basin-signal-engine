"""
BASIN::NEXUS - Gamification & Market Timing Module
═══════════════════════════════════════════════════════════════════════════════

Part of Basin::Nexus v1.0 Executive OS

FEATURES:
✅ Achievement Badges (Progress milestones)
✅ Daily Streaks (Consistency tracking)
✅ Market Timing Intelligence (Holidays, best days to apply)
✅ Motivational Quotes & Session Stats

Protocol: Build → Use → Win → Prove
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# ═══════════════════════════════════════════════════════════════
# MARKET TIMING INTELLIGENCE
# ═══════════════════════════════════════════════════════════════

def get_market_context() -> Dict:
    """
    Returns current market timing context for job hunting.
    Considers: day of week, time of day, holidays, month, quarter.
    """
    now = datetime.now()
    day_of_week = now.weekday()  # 0=Monday, 6=Sunday
    hour = now.hour
    month = now.month
    day = now.day
    
    # US Federal Holidays (2024-2025)
    holidays = {
        (1, 1): "New Year's Day",
        (1, 15): "MLK Day",
        (2, 19): "Presidents' Day",
        (5, 27): "Memorial Day",
        (7, 4): "Independence Day",
        (9, 2): "Labor Day",
        (10, 14): "Columbus Day",
        (11, 11): "Veterans Day",
        (11, 28): "Thanksgiving",
        (11, 29): "Day after Thanksgiving",
        (12, 24): "Christmas Eve",
        (12, 25): "Christmas",
        (12, 26): "Day after Christmas",
        (12, 31): "New Year's Eve",
    }
    
    # Check if today is a holiday
    is_holiday = (month, day) in holidays
    holiday_name = holidays.get((month, day), None)
    
    # Holiday period detection
    is_holiday_period = month == 12 and day >= 20 or month == 1 and day <= 5
    
    # Best times to apply
    # Research shows: Tuesday-Thursday, 6am-10am are optimal
    is_optimal_day = day_of_week in [1, 2, 3]  # Tue, Wed, Thu
    is_optimal_time = 6 <= hour <= 10
    
    # Quarter timing
    quarter = (month - 1) // 3 + 1
    is_q1_hiring_surge = month in [1, 2, 3]  # New budget
    is_q4_slowdown = month in [11, 12]  # Holiday slowdown
    
    # Scoring
    timing_score = 50  # Base
    
    if is_holiday:
        timing_score -= 40
    elif is_holiday_period:
        timing_score -= 25
    
    if is_optimal_day:
        timing_score += 20
    if is_optimal_time:
        timing_score += 15
    
    if day_of_week in [5, 6]:  # Weekend
        timing_score -= 20
    
    if is_q1_hiring_surge:
        timing_score += 15
    elif is_q4_slowdown:
        timing_score -= 15
    
    timing_score = max(0, min(100, timing_score))
    
    # Recommendations
    recommendations = []
    
    if is_holiday:
        recommendations.append(f"🎄 Today is {holiday_name}. Most recruiters are off. Use this time to PRACTICE, not apply.")
    
    if is_holiday_period:
        recommendations.append("📅 We're in the holiday period. Focus on prep now, apply heavily Jan 6+.")
    
    if day_of_week in [5, 6]:
        recommendations.append("📆 Weekend detected. Applications sent today may get buried. Prep now, send Monday.")
    
    if day_of_week == 0:  # Monday
        recommendations.append("📩 Monday: Inboxes are flooded. Consider sending Tue-Thu for better visibility.")
    
    if not is_optimal_time and 6 <= hour <= 22:
        recommendations.append(f"⏰ Best application time is 6-10am local. Consider scheduling sends.")
    
    if is_q1_hiring_surge:
        recommendations.append("🚀 Q1 Hiring Surge! Companies have fresh budgets. Apply aggressively.")
    
    if not recommendations:
        recommendations.append("✅ Good timing! The market is active. Focus on quality applications.")
    
    # Get timing label
    if timing_score >= 80:
        timing_label = "🟢 OPTIMAL"
    elif timing_score >= 60:
        timing_label = "🟡 GOOD"
    elif timing_score >= 40:
        timing_label = "🟠 MODERATE"
    else:
        timing_label = "🔴 SLOW"
    
    return {
        "score": timing_score,
        "label": timing_label,
        "is_holiday": is_holiday,
        "holiday_name": holiday_name,
        "is_holiday_period": is_holiday_period,
        "is_optimal_day": is_optimal_day,
        "is_optimal_time": is_optimal_time,
        "is_weekend": day_of_week in [5, 6],
        "day_name": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][day_of_week],
        "quarter": quarter,
        "recommendations": recommendations,
        "action": "PRACTICE" if timing_score < 50 else "APPLY"
    }


# ═══════════════════════════════════════════════════════════════
# ACHIEVEMENT BADGES SYSTEM
# ═══════════════════════════════════════════════════════════════

BADGES = {
    # Practice Badges
    "first_blood": {
        "name": "First Blood",
        "icon": "🩸",
        "description": "Complete your first practice session",
        "requirement": {"sessions": 1}
    },
    "five_sessions": {
        "name": "Warming Up",
        "icon": "🔥",
        "description": "Complete 5 practice sessions",
        "requirement": {"sessions": 5}
    },
    "ten_sessions": {
        "name": "Getting Serious",
        "icon": "💪",
        "description": "Complete 10 practice sessions",
        "requirement": {"sessions": 10}
    },
    "twenty_sessions": {
        "name": "Interview Warrior",
        "icon": "⚔️",
        "description": "Complete 20 practice sessions",
        "requirement": {"sessions": 20}
    },
    "fifty_sessions": {
        "name": "Legend",
        "icon": "👑",
        "description": "Complete 50 practice sessions",
        "requirement": {"sessions": 50}
    },
    
    # Score Badges
    "score_70": {
        "name": "Solid Foundation",
        "icon": "🎯",
        "description": "Score 70+ on a practice session",
        "requirement": {"min_score": 70}
    },
    "score_80": {
        "name": "Sharpshooter",
        "icon": "🏹",
        "description": "Score 80+ on a practice session",
        "requirement": {"min_score": 80}
    },
    "score_90": {
        "name": "Elite",
        "icon": "💎",
        "description": "Score 90+ on a practice session",
        "requirement": {"min_score": 90}
    },
    "score_95": {
        "name": "Perfect Answer",
        "icon": "🌟",
        "description": "Score 95+ on a practice session",
        "requirement": {"min_score": 95}
    },
    
    # Streak Badges
    "streak_3": {
        "name": "Consistency",
        "icon": "📅",
        "description": "Practice 3 days in a row",
        "requirement": {"streak": 3}
    },
    "streak_7": {
        "name": "Week Warrior",
        "icon": "🗓️",
        "description": "Practice 7 days in a row",
        "requirement": {"streak": 7}
    },
    "streak_14": {
        "name": "Unstoppable",
        "icon": "⚡",
        "description": "Practice 14 days in a row",
        "requirement": {"streak": 14}
    },
    "streak_30": {
        "name": "Legendary",
        "icon": "🏆",
        "description": "Practice 30 days in a row",
        "requirement": {"streak": 30}
    },
    
    # Special Badges
    "nightmare_survivor": {
        "name": "Nightmare Survivor",
        "icon": "💀",
        "description": "Complete a Nightmare difficulty session",
        "requirement": {"difficulty": "Nightmare"}
    },
    "cro_approved": {
        "name": "CRO Approved",
        "icon": "📈",
        "description": "Score 80+ with Marcus (CRO)",
        "requirement": {"persona": "Marcus", "min_score": 80}
    },
    "star_master": {
        "name": "STAR Master",
        "icon": "⭐",
        "description": "Get all 4 STAR elements in 5 sessions",
        "requirement": {"perfect_star_count": 5}
    },
    "conviction_king": {
        "name": "Conviction King",
        "icon": "💪",
        "description": "Score 80+ conviction in 3 sessions",
        "requirement": {"high_conviction_count": 3}
    },
}


def get_user_badges(stats: Dict) -> List[Dict]:
    """Check which badges the user has earned based on their stats."""
    earned = []
    
    total_sessions = stats.get("total_sessions", 0)
    max_score = stats.get("max_score", 0)
    current_streak = stats.get("current_streak", 0)
    
    # Check each badge
    if total_sessions >= 1:
        earned.append(BADGES["first_blood"])
    if total_sessions >= 5:
        earned.append(BADGES["five_sessions"])
    if total_sessions >= 10:
        earned.append(BADGES["ten_sessions"])
    if total_sessions >= 20:
        earned.append(BADGES["twenty_sessions"])
    if total_sessions >= 50:
        earned.append(BADGES["fifty_sessions"])
    
    if max_score >= 70:
        earned.append(BADGES["score_70"])
    if max_score >= 80:
        earned.append(BADGES["score_80"])
    if max_score >= 90:
        earned.append(BADGES["score_90"])
    if max_score >= 95:
        earned.append(BADGES["score_95"])
    
    if current_streak >= 3:
        earned.append(BADGES["streak_3"])
    if current_streak >= 7:
        earned.append(BADGES["streak_7"])
    if current_streak >= 14:
        earned.append(BADGES["streak_14"])
    if current_streak >= 30:
        earned.append(BADGES["streak_30"])
    
    return earned


def get_next_badge(stats: Dict) -> Optional[Dict]:
    """Get the next achievable badge."""
    total_sessions = stats.get("total_sessions", 0)
    max_score = stats.get("max_score", 0)
    current_streak = stats.get("current_streak", 0)
    
    # Session badges
    if total_sessions < 1:
        return {"badge": BADGES["first_blood"], "progress": f"{total_sessions}/1 sessions"}
    elif total_sessions < 5:
        return {"badge": BADGES["five_sessions"], "progress": f"{total_sessions}/5 sessions"}
    elif total_sessions < 10:
        return {"badge": BADGES["ten_sessions"], "progress": f"{total_sessions}/10 sessions"}
    elif total_sessions < 20:
        return {"badge": BADGES["twenty_sessions"], "progress": f"{total_sessions}/20 sessions"}
    
    # Score badges
    if max_score < 70:
        return {"badge": BADGES["score_70"], "progress": f"Best: {max_score}/70"}
    elif max_score < 80:
        return {"badge": BADGES["score_80"], "progress": f"Best: {max_score}/80"}
    elif max_score < 90:
        return {"badge": BADGES["score_90"], "progress": f"Best: {max_score}/90"}
    
    # Streak badges
    if current_streak < 7:
        return {"badge": BADGES["streak_7"], "progress": f"Streak: {current_streak}/7 days"}
    
    return None


# ═══════════════════════════════════════════════════════════════
# MOTIVATIONAL QUOTES
# ═══════════════════════════════════════════════════════════════

QUOTES = [
    ("The interview is not a test. It's a conversation where you prove you're the solution to their problem.", "Basin Protocol"),
    ("Every 'no' is one step closer to the right 'yes'.", "The Signal"),
    ("You're not looking for a job. You're looking for a mission that matches your signature.", "Executive OS"),
    ("Practice is not about perfection. It's about confidence.", "Interview Nexus"),
    ("The best candidates don't hope for success. They engineer it.", "Revenue Architect"),
    ("Your resume opened the door. Your answers will close the deal.", "GTM Strategy"),
    ("You're not competing against other candidates. You're competing against their expectations.", "The Difference"),
    ("The market doesn't care about your potential. It cares about your proof.", "Signal-First"),
    ("Nervous means you care. Use that energy.", "Bio-OS"),
    ("You've already done the work. Now you're just telling the story.", "STAR Method"),
]


def get_daily_quote() -> tuple:
    """Get a consistent quote for the day."""
    day_of_year = datetime.now().timetuple().tm_yday
    index = day_of_year % len(QUOTES)
    return QUOTES[index]


# ═══════════════════════════════════════════════════════════════
# RENDER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def render_market_timing_banner():
    """Display the market timing banner."""
    context = get_market_context()
    
    # Color based on score
    if context["score"] >= 60:
        border_color = "#4ade80"
        bg_color = "rgba(74, 222, 128, 0.1)"
    elif context["score"] >= 40:
        border_color = "#fbbf24"
        bg_color = "rgba(251, 191, 36, 0.1)"
    else:
        border_color = "#f87171"
        bg_color = "rgba(248, 113, 113, 0.1)"
    
    st.markdown(f"""
    <div style="background: {bg_color}; border: 1px solid {border_color}; border-radius: 8px; 
                padding: 12px 16px; margin-bottom: 15px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="color: {border_color}; font-weight: 600; font-size: 0.85rem;">
                    📊 MARKET TIMING: {context['label']}
                </span>
                <span style="color: #888; font-size: 0.75rem; margin-left: 10px;">
                    {context['day_name']} | Q{context['quarter']}
                </span>
            </div>
            <div style="background: {border_color}; color: #000; padding: 4px 10px; border-radius: 4px; 
                        font-size: 0.7rem; font-weight: 700;">
                {context['action']}
            </div>
        </div>
        <p style="color: #aaa; font-size: 0.75rem; margin: 8px 0 0 0; line-height: 1.4;">
            {context['recommendations'][0]}
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_badges_display(stats: Dict):
    """Display earned badges and next goal."""
    earned = get_user_badges(stats)
    next_badge = get_next_badge(stats)
    
    st.markdown("### 🏆 Achievements")
    
    if earned:
        # Display earned badges
        badge_html = "<div style='display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px;'>"
        for badge in earned:
            badge_html += f"""
            <div style="background: linear-gradient(135deg, #1a1a0a, #0a0a1a); border: 1px solid #D4AF37; 
                        border-radius: 8px; padding: 8px 12px; text-align: center; min-width: 80px;">
                <span style="font-size: 1.5rem;">{badge['icon']}</span>
                <p style="color: #D4AF37; margin: 4px 0 0 0; font-size: 0.65rem; font-weight: 600;">
                    {badge['name']}
                </p>
            </div>
            """
        badge_html += "</div>"
        st.markdown(badge_html, unsafe_allow_html=True)
    else:
        st.info("Complete your first session to earn badges!")
    
    if next_badge:
        st.markdown(f"""
        <div style="background: #0f0f15; border: 1px dashed #333; border-radius: 8px; padding: 12px; margin-top: 10px;">
            <p style="color: #888; margin: 0; font-size: 0.75rem;">NEXT BADGE</p>
            <div style="display: flex; align-items: center; gap: 10px; margin-top: 8px;">
                <span style="font-size: 1.5rem; opacity: 0.5;">{next_badge['badge']['icon']}</span>
                <div>
                    <p style="color: #D4AF37; margin: 0; font-weight: 600;">{next_badge['badge']['name']}</p>
                    <p style="color: #666; margin: 0; font-size: 0.7rem;">{next_badge['progress']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_daily_quote():
    """Display the daily motivational quote."""
    quote, source = get_daily_quote()
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0a0a0f, #1a1a2e); border-left: 3px solid #D4AF37; 
                padding: 15px 20px; margin: 15px 0; border-radius: 0 8px 8px 0;">
        <p style="color: #f0e6d3; font-style: italic; margin: 0; font-size: 0.9rem; line-height: 1.5;">
            "{quote}"
        </p>
        <p style="color: #D4AF37; margin: 8px 0 0 0; font-size: 0.75rem; font-weight: 600;">
            — {source}
        </p>
    </div>
    """, unsafe_allow_html=True)
