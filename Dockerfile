FROM python:3.9-slim

# Install system dependencies including Cairo
RUN apt-get update && apt-get install -y \
    libcairo2-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY api-app.py .

# Expose port
EXPOSE 8080

# Command to run the application
CMD ["python", "api-app.py"]