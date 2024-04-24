FROM python:3.8-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh

#CMD ["python", "/app/main.py"]
ENTRYPOINT ["/entrypoint.sh"]
