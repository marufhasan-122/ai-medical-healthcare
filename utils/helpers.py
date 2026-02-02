import sqlite3
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)
DB_PATH = "database/patient_records.db"

def save_record(symptoms, risk_level, score):
    # Input validation
    if not symptoms or not isinstance(symptoms, str):
        raise ValueError("Symptoms must be a non-empty string")
    
    if not isinstance(risk_level, str):
        raise ValueError("Risk level must be a string")
    
    if not isinstance(score, (int, float)) or score < 0 or score > 1:
        raise ValueError("Score must be a number between 0 and 1")
    
    # Ensure database directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symptoms TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                score REAL NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        cur.execute("""
            INSERT INTO records (symptoms, risk_level, score, created_at)
            VALUES (?, ?, ?, ?)
        """, (symptoms[:5000], risk_level, score, datetime.now().isoformat()))

        conn.commit()
        logger.info(f"Record saved: {risk_level} risk")
    
    except sqlite3.Error as e:
        logger.error(f"Database error while saving record: {e}")
        raise RuntimeError(f"Failed to save medical record: {e}")
    
    finally:
        if conn:
            conn.close()
