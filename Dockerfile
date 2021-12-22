FROM python:3
RUN apt update -yq && \
    apt install less

COPY app/ /chesspy

WORKDIR /chesspy

CMD python ./main.py board