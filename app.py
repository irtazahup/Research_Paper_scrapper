import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

st.set_page_config(page_title="AI Research Tracker", layout="wide")

st.title("🤖 Agentic Research Paper Tracker")

# 1. Choose which View/API to use
view = st.sidebar.radio("Navigate", ["Browse Papers", "View Statistics"])

# Define Base URL
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")  # Default to localhost if not set

if view == "Browse Papers":
    st.header("Latest Research Papers")
    
    # Sidebar Filter
    topic = st.sidebar.selectbox("Filter by Topic", ["All", "Generative AI", "NLP", "Computer Vision", "Reinforcement Learning"])
    
    # Call the /papers API
    params = {"topic": topic if topic != "All" else None}
    try:
        response = requests.get(f"{BASE_URL}/papers", params=params)
        if response.status_code == 200:
            papers = response.json()
            for p in papers:
                with st.expander(f"{p['title']} ({p.get('topic_tag', 'N/A')})"):
                    st.write(f"**Published:** {p['published_at']}")
                    st.write(p['summary'])
                    st.link_button("Read PDF", p['pdf_url'])
        else:
            st.error("API returned an error.")
    except requests.exceptions.ConnectionError:
        st.error("Backend is offline. Run 'uvicorn main:app' in your terminal.")

elif view == "View Statistics":
    st.header("📊 Paper Distribution")
    
    try:
        response = requests.get(f"{BASE_URL}/stats")
        if response.status_code == 200:
            stats_data = response.json() 
            
            # Use the EXACT keys from your JSON response
            df = pd.DataFrame(stats_data)
            
            # IMPORTANT: Check if the columns 'topic_tag' and 'count' exist
            if not df.empty:
                # Rename them AFTER the dataframe is created to make them look nice
                df = df.rename(columns={"topic_tag": "Topic", "count": "Paper Count"})
                
                # Create the chart
                st.bar_chart(df.set_index("Topic"))
                
                # Display the table (this will now show the actual data)
                st.subheader("Raw Totals")
                st.dataframe(df, hide_index=True, use_container_width=True)
            else:
                st.info("No data available.")

    except requests.exceptions.ConnectionError:
        st.error("Backend is offline.")
