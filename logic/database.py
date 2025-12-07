"""
BASIN::NEXUS - SQLite Persistence Layer
Saves all user data to a local SQLite database
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = "basin_nexus.db"

def get_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize all database tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # CRM Deals Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crm_deals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        role TEXT,
        stage TEXT DEFAULT '1. Identified',
        priority INTEGER DEFAULT 2,
        signal TEXT DEFAULT 'Medium',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # CRM Contacts Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crm_contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        company TEXT,
        role TEXT,
        strength TEXT DEFAULT '🔗',
        sector TEXT,
        notes TEXT,
        last_contact TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Voice Sessions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS voice_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        drill TEXT NOT NULL,
        transcript TEXT,
        words INTEGER DEFAULT 0,
        fillers INTEGER DEFAULT 0,
        has_metric BOOLEAN DEFAULT FALSE,
        wpm INTEGER DEFAULT 0,
        score INTEGER DEFAULT 0,
        feedback TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # XP & Achievements Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stat_key TEXT UNIQUE NOT NULL,
        stat_value TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Calendar Events Table (for interview tracking)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calendar_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT,
        event_date TIMESTAMP,
        event_type TEXT DEFAULT 'Interview',
        notes TEXT,
        outcome TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Objection Bank Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS objection_bank (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        objection TEXT NOT NULL,
        response TEXT,
        category TEXT,
        success_rate INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # ═══════════════════════════════════════════════════════════════
    # COMBAT SIMULATOR TABLES (Duolingo-Style Practice System)
    # ═══════════════════════════════════════════════════════════════
    
    # Combat Practice Sessions - Tracks each practice round
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS combat_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        role TEXT,
        interviewer_type TEXT DEFAULT 'Recruiter',
        question TEXT NOT NULL,
        category TEXT DEFAULT 'General',
        difficulty TEXT DEFAULT 'Medium',
        transcript TEXT,
        score INTEGER DEFAULT 0,
        feedback TEXT,
        duration_seconds INTEGER DEFAULT 0,
        word_count INTEGER DEFAULT 0,
        filler_count INTEGER DEFAULT 0,
        has_metrics BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Interviewer Persona Stats - Track performance per persona type
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS persona_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        persona_type TEXT UNIQUE NOT NULL,
        total_sessions INTEGER DEFAULT 0,
        total_score INTEGER DEFAULT 0,
        avg_score REAL DEFAULT 0,
        best_score INTEGER DEFAULT 0,
        last_practiced TIMESTAMP,
        mastery_level INTEGER DEFAULT 1,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # XP & Streak Tracking
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS practice_streaks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        streak_date DATE UNIQUE NOT NULL,
        sessions_completed INTEGER DEFAULT 0,
        xp_earned INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Question Bank - Stores practiced questions and performance
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS question_bank (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT UNIQUE NOT NULL,
        category TEXT DEFAULT 'General',
        interviewer_type TEXT DEFAULT 'Any',
        difficulty TEXT DEFAULT 'Medium',
        times_practiced INTEGER DEFAULT 0,
        avg_score REAL DEFAULT 0,
        best_response TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

# === CRM DEALS ===
def save_deal(company, role, stage="1. Identified", priority=2, signal="Medium", notes=""):
    """Save a new deal to the database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO crm_deals (company, role, stage, priority, signal, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (company, role, stage, priority, signal, notes))
    conn.commit()
    deal_id = cursor.lastrowid
    conn.close()
    return deal_id

def get_all_deals():
    """Get all deals from database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crm_deals ORDER BY priority ASC, created_at DESC")
    deals = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return deals

def update_deal(deal_id, **kwargs):
    """Update a deal"""
    conn = get_connection()
    cursor = conn.cursor()
    updates = ", ".join([f"{k} = ?" for k in kwargs.keys()])
    values = list(kwargs.values()) + [deal_id]
    cursor.execute(f"UPDATE crm_deals SET {updates}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", values)
    conn.commit()
    conn.close()

def delete_deal(deal_id):
    """Delete a deal"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM crm_deals WHERE id = ?", (deal_id,))
    conn.commit()
    conn.close()

# === CRM CONTACTS ===
def save_contact(name, company, role="", strength="🔗", sector="", notes=""):
    """Save a new contact"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO crm_contacts (name, company, role, strength, sector, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, company, role, strength, sector, notes))
    conn.commit()
    contact_id = cursor.lastrowid
    conn.close()
    return contact_id

def get_all_contacts():
    """Get all contacts"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crm_contacts ORDER BY strength DESC, name ASC")
    contacts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return contacts

def update_contact(contact_id, **kwargs):
    """Update a contact"""
    conn = get_connection()
    cursor = conn.cursor()
    updates = ", ".join([f"{k} = ?" for k in kwargs.keys()])
    values = list(kwargs.values()) + [contact_id]
    cursor.execute(f"UPDATE crm_contacts SET {updates} WHERE id = ?", values)
    conn.commit()
    conn.close()

