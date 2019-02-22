FROM python:3.6
RUN adduser --disabled-login hello_flask
WORKDIR /home/hello_flask
COPY . .
# debian系的
COPY ./sources.list /etc/apt/
RUN apt-get update &&apt-get install libssl-dev
RUN pip install -r requirements.txt -i https://pypi.doubanio.com/simple/
RUN chmod -R +x .
EXPOSE 5000:5000
ENTRYPOINT ["./boot.sh","run"]