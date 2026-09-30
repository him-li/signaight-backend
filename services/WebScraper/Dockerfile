FROM jinaai/jina:3.34-py311-standard

RUN apt-get -y update \
    && apt-get -y install dos2unix git curl wget build-essential python3-dev

## Add the wait script to the image
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

WORKDIR /opt/app

COPY --from=fullstorydev/grpcurl:latest /bin/grpcurl /bin/grpcurl

COPY ./lib /opt/app/lib/
RUN pip install --no-cache-dir -r /opt/app/lib/business_rules/requirements.txt \
    && pip install -e /opt/app/lib/business_rules

COPY ./services/WebScraper /opt/app
# build should run only in repo root context to include core library
COPY ./core /opt/app/core

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY ./services/entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh
RUN chmod 755 /entrypoint.sh

ENV PYTHONPATH=/opt/app
ENV PYTHONUNBUFFERED=True
# This is important to run jina flow with playwright inside
# playwright seems not compatible with uvloop
ENV JINA_DISABLE_UVLOOP=True

#EXPOSE 55961-55962
#ENTRYPOINT ["/entrypoint.sh"]
#CMD ["jina", "executor", "--uses", "config.yml", "--ports", "55961", "55962", "--protocols", "GRPC", "HTTP"]

EXPOSE 55961
ENTRYPOINT ["/entrypoint.sh"]
CMD ["jina", "executor", "--uses", "config.yml", "--ports", "55961",  "--protocols", "GRPC"]
