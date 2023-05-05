# Dockerfile for primary image
FROM jupyter/base-notebook:ubuntu-22.04 as base

ENV COMMANDBOX_HOME /home/jovyan/.CommandBox
ENV PATH /home/jovyan/.bin:$PATH

# Let's change to root user to install java 11
USER root

# Install Java
RUN apt-get update \
    && apt-get install -y gnupg ca-certificates curl \
    && curl -s https://repos.azul.com/azul-repo.key | gpg --dearmor -o /usr/share/keyrings/azul.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/azul.gpg] https://repos.azul.com/zulu/deb stable main" > /etc/apt/sources.list.d/zulu.list \
    && apt-get update \
    && apt-get install -y zulu11-jre-headless

# Install CommandBox v5.9.0
COPY --from=ortussolutions/commandbox@sha256:c1deedac96dd8ef1826ab5f0701c5c3748027acaf2191d11e0c62483963639d5 /usr/local/bin/box /home/jovyan/.bin/box
COPY --from=ortussolutions/commandbox@sha256:c1deedac96dd8ef1826ab5f0701c5c3748027acaf2191d11e0c62483963639d5 /usr/local/lib/CommandBox/ /home/jovyan/.CommandBox/

RUN chmod a+x /home/jovyan/.bin/box \
    && chown -R $NB_UID /home/jovyan/.bin \
    && chown -R $NB_UID /home/jovyan/.CommandBox \
    && echo "commandbox_home=${COMMANDBOX_HOME}" > /home/jovyan/.bin/commandbox.properties

# Let's change to  "$NB_USER" command so the image runs as a non root user by default
USER $NB_UID

# Let's define this parameter to install jupyter lab instead of the default juyter notebook command so we don't have to use it when running the container with the option -e
ENV JUPYTER_ENABLE_LAB=yes

FROM base AS development 
# Copy files to the /workspace dir for installation
COPY . /workspace

# Install the python module in development mode and install the kernels
USER root
RUN chown -R $NB_UID /workspace \
    && python -m pip install -e /workspace \
    && python -m cfml_kernel.cfscript.install \
    && python -m cfml_kernel.cfml.install

USER $NB_UID

FROM base AS main
# Copy files
COPY . /home/jovyan/.jupyter/cfml-kernel

# Install the python module and kernels
USER root
RUN chown -R $NB_UID /home/jovyan/.jupyter/cfml-kernel \
    && python -m pip install /home/jovyan/.jupyter/cfml-kernel \
    && python -m cfml_kernel.cfscript.install \
    && python -m cfml_kernel.cfml.install

USER $NB_UID