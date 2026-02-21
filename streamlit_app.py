import streamlit as st
import feedparser
from textblob import TextBlob
from datetime import datetime

# --- 1. PROFESSIONAL UI & GARAMOND STYLING ---
st.set_page_config(page_title="Equity Intel | Executive High-Coverage", layout="wide")

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
    hr { margin: 5px 0px !important; border-color: rgba(255,255,255,0.1); }
    .compact-text { font-size: 1rem; line-height: 1.2; margin-bottom: 2px; }
    .source-text { font-size: 0.8rem; color: #00FFCC !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE LOGIC ---
def get_sentiment(text):
    pol = TextBlob(text).sentiment.polarity
    if pol > 0.1: return "dot-green"
    elif pol < -0.1: return "dot-red"
    return "dot-yellow"

def fetch_fresh_news(query, count=50):
    # Appending a timestamp to the query forces the RSS to bypass any caching
    ts = int(datetime.now().timestamp())
    url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en&t={ts}"
    return feedparser.parse(url).entries[:count]

# --- 3. REFRESH HEADER ---
c1, c2 = st.columns([4, 1])
with c1:
    st.title("📈 Equity Intelligence Hub")
    st.caption(f"Status: **Live Updates** | Last Refreshed: {datetime.now().strftime('%H:%M:%S')}")
with c2:
    if st.button("🔄 REFRESH NOW"):
        st.rerun()

# --- 4. TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🇮🇳 MARKET", "🔍 PORTFOLIO", "📊 BROKERAGE", "⚡ MOMENTUM"])

# --- TAB 1: STRICT INDIAN EQUITY (High Density) ---
with tab1:
    # Strictly Indian sources and market keywords
    m_news = fetch_fresh_news('site:moneycontrol.com OR site:economictimes.indiatimes.com "Nifty" OR "Sensex"', 50)
    for n in m_news:
        dot = get_sentiment(n.title)
        st.markdown(f'<div class="compact-text"><span class="sentiment-dot {dot}"></span> **[{n.title}]({n.link})**</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="source-text">{n.published[:16]} | {n.source.title if "source" in n else "Market"}</div>', unsafe_allow_html=True)
        st.markdown("---")

# --- TAB 2: ROLLING PORTFOLIO (12 Stocks - Max Coverage) ---
with tab2:
    STOCKS = ["Patel Engineering", "Bluejet Healthcare", "ITC Hotels", "Lemontree Hotels", 
              "Sagility", "Rainbow Children Hospital", "Coforge", "Mrs Bectors", 
              "Gopal Snacks", "Bikaji Foods", "Snowman Logistics", "Varun Beverages"]
    
    for stock in STOCKS:
        s_news = fetch_fresh_news(f'"{stock}" stock news india', 3) # Shows top 3 fresh hits per stock
        if s_news:
            for n in s_news:
                dot = get_sentiment(n.title)
                st.markdown(f'<div class="compact-text"><span class="sentiment-dot {dot}"></span> **{stock.upper()}**: [{n.title}]({n.link})</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="source-text">{n.published[:16]}</div>', unsafe_allow_html=True)
            st.markdown("---")

# --- TAB 3 & 4 (BROKERAGE & MOMENTUM) ---
# ... (Follows same high-density logic as Tab 1)
