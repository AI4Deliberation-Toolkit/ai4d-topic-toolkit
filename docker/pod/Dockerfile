# Pod-only image: bundles Django app + PostgreSQL + supervisor in ONE container,
# because a Runpod pod runs a single container. NOT used by the server deployment,
# which continues to use docker/web/Dockerfile.
# Pin bookworm: the PGDG 'bookworm-pgdg' postgresql-17 package depends on
# libicu72, which only the bookworm base provides (trixie ships libicu76).
FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PGDATA=/data/pgdata \
    HF_HOME=/data/hf_cache \
    PATH="/usr/lib/postgresql/17/bin:${PATH}"

# PostgreSQL 17 (PGDG repo, to match the server's 17.x), supervisor, netcat, gosu
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg \
 && install -d /usr/share/postgresql-common/pgdg \
 && curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc \
        -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc \
 && echo "deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt bookworm-pgdg main" \
        > /etc/apt/sources.list.d/pgdg.list \
 && apt-get update && apt-get install -y --no-install-recommends \
        postgresql-17 supervisor netcat-traditional gosu \
 && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

COPY ./requirements.txt /usr/src/app/
WORKDIR /usr/src/app/

RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

COPY . /usr/src/app/

RUN cp docker/pod/supervisord.conf /etc/supervisor/supervisord.conf \
 && chmod +x docker/pod/pod-entrypoint.sh docker/pod/app-start.sh

EXPOSE 8000
ENTRYPOINT ["/usr/src/app/docker/pod/pod-entrypoint.sh"]
