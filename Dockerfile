# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
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

# Start Voilà with correct binding
# The key fix: use --ip=0.0.0.0 (not --VoilaConfiguration.ip)
CMD voila prediction.ipynb --port=$PORT --no-browser --ip=0.0.0.0 --allow-root
