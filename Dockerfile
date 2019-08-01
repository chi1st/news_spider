FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y git

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel
#FROM python:3.6
ENV PATH /usr/local/bin:$PATH
ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt
RUN pip3 install shadowsocks
RUN mkdir /etc/shadowsocks
RUN cp config.json /etc/shadowsocks/config.json
RUN sslocal -c /etc/shadowsocks/config.json -d start
RUN apt install -y privoxy
RUN cp -af gfw.action /etc/privoxy/
RUN export http_proxy=http://127.0.0.1:8118
RUN export https_proxy=http://127.0.0.1:8118
RUN export no_proxy=localhost
RUN echo 'actionsfile gfw.action' >> /etc/privoxy/config
RUN service privoxy start

CMD scrapy crawl cnn
CMD scrapy crawl bbc