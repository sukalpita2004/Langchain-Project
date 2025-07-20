from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser



# Model
MODEL_NAME = "gemma:2b"
llm = ChatOllama(model=MODEL_NAME)

# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a programming assistant that corrects code in any language and explains the fix."),
    ("user", "Here is my code:\n\n{question}\n\nFix it and explain the corrections.")
])
chain = prompt | llm | StrOutputParser()

# FastAPI App
app = FastAPI()

# Request Schema
class CodeInput(BaseModel):
    code: str

# API Route
@app.post("/fix-code")
async def fix_code(input: CodeInput):
    try:
        result = chain.invoke({"question": input.code})
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
