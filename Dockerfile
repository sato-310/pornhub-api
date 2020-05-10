FROM python:3.8.2

USER root

COPY / /app/

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "./src/app_start.py"]
