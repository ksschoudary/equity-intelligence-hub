import streamlit as st
import feedparser
from textblob import TextBlob
from datetime import datetime
import time

# --- 1. EXECUTIVE UI & AUTO-REFRESH ---
st.set_page_config(page_title="Equity Intel | Live Executive View", layout="wide")

# This forces the app to refresh every 15 minutes (900,000 milliseconds)
# Note: You may need to install 'streamlit-autorefresh' or just use this manual button
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, span, div, li {
        font-family: 'EB Garamond', serif !important;
        color: #FFFFFF !important;
    }
    .stApp { background-color: #001F3F; }
    .sentiment-dot { height: 10px; width: 10px; border-radius: 50%; display: inline-block; margin-right: 8px; }
    .dot-green { background-color: #28a745; }
    .dot-red { background-color: #dc3545; }
    .dot-yellow { background-color: #ffc107; }
    hr { margin: 8px 0px !important; border-color: rgba(255,255,255,0.1); }
    .stButton>button { background-color: #1a3a5a; color: white; border: 1px solid #00FFCC; font-family: 'EB Garamond'; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC: SENTIMENT & FETCH ---
def get_sentiment_color(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0.1:
        return "dot-green"
    elif analysis.sentiment.polarity < -0.1:
        return "dot-red"
    else:
        return "dot-yellow"

def fetch_news(query, count=50):
    url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en"
    return feedparser.parse(url).entries[:count]

# --- 3. REFRESH & TIMESTAMP HEADER ---
col_t, col_b = st.columns([4, 1])
with col_t:
    st.title("📈 Equity Intelligence Hub")
    st.caption(f"Last Refreshed: **{datetime.now().strftime('%H:%M:%S')}**")
with col_b:
    if st.button("🔄 Refresh Now"):
        st.rerun()

# --- 4. PORTFOLIO CONFIG ---
STOCKS = {
    "Patel Eng": "PATELENG.NS", "Bluejet": "BLUEJET.NS", "ITC Hotels": "ITCHOTELS.NS",
    "Lemontree": "LEMONTREE.NS", "Sagility": "SAGILITY.NS", "Rainbow": "RAINBOW.NS",
    "Coforge": "COFORGE.NS", "Mrs Bectors": "BECTORS.NS", "Gopal Snacks": "GOPAL.NS",
    "Bikaji": "BIKAJI.NS", "Snowman": "SNOWMAN.NS", "Varun Bev": "VBL.NS"
}

# --- 5. TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🇮🇳 MARKET", "🔍 WATCHLIST", "📊 BROKERAGE", "⚡ MOMENTUM"])

# --- TAB 1: MARKET ---
with tab1:
    market_news = fetch_news('site:moneycontrol.com OR site:economictimes.indiatimes.com "Nifty" OR "Sensex"', 50)
    for n in market_news:
        dot = get_sentiment_color(n.title)
        st.markdown(f'<span class="sentiment-dot {dot}"></span> **[{n.title}]({n.link})**', unsafe_allow_html=True)
        st.caption(f"{n.published[:16]} | {n.source.title if 'source' in n else 'Market'}")
        st.markdown("---")

# --- TAB 2: ROLLING WATCHLIST ---
with tab2:
    for name, ticker in STOCKS.items():
        s_news = fetch_news(f'"{name}" stock news india', 2)
        for n in s_news:
            dot = get_sentiment_color(n.title)
            st.markdown(f'<span class="sentiment-dot {dot}"></span> **{name.upper()}**: [{n.title}]({n.link})', unsafe_allow_html=True)
            st.caption(f"{n.published[:16]}")
        st.markdown("---")

# --- TAB 3: BROKERAGE ---
with tab3:
    b_news = fetch_news('("Motilal Oswal" OR "JP Morgan" OR "Jefferies" OR "ICICI Direct") report', 50)
    for n in b_news:
        dot = get_sentiment_color(n.title)
        st.markdown(f'<span class="sentiment-dot {dot}"></span> **[{n.title}]({n.link})**', unsafe_allow_html=True)
        st.caption(f"{n.published[:16]}")
        st.markdown("---")

# --- TAB 4: MOMENTUM ---
with tab4:
    m_news = fetch_news("Indian equity breakout momentum", 50)
    for n in m_news:
        dot = get_sentiment_color(n.title)
        st.markdown(f'<span class="sentiment-dot {dot}"></span> **[{n.title}]({n.link})**', unsafe_allow_html=True)
        st.caption(f"{n.published[:16]}")
        st.markdown("---")
