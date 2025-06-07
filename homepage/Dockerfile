FROM python:3.12-slim

RUN pip install flask pyyaml requests

WORKDIR /app

COPY app.py /app/
COPY templates/ /app/templates/
COPY static/ /app/static/

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
