# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Application environment variables (will be overridden by docker-compose)
# Using Neon serverless PostgreSQL
ENV GEMINI_API_KEY= \
    BETTER_AUTH_SECRET=your-super-secret-jwt-key-change-in-production \
    BUSINESS_SERVICE_URL=http://backend:8000 \
    CONVERSATION_RETENTION_DAYS=7 \
    DATABASE_URL=postgresql+asyncpg://user:password@ep-xxxx-region.neon.tech/dbname?sslmode=require

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

# Set working directory
WORKDIR /app

# Install uv as root before switching to non-root user
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY requirements.txt ./
COPY uv.lock* ./

# Install Python dependencies using uv (as root)
RUN uv pip install --system --no-cache-dir -r requirements.txt
RUN uv pip install --system --no-cache-dir openai-chatkit==1.4.0

# Switch to non-root user
USER appuser

# Add user's local bin to PATH
ENV PATH="/home/appuser/.local/bin:$PATH"

# Copy application code
COPY --chown=appuser:appuser . .

# Expose port
EXPOSE 8001

# Health check using curl
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
