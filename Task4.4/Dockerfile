FROM python:3.12-slim

# Run as a non-root user 
RUN useradd --create-home appuser
USER appuser
WORKDIR /home/appuser

# Copy only the script, no dependencies needed 
COPY summarise.py .

# Data is provided at runtime 
ENTRYPOINT ["python", "summarise.py"]
