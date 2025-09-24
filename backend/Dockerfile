FROM python:3.13-slim

WORKDIR /home

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code (but will be overridden by compose volume in local development)
COPY app ./app  

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