# === VOICE SESSIONS ===
def save_voice_session(drill, transcript="", words=0, fillers=0, has_metric=False, wpm=0, score=0, feedback=""):
    """Save a voice practice session"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO voice_sessions (drill, transcript, words, fillers, has_metric, wpm, score, feedback)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (drill, transcript, words, fillers, has_metric, wpm, score, feedback))
    conn.commit()
    session_id = cursor.lastrowid
    conn.close()
    return session_id

def get_voice_sessions(limit=50):
    """Get voice sessions"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM voice_sessions ORDER BY created_at DESC LIMIT ?", (limit,))
    sessions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return sessions

def get_voice_analytics():
    """Get voice session analytics"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COUNT(*) as total_sessions,
            AVG(wpm) as avg_wpm,
            AVG(fillers) as avg_fillers,
            SUM(CASE WHEN has_metric THEN 1 ELSE 0 END) as metric_hits,
            AVG(score) as avg_score
        FROM voice_sessions
    """)
    analytics = dict(cursor.fetchone())
    conn.close()
    return analytics

# === USER STATS ===
def save_stat(key, value):
    """Save or update a user stat"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_stats (stat_key, stat_value, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(stat_key) DO UPDATE SET stat_value = ?, updated_at = CURRENT_TIMESTAMP
    """, (key, str(value), str(value)))
    conn.commit()
    conn.close()

def get_stat(key, default=None):
    """Get a user stat"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT stat_value FROM user_stats WHERE stat_key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    return row['stat_value'] if row else default

def get_all_stats():
    """Get all user stats"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT stat_key, stat_value FROM user_stats")
    stats = {row['stat_key']: row['stat_value'] for row in cursor.fetchall()}
    conn.close()
    return stats

# === CALENDAR EVENTS ===
def save_calendar_event(title, company, event_date, event_type="Interview", notes=""):
    """Save a calendar event"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO calendar_events (title, company, event_date, event_type, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (title, company, event_date, event_type, notes))
    conn.commit()
    event_id = cursor.lastrowid
    conn.close()
    return event_id

def get_upcoming_events(days=7):
    """Get upcoming calendar events"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM calendar_events 
        WHERE event_date >= datetime('now') 
        AND event_date <= datetime('now', '+' || ? || ' days')
        ORDER BY event_date ASC
    """, (days,))
    events = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return events

# === OBJECTION BANK ===
def save_objection(objection, response, category="General"):
    """Save an objection"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO objection_bank (objection, response, category)
        VALUES (?, ?, ?)
    """, (objection, response, category))
    conn.commit()
    objection_id = cursor.lastrowid
    conn.close()
    return objection_id

def get_all_objections():
    """Get all objections"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM objection_bank ORDER BY category, created_at DESC")
    objections = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return objections


# ═══════════════════════════════════════════════════════════════
# COMBAT SIMULATOR FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def save_combat_session(company, role, interviewer_type, question, category="General", 
                        difficulty="Medium", transcript="", score=0, feedback="",
                        duration_seconds=0, word_count=0, filler_count=0, has_metrics=False):
    """Save a combat practice session"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO combat_sessions 
        (company, role, interviewer_type, question, category, difficulty, 
         transcript, score, feedback, duration_seconds, word_count, filler_count, has_metrics)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (company, role, interviewer_type, question, category, difficulty,
          transcript, score, feedback, duration_seconds, word_count, filler_count, has_metrics))
    conn.commit()
    session_id = cursor.lastrowid
    
    # Update persona stats
    update_persona_stats(interviewer_type, score)
    
    # Record streak/XP
    record_daily_practice(score)
    
    conn.close()
    return session_id

def get_combat_sessions(limit=50, company=None, interviewer_type=None):
    """Get combat sessions with optional filters"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM combat_sessions WHERE 1=1"
    params = []
    
    if company:
        query += " AND company = ?"
        params.append(company)
    if interviewer_type:
        query += " AND interviewer_type = ?"
        params.append(interviewer_type)
    
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    sessions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return sessions

def get_combat_analytics():
    """Get overall combat practice analytics"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COUNT(*) as total_sessions,
            AVG(score) as avg_score,
            MAX(score) as best_score,
            SUM(duration_seconds) as total_practice_time,
            AVG(word_count) as avg_words,
            AVG(filler_count) as avg_fillers,
            COUNT(DISTINCT company) as companies_practiced,
            COUNT(DISTINCT interviewer_type) as personas_practiced
        FROM combat_sessions
    """)
    analytics = dict(cursor.fetchone())
    conn.close()
    return analytics

