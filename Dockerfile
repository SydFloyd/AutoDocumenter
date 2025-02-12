FROM python:3.9

WORKDIR /app
COPY process_file.py /app/
COPY llm.py /app/

ENTRYPOINT ["python", "/app/process_file.py"]
