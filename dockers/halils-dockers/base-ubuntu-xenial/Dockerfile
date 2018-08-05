FROM ubuntu:xenial-20180705

ARG USERNAME=jovyan
ARG USERHOME=/home/jovyan
ARG USERID=1000
ARG USERGECOS=jovyan

ENV TZ 'Europe/London'
RUN echo $TZ > /etc/timezone && \
apt-get update && apt-get install -y tzdata && \
rm /etc/localtime && \
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
dpkg-reconfigure -f noninteractive tzdata 

RUN apt-get install --quiet --yes --no-install-recommends \
build-essential \
emacs \
git \
netcat \
python-dev \
python \
python3 \
unzip \
nano \
vim \
wget \
make \
screen \
tar \
&& apt-get clean



RUN adduser \
  --home "$USERHOME" \
  --uid $USERID \
  --gecos "$USERGECOS" \
  --disabled-password \
  "$USERNAME"

