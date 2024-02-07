FROM python:3.11-alpine as base

# upgrade apk and pip, add build dependencies to .build-deps virtual to be
# deleted later
RUN apk update --no-cache && \
    apk upgrade --no-cache && \
    apk add libpq && \
    apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
    apk add --no-cache bash && \
    apk add postgresql15=15.5-r0 \
    pip install --upgrade pip 

# Ensure that the environment uses UTF-8 encoding by default
ENV LANG en_US.UTF-8
ENV ENV /etc/profile
ENV PIP_NO_CACHE_DIR true

ENV APP_HOME /src/metro2/django

ARG USERNAME=default-user
ARG USER_UID=1002

RUN adduser -u $USER_UID -D $USERNAME

WORKDIR ${APP_HOME}

# Add `$HOME/.local/bin` to PATH
RUN echo 'export PATH=$HOME/.local/bin:$PATH' >> /etc/profile

COPY . .
    
RUN pip install -r ./requirements.txt

# Delete build dependencies
RUN apk del .build-deps

RUN chown -R $USERNAME:$USERNAME $APP_HOME

# Create the user
USER $USERNAME

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]