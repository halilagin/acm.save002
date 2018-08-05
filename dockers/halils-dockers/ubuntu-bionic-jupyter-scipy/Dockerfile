#see https://github.com/jupyter/docker-stacks
  
FROM ubuntu-bionic-jupyter-minimal:0.0.1


USER root

# ffmpeg for matplotlib anim
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean
    # &&rm -rf /var/lib/apt/lists/*

USER $NB_UID

# Install Python 3 packages
# Remove pyqt and qt pulled in for matplotlib since we're only ever going to
# use notebook-friendly backends in these images
RUN conda install --quiet --yes  'conda-forge::blas=*=openblas' 
RUN conda install --quiet --yes    'ipywidgets=7.2*' 
RUN conda install --quiet --yes    'pandas=0.23*' 
RUN conda install --quiet --yes    'numexpr=2.6*' 
RUN conda install --quiet --yes    'matplotlib=2.2*' 
RUN conda install --quiet --yes    'scipy=1.1*' 
RUN conda install --quiet --yes    'seaborn=0.9*' 
RUN conda install --quiet --yes    'scikit-learn=0.19*' 
RUN conda install --quiet --yes    'scikit-image=0.14*' 
RUN conda install --quiet --yes    'sympy=1.1*'
RUN conda install --quiet --yes    'cython=0.28*' 
RUN conda install --quiet --yes    'patsy=0.5*' 
RUN conda install --quiet --yes    'statsmodels=0.9*' 
RUN conda install --quiet --yes    'cloudpickle=0.5*' 
RUN conda install --quiet --yes    'dill=0.2*' 
RUN conda install --quiet --yes    'numba=0.38*' 
RUN conda install --quiet --yes    'bokeh=0.12*' 
RUN conda install --quiet --yes    'sqlalchemy=1.2*' 
RUN conda install --quiet --yes    'hdf5=1.10*' 
RUN conda install --quiet --yes    'h5py=2.7*' 
RUN conda install --quiet --yes    'vincent=0.4.*' 
RUN conda install --quiet --yes    'beautifulsoup4=4.6.*' 
RUN conda install --quiet --yes    'protobuf=3.*' 
RUN conda install --quiet --yes    'xlrd' 


RUN conda remove --quiet --yes --force qt pyqt && \
    conda clean -tipsy && \
    # Activate ipywidgets extension in the environment that runs the notebook server
    jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    # Also activate ipywidgets extension for JupyterLab
    jupyter labextension install @jupyter-widgets/jupyterlab-manager@^0.35 && \
    jupyter labextension install jupyterlab_bokeh@^0.5.0 && \
    npm cache clean --force && \
    rm -rf $CONDA_DIR/share/jupyter/lab/staging && \
    rm -rf /home/$NB_USER/.cache/yarn && \
    rm -rf /home/$NB_USER/.node-gyp && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# Install facets which does not have a pip or conda package at the moment
RUN cd /tmp && \
    git clone https://github.com/PAIR-code/facets.git && \
    cd facets && \
    jupyter nbextension install facets-dist/ --sys-prefix && \
    cd && \
    rm -rf /tmp/facets && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# Import matplotlib the first time to build the font cache.
ENV XDG_CACHE_HOME /home/$NB_USER/.cache/
RUN MPLBACKEND=Agg python -c "import matplotlib.pyplot" && \
    fix-permissions /home/$NB_USER

USER $NB_UID

