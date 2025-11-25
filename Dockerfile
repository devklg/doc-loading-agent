FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agent.py .
COPY load_frameworks.py .
COPY config.json .

# Create data directory for outputs
RUN mkdir -p /data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CHROMA_HOST=host.docker.internal
ENV CHROMA_PORT=8000

# Default command
CMD ["python", "agent.py"]
