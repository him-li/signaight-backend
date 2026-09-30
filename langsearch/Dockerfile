FROM python:3.12-slim-trixie

# install git and slim down image
RUN apt-get -y update && apt-get -y install dos2unix git tini \
    build-essential python3-dev dirmngr libdbus-glib-1-2 libxt6 libpci-dev

# Add the wait script to the image
COPY --from=ghcr.io/ufoscout/docker-compose-wait:latest /wait /wait
RUN chmod +x /wait

WORKDIR /opt/app

COPY ./lib /opt/app/lib/
RUN pip install --no-cache-dir -r /opt/app/lib/business_rules/requirements.txt \
    && pip install -e /opt/app/lib/business_rules

COPY ./core /opt/app/core/
COPY ./services /opt/app/services/
COPY ./langsearch /opt/app/langsearch/

#RUN pip install --upgrade pip && pip install --no-cache-dir \
#    -r /opt/app/core/requirements.txt \
#    -r /opt/app/services/requirements.txt \
#    -r /opt/app/langsearch/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir \
    -r /opt/app/langsearch/requirements.txt


COPY ./langsearch/entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh
RUN chmod 755 /entrypoint.sh

RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/man/?? /usr/share/man/??_*

ENV PYTHONPATH=/opt/app/langsearch:/opt/app
ENV PYTHONUNBUFFERED=True
# This is important to run jina flow with playwright inside
# playwright seems not compatible with uvloop
ENV JINA_DISABLE_UVLOOP=True

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]

# Here run tasks manager to perform searches with langgraph graph
CMD ["taskiq", "worker", "langsearch.app:broker", "--max-async-tasks", "24", "--max-threadpool-threads", "24"]
