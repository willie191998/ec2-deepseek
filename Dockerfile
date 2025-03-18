# Start from the Ollama base image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application
COPY . .

# Expose FastAPI port
EXPOSE 8080

# Run FastAPI
CMD ["uvicorn", "fastapi_ollama:app", "--host", "0.0.0.0", "--port", "8080"]
