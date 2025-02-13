FROM python:3.11-slim

WORKDIR /github/workspace
COPY . .

RUN ls -lah /github/workspace
RUN cat /github/workspace/entrypoint.sh || echo "entrypoint.sh missing"

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /github/workspace/entrypoint.sh
RUN ls -lah /github/workspace


ENTRYPOINT ["sh", "/github/workspace/entrypoint.sh"]
