# Dockerfile for mybinder.org
#
# Test this Dockerfile:
#
#     docker build -t cfml-jupyter-binder .
#     docker run --rm -p 8888:8888 --name cfml-jupyter-binder cfml-jupyter-binder:latest jupyter lab --ServerApp.token=''
#

FROM ghcr.io/jsteinshouer/cfml-jupyter:1.1.0

USER root

ARG EXAMPLES_PATH=/home/$NB_USER/cfml_examples
COPY notebook_examples/*.ipynb $EXAMPLES_PATH/
RUN chown -R $NB_UID:users $EXAMPLES_PATH

USER $NB_UID