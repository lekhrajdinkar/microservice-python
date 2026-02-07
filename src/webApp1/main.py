from fastapi import FastAPI, Query, Path, Header, Response, status
from fastapi.responses import JSONResponse, StreamingResponse

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(
        item_id: int = Path(...),
        q: str = Query(None),
        user_agent: str = Header(None)
):
    return {
        "item_id": item_id,
        "query": q,
        "user_agent": user_agent
    }

@app.get("/custom-response")
async def custom_response():
    return JSONResponse(
        content={"message": "Custom"},
        status_code=202,
        headers={"X-Custom-Header": "value"}
    )
