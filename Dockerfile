FROM python:3.6-alpine

RUN adduser -D hello_flask

WORKDIR /home/hello_flask

COPY . .


RUN python -m venv venv
RUN apt-get update && apt-get install -y mysql-client && rm -rf /var/lib/apt

RUN venv/bin/pip install -r requirements/requirements.txt -i https://pypi.douban.com/simple

RUN chmod +x .

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]






