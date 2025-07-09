import os
from dotenv import load_dotenv
import streamlit as st
from langchain.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()
print("LangChain API Key:", os.getenv("LANGCHAIN_API_KEY"))

#Ollama model
MODEL_NAME = "gemma:2b"
llm = ChatOllama(model=MODEL_NAME)

#chatbot prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the user queries."),
    ("user", "Question: {question}")
])

# Streamlit UI
st.title('LangChain Demo with Ollama (Local Model)')

# Session state to store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    st.write(message)

# User input
input_text = st.text_input("Ask me anything:")

if input_text.strip():
    user_message = f"User: {input_text}"
    st.session_state.messages.append(user_message)  
#AI response integration
    response = llm.invoke(input_text)
    ai_message = f"{response.content}"
    st.session_state.messages.append(ai_message)  

    # Display conversation
    st.write(ai_message)
