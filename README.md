# agent
## How-to
### 1. Run server
Change directory to mcp:
```
cd mcp
```
Run server on a selected port:
```
python -m uvicorn main:app --reload --port <port-number>
```
### 2. Query
Either run llm/main.py by:
```
cd llm
```
and run:
```
python main.py
```
or via curl command:
```
curl -X POST "http://localhost:8000/mcp/context" -H "Content-Type: application/json" -d "{\"user_id\": \"user_123\", \"context_type\": \"memory\", \"request_type\": \"retrieve\"}"
```
### 3. Useful commands
Check for port usage on terminal:
```
netstat -aon | findstr :<port-number>
```
if a port is currently in used, it will display:
```
TCP    127.0.0.1:<port-number>         0.0.0.0:0              LISTENING       7196
```
else, it returns nothing.
