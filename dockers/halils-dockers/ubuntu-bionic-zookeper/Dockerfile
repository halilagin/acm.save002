FROM base-ubuntu-bionic:0.0.1

ARG USERNAME=jovyan
ARG USERHOME=/home/jovyan
ARG USERID=1000
ARG USERGECOS=jovyan
ENV NB_USER jovyan



#jovyan already exists in base-ubuntu-bionic
#RUN adduser \
#  --home "$USERHOME" \
#  --uid $USERID \
#  --gecos "$USERGECOS" \
#  --disabled-password \
#  "$USERNAME"

#RUN apt-get update
RUN apt-get install -y \
  unzip \ 
  gnupg \ 
  wget \
  supervisor \
  docker.io \
  openssh-server && \
  # Removing documentation packages *after* installing them is kind of hacky,
  # but it only adds some overhead while building the image.
  apt-get --purge remove -y .\*-doc$ && \
  # Remove more unnecessary stuff
  apt-get clean -y



# JAVA
ARG JAVA_MAJOR_VERSION=8
ARG JAVA_UPDATE_VERSION=141
ARG JAVA_BUILD_NUMBER=15
ENV JAVA_HOME /usr/jdk1.${JAVA_MAJOR_VERSION}.0_${JAVA_UPDATE_VERSION}


#RUN curl -sL --retry 3 --insecure \
  #--header "Cookie: oraclelicense=accept-securebackup-cookie;" \
  #"http://download.oracle.com/otn-pub/java/jdk/${JAVA_MAJOR_VERSION}u${JAVA_UPDATE_VERSION}-b${JAVA_BUILD_NUMBER}/512cd62ec5174c3487ac17c61aaa89e8/server-jre-${JAVA_MAJOR_VERSION}u${JAVA_UPDATE_VERSION}-linux-x64.tar.gz" \

RUN wget -c -O "jdk-${JAVA_MAJOR_VERSION}u${JAVA_UPDATE_VERSION}-linux-x64.tar.gz" --no-check-certificate --no-cookies --header \
"Cookie: oraclelicense=accept-securebackup-cookie" \
"http://download.oracle.com/otn-pub/java/jdk/8u141-b15/336fa29ff2bb4ef291e347e091f7f4a7/jdk-${JAVA_MAJOR_VERSION}u${JAVA_UPDATE_VERSION}-linux-x64.tar.gz" \
  && tar -xvzf jdk-${JAVA_MAJOR_VERSION}u${JAVA_UPDATE_VERSION}-linux-x64.tar.gz  -C /usr/ \
  && ln -s $JAVA_HOME /usr/java \
  && rm -rf $JAVA_HOME/man

RUN echo 'root:123456' | chpasswd
RUN mkdir /var/run/sshd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

USER $NB_USER

ENV ZOOKEEPER_VERSION 3.4.12


WORKDIR /home/$NB_USER

#Download Zookeeper
RUN cd /home/$NB_USER && wget -q http://mirror.vorboss.net/apache/zookeeper/zookeeper-${ZOOKEEPER_VERSION}/zookeeper-${ZOOKEEPER_VERSION}.tar.gz && \
wget -q https://www.apache.org/dist/zookeeper/KEYS && \
wget -q https://www.apache.org/dist/zookeeper/zookeeper-${ZOOKEEPER_VERSION}/zookeeper-${ZOOKEEPER_VERSION}.tar.gz.asc && \
wget -q https://www.apache.org/dist/zookeeper/zookeeper-${ZOOKEEPER_VERSION}/zookeeper-${ZOOKEEPER_VERSION}.tar.gz.md5 && \
md5sum -c zookeeper-${ZOOKEEPER_VERSION}.tar.gz.md5 && \
gpg --import KEYS && \
gpg --verify zookeeper-${ZOOKEEPER_VERSION}.tar.gz.asc && \
tar -xzf zookeeper-${ZOOKEEPER_VERSION}.tar.gz 


ENV ZK_HOME /home/$NB_USER/zookeeper-${ZOOKEEPER_VERSION}

#Configure
RUN mv ${ZK_HOME}/conf/zoo_sample.cfg ${ZK_HOME}/conf/zoo.cfg
RUN sed  -i "s|/tmp/zookeeper|$ZK_HOME/data|g" $ZK_HOME/conf/zoo.cfg; mkdir $ZK_HOME/data

ADD start-zk.sh /usr/bin/start-zk.sh 
EXPOSE 22 2181 2888 3888


WORKDIR $ZK_HOME
VOLUME ["${ZOOKEEPER_HOME}/conf", "${ZOOKEEPER_HOME}/data"]

CMD /usr/sbin/sshd && bash /usr/bin/start-zk.sh


