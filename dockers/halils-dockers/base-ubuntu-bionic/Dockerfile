FROM ubuntu:bionic-20180526@sha256:c8c275751219dadad8fa56b3ac41ca6cb22219ff117ca98fe82b42f24e1ba64e

USER root

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
python3.6 \
unzip \
nano \
vim \
wget \
make \
screen \
tar 


RUN apt-get install -y libsnappy-dev
RUN apt-get install -y openssh-client openssh-server
RUN apt-get install -y net-tools dnsmasq
RUN apt-get install -y supervisor

# install dev tools
RUN apt-get  install -y curl which tar sudo  rsync wget  openssl  | true && \
    echo user=root >> /etc/dnsmasq.conf && \
    echo bogus-priv >> /etc/dnsmasq.conf && \
    echo interface=eth0 >> /etc/dnsmasq.conf && \
    echo no-dhcp-interface=eth0 >> /etc/dnsmasq.conf


RUN apt-get install -y curl
RUN apt-get clean
 
# passwordless ssh
RUN yes y | ssh-keygen -q -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key && \
    yes y | ssh-keygen -q -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key && \
    yes y | ssh-keygen -q -N "" -t rsa -f /root/.ssh/id_rsa && \
    cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys

#copy ssh keys to passwordless ssh connect
ADD ssh_client_conf/config /root/.ssh/config
ADD ssh_client_conf/authorized_keys /root/.ssh/authorized_keys
ADD ssh_client_conf/id_rsa /root/.ssh/id_rsa
ADD ssh_client_conf/id_rsa.pub /root/.ssh/id_rsa.pub
RUN chmod 644 /root/.ssh/authorized_keys && \
    chmod 600 /root/.ssh/config && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 644 /root/.ssh/id_rsa.pub && \
    chown root:root /root/.ssh/*

# fix the 254 error code
RUN sed  -i "/^[^#]*UsePAM/ s/.*/#&/"  /etc/ssh/sshd_config && \
    echo "UsePAM no" >> /etc/ssh/sshd_config 



ADD bootstrap.sh /etc/bootstrap.sh
RUN chown root:root /etc/bootstrap.sh && \
    chmod 700 /etc/bootstrap.sh

ENV BOOTSTRAP /etc/bootstrap.sh
COPY bootstrap.supervisor.conf /etc/supervisor/conf.d/supervisord.conf


RUN adduser \
  --home "$USERHOME" \
  --uid $USERID \
  --gecos "$USERGECOS" \
  --disabled-password \
  "$USERNAME"

CMD  ["/usr/bin/supervisord"]
#CMD ["/etc/init.d/supervisor","start"]
