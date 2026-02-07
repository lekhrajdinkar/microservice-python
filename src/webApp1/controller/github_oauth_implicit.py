# --- Step 6: GitHub OAuth Setup ---

from fastapi import Request
from fastapi.responses import JSONResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from .web2 import app
from dotenv import load_dotenv
import os
load_dotenv()

#app_config = load_env_config()['oauth']['okta']
GITHUB_CLIENT_ID=os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET=os.getenv("GITHUB_CLIENT_SECRET")

config: Config = Config(environ={
    "GITHUB_CLIENT_ID": os.getenv("GITHUB_CLIENT_ID", GITHUB_CLIENT_ID),
    "GITHUB_CLIENT_SECRET": os.getenv("GITHUB_CLIENT_SECRET", GITHUB_CLIENT_SECRET),
})

oauth = OAuth(config)
github = oauth.register(
    name='github',
    client_id=config('GITHUB_CLIENT_ID'),
    client_secret=config('GITHUB_CLIENT_SECRET'),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'read:user user:email'},
)

@app.get('/login/github')
async def login_via_github(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await github.authorize_redirect(request, redirect_uri)

@app.get('/auth/callback')
async def auth_callback(request: Request):
    token = await github.authorize_access_token(request)
    user = await github.get('user', token=token)
    user_info = user.json()
    return JSONResponse(content={"user": user_info})