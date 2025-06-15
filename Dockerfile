# Dockerfile for Research Evaluator Agent

FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency definitions
COPY pyproject.toml uv.lock ./

# Upgrade pip and install uv dependency manager
RUN pip install --upgrade pip \
    && pip install uv

# Sync project dependencies using uv
RUN uv sync

# Copy project source
COPY . .

# Expose HTTP API port
EXPOSE 8000

# Default command to start the server
CMD ["uvicorn", "src.research_evaluator_agent.server.app:app", "--host", "0.0.0.0", "--port", "8000"] 