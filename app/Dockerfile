# Start with a Python base image
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Install required packages
RUN pip install flask psutil

# Copy our app into the container
COPY app.py .

# Expose port 8080
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]
