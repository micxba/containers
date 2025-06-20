FROM python:3.13-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y build-essential libffi-dev && rm -rf /var/lib/apt/lists/*

# Install deps
COPY homer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY homer/app /app

# Use Gunicorn as the production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
