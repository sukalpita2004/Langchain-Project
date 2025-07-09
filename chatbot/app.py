import os
import ollama
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from langchain.chat_models import ChatOllama

#Load the Ollama model (Make sure it's running locally)
llm = ChatOllama(model="gemma:2b")


#Loading environment variables 
load_dotenv()
print("LangChain API Key:", os.getenv("LANGCHAIN_API_KEY"))
#Chatbot prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the user queries."),
    ("user", "Question: {question}")
])

MODEL_NAME = "gemma:2b"

# Responses using Ollama
def get_ollama_response(question):
    response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": question}])
    return response["message"]

# Streamlit UI
st.title('LangChain Demo with Ollama (Local Model)')
input_text = st.text_input("Search the topic you want")

# Process input and display response
if input_text.strip(): 
    response = get_ollama_response(input_text)
    st.write(response)
