import streamlit as st
from rag_pipeline import get_answer, load_pdf

st.title('RAG Chatbot')
uploaded_file = st.file_uploader('Upload a PDF', type='pdf')
if uploaded_file is None:
    st.stop()  # wait until a PDF is uploaded
collection = load_pdf(uploaded_file)  # vector db is ready

if 'messages' not in st.session_state:
    st.session_state['messages'] = []
messages = st.session_state['messages']

question = st.chat_input()
if question:
    messages.append({'role': 'user', 'content': question})
    answer, context = get_answer(question, collection)  # RAG/LLM
    if answer:
        messages.append({'role': 'assistant', 'content': answer})
        with st.expander('Sources'):
            st.write(context)

for msg in messages:
    with st.chat_message(msg['role']):
        st.write(msg['content'])