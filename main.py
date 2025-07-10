import streamlit as st
from scraper import get_website_content
from qa_system import QASystem

# Initialize
if "qa" not in st.session_state:
    st.session_state.qa = QASystem()
    st.session_state.content_loaded = False

# Load Content
url = "https://medicasapp.com/in"  # Your exact URL
if not st.session_state.content_loaded:
    with st.spinner("Loading website content..."):
        content = get_website_content(url)
        st.session_state.qa.process_content(content)
        st.session_state.content_loaded = True

# Q&A Interface
st.title("MedicasApp Q&A")
question = st.text_input("Ask about any service:")

if question:
    with st.spinner("Searching for answer..."):
        answer = st.session_state.qa.ask(question)
        st.markdown(f"**Answer:** {answer}")
        st.caption("Answer generated from exact webpage content")