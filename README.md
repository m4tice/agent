# Agent
## How-to
### 0. Activate the virtual environment
Open terminal and type the following command:  
```
source .venv/bin/activate
```
### 1. Run the application
Run the application:
```
python app\home.py
```
### 2. Run the LLM model
Either run llm/main.py by:
```
python llm\llm.py
```
After this, type your query in the same terminal.
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
