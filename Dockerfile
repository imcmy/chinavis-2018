FROM python:3
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

EXPOSE 5000

ADD . .
RUN pip install --no-cache-dir -r requirements.txt
