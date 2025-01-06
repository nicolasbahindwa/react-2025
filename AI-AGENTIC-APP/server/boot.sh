#!/bin/sh
echo "Starting Uvicorn with optimized reload settings..."
export PYTHONPATH=/app
uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --reload-dir /app \
    --reload-include "*.py" \
    --log-level info \
    --reload-delay 0.1 \
    --workers 1 \
    --ws websockets