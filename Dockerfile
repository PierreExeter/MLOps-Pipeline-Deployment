# Dockerfile
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.9.4 /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage Docker layer cache
COPY requirements.txt /app/requirements.txt

# Create and activate virtual environment, install dependencies
RUN uv venv --python 3.11 && \
    . /app/.venv/bin/activate && \
    uv pip install --no-cache-dir -U -r requirements.txt

# Make sure we use the virtual environment for all subsequent commands
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy application source after dependencies are installed (better caching)
COPY . /app

# Expose port
EXPOSE 5000

# Add a simple healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# Default command: run production server. Override for development as needed.
CMD ["python", "src/app.py", "--production"]
