import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Mount static directory
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# ✅ Set up template rendering
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# LLM Setup
MODEL_NAME = "gemma:2b"
llm = ChatOllama(model=MODEL_NAME)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a programming assistant that corrects code in any language and explains the fix."),
    ("user", "Here is my code:\n\n{question}\n\nFix it and explain the corrections.")
])
chain = prompt | llm | StrOutputParser()

class CodeInput(BaseModel):
    code: str

# ✅ Home page route
@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ Code fix API
@app.post("/fix-code")
async def fix_code(input: CodeInput):
    try:
        result = chain.invoke({"question": input.code})
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
