1. Dockerfile anpassen:

Dockerfile (optional)
Code 
2. main.py mit Debug-Logs ersetzen:

main.py (Final mit Debug + Port 10000)
Code 




FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]
