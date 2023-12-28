FROM python:3.12

ENV HOME /root

WORKDIR /root

COPY . .

RUN pip install -r requirements.txt

EXPOSE 4242

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait && python -u server.py && python -u updater.py