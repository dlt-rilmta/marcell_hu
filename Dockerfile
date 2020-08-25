FROM python:3.8-buster


ENV PYTHONUNBUFFERED 1
ENV JAVA_HOME=/usr/lib/jvm/adoptopenjdk-11-hotspot-amd64
ENV PATH="$JAVA_HOME/bin:${PATH}"
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${JAVA_HOME}/jre/lib/amd64/server/


# HFST
RUN apt-get update ; \
    apt-get install -y \
    hfst \
    software-properties-common \
    wget \
    ; \
    apt-get autoclean ; \
    apt-get autoremove -y


# JAVA
RUN wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | apt-key add - ; \
    add-apt-repository --yes https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/ ; \
    apt-get update && apt-get install -y adoptopenjdk-11-hotspot
RUN update-java-alternatives -s adoptopenjdk-11-hotspot-amd64


WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install --no-cache-dir uwsgi cython numpy && pip3 install --no-cache-dir \
    -r requirements.txt ;

COPY . /app

RUN adduser --no-create-home --system --shell /sbin/nologin --group uwsgi


ENTRYPOINT ["/app/docker/entrypoint.sh"]
