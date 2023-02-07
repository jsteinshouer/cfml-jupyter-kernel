# Dockerfile for primary image
FROM jupyter/base-notebook:ubuntu-22.04

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

COPY ./cfml_kernel /home/jovyan/.jupyter/kernels/cfml_kernel
COPY ./cfscript_kernel /home/jovyan/.jupyter/kernels/cfscript_kernel

RUN chown -R $NB_UID /home/jovyan/.jupyter/kernels \
    && pip install -e ./.jupyter/kernels/cfscript_kernel \
    && python -m cfscript_kernel.install \
    && pip install -e ./.jupyter/kernels/cfml_kernel \
    && python -m cfml_kernel.install

# Install CommandBox from minibox to help make the image smaller
COPY --from=foundeo/minibox:2023.01 /opt/box /home/jovyan/.bin
COPY --from=foundeo/minibox:2023.01 /root/.CommandBox/ /home/jovyan/.CommandBox/

RUN chmod a+x /home/jovyan/.bin/box \
    && chown -R $NB_UID /home/jovyan/.bin \
    && chown -R $NB_UID /home/jovyan/.CommandBox \
    && echo "commandbox_home=${COMMANDBOX_HOME}" > /home/jovyan/.bin/commandbox.properties

# Let's change to  "$NB_USER" command so the image runs as a non root user by default
USER $NB_UID

# Let's define this parameter to install jupyter lab instead of the default juyter notebook command so we don't have to use it when running the container with the option -e
ENV JUPYTER_ENABLE_LAB=yes