# Dockerfile
FROM python:3.11-slim

# Change working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.9.4 /uv /uvx /bin/

# Copy files to /app
ADD . /app

# Create and activate virtual environment
RUN uv venv --python 3.11
ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies
RUN uv pip install --no-cache-dir -U -r requirements.txt

# Expose port 
EXPOSE 5000

# Run the application
# Development
# CMD ["python", "src/app.py"]

# Production
CMD ["python", "src/app.py", "--production"]
