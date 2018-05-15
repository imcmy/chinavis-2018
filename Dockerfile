FROM python:3

WORKDIR /usr/src/app

EXPOSE 5000

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "-m", "flask", "run",  "--host=0.0.0.0" ]
