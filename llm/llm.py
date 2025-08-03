"""
author: @guu8hc
"""

import json
import requests
from ollama import Client

import sys
from pathlib import Path


# Add parent directory to path to import env.py
sys.path.append(str(Path(__file__).resolve().parent.parent))

from env import HOME_URL

# Ollama client (Ollama runs on default port 11434)
client = Client(host="http://localhost:11434")

# List of possible actions
ACTIONS = {
    "get_lighting_status": {
        "description": "Returns ON/OFF status of all lights.",
        "endpoint": f"{HOME_URL}/lights"
    }
}

def decide_action(user_input: str) -> str:
    """Ask the LLM which action matches the input."""
    try:
        system_prompt = "You are a virtual household assistant. Decide which action to call."
        actions_list = "\n".join([f"{k}: {v['description']}" for k, v in ACTIONS.items()])

        prompt = f"""
{system_prompt}

Available actions:
{actions_list}

User asked: "{user_input}"

Respond with ONLY the action name. Do not include any explanation or reasoning. Just return the exact action name from the list above.

Action name:"""

        response = client.chat(model="qwen3", messages=[
            {"role": "user", "content": prompt}
        ])

        raw_response = response['message']['content'].strip()
        
        # Extract action name from response (handle qwen3's thinking tags)
        if "<think>" in raw_response and "</think>" in raw_response:
            # Remove the thinking part and get what comes after
            action_name = raw_response.split("</think>")[-1].strip()
        else:
            action_name = raw_response
            
        return action_name
    
    except Exception as e:
        print(f"\033[91mError connecting to Ollama: {e}\033[0m")
        print("\033[93mMake sure Ollama is running with: ollama serve\033[0m")
        print("\033[93mAvailable models: qwen3\033[0m")
        return "get_lighting_status"  # fallback action

def call_action(action_name: str):
    """Call the correct FastAPI endpoint based on action."""
    
    if action_name not in ACTIONS:
        return {"error": f"Unknown action: {action_name}. Available actions: {list(ACTIONS.keys())}"}
    
    try:
        url = ACTIONS[action_name]["endpoint"]
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": f"Could not connect to {url}. Make sure the home service is running."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

def format_response(result: dict, action_name: str) -> str:
    """Convert JSON response to human-like response using LLM."""
    try:
        # Handle error responses
        if "error" in result:
            return f"\033[91mSorry, I encountered an issue: {result['error']}\033[0m"
        
        # Create a prompt for the LLM to format the response
        prompt = f"""
You are a helpful home assistant. Convert the following technical data into a natural, simple response.

Action performed: {action_name}
Data received: {json.dumps(result, indent=2)}

Respond in a simple, friendly way. Keep it short and clear.

Response:"""

        response = client.chat(model="qwen3", messages=[
            {"role": "user", "content": prompt}
        ])

        formatted_response = response['message']['content'].strip()
        
        # Handle qwen3's thinking tags if present
        if "<think>" in formatted_response and "</think>" in formatted_response:
            formatted_response = formatted_response.split("</think>")[-1].strip()
            
        return formatted_response
        
    except Exception as e:
        print(f"\033[91mError formatting response: {e}\033[0m")
        # Fallback to basic formatting
        if action_name == "get_lighting_status" and "lights" in result:
            lights = result["lights"]
            on_lights = [light for light in lights if light.get("status")]
            off_lights = [light for light in lights if not light.get("status")]
            
            response_parts = []
            if on_lights:
                on_names = [light.get("name", f"Light {light.get('id')}") for light in on_lights]
                response_parts.append(f"\033[92mOn: {', '.join(on_names)}\033[0m")
            if off_lights:
                off_names = [light.get("name", f"Light {light.get('id')}") for light in off_lights]
                response_parts.append(f"\033[91mOff: {', '.join(off_names)}\033[0m")
                
            return "Lighting status:\n" + "\n".join(response_parts)
        
        return f"Result: {json.dumps(result, indent=2)}"

def main():
    while True:
        user_input = input("\033[96mYou: \033[0m")
        if user_input.lower() in {"exit", "quit"}:
            break

        action = decide_action(user_input)
        print(f"\033[94mAction: {action}\033[0m")
        
        result = call_action(action)
        
        # Format the response in a human-like way
        human_response = format_response(result, action)
        print(f"\033[92m{human_response}\033[0m\n")

if __name__ == "__main__":
    main()
