# Use an official lightweight Python image
FROM python:3.11-slim

# Set environment variables to optimize Python for Docker
# Prevents Python from writing .pyc files and enables unbuffered output for real-time logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy dependencies file first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies without caching build wheels to minimize image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Create the data directory for SQLite database storage
RUN mkdir -p /app/data

# Inform Docker that the container listens on port 5000
EXPOSE 5000

# Run the Flask web application
CMD ["python", "app.py"]

