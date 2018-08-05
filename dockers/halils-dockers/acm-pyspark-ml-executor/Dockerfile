FROM ubuntu-bionic-pyspark:0.0.1

ENV NB_USER jovyan
ENV HOME /home/$NB_USER
ENV WD $HOME/acm/ml/classification/text-clsf

USER root






RUN mkdir -p /home/$NB_USER/spark.data
RUN mkdir -p $WD


WORKDIR $WD

COPY requirements.txt .
RUN pip install -r requirements.txt



