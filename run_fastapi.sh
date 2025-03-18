#!/bin/bash
source ~/fastapi_env/bin/activate
nohup python3.11 fastapi_ollama.py > fastapi.log 2>&1 &
echo "FastAPI application started. Check fastapi.log for details."
deactivate
