from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Model
MODEL_NAME = "gemma:2b"
llm = ChatOllama(model=MODEL_NAME)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a programming assistant that corrects code in any language and explains the fix."),
    ("user", "Here is my code:\n\n{question}\n\nFix it and explain the corrections.")
])
chain = prompt | llm | StrOutputParser()

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="chatbot/static"), name="static")

# Templates
templates = Jinja2Templates(directory="chatbot/templates")

class CodeInput(BaseModel):
    code: str

@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/fix-code")
async def fix_code(input: CodeInput):
    try:
        result = chain.invoke({"question": input.code})
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
