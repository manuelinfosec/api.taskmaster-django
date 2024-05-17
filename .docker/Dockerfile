FROM python:3.10-slim as base

RUN adduser --disabled-password --gecos '' user

# RUN apk --update add gcc build-base freetype-dev libpng-dev openblas-dev

USER user
WORKDIR /home/user/taskapp

ENV PATH="/home/user/.local/bin:$PATH"
COPY --chown=user:user requirements.txt .

# install supervisord
RUN pip install supervisor
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy over deployment files
COPY .docker/deployment/gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf
COPY .docker/deployment/daphne.conf /etc/supervisor/conf.d/daphne.conf

COPY --chown=user:user . .

RUN chmod +x scripts/*

FROM base as prod

CMD [ "sh", "scripts/run_gunirorn.sh" ]
