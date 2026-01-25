# Railway-optimized Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install only essential system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Railway uses PORT environment variable
ENV PORT=8000
EXPOSE 8000

# Run with minimal workers
CMD uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
