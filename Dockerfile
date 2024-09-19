FROM python:3.9-slim

RUN adduser --system --no-create-home nonroot

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py config.py gatus.py /app/

USER nonroot

CMD ["python", "main.py"]
