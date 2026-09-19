# Use lightweight python 3.12 image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.min.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.min.txt

# Copy source code and artifacts
COPY src/ src/
COPY data/ data/
COPY artifacts/ artifacts/

# Expose standard FastAPI port
EXPOSE 8000

# Start Uvicorn server
CMD ["uvicorn", "src.serve:app", "--host", "0.0.0.0", "--port", "8000"]