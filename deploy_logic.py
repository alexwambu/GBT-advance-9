import subprocess
import os
import json
from datetime import datetime

def handle_deployment(repo_url: str, domain: str):
    folder_name = repo_url.strip().split("/")[-1].replace(".git", "")
    
    # Remove old clone if exists
    if os.path.exists(folder_name):
        subprocess.run(["rm", "-rf", folder_name])
    
    # Clone repo
    result = subprocess.run(["git", "clone", repo_url], capture_output=True, text=True)
    
    # Create rpc_config
    rpc_config = {
        "RPC_URL": f"https://{domain}",
        "DOMAIN": domain,
        "DEPLOY_TIMESTAMP": datetime.now().isoformat()
    }
    with open("rpc_config.json", "w") as f:
        json.dump(rpc_config, f, indent=4)

    return {
        "message": f"Cloned {repo_url} to ./{folder_name}",
        "rpc_config": rpc_config,
        "status": "success"
    }
