from fetch import fetch_recent_ai_papers, get_latest_timestamp
from db_ingestion import save_papers_to_db
from tagging import enrich_metadata
import time


def run_pipeline():
    print("--- 🚀 Starting MLOps Pipeline ---")
    
    # 1. Ingest (Using 96h for now to ensure we have data)
    print("Step 1: Fetching papers from arXiv...")
    threshold = get_latest_timestamp()
    papers = fetch_recent_ai_papers(threshold)
    
    if not papers:
        print("No papers found in the last 96 hours. Skipping...")
    else:
        # 2. Save to DB
        print(f"Step 2: Syncing {len(papers)} papers to Database...")
        save_papers_to_db(papers)
        
        # 3. Enrich with AI
        print("Step 3: Enriching metadata using Groq AI...")
        enrich_metadata()
    
    print("--- ✅ Pipeline Completed ---")

if __name__ == "__main__":
    SIX_HOURS = 6 * 60 * 60  # seconds
    while True:
        try:
            run_pipeline()
        except Exception as e:
            print(f"❌ Pipeline failed: {e}")
        
        print(f"💤 Sleeping for 6 hours...")
        time.sleep(SIX_HOURS)
    
