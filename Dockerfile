FROM python:3.6-buster

COPY . /root
WORKDIR /root
RUN pip3 install . -r requirements.txt
CMD /bin/bash
