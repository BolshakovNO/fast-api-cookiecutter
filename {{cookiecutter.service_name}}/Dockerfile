FROM docker-standoff-snapshot.ptsecurity.ru/python:3.10.4-alpine3.15 as base

RUN echo "http://apt-mirror.build.ptsecurity.ru/alpine/v3.15/main" > /etc/apk/repositories && \
    echo "http://apt-mirror.build.ptsecurity.ru/alpine/v3.15/community" >> /etc/apk/repositories


WORKDIR /app
RUN apk update && \
    apk add python3-dev \
            gcc \
            libc-dev \
            libffi-dev \
            openssh \
            build-base

FROM base as requirements

COPY requirements.txt /app/
RUN pip install -U setuptools pip
RUN pip install -r requirements.txt

# # TEST IMAGE
# FROM requirements as test
#
# WORKDIR /app
# COPY requirements-test.txt /app/
# RUN pip install -r requirements-test.txt --index-url=https://pypi-proxy.ptsecurity.com --trusted-host=pypi-proxy.ptsecurity.com
#
# COPY ./{{cookiecutter.service_name}} /app/{{cookiecutter.service_name}}
# COPY ./tests /app/tests
# COPY ./scripts /app/scripts
#
# CMD python -m pytest tests

# RUNNING IMAGE
FROM requirements as prod

WORKDIR /app
COPY ./{{cookiecutter.service_name}} /app/{{cookiecutter.service_name}}
COPY ./scripts /app/scripts

CMD python -m {{cookiecutter.service_name}}.run