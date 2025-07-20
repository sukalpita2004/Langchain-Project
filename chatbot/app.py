import os
from dotenv import load_dotenv
import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# Model name used by Ollama
MODEL_NAME = "gemma:2b"

# Initialize LangChain model
llm = ChatOllama(model=MODEL_NAME)

# Prompt template for multi-language code correction
prompt = ChatPromptTemplate.from_messages([
    (
        "system", 
        "You are a programming assistant that helps users by correcting code written in any programming language "
        "(such as C, C++, Java, Python, JavaScript, etc.) and explaining the corrections in simple terms."
    ),
    (
        "user", 
        "Here is my code:\n\n{question}\n\nPlease fix it and explain what was wrong."
    )
])

# Combine prompt, model, and parser into a chain
chain = prompt | llm | StrOutputParser()

# Streamlit UI setup
st.title("🧠 Multi-Language Code Fixer (Ollama + LangChain)")
st.markdown("Paste your buggy code in any language. The model will correct it and explain the fix.")

# Input from user
input_text = st.text_area("🔍 Your Code:", height=300)

# On submit, run the LangChain pipeline
if input_text.strip():
    with st.spinner("Analyzing and fixing your code..."):
        response = chain.invoke({"question": input_text})
        st.markdown("### ✅ Fixed Code & Explanation:")
        st.write(response)
