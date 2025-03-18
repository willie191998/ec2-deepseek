from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
import requests
import logging
import sys
import uvicorn
import json
import socket
import os

def get_host():
    try:
        return socket.gethostbyname("host.docker.internal")
    except socket.gaierror:
        return "localhost"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("fastapi_app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("fastapi-ollama")

app = FastAPI()

# DeepSeek model name (ensure it matches your Ollama installation)
DEEPSEEK_MODEL = "deepseek-r1:7b"

class PromptRequest(BaseModel):
    prompt: str
    model: str = DEEPSEEK_MODEL  # Default to DeepSeek-R1 7B

@app.get("/")  # Add this if missing
def root():
    return {"message": "FastAPI is running!"}

@app.post("/generate")
async def generate(request: PromptRequest = Body(...)):
    logger.info(f"Received prompt request for model '{request.model}': {request.prompt[:50]}...")
    
    try:
        # Use the correct Ollama API endpoint
        # ollama_url = "http://localhost:11434/api/generate"
        # ollama_url = f"http://{get_host()}:11434/api/generate"
        # Set Ollama URL based on Docker environment
        # ollama_url = "http://host.docker.internal:11434/api/generate"
        ollama_url = os.getenv("OLLAMA_URL", "http://ollama:11434/api/generate")
        logger.info(f"Sending request to Ollama at {ollama_url}")
        
        # Format request for Ollama
        ollama_request = {
            "model": request.model,
            "prompt": request.prompt,
            "stream": False,
            "max_tokens": 300,
            "temperature": 0.4
        }

        logger.info(f"Request payload: {json.dumps(ollama_request)}")

        ollama_response = requests.post(
            ollama_url, 
            json=ollama_request,
            timeout=300  # Increased timeout
        )

        logger.info(f"Response status: {ollama_response.status_code}")
        logger.info(f"Response text: {ollama_response.text[:500]}...")

        if ollama_response.status_code == 200:
            response_data = ollama_response.json()
            response_text = response_data.get("response", "No response field in output")
            return {"response": response_text, "full_response": response_data}
        else:
            error_msg = f"Ollama error: {ollama_response.status_code} - {ollama_response.text}"
            logger.error(error_msg)
            raise HTTPException(status_code=502, detail=error_msg)
    except Exception as e:
        error_msg = f"Exception: {str(e)}"
        logger.error(error_msg, exc_info=True)  # Log the full stack trace
        raise HTTPException(status_code=500, detail=error_msg)

# Health check endpoint
@app.get("/health")
async def health():
    logger.info("Health check endpoint called")
    return {"status": "ok"}

# List available models
@app.get("/models")
async def list_models():
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            return {"available_models": response.json()["models"]}
        else:
            return {"error": f"Failed to get models, status code: {response.status_code}"}
    except Exception as e:
        return {"error": f"Exception when getting models: {str(e)}"}

# Run the application
if __name__ == "__main__":
    logger.info("Starting FastAPI application on 0.0.0.0:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)


