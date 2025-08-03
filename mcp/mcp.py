"""
author: @GUU8HC
"""

from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional, Literal
import uvicorn

from db import db_instance
from light import light_system_instance
    
# Create FastAPI instance
mcp_instance = FastAPI(
    title="MCP",
    description="Model Context Protocol API",
    version="1.0.0"
)

class ContextRequest(BaseModel):
    context_type: Literal["status"]
    request_type: Literal["retrieve", "update"]

@app.get("/mcp/context")
async def mcp_context_handler(req: ContextRequest):
    context_type = req.query_params.get("context_type")
    request_type = req.query_params.get("request_type")

    if request_type == "retrieve":
        if context_type == "status":
            lights_status = light_system_instance.get_all_lights_status()
            return {
                "context": {
                    "type": "text", "value": f"Light status: {lights_status}"
                }
            }

    return {"context": []}