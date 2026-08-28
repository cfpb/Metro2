#############################################################################
## Stage: base python/django image
FROM python:3.14-alpine AS base

# Ensure that the environment uses UTF-8 encoding by default
ENV LANG=en_US.UTF-8
ENV ENV=/etc/profile
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=true
ENV PIP_ROOT_USER_ACTION=ignore

ENV APP_HOME=/src/metro2
WORKDIR ${APP_HOME}/django

# Add Zscaler Root CA certificate and rebuild CA certificates
ADD https://raw.githubusercontent.com/cfpb/zscaler-cert/3982ebd9edf9de9267df8d1732ff5a6f88e38375/zscaler_root_ca.pem /usr/local/share/ca-certificates/zscaler_root_ca.crt
RUN apk add --no-cache --no-check-certificate ca-certificates && update-ca-certificates

# upgrade apk and pip, add build dependencies to .build-deps virtual to be
# deleted later
RUN apk update --no-cache && \
    apk upgrade --no-cache && \
    apk add libpq && \
    apk add --virtual .build-deps gcc python3-dev musl-dev && \
    apk add --no-cache aws-cli bash jq && \
    apk add libffi-dev && \
    pip install --upgrade pip

# Copy the django application into the WORKDIR
COPY . .

RUN pip install -r ./requirements.txt

# Delete build dependencies
RUN apk del .build-deps

#############################################################################
### Stage: development application
FROM base AS dev

# Write the VERSION arg to a file in APP_HOME
ARG VERSION=unknown
RUN echo "$VERSION" > $APP_HOME/version.txt

# Run as a non-root user
ARG USERNAME=default
ARG USER_UID=1000
RUN adduser -u $USER_UID -D $USERNAME
RUN chown -R $USERNAME:$USERNAME $APP_HOME
USER $USERNAME

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
