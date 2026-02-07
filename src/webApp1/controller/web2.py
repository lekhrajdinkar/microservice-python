# netstat -ano | findstr :8000
# taskkill /PID xxxx /F

from fastapi import FastAPI, Header, Query, Path, Body, Request, Depends, HTTPException
from typing import Optional
from src.commonModule.init_srv import load_env_config
from src.webApp1.controller.okta_oauth import verify_okta_token, request_token
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from contextlib import asynccontextmanager
import redis.asyncio as redis
from dotenv import load_dotenv
import os
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    #app_config = load_env_config();
    #print("appconfig", app_config)
    redis_url = os.getenv('REDIS_CLOUD_URL')
    redis_url = f"redis://{redis_url}"
    print("redis_url", redis_url)
    redis_client = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_client)
    app.state.redis = redis_client
    yield
    await redis_client.close()

app = FastAPI(
    lifespan=lifespan,
    title="Python API doc",
    description="API for python POC",
    version="1.0.0",
    contact={"name": "Lekhraj Dinkar", "email": "LekhrajDinkarus@gmail.com"}
)

# --- Step 1: Path, Query, Header, and Body Parameters ---
"""
item_id is a path parameter extracted from the URL path (e.g., /items/{item_id}).
... vs None ==== mandatory vs optional
Path(...) means this parameter is required.
Body(...) required
"""  # 5 requests per minute per IP


@app.get("/data-from-redis-cache/{item_id}")
async def get_data(item_id: int, request: Request):
    redis = request.app.state.redis
    key = f"item:{item_id}"
    cached = await redis.get(key)
    if cached:
        return {"source": "cache", "item_id": item_id, "data": cached}

    data = f"value-for-item-{item_id}"
    await redis.set(key, data, ex=30)
    return {"source": "fresh", "item_id": item_id, "data": data}


@app.post("/items/{item_id}")
async def full_pack_api(
        request: Request,
        item_id: int = Path(..., description="The ID of the item (required)"),
        q1: Optional[str] = Query(..., description="Query string parameter (required str)"),
        q2: Optional[int] = Query(None, description="Query string parameter (optional int)"),
        h1: Optional[str] = Header(..., description="header (required str)"),
        h2: Optional[int] = Header(None, description="header (optional int)"),
        payload: dict = Body(None, description="Request body as a dictionary"),
        #token_payload: dict = Depends(verify_token),
        #gh_app: dict = Depends(verify_github_token)
        authorization: str = Header(...)
):
    all_header = dict(request.headers)
    all_qp = dict(request.query_params)

    token = authorization.removeprefix("Bearer ").strip()
    user_info = await verify_okta_token(token)

    return {
        "item_id": item_id,
        "query_param_1": q1, "query_param_2": q2,
        "header_1": h1, "header_2": h2,
        "payload": payload,
        "all_header": all_header,
        "all_qp": all_qp,
        "user_info": user_info
    }


# --- Step 2: Custom JSON Response ---
@app.get("/custom-response")
async def custom_response():
    data = {
        "status": "Accepted",
        "note": "This is a custom response."
    }
    headers = {
        "X-My-Header": "CustomHeaderValue"
    }
    return JSONResponse(status_code=202, content=data, headers=headers)


# --- Step 3:  okta token ---
@app.post("/okta/request-token")
async def okta_request_token():
    return request_token()


# --- Step 4.1 : rate limiting --- slowapi :: Good for development/testing
"""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

apply : @limiter.limit("5/minute")  # 5 requests per minute per IP
"""


# --- Step 4.2 : rate limiting and caching ---
"""
✅ 1. API Gateway (Recommended)
✅ 2. AWS WAF (Web Application Firewall)
✅ 3. Redis-based Limiting (in FastAPI)
if  behind ALB/NLB and want "app-level throttling"
Use fastapi-limiter with Elasticache Redis
It works well in microservices if rate limits differ per endpoint/user/token

| Layer                         | Rate Limiting Role                       |
| ----------------------------  | ---------------------------------------- |
| **AWS WAF**                   | Edge protection against DDoS/brute force |
| **API Gateway + AWS redis**    | General per-IP throttle, protect entry   |
| **FastAPI App**               | Per-user or per-scope custom limits      |

AWS Elasticsearch redis (no boto3), ⬅️
- Caching API responses 🫙
- Session storage 🫙
- Rate limiting 🚫
- run locally : 
    docker run --name redis-local -p 6379:6379 -d redis
    docker run -d --name redisinsight -p 8001:8001 redislabs/redisinsight:latest  (UI)

| Library           | Description                               |
| ----------------- | ----------------------------------------- |
| `redis`           | Synchronous Python Redis client           |
| `aioredis`        | Async Redis client (used in FastAPI apps) |
| `fastapi-limiter` | Built on `aioredis` for rate limiting     |

"""


@app.get("/rate-limited-api", dependencies=[Depends(RateLimiter(times=3, seconds=60))])
async def rateLimitedApi():
    return {"message": "You can call this API 3 times per minute"}


# =========== file upload / downloads
# FileResponse, UploadFile
from fastapi.responses import FileResponse
import os
from fastapi import  File, UploadFile, Form

@app.get("/download")
def download_file():
    """
    FileResponse handles setting proper headers like Content-Disposition for downloading.
    media_type="application/octet-stream" tells the browser to download it instead of displaying.
    filename= controls what name the user sees when saving the file.
    """
    file_path = "src/webModule/controller/openapi.json"  # Make sure this file exists
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename="openapi_2.json",
            media_type="application/octet-stream"
        )
    return {"error": "File not found"}

@app.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        description: str = Form(...)
):
    """
    UploadFile = File(...): Tells FastAPI to expect a file part in a multipart request.
    description: str = Form(...): Extracts regular form field from the same request.
    """
    content = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "description": description,
        "size": len(content)
    }