FROM python:3.10
RUN apt update -yq && \
    apt install less && \
    pip install flake8 pylint

COPY app/ /chesspy

WORKDIR /chesspy

RUN flake8 --max-line-length 140 main.py chesspy/
# RUN pylint main.py chesspy/

CMD python ./main.py