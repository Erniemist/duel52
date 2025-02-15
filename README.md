# Installation
- Clone the repo
- Install [python 3.12](https://www.python.org/downloads/release/python-3128/)
- `python -m venv .venv`
- POSIX
  - bash: `source .venv/bin/activate`
  - fish: `source .venv/bin/activate.fish`
- Windows: `.venv\Scripts\activate.bat`
- VS Code: Settings > Workspace > Activate Env in Current Terminal (restart Terminal)
- `pip install -r requirements.txt`
- `pytest`
- `python src/client.py`
- 
To run local server:
- Create .env file containing:
WEBSOCKET_URI=ws://localhost:8001
PORT=8001
then
- `python src/server.py`

rules: http://juddmadden.com/duel52/
