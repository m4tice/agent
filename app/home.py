from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import sys
from pathlib import Path

from typing import Dict, List
from pydantic import BaseModel
from fastapi import HTTPException


# Add parent directory to path to import env.py
sys.path.append(str(Path(__file__).resolve().parent.parent))

from env import BASE, HOME_URL, HOME_PORT, STATE_ON, STATE_OFF

# === Setup FastAPI =============================
# Create FastAPI instance
home = FastAPI()

# Get the directory where this file is located
BASE_DIR = Path(__file__).resolve().parent

# Serve static files (CSS & JS) - relative to this file's location
home.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Jinja2 template setup - relative to this file's location
templates = Jinja2Templates(directory=BASE_DIR / "templates")


# === Database =============================
lights = {
        1: {
            "name": "Living Room",
            "status": STATE_OFF
        },
        2: {
            "name": "Kitchen",
            "status": STATE_OFF
        },
        3: {
            "name": "Bedroom",
            "status": STATE_ON
        },
        4: {
            "name": "Bathroom",
            "status": STATE_OFF
        }
    }


# Pydantic models for request and response
class LightRequest(BaseModel):
    light_id: int

class LightResponse(BaseModel):
    message: str
    light_id: int
    status: bool


# Define the home route
@home.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "lights": lights})

# Define the API endpoints
@home.get("/lights")
def get_lights_status() -> Dict[str, List[Dict]]:
    return {"lights": [{"id": light_id, **light_info} for light_id, light_info in lights.items()]}

@home.post("/lights/on", response_model=LightResponse)
def light_on(request: LightRequest):
    # ID validation
    if request.light_id not in lights:
        raise HTTPException(status_code=400, detail=f"Invalid light_id. Must be between 0 and {len(lights)-1}")

    status_on = STATE_ON
    lights[request.light_id]['status'] = status_on
    return LightResponse(
        message=f"Light {request.light_id} turned on",
        light_id=request.light_id,
        status=status_on
    )

@home.post("/lights/off", response_model=LightResponse)
def light_off(request: LightRequest):
    # ID validation
    if request.light_id not in lights:
        raise HTTPException(status_code=400, detail=f"Invalid light_id. Must be between 0 and {len(lights)-1}")
    
    status_off = STATE_OFF
    lights[request.light_id]['status'] = status_off
    return LightResponse(
        message=f"Light {request.light_id} turned off",
        light_id=request.light_id,
        status=status_off
    )

if __name__ == "__main__":
    # Run the app with uvicorn using settings from env.py
    uvicorn.run(home, host=BASE, port=HOME_PORT)
