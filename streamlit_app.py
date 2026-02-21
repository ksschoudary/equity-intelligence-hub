import streamlit as st
import requests
import yfinance as yf
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(page_title="Equity Intelligence Hub", layout="wide")
ALPHA_VANTAGE_KEY = "YOUR_KEY" # Get for free at alphavantage.co

# Your Specific Portfolio
MY_STOCKS = [
    "PATELENG.NS", "BLUEJET.NS", "ITC.NS", "LEMONTREE.NS", 
    "SAGILITY.NS", "RAINBOW.NS", "COFORGE.NS", "BECTORS.NS", 
    "GOPAL.NS", "BIKAJI.NS", "SNOWMAN.NS", "VBL.NS"
]

# --- UI TABS ---
tab1, tab2, tab3 = st.tabs(["🇮🇳 Indian Market & Sectors", "🔍 My Stock Intelligence", "📊 Brokerage Pulse"])

# --- SEGMENT 1: GENERAL MARKET NEWS ---
with tab1:
    st.header("Indian Equity & Sectoral Feed")
    # Using Alpha Vantage 'Topics' to filter for Financial Markets
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=financial_markets&apikey={ALPHA_VANTAGE_KEY}'
    data = requests.get(url).json()
    
    if "feed" in data:
        for item in data["feed"][:8]: # Top 8 general news
            with st.expander(f"{item['title']}"):
                st.write(f"**Source:** {item['source']} | **Sentiment:** {item['overall_sentiment_label']}")
                st.write(item['summary'])
                st.link_button("Read full article", item['url'])

# --- SEGMENT 2: PORTFOLIO SPECIFIC (FILINGS & UPDATES) ---
with tab2:
    st.header("Portfolio Watchtower")
    selected_stock = st.selectbox("Select stock to inspect:", MY_STOCKS)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Price & Events")
        ticker_data = yf.Ticker(selected_stock)
        st.write(ticker_data.history(period="5d"))
        
        # Corporate Actions
        st.write("**Recent Actions:**")
        st.write(ticker_data.actions.tail(3))

    with col2:
        st.subheader("Specific Updates & Reports")
        # Custom search for the specific stock across news
        stock_url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={selected_stock}&apikey={ALPHA_VANTAGE_KEY}'
        stock_news = requests.get(stock_url).json()
        
        if "feed" in stock_news:
            for news in stock_news["feed"][:5]:
                st.info(f"**{news['title']}**\n\n{news['summary'][:150]}...")
                st.caption(f"Source: {news['source']}")
        else:
            st.write("No recent specific updates found in the news cycle.")

# --- SEGMENT 3: BROKERAGE EXCLUSIVE ---
with tab3:
    st.header("Brokerage & Analyst Reports")
    st.caption("Tracking mentions from: Motilal Oswal, JP Morgan, Jefferies, ICICI Direct")
    
    # Logic: Search general news but filter for 'Brokerage' names
    brokerage_firms = ["Motilal Oswal", "JP Morgan", "Jefferies", "ICICI Direct", "Goldman Sachs"]
    
    # Using the general feed but filtering via Python
    if "feed" in data:
        found_report = False
        for item in data["feed"]:
            if any(firm.lower() in item['title'].lower() or firm.lower() in item['summary'].lower() for firm in brokerage_firms):
                found_report = True
                st.success(f"**ANALYST MOVE:** {item['title']}")
                st.write(item['summary'])
                st.link_button("View Analysis", item['url'])
                st.divider()
        
        if not found_report:
            st.write("No major brokerage reports detected in the last 24 hours.")
