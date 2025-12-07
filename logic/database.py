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

# Initialize database on import
init_database()
