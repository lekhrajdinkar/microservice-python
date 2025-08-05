import httpx
from fastapi import APIRouter
from src.commonModule.init_srv import load_env_config

router = APIRouter()

app_config = load_env_config()['oauth']['gh']
GITHUB_CLIENT_ID=app_config['GITHUB_CLIENT_ID']
GITHUB_CLIENT_SECRET=app_config['GITHUB_CLIENT_SECRET']

@router.post("/github-token")
async def github_token():
    """1 Add a Token Fetching Endpoint"""
    data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    headers = {"Accept": "application/json"}
    resp = await httpx.post(
        "https://github.com/login/oauth/access_token",
        data=data, headers=headers
    )
    token_data = resp.json()
    if "access_token" not in token_data:
        raise HTTPException(401, "GitHub token fetch failed")
    return {"access_token": token_data["access_token"]}


from fastapi import Depends, Header, HTTPException

async def verify_github_token(authorization: str = Header(...)):
    """2. Create a Dependency to Verify GitHub Token"""
    token = authorization.removeprefix("Bearer ").strip()
    resp = await httpx.get(
        "https://api.github.com/app",
        headers={"Authorization": f"Bearer {token}"}
    )
    if resp.status_code != 200:
        raise HTTPException(401, "Invalid GitHub token")
    return resp.json()

"""
3. Protect Your /items/{item_id} Endpoint

@app.post("/items/{item_id}")
async def handle(
    item_id: int,
    ...,
    gh_app: dict = Depends(verify_github_token)
):
    return { "item_id": item_id, ..., "gh_app": gh_app }
    
    
📌 Final Behavior
Client calls POST /github-token → gets access_token.
Client calls POST /items/123 with header: Authorization: Bearer <that_token>
FastAPI sends token to GitHub API (GET /app) to verify → ensures validity as an app.

| Flow                      | Supported? | Notes                                                                     |
| ------------------------- | ---------- | ------------------------------------------------------------------------- |
| **Authorization Code**    | ✅ Yes      | Used for user login via browser (interactive)                             |
| **Client Credentials**    | ❌ No       | **Not supported** — GitHub has no concept of machine-to-machine auth      |
| **Personal Access Token** | ✅ Yes      | Manual token generation from GitHub settings                              |
| **GitHub App JWT**        | ✅ Yes      | Used by GitHub Apps, uses **private key + JWT** to get installation token |


"""
