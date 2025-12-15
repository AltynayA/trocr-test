FROM python:3.9-slim

# Python behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# System dependencies (PDF + images)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libgl1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Working directory
WORKDIR /app

# Python dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    torch \
    torchvision \
    transformers \
    pillow \
    python-multipart \
    pdf2image

# Copy the CONTENTS of app/ into /app
COPY app /app

# Expose API port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
