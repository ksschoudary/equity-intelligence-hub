import streamlit as st
import feedparser
from datetime import datetime

# --- 1. COMPACT EXECUTIVE UI STYLING ---
st.set_page_config(page_title="Equity Intel | Compact View", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, span, div, li {
        font-family: 'EB Garamond', serif !important;
        color: #FFFFFF !important;
    }
    
    .stApp {
        background-color: #001F3F; /* Midnight Blue */
    }
    
    /* COMPACT SPACING: Reducing vertical gaps */
    .stMarkdown, .element-container {
        margin-bottom: -10px !important;
        padding-bottom: 0px !important;
    }
    
    hr {
        margin: 5px 0px !important;
        border-color: rgba(255, 255, 255, 0.1);
    }

    .news-line {
        padding: 2px 0px;
        line-height: 1.2;
    }

    .fresh-tag {
        color: #00FFCC; /* Neon Teal */
        font-size: 0.85rem;
        font-weight: bold;
        margin-right: 10px;
    }

    .stock-label {
        color: #FFD700; /* Gold */
        font-size: 0.85rem;
        font-weight: bold;
        text-transform: uppercase;
        margin-right: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONFIGURATION & PORTFOLIO ---
# Updated list with ITCHOTELS.NS
STOCKS = {
    "Patel Eng": "PATELENG.NS",
    "Bluejet Health": "BLUEJET.NS",
    "ITC Hotels": "ITCHOTELS.NS",
    "Lemontree": "LEMONTREE.NS",
    "Sagility": "SAGILITY.NS",
    "Rainbow": "RAINBOW.NS",
    "Coforge": "COFORGE.NS",
    "Mrs Bectors": "BECTORS.NS",
    "Gopal Snacks": "GOPAL.NS",
    "Bikaji": "BIKAJI.NS",
    "Snowman": "SNOWMAN.NS",
    "Varun Beverages": "VBL.NS"
}

# --- 3. SCRAPER LOGIC ---
def fetch_news(query, count=50):
    url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en"
    return feedparser.parse(url).entries[:count]

# --- 4. TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🇮🇳 MARKET", "🔍 PORTFOLIO INTEL", "📊 BROKERAGE", "⚡ MOMENTUM"])

# --- TAB 1: INDIAN EQUITY (STRICT) ---
with tab1:
    st.subheader("Strictly Indian Equity Market")
    # Concentrated Indian financial news
    market_news = fetch_news('site:moneycontrol.com OR site:economictimes.indiatimes.com "Nifty" OR "Sensex"', 50)
    for n in market_news:
        st.markdown(f'<div class="news-line"><span class="fresh-tag">{n.published[:16]}</span> **[{n.title}]({n.link})**</div>', unsafe_allow_html=True)
        st.markdown("---")

# --- TAB 2: ROLLING PORTFOLIO (NO FILTERS) ---
with tab2:
    st.subheader("Rolling Watchlist Intelligence")
    for name, ticker in STOCKS.items():
        # Fetch 2 most recent headlines per stock for a rolling effect
        s_news = fetch_news(f'"{name}" stock news india', 2)
        for n in s_news:
            st.markdown(f'<div class="news-line"><span class="stock-label">{name}</span> <span class="fresh-tag">{n.published[:16]}</span> **[{n.title}]({n.link})**</div>', unsafe_allow_html=True)
        st.markdown("---")

# --- TAB 3: BROKERAGE ---
with tab3:
    st.subheader("Brokerage Reports & Analyst Calls")
    b_news = fetch_news('("Motilal Oswal" OR "JP Morgan" OR "Jefferies" OR "ICICI Direct") stock report', 50)
    for n in b_news:
        st.markdown(f'<div class="news-line"><span class="fresh-tag">{n.published[:16]}</span> **[{n.title}]({n.link})**</div>', unsafe_allow_html=True)
        st.markdown("---")

# --- TAB 4: MOMENTUM ---
with tab4:
    st.subheader("General Momentum Scan")
    m_news = fetch_news("Indian equity momentum breakout stocks", 50)
    for n in m_news:
        st.markdown(f'<div class="news-line"><span class="fresh-tag">{n.published[:16]}</span> **[{n.title}]({n.link})**</div>', unsafe_allow_html=True)
        st.markdown("---")
