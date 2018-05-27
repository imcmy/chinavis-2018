FROM python:3
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

ADD requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

EXPOSE 5000
