#############################################################################
## Stage: base front-end image image
FROM node:24-alpine AS base

# Ensure that the environment uses UTF-8 encoding by default
ENV LANG=en_US.UTF-8
ENV ENV=/etc/profile
ENV PIP_NO_CACHE_DIR=true

ENV APP_HOME=/src/frontend
WORKDIR ${APP_HOME}

# Add Zscaler Root CA certificate, rebuild CA certificates, and both the root
# cert and the rebuilt ca-certificates cert to APP_HOME for reuse.
ADD https://raw.githubusercontent.com/cfpb/zscaler-cert/refs/heads/main/zscaler_root_ca.pem /usr/local/share/ca-certificates/zscaler_root_ca.crt
RUN apk add --no-cache --no-check-certificate ca-certificates && update-ca-certificates
ENV NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt

# Make sure everything is up to date
RUN apk update --no-cache && apk upgrade --no-cache

COPY . ${APP_HOME}

# Prepare yarn
RUN corepack enable && \
    corepack prepare --activate && \
    yarn

#############################################################################
### Stage: dev to run `yarn dev` as a non-root user
FROM base AS dev

# Run as a non-root user
ARG USERNAME=default
ARG USER_UID=1001
RUN adduser -u $USER_UID -D $USERNAME
RUN chown -R $USERNAME:$USERNAME $APP_HOME
USER $USERNAME

CMD ["yarn", "dev"]

#############################################################################
### Stage: builder to run `yarn build` and build the frontend
FROM base AS builder
RUN yarn build
