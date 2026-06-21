# rag/NexusDB.py
import sqlite3
import os

# Safe absolute path so it always goes to the root folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)# remove the file name in the path and move one level up in your directory tree (out of the rag folder and into its parent folder).
DB_PATH = os.path.join(PROJECT_ROOT, "Nexus_Chat_History.db")

def init_db():
    """Creates the database and necessary tables if they do not exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        user_query TEXT,
        model_response TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def save_chat_turn(session_id, user_query, model_response):
    """Saves a full prompt-and-response turn to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chat_messages (session_id, user_query, model_response)
        VALUES (?, ?, ?)
    """, (session_id, user_query, model_response))
    conn.commit()
    conn.close()

init_db()