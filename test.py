import arxiv
import datetime
from db_ingestion import save_papers_to_db

def fetch_recent_ai_papers(hours_back=96): # Changed to 96 hours to bypass the weekend gap
    client = arxiv.Client()

    # Search for AI (cs.AI) or Machine Learning (cs.LG)
    search = arxiv.Search(
        query="cat:cs.AI OR cat:cs.LG",
        max_results=20,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    now = datetime.datetime.now(datetime.timezone.utc)
    threshold = now - datetime.timedelta(hours=hours_back)
    
    new_papers = []
    print(f"--- Checking for papers since {threshold} (Last {hours_back}h) ---")

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
        
