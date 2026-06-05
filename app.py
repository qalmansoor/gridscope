import streamlit as st
import anthropic
import os
from combined_fetcher import fetch_all_articles as fetch_articles
from summariser import generate_briefing
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="GridScope | GCC Energy Intelligence",
    page_icon="⚡",
    layout="wide"
)

# Header
st.title("⚡ GridScope")
st.subheader("GCC Energy Intelligence Briefing")
st.caption(f"Powered by live RSS feeds + Claude AI | Last generated: {datetime.now().strftime('%A, %d %B %Y')}")

st.divider()

# Session state — stores the briefing so it persists between button clicks
if "briefing" not in st.session_state:
    st.session_state.briefing = None
if "articles" not in st.session_state:
    st.session_state.articles = None
if "generated_at" not in st.session_state:
    st.session_state.generated_at = None

# Sidebar
with st.sidebar:
    st.header("About GridScope")
    st.write(
        "GridScope is an AI-powered weekly intelligence tool that monitors "
        "global energy news and produces structured briefings relevant to "
        "GCC energy markets, utilities, and national energy strategies."
    )
    st.divider()
    st.write("**Sources monitored:**")
    st.write("- BBC Business")
    st.write("- Financial Times Energy")
    st.write("- Energy Monitor")
    st.write("- Carbon Brief")
    st.write("- Oil Price News")
    st.divider()
    st.write("Built by Qasim | IE Business School MBA 2025")

# Main generate button
col1, col2 = st.columns([1, 3])
with col1:
    generate_btn = st.button(
        "🔄 Generate Briefing",
        type="primary",
        use_container_width=True
    )

# When button is clicked
if generate_btn:
    with st.spinner("Fetching latest energy news..."):
        articles = fetch_articles()
        st.session_state.articles = articles

    if len(articles) == 0:
        st.error("No articles fetched. Check your internet connection or RSS feeds.")
    else:
        with st.spinner(f"Analysing {len(articles)} articles with Claude..."):
            briefing = generate_briefing(articles)
            st.session_state.briefing = briefing
            st.session_state.generated_at = datetime.now().strftime("%H:%M, %d %B %Y")

# Display briefing if it exists
if st.session_state.briefing:
    st.success(f"Briefing generated at {st.session_state.generated_at} from {len(st.session_state.articles)} articles")

    st.divider()

    # Display the briefing text
    st.markdown(st.session_state.briefing)

    st.divider()

    # Source articles expander
    with st.expander("📰 View source articles used"):
        for a in st.session_state.articles:
            st.markdown(f"**[{a['source']}] {a['title']}**")
            st.caption(f"Published: {a['published']}")
            st.write(a['summary'][:200] + "...")
            if a['link']:
                st.markdown(f"[Read full article]({a['link']})")
            st.divider()

    # Copy to clipboard section
    st.subheader("📋 Export for LinkedIn")
    st.text_area(
        "Copy this briefing to post on LinkedIn:",
        value=st.session_state.briefing,
        height=300
    )

else:
    # Empty state
    st.info("Click **Generate Briefing** to fetch the latest GCC energy intelligence.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Sources Monitored", "5")
    with col2:
        st.metric("Articles Per Run", "~15")
    with col3:
        st.metric("Analysis Model", "Claude")