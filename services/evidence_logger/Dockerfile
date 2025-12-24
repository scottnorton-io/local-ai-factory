FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY services/evidence_logger/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY services/common ./services/common
COPY services/evidence_logger ./services/evidence_logger

EXPOSE 9000

CMD ["uvicorn", "services.evidence_logger.main:app", "--host", "0.0.0.0", "--port", "9000"]
