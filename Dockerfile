FROM python:3.11-slim

WORKDIR /github/workspace
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# RUN ls -lah /github/workspace

ENTRYPOINT ["python", "AutoDocstring.py"]
