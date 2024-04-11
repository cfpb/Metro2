FROM node:20-alpine as base

# Ensure that the environment uses UTF-8 encoding by default
ENV LANG en_US.UTF-8
ENV ENV /etc/profile
ENV PIP_NO_CACHE_DIR true

ENV APP_HOME /src/frontend

ARG USERNAME=default-user
ARG USER_UID=1001

WORKDIR ${APP_HOME}

# Add `$HOME/.local/bin` to PATH
RUN echo 'export PATH=$HOME/.local/bin:$PATH' >> /etc/profile

COPY . .

RUN adduser -u $USER_UID -D $USERNAME && \
    yarn && \
    chown -R $USERNAME:$USERNAME $APP_HOME

# Create the user
USER $USERNAME