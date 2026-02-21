import streamlit as st
import feedparser
from textblob import TextBlob
from datetime import datetime

# --- 1. EXECUTIVE UI STYLING ---
st.set_page_config(page_title="Equity Intel | Executive Hub", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;700&display=swap');
    
    /* Force Garamond and Midnight Blue */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, span, div, li {
        font-family: 'EB Garamond', serif !important;
        color: #FFFFFF !important;
    }
    .stApp { background-color: #001F3F; }
    
    /* Sentiment Indicators */
    .sentiment-dot {
        height: 10px; width: 10px; border-radius: 50%;
        display: inline-block; margin-right: 8px;
    }
    .dot-green { background-color: #28a745; }
    .dot-red { background-color: #dc3545; }
    .dot-yellow { background-color: #ffc107; }

    /* Ultra-Compact Layout */
    .news-container { margin-bottom: 2px; padding: 0px; }
    .fresh-tag { color: #00FFCC; font-size: 0.8rem; font-weight: bold; }
    hr { margin: 4px 0px !important; opacity: 0.2; }
    
    a { text-decoration: none !important; color: #FFFFFF !important; font-weight: 500; }
    a:hover { color: #FFD700 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC: FRESHNESS & SENTIMENT ---
def get_sentiment(text):
    pol = TextBlob(text).sentiment.polarity
    if pol > 0.1: return "dot-green"
    if pol < -0.1: return "dot-red"
    return "dot-yellow"

def fetch_fresh_news(query, limit=5):
    # 'when:1d' forces Google News to only show results from the last 24 hours
    ts = int(datetime.now().timestamp())
    rss_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}+when:1d&hl=en-IN&gl=IN&ceid=IN:en&t={ts}"
    feed = feedparser.parse(rss_url)
    return feed.entries[:limit]

# --- 3. HEADER ---
c1, c2 = st.columns([4, 1])
with c1:
    st.title("📈 Equity Intelligence Hub")
    st.caption(f"Refreshed: **{datetime.now().strftime('%d %b %H:%M:%S')}** | Focus: Last 24 Hours")
with c2:
    if st.button("🔄 REFRESH NOW"):
        st.rerun()

# --- 4. TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🇮🇳 MARKET", "🔍 WATCHLIST", "📊 BROKERAGE", "⚡ MOMENTUM"])

with tab1:
    st.subheader("Indian Equity Pulse")
    market_query = 'site:moneycontrol.com OR site:economictimes.indiatimes.com "Nifty" OR "Sensex"'
    news = fetch_fresh_news(market_query, 50)
    if not news: st.info("No fresh market news in the last 24h. Expanding search...")
    for n in news:
        dot = get_sentiment(n.title)
        st.markdown(f'<div class="news-container"><span class="sentiment-dot {dot}"></span> **[{n.title}]({n.link})**</div>', unsafe_allow_html=True)
        st.markdown(f'<span class="fresh-tag">{n.published[:16]}</span>', unsafe_allow_html=True)
        st.markdown("---")

with tab2:
    st.subheader("Rolling Watchlist - Last 24h")
    WATCHLIST = ["Patel Engineering", "Bluejet Healthcare", "ITC Hotels", "Lemontree Hotels", 
                 "Sagility", "Rainbow Children Hospital", "Coforge", "Mrs Bectors", 
                 "Gopal Snacks", "Bikaji Foods", "Snowman Logistics", "Varun Beverages"]
    
    for stock in WATCHLIST:
        # We fetch only the freshest 3 items per stock to keep the feed high-quality
        s_news = fetch_fresh_news(f'"{stock}" stock', 3)
        if s_news:
            for n in s_news:
                dot = get_sentiment(n.title)
                st.markdown(f'<div class="news-container"><span class="sentiment-dot {dot}"></span> **{stock.upper()}**: [{n.title}]({n.link})</div>', unsafe_allow_html=True)
                st.caption(n.published[:16])
            st.markdown("---")

# --- (Tab 3 & 4 follow same logic) ---
