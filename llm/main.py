import requests

context = requests.post(
    "http://localhost:8000/mcp/context",
    json={
        "user_id": "user_123",
        "context_type": "memory",
        "request_type": "retrieve"
    }
).json()["context"]

print("Retrieved context:", context)
