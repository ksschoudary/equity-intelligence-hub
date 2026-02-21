import streamlit as st
import feedparser
from datetime import datetime

# --- 1. COMPACT EXECUTIVE UI STYLING ---
st.set_page_config(page_title="Equity Intel | Executive View", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, span, div, li {
        font-family: 'EB Garamond', serif !important;
        color: #FFFFFF !important;
    }
    
    .stApp { background-color: #001F3F; } /* Midnight Blue */
    
    /* ULTRA-COMPACT SPACING */
    .stMarkdown { margin-bottom: -12px !important; }
    hr { margin: 8px 0px !important; border-color: rgba(255,255,255,0.1); }

    .news-line { padding: 4px 0px; line-height: 1.3; }
    .fresh-tag { color: #00FFCC; font-size: 0.85rem; font-weight: bold; margin-right: 8px; }
    .stock-tag { color: #FFD700; font-size: 0.85rem; font-weight: bold; margin-right: 8px; text-transform: uppercase; }
    
    a { text-decoration: none !important; color: #FFFFFF !important; }
    a:hover { color: #00FFCC !important; text-decoration: underline !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PORTFOLIO CONFIGURATION ---
STOCKS = {
    "Patel Eng": "PATELENG.NS", "Bluejet": "BLUEJET.NS", "ITC Hotels": "ITCHOTELS.NS",
    "Lemontree": "LEMONTREE.NS", "Sagility": "SAGILITY.NS", "Rainbow": "RAINBOW.NS",
    "Coforge": "COFORGE.NS", "Mrs Bectors": "BECTORS.NS", "Gopal Snacks": "GOPAL.NS",
    "Bikaji": "BIKAJI.NS", "Snowman": "SNOWMAN.NS", "Varun Bev": "VBL.NS"
}

# --- 3. SECURE SCRAPER ---
def fetch_news(query, count=50):
    url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)
    return feed.entries[:count]

# --- 4. TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🇮🇳 MARKET", "🔍 WATCHLIST", "📊 BROKERAGE", "⚡ MOMENTUM"])

# --- TAB 1: STRICT INDIAN EQUITY ---
with tab1:
    st.subheader("Indian Equity Market - Live Headlines")
    market_news = fetch_news('site:moneycontrol.com OR site:economictimes.indiatimes.com "Nifty" OR "Sensex"', 50)
    for n in market_news:
        # Rendering as clean Markdown links to avoid raw URL errors
        st.markdown(f"**[{n.title}]({n.link})**")
        st.caption(f"{n.published[:16]} | {n.source.title if 'source' in n else 'Market'}")
        st.markdown("---")

# --- TAB 2: ROLLING WATCHLIST (NO FILTERS) ---
with tab2:
    st.subheader("Rolling Stock Intelligence")
    for name, ticker in STOCKS.items():
        s_news = fetch_news(f'"{name}" stock news india', 2)
        for n in s_news:
            st.markdown(f"**{name.upper()}**: [{n.title}]({n.link})")
            st.caption(f"{n.published[:16]}")
        st.markdown("---")

# --- TAB 3: BROKERAGE ---
with tab3:
    st.subheader("Brokerage Reports & Analyst Calls")
    b_news = fetch_news('("Motilal Oswal" OR "JP Morgan" OR "Jefferies" OR "ICICI Direct") report', 50)
    for n in b_news:
        st.markdown(f"**[{n.title}]({n.link})**")
        st.caption(f"{n.published[:16]}")
        st.markdown("---")

# --- TAB 4: MOMENTUM ---
with tab4:
    st.subheader("Momentum & Search Hits")
    m_news = fetch_news("Indian equity breakout momentum", 50)
    for n in m_news:
        st.markdown(f"**[{n.title}]({n.link})**")
        st.caption(f"{n.published[:16]}")
        st.markdown("---")
