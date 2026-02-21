import streamlit as st
import requests
import feedparser
from datetime import datetime

# --- 1. EXECUTIVE UI STYLING (The "Wheat App" Aesthetic) ---
st.set_page_config(page_title="Equity Intelligence | Executive View", layout="wide")

# We use CSS injection ONLY for the UI framework (Safe)
# This forces the Garamond font and Midnight Blue theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;700&display=swap');
    
    /* Apply Garamond to the entire app */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, span, div, li {
        font-family: 'EB Garamond', serif !important;
    }
    
    /* Executive Midnight Blue Theme */
    .stApp {
        background-color: #001F3F;
    }
    
    /* Style the Sidebar and Headers */
    [data-testid="stSidebar"] {
        background-color: #001933;
    }
    
    h1, h2, h3 {
        color: #FFD700 !important; /* Executive Gold */
        border-bottom: 1px solid #1a3a5a;
    }

    /* Clean News Feed styling */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.05);
        border: none;
        padding: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONFIGURATION & PORTFOLIO ---
STOCKS_NSE = ["PATELENG.NS", "BLUEJET.NS", "ITC.NS", "LEMONTREE.NS", "SAGILITY.NS", 
              "RAINBOW.NS", "COFORGE.NS", "BECTORS.NS", "GOPAL.NS", "BIKAJI.NS", "SNOWMAN.NS", "VBL.NS"]
STOCKS_RAW = [s.replace(".NS", "") for s in STOCKS_NSE]

# --- 3. SECURE NEWS FETCHER ---
def get_sanitized_news(query):
    """Fetches news and returns a safe list of headline dictionaries."""
    rss_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(rss_url)
    
    sanitized_data = []
    for entry in feed.entries[:50]:
        sanitized_data.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "source": entry.source.title if 'source' in entry else "Market Link"
        })
    return sanitized_data

# --- 4. EXECUTIVE TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🇮🇳 MARKET", "🔍 PORTFOLIO", "📊 BROKERAGE", "⚡ MOMENTUM"])

# --- TAB 1: STRICT INDIAN EQUITY ---
with tab1:
    st.header("Indian Equity Market Pulse")
    # Strictly filtered query for Indian exchanges
    news = get_sanitized_news('site:economictimes.indiatimes.com OR site:moneycontrol.com "Nifty" "Sensex"')
    
    for item in news:
        # We use st.caption and st.markdown(link) which are sanitized by Streamlit
        st.caption(f"🕒 {item['published']} | {item['source']}")
        st.markdown(f"**[{item['title']}]({item['link']})**")
        st.divider()

# --- TAB 2: PORTFOLIO WATCHTOWER ---
with tab2:
    selected = st.selectbox("Select Portfolio Asset", STOCKS_RAW)
    st.header(f"{selected} Intelligence")
    news = get_sanitized_news(f'"{selected}" stock news india')
    
    for item in news:
        st.caption(f"🕒 {item['published']} | {item['source']}")
        st.markdown(f"**[{item['title']}]({item['link']})**")
        st.divider()

# --- TAB 3: BROKERAGE INTELLIGENCE ---
with tab3:
    st.header("Analyst Reports & Calls")
    query = '("Motilal Oswal" OR "JP Morgan" OR "Jefferies" OR "ICICI Direct") stock report'
    news = get_sanitized_news(query)
    
    for item in news:
        st.info(f"Report from: {item['source']}")
        st.markdown(f"**[{item['title']}]({item['link']})**")
        st.divider()

# --- TAB 4: WEB MOMENTUM ---
with tab4:
    st.header("General Web Momentum")
    selected_mom = st.selectbox("Analyze Momentum for", STOCKS_RAW, key="mom_sel")
    news = get_sanitized_news(f"{selected_mom} latest updates")
    
    for item in news:
        st.caption(f"🕒 {item['published']}")
        st.markdown(f"**[{item['title']}]({item['link']})**")
        st.divider()
