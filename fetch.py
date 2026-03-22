import os

import arxiv
import datetime

import psycopg2
from db_ingestion import save_papers_to_db



def get_latest_timestamp():
    conn = psycopg2.connect(os.getenv("CONNECTION_STRING"))
    cur = conn.cursor()
    cur.execute("SELECT MAX(published_at) FROM papers")
    result = cur.fetchone()[0]
    cur.close()
    conn.close()
    # If DB is empty, default to 96h; otherwise, use the last paper's date
    return result if result else (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=96))

# Then in your fetch function:
threshold = get_latest_timestamp()
# Now it only fetches papers published AFTER the last one in your DB.


def fetch_recent_ai_papers(dayToFetchFrom): # Changed to 96 hours to bypass the weekend gap
    client = arxiv.Client()

    # Search for AI (cs.AI) or Machine Learning (cs.LG)
    search = arxiv.Search(
        query="cat:cs.AI OR cat:cs.LG",
        max_results=20,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    now = datetime.datetime.now(datetime.timezone.utc)
    threshold = dayToFetchFrom
    
    new_papers = []
    print(f"--- Checking for papers since {threshold} ")

    for result in client.results(search):
        # ArXiv 'published' date is when the version was first submitted
        if result.published > threshold:
            new_papers.append({
                "title": result.title,
                "published": result.published,
                "id": result.entry_id.split('/')[-1],
                "summary": result.summary,
                "pdf_url": result.pdf_url
            })
        else:
            break

    return new_papers

if __name__ == "__main__":
    papers = fetch_recent_ai_papers(96)
    print(f"Found {len(papers)} papers.")
    for p in papers[:3]: # Show first 3 for verification
        print(f"[{p['published']}] {p['title']} {p['pdf_url']}")
    
    if papers:
        save_papers_to_db(papers)
        
