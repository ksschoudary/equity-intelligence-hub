import streamlit as st
import requests
import yfinance as yf
import feedparser
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime

# --- 1. PWA & PAGE CONFIG ---
st.set_page_config(page_title="Equity Intelligence Hub", layout="wide")

# This injects the PWA manifest into the app's HTML
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

# --- 2. CONFIG & ASSETS ---
ALPHA_VANTAGE_KEY = st.secrets.get("ALPHA_VANTAGE_KEY", "YOUR_KEY") # Set in Streamlit Cloud Secrets

# Your specific watchlist
STOCKS_NSE = [
    "PATELENG.NS", "BLUEJET.NS", "ITC.NS", "LEMONTREE.NS", 
    "SAGILITY.NS", "RAINBOW.NS", "COFORGE.NS", "BECTORS.NS", 
    "GOPAL.NS", "BIKAJI.NS", "SNOWMAN.NS", "VBL.NS"
]

STOCKS_RAW = [s.replace(".NS", "") for s in STOCKS_NSE]

# --- 3. THE TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🇮🇳 Indian Market", 
    "🔍 My Stock Intel", 
    "📊 Brokerage Pulse", 
    "⚡ Momentum Pulse"
])

# --- SEGMENT 1: GENERAL MARKET ---
with tab1:
    st.header("Indian Equity & Sectoral Feed")
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=financial_markets&apikey={ALPHA_VANTAGE_KEY}'
    try:
        data = requests.get(url).json()
        if "feed" in data:
            for item in data["feed"][:8]:
                with st.expander(f"{item['title']}"):
                    st.write(f"**Source:** {item['source']} | **Sentiment:** {item['overall_sentiment_label']}")
                    st.write(item['summary'])
                    st.link_button("Read full article", item['url'])
    except:
        st.error("Market API limit reached. Try again later.")

# --- SEGMENT 2: PORTFOLIO SPECIFIC ---
with tab2:
    st.header("Portfolio Watchtower")
    selected_stock = st.selectbox("Select stock to inspect:", STOCKS_NSE)
    ticker_data = yf.Ticker(selected_stock)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Last 5 Days Price")
        st.dataframe(ticker_data.history(period="5d"))
    with col2:
        st.subheader("Corporate Actions")
        st.write(ticker_data.actions.tail(5))

# --- SEGMENT 3: BROKERAGE EXCLUSIVE ---
with tab3:
    st.header("Brokerage & Analyst Reports")
    firms = ["Motilal Oswal", "JP Morgan", "Jefferies", "ICICI Direct", "Goldman Sachs", "Investec"]
    
    st.info("Filtering market feeds for brokerage mentions...")
    # Re-using tab1 data to find brokerage keywords
    if "feed" in data:
        for item in data["feed"]:
            if any(firm.lower() in item['title'].lower() for firm in firms):
                st.success(f"**{item['title']}**")
                st.link_button("View Analysis
