FROM python:3.6-alpine

RUN adduser -D hello_flask

WORKDIR /home/hello_flask

COPY . .

RUN python -m venv venv

RUN venv/bin/pip install -r requirements/requirements.txt

RUN chmod +x .

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]






