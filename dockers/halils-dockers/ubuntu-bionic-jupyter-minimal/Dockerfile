#see https://github.com/jupyter/docker-stacks
  
FROM ubuntu-bionic-base-jupyter:0.0.1


USER root
ENV NB_UID 1000
ENV NB_USER jovyan
# Install all OS dependencies for fully functional notebook server
RUN apt-get update && apt-get install -yq --no-install-recommends \
    inkscape \
    jed \
    libsm6 \
    libxext-dev \
    libxrender1 \
    lmodern \
    && apt-get clean 
    # && rm -rf /var/lib/apt/lists/*

# Switch back to jovyan to avoid accidental container runs as root
USER $NB_USER
