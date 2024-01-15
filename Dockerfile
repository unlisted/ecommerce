# syntax=docker/dockerfile:1.4
FROM python:3.12-alpine AS builder

# upgrade pip
RUN pip install --upgrade pip

# get curl for healthchecks
RUN apk add curl
RUN apk add build-base
RUN apk add libffi-dev

# permissions and nonroot user for tightened security
RUN adduser -D nonroot

# home dir for everything
RUN mkdir -p /home/ecommerce/ecommerce && chown -R nonroot:nonroot /home/ecommerce

WORKDIR /home/ecommerce
USER nonroot

# copy all the files to the container
COPY --chown=nonroot:nonroot . .

# install poetry
ENV POETRY_HOME=/home/ecommerce/poetry
RUN curl -sSL https://install.python-poetry.org | python3 - 

# python virtual env setup
ENV VIRTUAL_ENV=/home/ecommerce/venv
RUN python -m venv $VIRTUAL_ENV

# uncomment if there's a rust dependency
# RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

ENV HOME=/home/ecommerce
ENV PATH="$VIRTUAL_ENV/bin:$HOME/.cargo/bin:$POETRY_HOME/bin:$PATH"
ENV DEBUG=${DEBUG}

RUN poetry install

# define the port number the container should expose
EXPOSE 8080
#EXPOSE 5678

# default command
CMD ["/bin/sh", "./entrypoint.sh"]