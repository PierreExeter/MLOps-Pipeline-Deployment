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

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -U -r requirements.txt

# Copy files to /app
ADD . /app

# Expose port 
EXPOSE 5000

# Run the application
# Development
# CMD ["python", "src/app.py"]

# Production
CMD ["python", "src/app.py", "--production"]
