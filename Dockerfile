# Dockerfile for mybinder.org
#
# Test this Dockerfile:
#
#     docker build -t cfml-jupyter-binder .
#     docker run --rm -p 8888:8888 --name cfml-jupyter-binder cfml-jupyter-binder:latest jupyter lab --ServerApp.token=''
#

FROM ghcr.io/jsteinshouer/cfml-jupyter-kernel:0.1

USER root

ARG EXAMPLES_PATH=/home/$NB_USER/cfml_examples
COPY notebooks/*.ipynb $EXAMPLES_PATH/
RUN chown -R $NB_UID:users $EXAMPLES_PATH

USER $NB_UID