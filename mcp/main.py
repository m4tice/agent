from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Literal

app = FastAPI()

# Define the expected structure of incoming context requests
class ContextRequest(BaseModel):
    user_id: str
    context_type: Literal["memory", "tools", "settings"]
    request_type: Literal["retrieve", "update"]

# Example response (could pull from a real database)
def get_context_for_user(user_id: str):
    return [
        {"type": "text", "value": f"User {user_id} prefers dark mode."},
        {"type": "text", "value": "Their favorite language is Python."}
    ]

@app.post("/mcp/context")
async def mcp_context_handler(req: ContextRequest):
    if req.request_type == "retrieve" and req.context_type == "memory":
        context = get_context_for_user(req.user_id)
        return {"context": context}
    return {"context": []}
