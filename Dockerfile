# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for some Python packages)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your files
COPY . .

# Set the port (Render will override this)
ENV PORT=10000

# Expose the port
EXPOSE $PORT

# Start Voilà with explicit binding to 0.0.0.0
CMD voila prediction.ipynb --port=$PORT --no-browser --VoilaConfiguration.ip=0.0.0.0 --VoilaConfiguration.port=$PORT