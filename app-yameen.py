import streamlit as st
from populate_database import load_documents, split_documents, add_to_chroma
from query_data import query_rag
 
st.set_page_config(page_title="Local Lookup", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Local Lookup 💬🦙")
         
if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about your documents!"}
    ]
 
@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the documents – hang tight! This should only take a few minutes."):
        documents = load_documents()
        chunks = split_documents(documents)
        add_to_chroma(chunks)
 
load_data()
 
if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
 
for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])
 
# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = query_rag(prompt)
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) # Add response to message history