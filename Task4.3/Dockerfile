# Build dependencies
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final runtime image 
FROM python:3.12-slim
WORKDIR /app

# Create and use a non-root user for security
RUN useradd --create-home appuser

# Copy only the installed packages from the builder stage
COPY --from=builder /install /usr/local
COPY main.py .

USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]