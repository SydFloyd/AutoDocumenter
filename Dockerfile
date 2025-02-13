FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN ls -lah /app

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /app/entrypoint.sh
RUN ls -lah /app


ENTRYPOINT ["/app/entrypoint.sh"]
