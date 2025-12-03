# student-service/Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app code
COPY app/ ./app/

# Expose port
EXPOSE 80

# Run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
