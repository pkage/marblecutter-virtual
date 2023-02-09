# # Only 3.11>Python>3.8 is compatible from testing
# FROM python:3.10-slim

# base off latest gdal
FROM osgeo/gdal:ubuntu-small-3.6.2

# have to manually install python
RUN apt-get update -y
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update -y
RUN apt-get install python3.10 python3.10-dev -y

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.10 get-pip.py

ENV PORT=8085

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV GDAL_CACHEMAX 512
ENV GDAL_DISABLE_READDIR_ON_OPEN TRUE
ENV GDAL_HTTP_MERGE_CONSECUTIVE_RANGES YES
ENV VSI_CACHE TRUE
# tune this according to how much memory is available
ENV VSI_CACHE_SIZE 536870912
# override this accordingly; should be 2-4x $(nproc)
ENV WEB_CONCURRENCY 4


# Add 'psycopg2' dependencies and 'tini' packages
RUN apt-get update && apt-get install -y \
        gcc \
        g++ \
        tini && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/marblecutter

COPY . .

# needs to run in venv because nothing is ever easy
RUN python3.10 -m pip install --no-cache-dir poetry && \
    poetry install --no-interaction


ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "sh", "-c", "poetry run uvicorn ${APP} --host 0.0.0.0 --port ${PORT} --reload" ]
