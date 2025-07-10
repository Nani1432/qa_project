import streamlit as st
from scraper import get_website_content
from qa_system import QASystem

# Page setup
st.set_page_config(page_title="Dynamic Website Q&A", layout="centered")
st.title("🌐 Web Q&A with Ollama")

# Session state init
if "qa" not in st.session_state:
    st.session_state.qa = QASystem()
    st.session_state.content_loaded = False
    st.session_state.last_url = None

# URL input
url = st.text_input("Enter a website URL to ask questions about:", placeholder="https://example.com")

# Button to scrape and process
if st.button("Load Website Content"):
    if url:
        with st.spinner("Scraping and processing..."):
            try:
                content = get_website_content(url)
                st.session_state.qa.process_content(content)
                st.session_state.content_loaded = True
                st.session_state.last_url = url
                st.success("Website loaded and ready for questions!")
            except Exception as e:
                st.session_state.content_loaded = False
                st.error(f"Failed to load content: {str(e)}")
    else:
        st.warning("Please enter a valid URL.")

# Question input
if st.session_state.content_loaded and url == st.session_state.last_url:
    question = st.text_input("Ask a question about the page:")
    if question:
        with st.spinner("Thinking..."):
            try:
                answer = st.session_state.qa.ask(question)
                st.markdown(f"**Answer:** {answer}")
                st.caption("🔍 Answer generated from scraped content")
            except Exception as e:
                st.error(f"Error: {str(e)}")
