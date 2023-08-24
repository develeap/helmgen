FROM python:3-alpine

RUN pip3 install pipenv

COPY app/ /cli-helmgen-python
RUN cd /cli-helmgen-python && \
    pipenv install && \
    python setup.py install && \
    rm -rf /cli-helmgen-python

ENTRYPOINT [ "helmgen" ]