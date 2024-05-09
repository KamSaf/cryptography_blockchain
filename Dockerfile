FROM ubuntu

WORKDIR /app

ADD . /app

RUN apt update
RUN apt install python3-pip -y
RUN pip install -r requirements.txt

CMD [ "flask", "run", "--host", "0.0.0.0"]