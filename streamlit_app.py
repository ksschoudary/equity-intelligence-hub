import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime

# List of your 12 specific companies
MY_STOCKS_RAW = [
    "Patel Engineering", "Bluejet Healthcare", "ITC Hotels", "Lemontree Hotels", 
    "Sagility", "Rainbow Children Hospital", "Coforge", "Mrs Bectors", 
    "Gopal Snacks", "Bikaji Foods", "Snowman Logistics", "Varun Beverages"
]

# --- ADDING TAB 4 ---
# (Inside your existing st.tabs list)
tab1, tab2, tab3, tab4 = st.tabs([
    "🇮🇳 Indian Market", 
    "🔍 My Stock Intel", 
    "📊 Brokerage Pulse", 
    "⚡ Momentum Pulse"
])

with tab4:
    st.header("Web Momentum & Search Hits")
    st.caption("Capturing mentions from Google News and Financial Search Engines")

    selected_moment = st.selectbox("Pick a company to see web momentum:", MY_STOCKS_RAW)
    
    # 1. Construct Google News RSS Query
    # We search for the company name + "share price" or "news" to filter for relevant hits
    query = f"{selected_moment} stock news"
    rss_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en"
    
    # 2. Parse the Feed
    feed = feedparser.parse(rss_url)
    
    if feed.entries:
        for entry in feed.entries[:10]:  # Show top 10 recent hits
            with st.container():
                # Clean up the date
                date_published = entry.published[:16] if 'published' in entry else "Recent"
                
                st.markdown(f"**{entry.title}**")
                st.caption(f"📅 {date_published} | 🌐 Source: {entry.source.title if 'source' in entry else 'Web'}")
                st.link_button("View Search Result", entry.link)
                st.divider()
    else:
        st.info(f"No recent web momentum found for {selected_moment}. Try refreshing.")
