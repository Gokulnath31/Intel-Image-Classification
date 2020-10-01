FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3 python3-pip sudo

RUN useradd -m goku

RUN chown -R goku:goku /home/goku/

COPY --chown=goku . /home/goku/app/

USER goku

RUN cd /home/goku/app/ && pip3 install -r requirements.txt

WORKDIR /home/goku/app

EXPOSE 8080

ENTRYPOINT python3 api.py
