FROM jinaai/jina:3.34-py311-standard

# install git and slim down image
RUN apt-get -y update && apt-get -y install dos2unix git curl wget tini \
    build-essential python3-dev libdbus-glib-1-2 libxt6 libpci-dev

# Add the wait script to the image
COPY --from=ghcr.io/ufoscout/docker-compose-wait:latest /wait /wait
COPY --from=fullstorydev/grpcurl:latest /bin/grpcurl /bin/grpcurl
RUN chmod +x /wait /bin/grpcurl

WORKDIR /opt/app

COPY ./lib /opt/app/lib/
RUN pip install  --no-cache-dir -r  /opt/app/lib/business_rules/requirements.txt \
    && pip install -e /opt/app/lib/business_rules

COPY ./core /opt/app/core/
COPY ./cli /opt/app/cli/
COPY ./services /opt/app/services/

#install with override docarray for master jina branch to support DocArrayv2
RUN pip install --upgrade pip && pip install --no-cache-dir \
    -r /opt/app/cli/requirements.txt \
    -r /opt/app/services/requirements.txt

COPY ./services/entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh
RUN chmod 755 /entrypoint.sh

RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/man/?? /usr/share/man/??_*

ENV PYTHONPATH=/opt/app
ENV PYTHONUNBUFFERED=True
# This is important to run jina flow with playwright inside
# playwright seems not compatible with uvloop
ENV JINA_DISABLE_UVLOOP=True

EXPOSE 51234-60000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["tini", "-v", "--", "python", "services/complex.py"]