def update_persona_stats(persona_type, score):
    """Update stats for an interviewer persona"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get current stats
    cursor.execute("SELECT * FROM persona_stats WHERE persona_type = ?", (persona_type,))
    existing = cursor.fetchone()
    
    if existing:
        existing = dict(existing)
        new_total = existing['total_sessions'] + 1
        new_score_sum = existing['total_score'] + score
        new_avg = new_score_sum / new_total
        new_best = max(existing['best_score'], score)
        
        # Calculate mastery level (1-10 based on sessions and scores)
        mastery = min(10, (new_total // 5) + (1 if new_avg >= 80 else 0) + (1 if new_avg >= 90 else 0))
        
        cursor.execute("""
            UPDATE persona_stats 
            SET total_sessions = ?, total_score = ?, avg_score = ?, 
                best_score = ?, mastery_level = ?, last_practiced = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
            WHERE persona_type = ?
        """, (new_total, new_score_sum, new_avg, new_best, mastery, persona_type))
    else:
        cursor.execute("""
            INSERT INTO persona_stats (persona_type, total_sessions, total_score, avg_score, best_score, mastery_level, last_practiced)
            VALUES (?, 1, ?, ?, ?, 1, CURRENT_TIMESTAMP)
        """, (persona_type, score, score, score))
    
    conn.commit()
    conn.close()

def get_persona_stats():
    """Get all persona stats"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM persona_stats ORDER BY mastery_level DESC, avg_score DESC")
    stats = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return stats

def record_daily_practice(score):
    """Record daily practice for streak tracking"""
    from datetime import date
    today = date.today().isoformat()
    
    # XP earned based on score
    xp = 10 + (score // 10)  # Base 10 XP + bonus for score
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM practice_streaks WHERE streak_date = ?", (today,))
    existing = cursor.fetchone()
    
    if existing:
        existing = dict(existing)
        cursor.execute("""
            UPDATE practice_streaks 
            SET sessions_completed = sessions_completed + 1, xp_earned = xp_earned + ?
            WHERE streak_date = ?
        """, (xp, today))
    else:
        cursor.execute("""
            INSERT INTO practice_streaks (streak_date, sessions_completed, xp_earned)
            VALUES (?, 1, ?)
        """, (today, xp))
    
    conn.commit()
    conn.close()

def get_streak_info():
    """Get current streak and XP info"""
    from datetime import date, timedelta
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Calculate current streak
    today = date.today()
    streak = 0
    check_date = today
    
    while True:
        cursor.execute("SELECT * FROM practice_streaks WHERE streak_date = ?", (check_date.isoformat(),))
        day = cursor.fetchone()
        if day:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break
    
    # Get total XP
    cursor.execute("SELECT SUM(xp_earned) as total_xp FROM practice_streaks")
    result = cursor.fetchone()
    total_xp = result['total_xp'] if result and result['total_xp'] else 0
    
    # Calculate level (every 100 XP = 1 level)
    level = (total_xp // 100) + 1
    xp_in_level = total_xp % 100
    
    # Get today's sessions
    cursor.execute("SELECT sessions_completed FROM practice_streaks WHERE streak_date = ?", (today.isoformat(),))
    today_result = cursor.fetchone()
    today_sessions = today_result['sessions_completed'] if today_result else 0
    
    conn.close()
    
    return {
        'streak': streak,
        'total_xp': total_xp,
        'level': level,
        'xp_in_level': xp_in_level,
        'xp_to_next': 100 - xp_in_level,
        'today_sessions': today_sessions
    }

def save_to_question_bank(question, category="General", interviewer_type="Any", difficulty="Medium"):
    """Save a question to the bank for tracking"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM question_bank WHERE question = ?", (question,))
    existing = cursor.fetchone()
    
    if not existing:
        cursor.execute("""
            INSERT INTO question_bank (question, category, interviewer_type, difficulty)
            VALUES (?, ?, ?, ?)
        """, (question, category, interviewer_type, difficulty))
        conn.commit()
    
    conn.close()

def update_question_performance(question, score, best_response=None):
    """Update performance stats for a question"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM question_bank WHERE question = ?", (question,))
    existing = cursor.fetchone()
    
    if existing:
        existing = dict(existing)
        new_times = existing['times_practiced'] + 1
        new_avg = ((existing['avg_score'] * existing['times_practiced']) + score) / new_times
        
        cursor.execute("""
            UPDATE question_bank 
            SET times_practiced = ?, avg_score = ?, best_response = COALESCE(?, best_response)
            WHERE question = ?
        """, (new_times, new_avg, best_response, question))
    
    conn.commit()
    conn.close()

def get_question_bank(category=None, interviewer_type=None):
    """Get questions from the bank"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM question_bank WHERE 1=1"
    params = []
    
    if category:
        query += " AND category = ?"
        params.append(category)
    if interviewer_type:
        query += " AND interviewer_type = ?"
        params.append(interviewer_type)
    
    query += " ORDER BY times_practiced ASC, avg_score ASC"  # Prioritize least practiced, lowest score
    
    cursor.execute(query, params)
    questions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return questions


# Initialize database on import
init_database()

