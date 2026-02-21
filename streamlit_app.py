import streamlit as st
import feedparser
from textblob import TextBlob
from datetime import datetime

# --- 1. EXECUTIVE UI STYLING (Garamond & Midnight Blue) ---
st.set_page_config(page_title="Equity Intelligence | Executive View", layout="wide")

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
    
    .sentiment-dot {
        height: 10px; width: 10px; border-radius: 50%;
        display: inline-block; margin-right: 8px;
    }
    .dot-green { background-color: #28a745; }
    .dot-red { background-color: #dc3545; }
    .dot-yellow { background-color: #ffc107; }
    
    /* COMPACT SPACING */
    .stMarkdown { margin-bottom: -10px !important; }
    hr { margin: 6px 0px !important; border-color: rgba(255,255,255,0.1); }
    
    .news-line { font-size: 1.05rem; line-height: 1.2; }
    .meta-text { font-size: 0.8rem; color: #00FFCC !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE UTILITIES ---
def get_sentiment_dot(text):
    try:
        pol = TextBlob(text).sentiment.polarity
        if pol > 0.1: return "dot-green"
        if pol < -0.1: return "dot-red"
    except:
        pass
    return "dot-yellow"

def fetch_fresh_news(query, limit=50):
    # Adding a timestamp bypasses stale caches for maximum freshness
    ts = int(datetime.now().timestamp())
    rss_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en&t={ts}"
    feed = feedparser.parse(rss_url)
    return feed.entries[:limit]

# --- 3. REFRESH HEADER ---
c1, c2 = st.columns([4, 1])
with c1:
    st.title("📈 Equity Intelligence Hub")
    st.caption(f"Last Refreshed: **{datetime.now().strftime('%H:%M:%S')}**")
with c2:
    if st.button("🔄 REFRESH NOW"):
        st.rerun()

# --- 4. TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🇮🇳 MARKET", "🔍 WATCHLIST", "📊 BROKERAGE", "⚡ MOMENTUM"])

# --- TAB 1: STRICT INDIAN EQUITY ---
with tab1:
    st.subheader("Indian Equity Market - Live Pulse")
    market_query = 'site:moneycontrol.com OR site:economictimes.indiatimes.com "Nifty" OR "Sensex"'
    news = fetch_fresh_news(market_query, 50)
    for n in news:
        dot = get_sentiment_dot(n.title)
        st.markdown(f'<div class="news-line"><span class="sentiment-dot {dot}"></span> **[{n.title}]({n.link})**</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="meta-text">{n.published[:16]} | {n.source.title if "source" in n else "Market"}</div>', unsafe_allow_html=True)
        st.markdown("---")

# --- TAB 2: ROLLING PORTFOLIO (12 STOCKS) ---
with tab2:
    st.subheader("Stock-Wise Intelligence (Rolling Feed)")
    WATCHLIST = [
        "Patel Engineering", "Bluejet Healthcare", "ITC Hotels", "Lemontree Hotels", 
        "Sagility", "Rainbow Children Hospital", "Coforge", "Mrs Bectors", 
        "Gopal Snacks", "Bikaji Foods", "Snowman Logistics", "Varun Beverages"
    ]
    
    for stock in WATCHLIST:
        # Fetching top 3 news items for every stock for maximum coverage
        stock_news = fetch_fresh_news(f'"{stock}" stock news india', 3)
        for n in stock_news:
            dot = get_sentiment_dot(n.title)
            st.markdown(f'<div class="news-line"><span class="sentiment-dot {dot}"></span> **{stock.upper()}**: [{n.title}]({n.link})</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="meta-text">{n.published[:16]}</div>', unsafe_allow_html=True)
        st.markdown("---")

# --- TAB 3: BROKERAGE INTELLIGENCE ---
with tab3:
    st.subheader("Brokerage Reports & Analyst Calls")
    brokerage_query = '("Motilal Oswal" OR "JP Morgan" OR "Jefferies" OR "ICICI Direct") stock report'
    news = fetch_fresh_news(brokerage_query, 50)
    for n in news:
        dot = get_sentiment_dot(n.title)
        st.markdown(f'<div class="news-line"><span class="sentiment-dot {dot}"></span> **[{n.title}]({n.link})**</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="meta-text">{n.published[:16]}</div>', unsafe_allow_html=True)
        st.markdown("---")

# --- TAB 4: MOMENTUM ---
with tab4:
    st.subheader("Web Momentum & Search Hits")
    # Capturing broader search momentum
    news = fetch_fresh_news("Indian equity breakout stocks momentum", 50)
    for n in news:
        dot = get_sentiment_dot(n.title)
        st.markdown(f'<div class="news-line"><span class="sentiment-dot {dot}"></span> **[{n.title}]({n.link})**</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="meta-text">{n.published[:16]}</div>', unsafe_allow_html=True)
        st.markdown("---")
