import streamlit as st
from system import delete_existing_db, creating_db, results

st.title("Open-Source RAG System 🤗🦜")

if 'db_initialized' not in st.session_state:
    st.session_state['db_initialized'] = False
if 'current_file' not in st.session_state:
    st.session_state['current_file'] = None

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None and uploaded_file != st.session_state['current_file']:
    with open("document/uploaded_document.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    delete_existing_db()
    creating_db("document/uploaded_document.pdf")
    st.session_state['db_initialized'] = True
    st.session_state['current_file'] = uploaded_file
    st.success("Database created successfully!")

query = st.text_input("Enter your query")

if query:
    if not st.session_state['db_initialized']:
        st.warning("Please upload a PDF first.")
    else:
        answer = results(query)
        st.write(f"Answer: {answer}")
