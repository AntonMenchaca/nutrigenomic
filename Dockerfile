# Use a lightweight Python image
FROM python:3.9-slim

# Set a working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY app.py /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3000", "app:app"]
