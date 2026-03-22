from fastapi import FastAPI, Query
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="AI Research Paper API")

def get_db_connection():
    return psycopg2.connect(os.getenv("CONNECTION_STRING"), cursor_factory=RealDictCursor)

@app.get("/papers")
def get_papers(topic: str = None, limit: int = 10):
    """Fetch papers with optional filtering by AI Topic."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    if topic:
        query = "SELECT * FROM papers WHERE topic_tag = %s ORDER BY published_at DESC LIMIT %s"
        cur.execute(query, (topic, limit))
    else:
        query = "SELECT * FROM papers ORDER BY published_at DESC LIMIT %s"
        cur.execute(query, (limit,))
    
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

@app.get("/stats")
def get_stats():
    """Returns a count of papers per topic for your UI charts."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT topic_tag, COUNT(*) as count FROM papers GROUP BY topic_tag")
    stats = cur.fetchall()
    cur.close()
    conn.close()
    return stats
