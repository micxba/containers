FROM python:3.12-slim

WORKDIR /app

COPY homepage/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY homepage/app.py .
COPY homepage/templates ./templates
COPY homepage/static ./static

CMD ["python", "app.py"]
