from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os
from deploy_logic import handle_deployment

# ✅ Create the static/logo folder if it doesn't exist
os.makedirs("static/logo", exist_ok=True)

app = FastAPI()

# ✅ Allow all CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve static files (like uploaded logos)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/deploy/")
async def deploy_app(
    repo_url: str = Form(...),
    domain: str = Form(...),
    logo: UploadFile = None
):
    logo_path = "static/logo/logo.png"
    if logo:
        with open(logo_path, "wb") as f:
            shutil.copyfileobj(logo.file, f)

    return handle_deployment(repo_url, domain)
