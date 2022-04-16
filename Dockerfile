FROM python:3.6-buster
LABEL maintainer="codyzacharias@pm.me"

COPY . /root

WORKDIR /root

RUN pip3 install . -r requirements.txt

CMD /bin/bash
