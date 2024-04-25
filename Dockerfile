FROM python:3.8-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY entrypoint.sh /app/
COPY ./src /app/

#CMD ["python", "/app/main.py"]
ENTRYPOINT ["sh","/app/entrypoint.sh"]
