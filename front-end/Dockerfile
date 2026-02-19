FROM node:24-alpine AS base

# Ensure that the environment uses UTF-8 encoding by default
ENV LANG=en_US.UTF-8
ENV ENV=/etc/profile
ENV PIP_NO_CACHE_DIR=true

ENV APP_HOME=/src/frontend

ARG USERNAME=default-user
ARG USER_UID=1001
RUN adduser -u $USER_UID -D $USERNAME

WORKDIR ${APP_HOME}

# Add `$HOME/.local/bin` to PATH
RUN echo 'export PATH=$HOME/.local/bin:$PATH' >> /etc/profile

COPY . .

# Add Zscaler Root CA certificate, rebuild CA certificates, and both the root
# cert and the rebuilt ca-certificates cert to APP_HOME for reuse.
ADD https://raw.githubusercontent.com/cfpb/zscaler-cert/refs/heads/main/zscaler_root_ca.pem /usr/local/share/ca-certificates/zscaler_root_ca.crt
RUN apk add --no-cache --no-check-certificate ca-certificates && update-ca-certificates
ENV NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt

# Enabled Corepack
RUN corepack enable

# Fetch the Yarn version specified in package.json
RUN corepack prepare --activate

RUN yarn && \
    chown -R $USERNAME:$USERNAME $APP_HOME

# Create the user
USER $USERNAME
