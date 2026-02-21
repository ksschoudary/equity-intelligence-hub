import streamlit as st
import feedparser
from textblob import TextBlob
from datetime import datetime

# --- 1. EXECUTIVE UI STYLING ---
st.set_page_config(page_title="Equity Intel | Executive View", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, span, div, li {
        font-family: 'EB Garamond', serif !important;
        color: #FFFFFF !important;
    }
    .stApp { background-color: #001F3F; }
    
    /* CLEAN COMPACT LAYOUT */
    .news-card { padding: 4px 0px; margin-bottom: 2px; }
    .fresh-tag { color: #00FFCC; font-size: 0.8rem; font-weight: bold; }
    .sentiment-dot { height: 8px; width: 8px; border-radius: 50%; display: inline-block; margin-right: 6px; }
    .dot-green { background-color: #28a745; }
    .dot-red { background-color: #dc3545; }
    .dot-yellow { background-color: #ffc107; }
    
    hr { margin: 6px 0px !important; border-color: rgba(255, 255, 255, 0.1); }
    a { text-decoration: none !important; color: #FFFFFF !important; }
    a:hover { color: #FFD700 !important; text-decoration: underline !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE UTILITIES ---
def analyze_sentiment(text):
    pol = TextBlob(text).sentiment.polarity
    if pol > 0.1: return "dot-green"
    if pol < -0.1: return "dot-red"
    return "dot-yellow"

def fetch_data(query, count=50):
    # Cache-busting with timestamp
    ts = int(datetime.now().timestamp())
    url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en&t={ts}"
    return feedparser.parse(url).entries[:count]

# --- 3. HEADER & WATCHLIST ---
c1, c2 = st.columns([4, 1])
with c1:
    st.title("📈 Equity Intelligence Hub")
    st.caption(f"Refreshed: {datetime.now().strftime('%H:%M:%S')} | **Real-Time Portfolio Intelligence**")
with c2:
    if st.button("🔄 REFRESH NOW"):
        st.rerun()

STOCKS = ["Patel Engineering", "Bluejet Healthcare", "ITC Hotels", "Lemontree Hotels", 
          "Sagility", "Rainbow Hospital", "Coforge", "Mrs Bectors", 
          "Gopal Snacks", "Bikaji Foods", "Snowman Logistics", "Varun Beverages"]

# --- 4. TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🇮🇳 MARKET", "🔍 WATCHLIST", "📊 BROKERAGE", "⚡ MOMENTUM"])

# TAB 1: MARKET
with tab1:
    st.subheader("Indian Equity Market Pulse")
    market_news = fetch_data('site:moneycontrol.com OR site:economictimes.indiatimes.com "Nifty" OR "Sensex"', 50)
    for n in market_news:
        dot = analyze_sentiment(n.title)
        st.markdown(f'<span class="sentiment-dot {dot}"></span> **[{n.title}]({n.link})**', unsafe_allow_html=True)
        st.caption(f"{n.published[:16]} | {n.source.title if 'source' in n else 'Market'}")
        st.markdown("---")

# TAB 2: WATCHLIST (Rolling Coverage)
with tab2:
    st.subheader("Rolling Portfolio Intelligence")
    for s in STOCKS:
        s_news = fetch_data(f'"{s}" stock news india', 3)
        for n in s_news:
            dot = analyze_sentiment(n.title)
            st.markdown(f'<span class="sentiment-dot {dot}"></span> **{s.upper()}**: [{n.title}]({n.link})', unsafe_allow_html=True)
            st.caption(f"{n.published[:16]}")
        st.markdown("---")

# TAB 3: BROKERAGE (Broader Search to avoid empty tab)
with tab3:
    st.subheader("Analyst Upgrades & Brokerage Reports")
    # Added broader terms like 'target price' and 'buy sell'
    b_news = fetch_data('("Motilal Oswal" OR "JP Morgan" OR "Jefferies" OR "ICICI Direct" OR "target price" OR "stock upgrade") india', 50)
    if b_news:
        for n in b_news:
            dot = analyze_sentiment(n.title)
            st.markdown(f'<span class="sentiment-dot {dot}"></span> **[{n.title}]({n.link})**', unsafe_allow_html=True)
            st.caption(f"{n.published[:16]}")
            st.markdown("---")
    else:
        st.info("No brokerage news in the current window.")

# TAB 4: MOMENTUM (High Volatility Hits)
with tab4:
    st.subheader("Market Momentum & High Volume Hits")
    # Capturing buzzwords like 'upper circuit' and 'breakout'
    m_news = fetch_data('"upper circuit" OR "multibagger" OR "breakout stock" OR "heavy volume" india', 50)
    for n in m_news:
        dot = analyze_sentiment(n.title)
        st.markdown(f'<span class="sentiment-dot {dot}"></span> **[{n.title}]({n.link})**', unsafe_allow_html=True)
        st.caption(f"{n.published[:16]}")
        st.markdown("---")
