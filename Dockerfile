FROM python:3.12-slim

WORKDIR /app

# Dependencies first — this layer is cached until requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code last — changes here don't invalidate the install layer
COPY app/ ./app/

# Non-root user: Kubernetes PodSecurity policies often reject root containers
RUN useradd --create-home --uid 1000 appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
