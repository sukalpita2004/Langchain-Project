import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from huggingface_hub import InferenceClient

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Mount static directory
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# ✅ Set up template rendering
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# ✅ Hugging Face Setup (replace with your token or set as env var in Render)
HF_TOKEN = os.getenv("HF_TOKEN")  # Add this in Render's env variables
client = InferenceClient(model=HF_MODEL, token=HF_TOKEN)

# ✅ Model to use — can be changed
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"

class CodeInput(BaseModel):
    code: str

@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/fix-code")
async def fix_code(input: CodeInput):
    prompt = f"""You are a helpful programming assistant. Fix the following code and explain the changes:\n\n{input.code}"""
    try:
        output = client.text_generation(prompt=prompt, max_new_tokens=512)
        return {"success": True, "result": output}
    except Exception as e:
        return {"success": False, "error": str(e)}
