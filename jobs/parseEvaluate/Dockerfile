FROM python:3.11-alpine as base

# Ensure that the environment uses UTF-8 encoding by default
ENV LANG en_US.UTF-8
ENV ENV /etc/profile
ENV PIP_NO_CACHE_DIR true

# Stops Python default buffering to stdout, improving logging to the console.
ENV PYTHONUNBUFFERED 1

ENV APP_HOME /src/parseEvaluate

ARG USERNAME=default-user
ARG USER_UID=1000

WORKDIR ${APP_HOME}

# Add `$HOME/.local/bin` to PATH
RUN echo 'export PATH=$HOME/.local/bin:$PATH' >> /etc/profile

COPY . .

# upgrade apk and pip, add build dependencies to .build-deps virtual to be
# deleted later
RUN apk update --no-cache && \
    apk upgrade --no-cache && \
    apk add libpq && \
    apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
    apk add --no-cache bash && \
    pip install --upgrade pip && \
    adduser -u $USER_UID -D $USERNAME

# install requirements
RUN pip install -r ./requirements.txt

# Delete build dependencies
RUN apk del .build-deps

# allow setup shell scripts to run in container
RUN chmod +x ./setup.sh ./unzip.sh ./ingest-data.sh && \
    chown -R $USERNAME:$USERNAME $APP_HOME

# Create the user
USER $USERNAME
