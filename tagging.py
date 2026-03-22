import os
import psycopg2
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Clients
db_conn = psycopg2.connect(os.getenv("CONNECTION_STRING"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_tag(title, summary):
    """The 'Agentic' part: Asking the LLM to categorize based on context."""
    prompt = f"""
    You are an expert AI Research Assistant. Categorize the following research paper into ONE of these categories: 
    [Computer Vision, Natural Language Processing, Reinforcement Learning, Generative AI, Robotics, Optimization].
    
    Title: {title}
    Summary: {summary}
    
    Respond with ONLY the category name.
    NOTE: The category Name should be at least 2 words if applicable (e.g., "Computer Vision", not just "Vision").
    """
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile", # High-quality free-tier model
            temperature=0, # Keep it consistent
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq Error: {e}")
        return "Uncategorized"

def enrich_metadata():
    cur = db_conn.cursor()
    
    # 1. Find papers that need a tag
    cur.execute("SELECT id, title, summary FROM papers WHERE topic_tag IS NULL LIMIT 10;")
    rows = cur.fetchall()
    
    if not rows:
        print("No new papers to categorize.")
        return

    print(f"Categorizing {len(rows)} papers...")

    for paper_id, title, summary in rows:
        tag = get_ai_tag(title, summary)
        
        # 2. Update the row with the new tag
        cur.execute(
            "UPDATE papers SET topic_tag = %s WHERE id = %s",
            (tag, paper_id)
        )
        print(f"Paper [{paper_id}] tagged as: {tag}")

    db_conn.commit()
    cur.close()

if __name__ == "__main__":
    enrich_metadata()
    db_conn.close()
