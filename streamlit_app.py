# --- SEGMENT 3: BROKERAGE EXCLUSIVE ---
with tab3:
    st.header("Brokerage & Analyst Reports")
    firms = ["Motilal Oswal", "JP Morgan", "Jefferies", "ICICI Direct", "Goldman Sachs", "Investec"]
    
    st.info("Filtering market feeds for brokerage mentions...")
    if "feed" in data:
        for item in data["feed"]:
            # Check if any brokerage firm is mentioned in the title
            if any(firm.lower() in item['title'].lower() for firm in firms):
                st.success(f"**{item['title']}**")
                # FIXED: Added the missing closing quote and parenthesis below
                st.link_button("View Analysis", item['url'])
                st.divider()

# --- SEGMENT 4: MOMENTUM (SEARCH SCRAPER) ---
with tab4:
    st.header("Web Momentum & Search Hits")
    selected_moment = st.selectbox("Pick a company:", STOCKS_RAW)
    
    query = f"{selected_moment} stock latest news"
    rss_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en"
    
    feed = feedparser.parse(rss_url)
    if feed.entries:
        for entry in feed.entries[:10]:
            with st.container():
                st.markdown(f"**{entry.title}**")
                st.caption(f"Source: {entry.source.title if 'source' in entry else 'Web'}")
                # FIXED: Ensuring all links are properly closed
                st.link_button("View Search Hit", entry.link)
                st.divider()
