FROM python:3.11-slim

WORKDIR /workspace

# Install Python deps
COPY backend/requirements.txt /workspace/backend/requirements.txt
RUN pip install --no-cache-dir -r /workspace/backend/requirements.txt

# Copy app source (keep backend/ package layout for imports)
COPY backend /workspace/backend
COPY frontend /frontend

EXPOSE 8000

# Seed DB then run API (DB_HOST=db from docker-compose)
CMD ["sh", "-c", "cd /workspace/backend && python -u setup_db.py && cd /workspace && uvicorn backend.main:app --host 0.0.0.0 --port 8000"]
