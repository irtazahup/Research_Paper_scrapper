FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Command to run the API (Standard Production Server)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
