import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="AI Estimating Assistant",
    page_icon="🏗️",
    layout="wide"
)

st.title("AI Estimating Assistant (Phase 1 MVP)")

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Document Upload", "Scope Gaps & RFI", "Conflict Detection", "Takeoff"])

st.markdown("---")

if page == "Document Upload":
    st.header("Document Intake")
    uploaded_files = st.file_uploader("Upload Plans & Specs (PDF)", accept_multiple_files=True, type=['pdf'])
    
    if st.button("Process Documents"):
        if uploaded_files:
            st.info("Sending documents to processing pipeline... (Mock UI)")
            # Add API request logic here
            st.success("Documents processed successfully!")
        else:
            st.warning("Please upload files first.")

elif page == "Scope Gaps & RFI":
    st.header("Scope Gaps & RFI Generation")
    st.info("Upload documents first to start analyzing scope gaps.")

elif page == "Conflict Detection":
    st.header("Conflict Detection")
    st.info("Feature under construction")

elif page == "Takeoff":
    st.header("Schedule-Count Takeoff")
    st.info("Feature under construction")

st.markdown("---")
st.header("💬 AI Estimator Assistant")
st.write("Ask the assistant to perform calculations, lookup prices, or search specs. It will use its tools.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("E.g. What is the price of GYP-001?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking... ⏳")
        try:
            res = requests.post(f"{API_URL}/api/v1/agent/chat", json={"query": prompt})
            if res.status_code == 200:
                answer = res.json()["response"]
                message_placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                message_placeholder.error(f"Error: {res.text}")
        except Exception as e:
            message_placeholder.error(f"Connection failed: {e}")

# Check Backend Status
try:
    response = requests.get(f"{API_URL}/")
    if response.status_code == 200:
        st.sidebar.success("Backend: Connected")
    else:
        st.sidebar.error("Backend: Error")
except:
    st.sidebar.error("Backend: Disconnected")
