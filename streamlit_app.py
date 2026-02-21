import streamlit as st
import feedparser
from textblob import TextBlob
from datetime import datetime, timedelta
import pytz
import streamlit.components.v1 as components

# --- 1. PWA & PAGE CONFIG ---
st.set_page_config(page_title="Equity Intelligence Hub", layout="wide")

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

# --- 2. EXECUTIVE UI STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, span, div, li {
        font-family: 'EB Garamond', serif !important;
        color: #FFFFFF !important;
    }
    .stApp { background-color: #001F3F; }
    .news-line { padding: 2px 0px; line-height: 1.2; }
    .fresh-tag { color: #00FFCC; font-size: 0.85rem; font-weight: bold; margin-right: 10px; }
    .stock-label { color: #FFD700; font-size: 0.85rem; font-weight: bold; text-transform: uppercase; margin-right: 10px; }
    .sentiment-dot { height: 9px; width: 9px; border-radius: 50%; display: inline-block; margin-right: 8px; }
    .dot-green { background-color: #28a745; }
    .dot-red { background-color: #dc3545; }
    .dot-yellow { background-color: #ffc107; }
    hr { margin: 5px 0px !important; border-color: rgba(255, 255, 255, 0.1); }
    a { text-decoration: none !important; color: #FFFFFF !important; }
    a:hover { color: #00FFCC !important; text-decoration: underline !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. UTILITIES ---
def get_ist_now():
    return datetime.now(pytz.timezone('Asia/Kolkata'))

def get_relative_time(pub_parsed):
    if not pub_parsed: return "Recent"
    try:
        pub_dt = datetime(*pub_parsed[:6]).replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata'))
        diff = get_ist_now() - pub_dt
        if diff.days > 0: return f"{diff.days}d ago"
        hours = diff.seconds // 3600
        if hours > 0: return f"{hours}h ago"
        return f"{diff.seconds // 60}m ago"
    except: return "Recent"

def fetch_data(query, count=25):
    # Cache-busting prevents silent data loss
    ts = int(datetime.now().timestamp())
    url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en&t={ts}"
    feed = feedparser.parse(url)
    return feed.entries[:count] if feed.entries else []

# --- 4. HEADER ---
c1, c2 = st.columns([4, 1])
with c1:
    st.title("📈 Equity Intelligence Hub")
    st.caption(f"Last Updated (IST): **{get_ist_now().strftime('%H:%M:%S')}**")
with c2:
    if st.button("🔄 REFRESH NOW"):
        st.rerun()

WATCHLIST = ["Patel Engineering", "Bluejet Healthcare", "ITC Hotels", "Lemontree Hotels", 
             "Sagility", "Rainbow Hospital", "Coforge", "Mrs Bectors", 
             "Gopal Snacks", "Bikaji Foods", "Snowman Logistics", "Varun Beverages"]

# --- 5. TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🇮🇳 MARKET", "🔍 WATCHLIST", "📊 BROKERAGE", "⚡ MOMENTUM"])

# TAB 1: MARKET
with tab1:
    st.subheader("Indian Equity Market Pulse")
    market_news = fetch_data('site:moneycontrol.com OR site:economictimes.indiatimes.com "Nifty" OR "Sensex"', 50)
    if not market_news:
        st.warning("Market feed temporarily unavailable. Try refreshing.")
    for n in market_news:
        pol = TextBlob(n.title).sentiment.polarity
        dot = "dot-green" if pol > 0.1 else "dot-red" if pol < -0.1 else "dot-yellow"
        fresh = get_relative_time(n.published_parsed if hasattr(n, 'published_parsed') else None)
        st.markdown(f'<div class="news-line"><span class="sentiment-dot {dot}"></span> **<a href="{n.link}" target="_blank">{n.title}</a>**</div>', unsafe_allow_html=True)
        st.caption(f"🕒 {fresh} | {n.source.title if 'source' in n else 'Market'}")
        st.markdown("---")

# TAB 2: UNIFIED WATCHLIST (FRESHNESS BASIS)
with tab2:
    st.subheader("Portfolio Intel (Latest First)")
    all_n = []
    for s in WATCHLIST:
        sn = fetch_data(f'"{s}" stock news india', 5)
        for n in sn:
            all_n.append({
                "s": s, "t": n.title, "l": n.link, 
                "f": get_relative_time(n.published_parsed if hasattr(n, 'published_parsed') else None),
                "ts": datetime(*n.published_parsed[:6]) if hasattr(n, 'published_parsed') else datetime.now()
            })
    if not all_n:
        st.info("Scanning for news updates...")
    else:
        all_n.sort(key=lambda x: x['ts'], reverse=True)
        for n in all_n[:50]:
            st.markdown(f'<div class="news-line"><span class="stock-label">{n["s"]}</span> **<a href="{n["l"]}" target="_blank">{n["t"]}</a>**</div>', unsafe_allow_html=True)
            st.caption(f"🕒 {n['f']}")
            st.markdown("---")

# TAB 3: BROKERAGE
with tab3:
    st.subheader("Analyst Reports & Brokerage Pulse")
    # Added broader fallback keywords
    b_news = fetch_data('("Motilal Oswal" OR "JP Morgan" OR "Jefferies" OR "ICICI Direct" OR "target price" OR "stock upgrade") india', 50)
    if not b_news:
        st.info("No brokerage calls detected in the last 24h.")
    for n in b_news:
        fresh = get_relative_time(n.published_parsed if hasattr(n, 'published_parsed') else None)
        st.markdown(f'<div class="news-line">**<a href="{n.link}" target="_blank">{n.title}</a>**</div>', unsafe_allow_html=True)
        st.caption(f"🕒 {fresh}")
        st.markdown("---")

# TAB 4: MOMENTUM
with tab4:
    st.subheader("Market Momentum & Breakouts")
    m_news = fetch_data('"upper circuit" OR "breakout stock" OR "heavy volume" OR "multibagger" india', 50)
    if not m_news:
        st.info("Searching for breakout momentum...")
    for n in m_news:
        fresh = get_relative_time(n.published_parsed if hasattr(n, 'published_parsed') else None)
        st.markdown(f'<div class="news-line">**<a href="{n.link}" target="_blank">{n.title}</a>**</div>', unsafe_allow_html=True)
        st.caption(f"🕒 {fresh}")
        st.markdown("---")
