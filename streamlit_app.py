import streamlit as st
import requests
import yfinance as yf
import feedparser
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime

# --- 1. PWA & PAGE SETUP ---
st.set_page_config(page_title="Equity Intelligence Hub", layout="wide", page_icon="📈")

# This injects the PWA manifest so it can be installed on your phone
components.html(
    """
    <link rel="manifest" href="/manifest.json">
    <script>
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js');
      }
    </script>
    """,
    height=0,
)

# --- 2. CONFIG & PORTFOLIO ---
# Set your ALPHA_VANTAGE_KEY in Streamlit Cloud Secrets
ALPHA_VANTAGE_KEY = st.secrets.get("ALPHA_VANTAGE_KEY", "DEMO_KEY")

# Your specific list of 12 stocks
STOCKS_NSE = [
    "PATELENG.NS", "BLUEJET.NS", "ITC.NS", "LEMONTREE.NS", 
    "SAGILITY.NS", "RAINBOW.NS", "COFORGE.NS", "BECTORS.NS", 
    "GOPAL.NS", "BIKAJI.NS", "SNOWMAN.NS", "VBL.NS"
]
STOCKS_RAW = [s.replace(".NS", "") for s in STOCKS_NSE]

st.title("📈 Equity Intelligence Hub")
st.caption(f"Market Status: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- 3. TAB DEFINITION ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🇮🇳 Indian Market", 
    "🔍 My Stock Intel", 
    "📊 Brokerage Pulse", 
    "⚡ Momentum Pulse"
])

# --- TAB 1: GENERAL INDIAN MARKET ---
with tab1:
    st.header("Indian Equity & Sectoral Feed")
    market_url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=financial_markets&apikey={ALPHA_VANTAGE_KEY}'
    
    try:
        response = requests.get(market_url)
        data = response.json()
        if "feed" in data:
            for item in data["feed"][:8]:
                with st.expander(f"{item['title']}"):
                    st.write(f"**Source:** {item['source']} | **Sentiment:** {item['overall_sentiment_label']}")
                    st.write(item['summary'])
                    st.link_button("Read Full Story", item['url'])
        else:
            st.warning("Daily news limit reached. Please check back later.")
    except Exception as e:
        st.error(f"Error connecting to Market API: {e}")

# --- TAB 2: PORTFOLIO WATCHTOWER ---
with tab2:
    st.header("Stock-Specific Intelligence")
    selected_stock = st.selectbox("Select stock to inspect:", STOCKS_NSE)
    ticker = yf.Ticker(selected_stock)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Price History (5 Days)")
        st.dataframe(ticker.history(period="5d"))
    with col2:
        st.subheader("Corporate Actions")
        actions = ticker.actions.tail(5)
        if not actions.empty:
            st.table(actions)
        else:
            st.write("No recent dividends or splits.")

# --- TAB 3: BROKERAGE EXCLUSIVE ---
with tab3:
    st.header("Brokerage & Analyst Reports")
    firms = ["Motilal Oswal", "JP Morgan", "Jefferies", "ICICI Direct", "Goldman Sachs", "Investec", "CLSA"]
    st.info("Searching feeds for brokerage upgrades and target price changes...")
    
    found_any = False
    if 'data' in locals() and "feed" in data:
        for item in data["feed"]:
            if any(firm.lower() in item['title'].lower() for firm in firms):
                found_any = True
                st.success(f"**REPORT:** {item['title']}")
                st.link_button("View Analysis", item['url'])
                st.divider()
    
    if not found_any:
        st.write("No major brokerage reports found in the current news cycle.")

# --- TAB 4: MOMENTUM PULSE (SEARCH SCRAPER) ---
with tab4:
    st.header("⚡ Web Momentum & Search Hits")
    selected_moment = st.selectbox("Search across web for company momentum:", STOCKS_RAW)
    
    query = f"{selected_moment} share latest news"
    rss_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en"
    
    feed = feedparser.parse(rss_url)
    if feed.entries:
        for entry in feed.entries[:12]:
            with st.container():
                st.markdown(f"**{entry.title}**")
                st.caption(f"Source: {entry.source.title if 'source' in entry else 'Web'} | {entry.published}")
                st.link_button("View Result", entry.link)
                st.divider()
    else:
        st.info("No recent web hits found.")
