FROM python:3.11-slim

WORKDIR /app

# Install Python deps
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app source
COPY backend /app

# Expose FastAPI
EXPOSE 8000

# Copy frontend so backend can serve it
COPY frontend /frontend

# Start: seed DB, then run app
CMD ["sh", "-c", "python -u setup_db.py && uvicorn main:app --host 0.0.0.0 --port 8000"]


