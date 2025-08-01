import os
import shutil
import subprocess
import uuid
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static folder for logo hosting
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/deploy/")
async def deploy_app(
    repo_url: str = Form(...),
    domain: str = Form(...),
    logo: UploadFile = None,
):
    deployment_id = str(uuid.uuid4())
    deployment_path = f"deployed_app/{deployment_id}"
    os.makedirs(deployment_path, exist_ok=True)

    try:
        subprocess.run(["git", "clone", repo_url, deployment_path], check=True)
    except subprocess.CalledProcessError:
        return JSONResponse(content={"error": "Git clone failed"}, status_code=500)

    if logo:
        logo_dir = "static/logo"
        os.makedirs(logo_dir, exist_ok=True)
        logo_path = os.path.join(logo_dir, "logo.png")
        with open(logo_path, "wb") as f:
            f.write(await logo.read())

    rpc_config_path = os.path.join(deployment_path, "rpc_config.txt")
    with open(rpc_config_path, "w") as rpc_file:
        rpc_file.write(f"RPC_URL=https://{domain}\n")

    return {
        "message": "App deployed successfully!",
        "rpc_url": f"https://{domain}",
        "logo_url": f"/static/logo/logo.png",
        "deployment_id": deployment_id,
    }

@app.get("/")
def root():
    return {"message": "Deployment service is online. Use POST /deploy/ to deploy your app."}
