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


RUN apt-get update && apt-get install -y \
  texlive-full \
  pandoc\
  python-pygments && \
  # Removing documentation packages *after* installing them is kind of hacky,
  # but it only adds some overhead while building the image.
  apt-get --purge remove -y .\*-doc$ && \
  # Remove more unnecessary stuff
  apt-get clean -y
