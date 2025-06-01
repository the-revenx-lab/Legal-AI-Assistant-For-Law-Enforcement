FROM python:3.8.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Train the Rasa model
RUN rasa train

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=10000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Expose the port
EXPOSE $PORT

# Start command
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "10000"] 