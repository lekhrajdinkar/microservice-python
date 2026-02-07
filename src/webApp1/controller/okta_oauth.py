import httpx, base64
from fastapi import HTTPException

import os
from dotenv import load_dotenv
from src.webApp1.service.init_srv import load_env_config
load_dotenv()
app_config = load_env_config()['oauth']['okta']

OKTA_CLIENT_SECRET = os.getenv("OKTA_CLIENT_SECRET")
OKTA_CLIENT_ID=app_config['OKTA_CLIENT_ID']
OKTA_TOKEN_URL=app_config['OKTA_TOKEN_URL']
OKTA_INTROSPECT_URL=app_config['OKTA_INTROSPECT_URL']
OKTA_SCOPE=app_config['OKTA_SCOPE']

# not in use
async def get_okta_token_async():
    auth = base64.b64encode(f"{OKTA_CLIENT_ID}:{OKTA_CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "client_credentials",
        "scope": OKTA_SCOPE
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(OKTA_TOKEN_URL, headers=headers, data=data)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Failed to fetch token from Okta")
        return resp.json()

async def verify_okta_token(token: str):
    auth = base64.b64encode(f"{OKTA_CLIENT_ID}:{OKTA_CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "token": token,
        "token_type_hint": "access_token"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(OKTA_INTROSPECT_URL, headers=headers, data=data)
        result = resp.json()
        if not result.get("active"):
            raise HTTPException(401, detail="Invalid or expired token")
        return result

def request_token():
    client_id = OKTA_CLIENT_ID
    client_secret = OKTA_CLIENT_SECRET
    token_url = OKTA_TOKEN_URL

    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "client_credentials",
        "scope": "fastapiweb2"
    }

    response = httpx.post(token_url, headers=headers, data=data)
    print(response.status_code, response.json())
    return response.json()
