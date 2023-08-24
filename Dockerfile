FROM python:3-alpine

RUN pip3 install pipenv
ENV GIT_PYTHON_REFRESH=quiet 
RUN apk add git && \
    git config --global user.email "kfir.bekhavod@develeap.com" && \
    git config --global user.name "kfir.bekhavod"
COPY app/helmgen /cli-helmgen-python
RUN cd /cli-helmgen-python && \
    pipenv install --system && \
    python setup.py install && \
    rm -rf /cli-helmgen-python

ENTRYPOINT [ "helmgen" ]