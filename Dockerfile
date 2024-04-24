FROM python:3.8-slim
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app
# COPY entrypoint.sh /app
#CMD ["python", "/app/main.py"]

ENTRYPOINT ["app/entrypoint.sh"]
