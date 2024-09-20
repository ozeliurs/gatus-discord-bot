FROM python:3.9-slim

RUN adduser --system --no-create-home nonroot
USER nonroot

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/

CMD ["python", "src/main.py"]
