FROM python:3.9

WORKDIR /app
COPY AutoDocstring.py /app/
COPY llm.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "AutoDocstring.py"]
