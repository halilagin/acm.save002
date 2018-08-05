FROM base-ubuntu-bionic:0.0.1

ARG USERNAME=jovyan
ARG USERHOME=/home/jovyan
ARG USERID=1000
ARG USERGECOS=jovyan



#jovyan already exists in base-ubuntu-bionic
#RUN adduser \
#  --home "$USERHOME" \
#  --uid $USERID \
#  --gecos "$USERGECOS" \
#  --disabled-password \
#  "$USERNAME"


# Install Oracle Java 8
ENV JAVA_VER 8
ENV JAVA_HOME /usr/lib/jvm/java-8-oracle

RUN apt-get -y --force-yes --no-install-recommends install gnupg

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
