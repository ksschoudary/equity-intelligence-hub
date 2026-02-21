import streamlit as st
import requests
import yfinance as yf
import feedparser
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime

# --- 1. PAGE CONFIG & PWA INJECTION ---
st.set_page_config(page_title="Equity Intelligence Hub", layout="wide", page_icon="📈")

# PWA Manifest Injection
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

# --- 2. CONFIGURATION & DATA ---
# This pulls your API key from Streamlit Cloud Secrets
ALPHA_VANTAGE_KEY = st.secrets.get("ALPHA_VANTAGE_KEY", "DEMO_KEY")

# Your specific list of 12 stocks
STOCKS_NSE = [
    "PATELENG.NS", "BLUEJET.NS", "ITC.NS", "LEMONTREE.NS", 
    "SAGILITY.NS", "RAINBOW.NS", "COFORGE.NS", "BECTORS.NS", 
    "GOPAL.NS", "BIKAJI.NS", "SNOWMAN.NS", "VBL.NS"
]

# Clean names for search purposes
STOCKS_RAW = [s.replace(".NS", "") for s in STOCKS_NSE]

st.title("📈 Equity Intelligence Hub")
st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- 3. DEFINING TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🇮🇳 Indian Market", 
    "🔍 My Stock Intel", 
    "📊 Brokerage Pulse", 
    "⚡ Momentum Pulse"
])

# --- SEGMENT 1: GENERAL INDIAN MARKET ---
with tab1:
    st.header("Indian Equity & Sectoral News")
    # Using Alpha Vantage 'financial_markets' topic for general Indian context
    market_url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=financial_markets&apikey={ALPHA_VANTAGE_KEY}'
    
    try
