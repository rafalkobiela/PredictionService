FROM python:3.9-slim-buster as builder
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /usr/local/bin/wait
RUN chmod +x /usr/local/bin/wait
RUN pip install --upgrade pip
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

FROM python:3.9-slim-buster as runner
COPY --from=builder /usr/local /usr/local
COPY src/ /web_app/src
COPY alembic/ /web_app/alembic
COPY alembic.ini /web_app/alembic.ini

WORKDIR /web_app
ARG UVICORN_WORKERS
ARG APPLICATION_PORT

CMD /usr/local/bin/wait && alembic upgrade head && gunicorn src.main:app -b 0.0.0.0:${APPLICATION_PORT} -w ${UVICORN_WORKERS} -k uvicorn.workers.UvicornWorker
