import streamlit as st
import feedparser
from textblob import TextBlob
from datetime import datetime, timedelta
import pytz
import streamlit.components.v1 as components

# --- 1. PWA INJECTION & PAGE CONFIG ---
st.set_page_config(page_title="Equity Intelligence Hub", layout="wide")

# This links your manifest.json and sw.js to make the app installable
components.html(
    f"""
    <link rel="manifest" href="/manifest.json">
    <script>
      if ('serviceWorker' in navigator) {{
        navigator.serviceWorker.register('/sw.js');
      }}
    </script>
    """,
    height=0,
)

# --- 2. EXECUTIVE UI STYLING (EB Garamond & Midnight Blue) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, span, div, li {
        font-family: 'EB Garamond', serif !important;
        color: #FFFFFF !important;
    }
    .stApp { background-color: #001F3F; }
    
    /* COMPACT SPACING */
    .stMarkdown, .element-container { margin-bottom: -12px !important; }
    hr { margin: 8px 0px !important; border-color: rgba(255, 255, 255, 0.1); }

    .news-line { padding: 4px 0px; line-height: 1.3; }
    .fresh-tag { color: #00FFCC; font-size: 0.85rem; font-weight: bold; margin-right: 10px; }
    .stock-label { color: #FFD700; font-size: 0.85rem; font-weight: bold; text-transform: uppercase; margin-right: 10px; }
    .sentiment-dot { height: 9px; width: 9px; border-radius: 50%; display: inline-block; margin-right: 8px; }
    .dot-green { background-color: #28a745; }
    .dot-red { background-color: #dc3545; }
    .dot-yellow { background-color: #ffc107; }
    
    a { text-decoration: none !important; color: #FFFFFF !important; }
    a:hover { color: #00FFCC !important; text-decoration: underline !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE UTILITIES: IST & FRESHNESS ---
def get_ist_now():
    return datetime.now(pytz.timezone('Asia/Kolkata'))

def get_relative_time(published_parsed):
    """Converts RSS time to human-readable IST relative time"""
    if not published_parsed:
        return "Recent"
    # Convert UTC feed time to IST
    pub_dt = datetime(*published_parsed[:6]).replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata'))
    diff = get_ist_now() - pub_dt
    
    if diff.days > 0:
        return f"{diff.days}d ago"
    hours = diff.seconds // 3600
    if hours > 0:
        return f"{hours}h ago"
    minutes = (diff.seconds % 3600) // 60
    return f"{minutes}m ago"

def get_sentiment(text):
    pol = TextBlob(text).sentiment.polarity
    if pol > 0.1: return "dot-green"
    if pol < -0.1: return "dot-red"
    return "dot-yellow"

def fetch_data(query, count=25):
    ts = int(datetime.now().timestamp())
    url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en&t={ts}"
    return feedparser.parse(url).entries[:count]

# --- 4. HEADER ---
c1, c2 = st.columns([4, 1])
with c1:
    st.title("📈 Equity Intelligence Hub")
    st.caption(f"Last Updated (IST): **{get_ist_now().strftime('%H:%M:%S')}** | Executive High-Density Feed")
with c2:
    if st.button("🔄 REFRESH NOW"):
        st.rerun()

WATCHLIST = [
    "Patel Engineering", "Bluejet Healthcare", "ITC Hotels", "Lemontree Hotels", 
    "Sagility", "Rainbow Hospital", "Coforge", "Mrs Bectors", 
    "Gopal Snacks", "Bikaji Foods", "Snowman Logistics", "Varun Beverages"
]

# --- 5. TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🇮🇳 MARKET", "🔍 WATCHLIST", "📊 BROKERAGE", "⚡ MOMENTUM"])

# TAB 1: MARKET
with tab1:
    st.subheader("Indian Equity Market Pulse")
    market_news = fetch_data('site:moneycontrol.com OR site:economictimes.indiatimes.com "Nifty" OR "Sensex"', 50)
    for n in market_news:
        dot = get_sentiment(n.title)
        fresh = get_relative_time(n.published_parsed if hasattr(n, 'published_parsed') else None)
        st.markdown(f'<div class="news-line"><span class="sentiment-dot {dot}"></span> **<a href="{n.link}" target="_blank">{n.title}</a>**</div>', unsafe_allow_html=True)
        st.caption(f"🕒 {fresh} | {n.source.title if 'source' in n else 'Market'}")
        st.markdown("---")

# TAB 2: UNIFIED WATCHLIST (FRESHNESS BASIS)
with tab2:
    st.subheader("Unified Portfolio Intelligence (Latest First)")
    all_news = []
    for stock in WATCHLIST:
        s_news = fetch_data(f'"{stock}" stock news india', 5)
        for n in s_news:
            all_news.append({
                "stock": stock, "title": n.title, "link": n.link, 
                "fresh": get_relative_time(n.published_parsed if hasattr(n, 'published_parsed') else None),
                "ts": datetime(*n.published_parsed[:6]) if hasattr(n, 'published_parsed') else datetime.now()
            })
    # Sort strictly by timestamp (newest first)
    all_news.sort(key=lambda x: x['ts'], reverse=True)
    
    for n in all_news[:50]:
        dot = get_sentiment(n['title'])
        st.markdown(f'<div class="news-line"><span class="sentiment-dot {dot}"></span> <span class="stock-label">{n["stock"]}</span> **<a href="{n["link"]}" target="_blank">{n["title"]}</a>**</div>', unsafe_allow_html=True)
        st.caption(f"🕒 {n['fresh']}")
        st.markdown("---")

# TAB 3: BROKERAGE
with tab3:
    st.subheader("Analyst Reports & Brokerage Pulse")
    b_news = fetch_data('("Motilal Oswal" OR "JP Morgan" OR "Jefferies" OR "ICICI Direct" OR "target price") india', 50)
    for n in b_news:
        dot = get_sentiment(n.title)
        fresh = get_relative_time(n.published_parsed if hasattr(n, 'published_parsed') else None)
        st.markdown(f'<div class="news-card"><span class="sentiment-dot {dot}"></span> **<a href="{n.link}" target="_blank">{n.title}</a>**</div>', unsafe_allow_html=True)
        st.caption(f"🕒 {fresh}")
        st.markdown("---")

# TAB 4: MOMENTUM
with tab4:
    st.subheader("Market Momentum & Breakouts")
    m_news = fetch_data('"upper circuit" OR "breakout stock" OR "heavy volume" india', 50)
    for n in m_news:
        dot = get_sentiment(n.title)
        fresh = get_relative_time(n.published_parsed if hasattr(n, 'published_parsed') else None)
        st.markdown(f'<div class="news-card"><span class="sentiment-dot {dot}"></span> **<a href="{n.link}" target="_blank">{n.title}</a>**</div>', unsafe_allow_html=True)
        st.caption(f"🕒 {fresh}")
        st.markdown("---")
