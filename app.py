import streamlit as st
import os
from combined_fetcher import fetch_all_articles
from summariser import generate_briefing
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="GridScope | GCC Energy Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for executive-grade styling
st.markdown("""
<style>
    /* Main background and font */
    .main { background-color: #0f1117; }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Header styling */
    .gridscope-header {
        background: linear-gradient(135deg, #1a1f2e 0%, #0d1117 100%);
        border-left: 4px solid #f0a500;
        padding: 24px 32px;
        border-radius: 8px;
        margin-bottom: 24px;
    }
    
    .gridscope-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin: 0;
    }
    
    .gridscope-subtitle {
        font-size: 0.95rem;
        color: #8b9ab0;
        margin-top: 4px;
    }

    /* Metric cards */
    .metric-card {
        background: #1a1f2e;
        border: 1px solid #2a3142;
        border-radius: 8px;
        padding: 16px 20px;
        text-align: center;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f0a500;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #8b9ab0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }

    /* Signal to watch box */
    .signal-box {
        background: linear-gradient(135deg, #1a2535 0%, #0d1520 100%);
        border: 1px solid #f0a500;
        border-left: 4px solid #f0a500;
        border-radius: 8px;
        padding: 20px 24px;
        margin: 16px 0;
    }
    
    .signal-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: #f0a500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    /* Development cards */
    .dev-card {
        background: #1a1f2e;
        border: 1px solid #2a3142;
        border-radius: 8px;
        padding: 20px 24px;
        margin: 12px 0;
    }

    /* Sentiment bar */
    .sentiment-bar {
        background: linear-gradient(90deg, #1a2535, #2a3545);
        border-radius: 8px;
        padding: 16px 24px;
        border-left: 4px solid #4a9eff;
        margin: 16px 0;
        font-style: italic;
        color: #c8d4e0;
    }

    /* Section headers */
    .section-header {
        font-size: 0.75rem;
        font-weight: 700;
        color: #8b9ab0;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 24px 0 12px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid #2a3142;
    }

    /* Timestamp badge */
    .timestamp-badge {
        background: #1a1f2e;
        border: 1px solid #2a3142;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.78rem;
        color: #8b9ab0;
        display: inline-block;
    }

    /* Generate button override */
    .stButton > button {
        background: linear-gradient(135deg, #f0a500 0%, #e09400 100%);
        color: #0d1117;
        font-weight: 700;
        font-size: 0.95rem;
        border: none;
        border-radius: 8px;
        padding: 12px 32px;
        letter-spacing: 0.3px;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #ffb520 0%, #f0a500 100%);
        transform: translateY(-1px);
    }

    /* Sidebar styling */
    .css-1d391kg { background-color: #0d1117; }
    
    /* Source pill */
    .source-pill {
        background: #1a1f2e;
        border: 1px solid #2a3142;
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 0.72rem;
        color: #8b9ab0;
        display: inline-block;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if "briefing" not in st.session_state:
    st.session_state.briefing = None
if "articles" not in st.session_state:
    st.session_state.articles = None
if "generated_at" not in st.session_state:
    st.session_state.generated_at = None

# Sidebar
with st.sidebar:
    st.markdown("### ⚡ GridScope")
    st.markdown("---")
    st.markdown("""
**GCC Energy Intelligence**

AI-powered briefings for energy sector executives and strategists operating in Gulf markets.

Built by monitoring live RSS feeds and news sources, then synthesising with Claude AI into structured analyst-grade output.
    """)
    st.markdown("---")
    st.markdown("**Sources monitored**")
    sources = [
        "Financial Times Energy", "Energy Monitor",
        "Carbon Brief", "Oil Price News", "BBC Business",
        "Al Monitor", "PV Tech", "OilPrice.com",
        "The National", "NewsAPI GCC Queries"
    ]
    for s in sources:
        st.markdown(f"<span class='source-pill'>{s}</span>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<span style='font-size:0.78rem; color:#8b9ab0'>Built by Qasim | IE Business School MBA 2025<br>Energy × AI × Strategy</span>", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class='gridscope-header'>
    <div class='gridscope-title'>⚡ GridScope</div>
    <div class='gridscope-subtitle'>GCC Energy Intelligence Briefing &nbsp;·&nbsp; Powered by live news feeds + Claude AI</div>
</div>
""", unsafe_allow_html=True)

# Top metrics row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class='metric-card'>
        <div class='metric-value'>10+</div>
        <div class='metric-label'>Sources Monitored</div>
    </div>""", unsafe_allow_html=True)
with col2:
    article_count = len(st.session_state.articles) if st.session_state.articles else "—"
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{article_count}</div>
        <div class='metric-label'>Articles Analysed</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{datetime.now().strftime('%d %b')}</div>
        <div class='metric-label'>Briefing Date</div>
    </div>""", unsafe_allow_html=True)
with col4:
    status = "Ready" if st.session_state.briefing else "Awaiting"
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{'✓' if st.session_state.briefing else '○'}</div>
        <div class='metric-label'>Briefing Status</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Generate button
col_btn, col_time = st.columns([1, 3])
with col_btn:
    generate_btn = st.button("⚡ Generate Briefing", use_container_width=True)
with col_time:
    if st.session_state.generated_at:
        st.markdown(f"<div style='padding-top:8px'><span class='timestamp-badge'>Last generated: {st.session_state.generated_at}</span></div>", unsafe_allow_html=True)

# Generation logic
if generate_btn:
    with st.spinner("Fetching latest energy intelligence..."):
        articles = fetch_all_articles()
        st.session_state.articles = articles

    if len(articles) == 0:
        st.error("No articles fetched. Check your internet connection.")
    else:
        with st.spinner(f"Synthesising {len(articles)} articles with Claude AI..."):
            briefing = generate_briefing(articles)
            st.session_state.briefing = briefing
            st.session_state.generated_at = datetime.now().strftime("%H:%M · %d %B %Y")
        st.rerun()

# Display briefing
if st.session_state.briefing:
    st.markdown("<div class='section-header'>This Week's Briefing</div>", unsafe_allow_html=True)
    # Ensure --- is always a thematic break, never a setext h2 heading
    briefing_text = st.session_state.briefing.replace('\n---', '\n\n---')
    st.markdown(briefing_text)

    st.markdown("---")

    # Source articles
    with st.expander("📰 View source articles"):
        for a in st.session_state.articles:
            col_s, col_t = st.columns([1, 4])
            with col_s:
                st.markdown(f"<span class='source-pill'>{a['source']}</span>", unsafe_allow_html=True)
            with col_t:
                st.markdown(f"**{a['title']}**")
                st.caption(a['summary'][:200] + "...")
                if a['link']:
                    st.markdown(f"[Read →]({a['link']})")
            st.divider()

    # LinkedIn export
    st.markdown("<div class='section-header'>Export for LinkedIn</div>", unsafe_allow_html=True)
    st.text_area(
        "Copy and paste directly to LinkedIn:",
        value=st.session_state.briefing,
        height=250,
        label_visibility="collapsed"
    )

else:
    # Empty state
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("Click **⚡ Generate Briefing** above to fetch and synthesise the latest GCC energy intelligence.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **What GridScope does**
        
        Monitors 10+ live energy news sources and synthesises them into a structured weekly briefing relevant to GCC markets.
        """)
    with col2:
        st.markdown("""
        **Who it's for**
        
        Energy executives, strategy teams, and investment professionals operating in or targeting Gulf energy markets.
        """)
    with col3:
        st.markdown("""
        **How to use it**
        
        Click Generate Briefing. Review the three developments and signal to watch. Export directly to LinkedIn.
        """)