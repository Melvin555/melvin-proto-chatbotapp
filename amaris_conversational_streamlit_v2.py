# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 22:16:16 2025

@author: JPHarsonMe
"""

import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain.schema import HumanMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv("//Users//melvinharsono//workingdirectory//environment//melvin_openai_cred.env")

working_dir = "//Users//melvinharsono//workingdirectory//melvin-proto-chatbotapp//"

# Load FAISS database
def load_faiss_db(db_path):
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment=os.environ.get("AZURE_DEPLOYMENT_EMBEDDINGS"),
        openai_api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    )
    return FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)

# Retrieve relevant documents from FAISS
def retrieve_relevant_docs(query, db, top_k=3):
    return db.similarity_search(query, k=top_k)

# Generate response using Azure OpenAI
def generate_response(query, retrieved_docs, conversation_history):
    context = "\n".join([doc.page_content for doc in retrieved_docs])

    # Add conversation history to the prompt
    full_conversation = "\n".join(conversation_history) + "\nUser's question: " + query

    prompt = f"""You are a helpful assistant. Answer the user's question based on the provided context.
    If there is link to web or file, please add thm in the reply.
    
    Context:
    {context}
    
    Conversation history:
    {full_conversation}
    
    User's question: {query}
    
    If the answer is not in the context, reply with:
    '申し訳ありませんが、データベースにない課題です。こちらのリンクをご参考にしていただければ幸いです。：www.amaris.com'
    """

    chat_model = AzureChatOpenAI(
        azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        temperature=0.3,
        max_tokens=500
    )

    response = chat_model([HumanMessage(content=prompt)])
    return response.content  # Only return the response, don't update history

# Streamlit UI for chatting
def chat_ui():
    st.title("Amaris Chatbot [FAQ Search]")
    st.write("ご質問いただければ、最も関連性の高いFAQをお探しします。")

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    if 'faiss_db' not in st.session_state:
        # Load FAISS database on first use
        st.session_state.faiss_db = load_faiss_db(working_dir + "amaris-faiss-db-output")

    # Display chat history
    for message in st.session_state.conversation_history:
        with st.chat_message("user" if message.startswith("User:") else "assistant"):
            st.markdown(message.replace("User: ", "").replace("Assistant: ", ""))

    # User input
    user_query = st.chat_input("こちらに入力してください！")
    if user_query:
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.conversation_history.append(f"User: {user_query}")

        # Retrieve relevant documents from FAISS
        relevant_docs = retrieve_relevant_docs(user_query, st.session_state.faiss_db)

        # Generate a response based on the user query and conversation history
        response = generate_response(user_query, relevant_docs, st.session_state.conversation_history)

        # Update conversation history in session state
        st.session_state.conversation_history.append(f"Assistant: {response}")

        # Display the assistant's response in the chat
        with st.chat_message("assistant"):
            st.markdown(response)

if __name__ == "__main__":
    chat_ui()
