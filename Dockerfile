FROM python:3

COPY app/ /chesspy

WORKDIR /chesspy

CMD python ./main.py board