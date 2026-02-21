import streamlit as st
import feedparser
from textblob import TextBlob
from datetime import datetime

# --- 1. EXECUTIVE UI STYLING (Garamond & Midnight Blue) ---
st.set_page_config(page_title="Equity Intelligence Hub", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, span, div, li {
        font-family: 'EB Garamond', serif !important;
        color: #FFFFFF !important;
    }
    .stApp { background-color: #001F3F; }
    
    /* COMPACT SPACING & NEWS CARD */
    .news-card { padding: 4px 0px; margin-bottom: 2px; line-height: 1.3; }
    .fresh-tag { color: #00FFCC; font-size: 0.85rem; font-weight: bold; margin-right: 10px; }
    .stock-label { color: #FFD700; font-size: 0.85rem; font-weight: bold; text-transform: uppercase; margin-right: 10px; }
    .sentiment-dot { height: 9px; width: 9px; border-radius: 50%; display: inline-block; margin-right: 8px; }
    .dot-green { background-color: #28a745; }
    .dot-red { background-color: #dc3545; }
    .dot-yellow { background-color: #ffc107; }
    
    hr { margin: 6px 0px !important; border-color: rgba(255, 255, 255, 0.1); }
    a { text-decoration: none !important; color: #FFFFFF !important; }
    a:hover { color: #00FFCC !important; text-decoration: underline !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE UTILITIES ---
def get_sentiment(text):
    pol = TextBlob(text).sentiment.polarity
    if pol > 0.1: return "dot-green"
    if pol < -0.1: return "dot-red"
    return "dot-yellow"

def fetch_data(query, count=20):
    # Cache-busting with timestamp to bypass stale results
    ts = int(datetime.now().timestamp())
    url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en&t={ts}"
    return feedparser.parse(url).entries[:count]

# --- 3. HEADER & WATCHLIST ---
c1, c2 = st.columns([4, 1])
with c1:
    st.title("📈 Equity Intelligence Hub")
    st.caption(f"Refreshed: **{datetime.now().strftime('%H:%M:%S')}** | Professional High-Density Feed")
with c2:
    if st.button("🔄 REFRESH NOW"):
        st.rerun()

WATCHLIST = [
    "Patel Engineering", "Bluejet Healthcare", "ITC Hotels", "Lemontree Hotels", 
    "Sagility", "Rainbow Hospital", "Coforge", "Mrs Bectors", 
    "Gopal Snacks", "Bikaji Foods", "Snowman Logistics", "Varun Beverages"
]

# --- 4. TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🇮🇳 MARKET", "🔍 WATCHLIST", "📊 BROKERAGE", "⚡ MOMENTUM"])

# TAB 1: MARKET
with tab1:
    st.subheader("Indian Equity Market Pulse")
    news = fetch_data('site:moneycontrol.com OR site:economictimes.indiatimes.com "Nifty" OR "Sensex"', 50)
    for n in news:
        dot = get_sentiment(n.title)
        # Using HTML <a> tag to prevent Markdown URL leakage
        st.markdown(f'<div class="news-card"><span class="sentiment-dot {dot}"></span> **<a href="{n.link}" target="_blank">{n.title}</a>**</div>', unsafe_allow_html=True)
        st.caption(f"{n.published[:16]} | {n.source.title if 'source' in n else 'Market'}")
        st.markdown("---")

# TAB 2: UNIFIED WATCHLIST (FRESHNESS ONLY)
with tab2:
    st.subheader("Unified Portfolio Intelligence (Latest First)")
    all_news = []
    # Collect news for all 12 stocks
    for stock in WATCHLIST:
        s_news = fetch_data(f'"{stock}" stock news india', 5)
        for n in s_news:
            all_news.append({
                "stock": stock, "title": n.title, "link": n.link, "date": n.published,
                "ts": datetime(*n.published_parsed[:6]) if hasattr(n, 'published_parsed') else datetime.now()
            })
    
    # Sort entire bucket by absolute timestamp (newest at top)
    all_news.sort(key=lambda x: x['ts'], reverse=True)
    
    for n in all_news[:50]:
        dot = get_sentiment(n['title'])
        st.markdown(f'<div class="news-card"><span class="sentiment-dot {dot}"></span> <span class="stock-label">{n["stock"]}</span> **<a href="{n["link"]}" target="_blank">{n["title"]}</a>**</div>', unsafe_allow_html=True)
        st.caption(f"🕒 {n['date'][:16]}")
        st.markdown("---")

# TAB 3 & 4 (BROKERAGE & MOMENTUM)
with tab3:
    st.subheader("Brokerage Reports & Analyst Intel")
    news = fetch_data('("Motilal Oswal" OR "JP Morgan" OR "Jefferies" OR "ICICI Direct") report india', 50)
    for n in news:
        dot = get_sentiment(n.title)
        st.markdown(f'<div class="news-card"><span class="sentiment-dot {dot}"></span> **<a href="{n.link}" target="_blank">{n.title}</a>**</div>', unsafe_allow_html=True)
        st.caption(f"{n.published[:16]}")
        st.markdown("---")

with tab4:
    st.subheader("Market Momentum & Breakouts")
    news = fetch_data('"upper circuit" OR "breakout stock" OR "heavy volume" india', 50)
    for n in news:
        dot = get_sentiment(n.title)
        st.markdown(f'<div class="news-card"><span class="sentiment-dot {dot}"></span> **<a href="{n.link}" target="_blank">{n.title}</a>**</div>', unsafe_allow_html=True)
        st.caption(f"{n.published[:16]}")
        st.markdown("---")
