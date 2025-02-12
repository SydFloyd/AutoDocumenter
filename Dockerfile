FROM python:3.9

WORKDIR /app
COPY AutoDocstring.py /app/
COPY llm.py /app/

ENTRYPOINT ["python", "/app/AutoDocstring.py"]
