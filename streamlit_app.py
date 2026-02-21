import streamlit as st
import requests
import feedparser
from datetime import datetime

# --- 1. EXECUTIVE UI STYLING (The Wheat App Method) ---
st.set_page_config(page_title="Equity Intelligence | Executive View", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, span, div {
        font-family: 'EB Garamond', serif !important;
        color: #FFFFFF !important;
    }
    
    .stApp {
        background-color: #001F3F; /* Midnight Blue */
    }
    
    .news-card {
        padding: 10px;
        border-bottom: 1px solid #1a3a5a;
        margin-bottom: 5px;
    }
    
    .freshness-tag {
        font-size: 0.8rem;
        color: #00FFCC !important; /* Neon Teal for Freshness */
        font-weight: bold;
    }
    
    .headline {
        font-size: 1.1rem;
        font-weight: 500;
        text-decoration: none;
        color: #FFFFFF !important;
    }
    
    .headline:hover {
        color: #FFD700 !important; /* Gold on hover */
    }
    </style>
    """, unsafe_allow_value=True)

# --- 2. CONFIGURATION ---
STOCKS_NSE = ["PATELENG.NS", "BLUEJET.NS", "ITC.NS", "LEMONTREE.NS", "SAGILITY.NS", 
              "RAINBOW.NS", "COFORGE.NS", "BECTORS.NS", "GOPAL.NS", "BIKAJI.NS", "SNOWMAN.NS", "VBL.NS"]
STOCKS_RAW = [s.replace(".NS", "") for s in STOCKS_NSE]

# --- 3. NEWS SCRAPER FUNCTION ---
def get_fresh_news(query, limit=50):
    # Using Google News RSS for maximum freshness and speed
    rss_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(rss_url)
    return feed.entries[:limit]

# --- 4. TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🇮🇳 INDIAN EQUITY", "🔍 PORTFOLIO", "📊 BROKERAGE", "⚡ MOMENTUM"])

# --- TAB 1: INDIAN EQUITY (Strictly Market) ---
with tab1:
    st.markdown("### 🇮🇳 Indian Equity Market - Live Pulse")
    # Strict filter for Indian market news
    market_news = get_fresh_news('Indian Stock Market "Nifty" "Sensex"', limit=50)
    
    for entry in market_news:
        st.markdown(f"""
            <div class="news-card">
                <span class="freshness-tag">{entry.published}</span><br>
                <a class="headline" href="{entry.link}" target="_blank">{entry.title}</a>
            </div>
            """, unsafe_allow_html=True)

# --- TAB 2: PORTFOLIO (Selected Stock News) ---
with tab2:
    selected = st.selectbox("Select Portfolio Stock", STOCKS_RAW)
    st.markdown(f"### 🔍 {selected} Intelligence")
    stock_news = get_fresh_news(f'"{selected}" stock news', limit=50)
    
    for entry in stock_news:
        st.markdown(f"""
            <div class="news-card">
                <span class="freshness-tag">{entry.published}</span><br>
                <a class="headline" href="{entry.link}" target="_blank">{entry.title}</a>
            </div>
            """, unsafe_allow_html=True)

# --- TAB 3: BROKERAGE (Analyst Mentions) ---
with tab3:
    st.markdown("### 📊 Top Brokerage Calls & Upgrades")
    brokerage_news = get_fresh_news('"Motilal Oswal" OR "JP Morgan" OR "Jefferies" OR "ICICI Direct" report', limit=50)
    
    for entry in brokerage_news:
        st.markdown(f"""
            <div class="news-card">
                <span class="freshness-tag">{entry.published}</span><br>
                <a class="headline" href="{entry.link}" target="_blank">{entry.title}</a>
            </div>
            """, unsafe_allow_html=True)

# --- TAB 4: MOMENTUM (Web Search Hits) ---
with tab4:
    st.markdown("### ⚡ General Web Momentum")
    selected_mom = st.selectbox("Check Momentum for", STOCKS_RAW, key="mom_select")
    mom_news = get_fresh_news(f"{selected_mom} latest updates", limit=50)
    
    for entry in mom_news:
        st.markdown(f"""
            <div class="news-card">
                <span class="freshness-tag">{entry.published}</span><br>
                <a class="headline" href="{entry.link}" target="_blank">{entry.title}</a>
            </div>
            """, unsafe_allow_html=True)
