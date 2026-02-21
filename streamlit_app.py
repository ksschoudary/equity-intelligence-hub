import streamlit as st
import feedparser
from textblob import TextBlob
from datetime import datetime, timedelta
import pytz  # For IST conversion

# --- 1. EXECUTIVE UI STYLING ---
st.set_page_config(page_title="Equity Intelligence | Live IST View", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, span, div, li {
        font-family: 'EB Garamond', serif !important;
        color: #FFFFFF !important;
    }
    .stApp { background-color: #001F3F; }
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

# --- 2. CORE UTILITIES: IST & FRESHNESS ---
def get_ist_now():
    return datetime.now(pytz.timezone('Asia/Kolkata'))

def get_freshness(published_parsed):
    """Calculates freshness like '2 hours ago' or '1 day ago'"""
    if not published_parsed:
        return "Recent"
    
    # Convert feed timestamp to IST-aware datetime
    pub_dt = datetime(*published_parsed[:6]).replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata'))
    now_ist = get_ist_now()
    diff = now_ist - pub_dt
    
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

def fetch_data(query, count=20):
    ts = int(datetime.now().timestamp())
    url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en&t={ts}"
    return feedparser.parse(url).entries[:count]

# --- 3. HEADER ---
c1, c2 = st.columns([4, 1])
with c1:
    st.title("📈 Equity Intelligence Hub")
    # Displaying Last Updated time in IST
    st.caption(f"Last Updated (IST): **{get_ist_now().strftime('%H:%M:%S')}** | Professional High-Density Feed")
with c2:
    if st.button("🔄 REFRESH NOW"):
        st.rerun()

WATCHLIST = ["Patel Engineering", "Bluejet Healthcare", "ITC Hotels", "Lemontree Hotels", 
             "Sagility", "Rainbow Hospital", "Coforge", "Mrs Bectors", 
             "Gopal Snacks", "Bikaji Foods", "Snowman Logistics", "Varun Beverages"]

# --- 4. TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🇮🇳 MARKET", "🔍 WATCHLIST", "📊 BROKERAGE", "⚡ MOMENTUM"])

# TAB 2: UNIFIED WATCHLIST (FRESHNESS BASIS)
with tab2:
    st.subheader("Unified Portfolio Intelligence (Latest First)")
    all_news = []
    for stock in WATCHLIST:
        s_news = fetch_data(f'"{stock}" stock news india', 5)
        for n in s_news:
            all_news.append({
                "stock": stock, "title": n.title, "link": n.link, 
                "freshness": get_freshness(n.published_parsed if hasattr(n, 'published_parsed') else None),
                "ts": datetime(*n.published_parsed[:6]) if hasattr(n, 'published_parsed') else datetime.now()
            })
    
    all_news.sort(key=lambda x: x['ts'], reverse=True)
    
    for n in all_news[:50]:
        dot = get_sentiment(n['title'])
        st.markdown(f'<div class="news-card"><span class="sentiment-dot {dot}"></span> <span class="stock-label">{n["stock"]}</span> **<a href="{n["link"]}" target="_blank">{n["title"]}</a>**</div>', unsafe_allow_html=True)
        st.caption(f"🕒 {n['freshness']}") # Now showing '2h ago' instead of full date
        st.markdown("---")

# ... (Tab 1, 3, and 4 follow the same pattern)
