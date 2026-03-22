import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def save_papers_to_db(papers):
    conn = psycopg2.connect(os.getenv("CONNECTION_STRING"))
    cur = conn.cursor()
    
    insert_query = """
    INSERT INTO papers (id, title, summary, published_at, pdf_url)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
    """
    
    for p in papers:
        cur.execute(insert_query, (
            p['id'], 
            p['title'], 
            p['summary'], 
            p['published'], 
            p['pdf_url']
        ))
    
    conn.commit()
    print(f"Successfully synced {cur.rowcount} new papers to the database.")
    cur.close()
    conn.close()

# You can now call this after your fetch_recent_ai_papers() function!
