FROM python:3.8

RUN python -m pip install \
    requests \
    pymongo

RUN \
    mkdir /var/stacks && \
    mkdir /var/stacks/stacks_core

VOLUME /var/stacks/logs
VOLUME /var/stacks/data
VOLUME /var/stacks/data_archive

COPY ./config.json /var/stacks/config.json
COPY ./ /var/stacks/stacks_core/
WORKDIR /var/stacks
