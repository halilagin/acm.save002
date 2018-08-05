#see https://github.com/jupyter/docker-stacks
  
FROM ubuntu-bionic-jupyter-scipy:0.0.1

USER root

RUN conda install --quiet --yes  jupyter_contrib_nbextensions


USER $NB_USER

