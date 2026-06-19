FROM python:3.10-slim

# Create a dedicated, non-root system user named 'appuser'
RUN addgroup --system appgroup && adduser --system --group appuser

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Transfer ownership of all project files to the new user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user before running the app
USER appuser

# Expose the Flask port
EXPOSE 5000

# Command to run the application
CMD ["python3", "app.py"]
