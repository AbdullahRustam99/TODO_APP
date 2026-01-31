# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Install uv for faster dependency management
RUN pip install uv

# Copy uv.lock and requirements.txt and install dependencies
COPY uv.lock .
COPY requirements.txt .
RUN uv pip install --system --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the FastAPI application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
