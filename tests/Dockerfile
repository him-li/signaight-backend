FROM jinaai/jina:3.34-py311-standard

# install git and slim down image
RUN apt-get -y update && apt-get -y install dos2unix git tini \
    build-essential python3-dev dirmngr

# Add the wait script to the image
COPY --from=ghcr.io/ufoscout/docker-compose-wait:latest /wait /wait
COPY --from=fullstorydev/grpcurl:latest /bin/grpcurl /bin/grpcurl
RUN chmod +x /wait /bin/grpcurl

WORKDIR /opt/app

COPY ./lib /opt/app/lib/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /opt/app/lib/business_rules/requirements.txt \
    && pip install -e /opt/app/lib/business_rules

COPY ./core /opt/app/core/
COPY ./cli /opt/app/cli/
COPY ./services /opt/app/services/
COPY ./tasks /opt/app/tasks/
COPY ./api /opt/app/api/
COPY ./tests /opt/app/tests/

#install with override docarray for master jina branch to support DocArrayv2
RUN pip install --upgrade pip && pip install --no-cache-dir \
    -r /opt/app/core/requirements.txt \
    -r /opt/app/cli/requirements.txt \
    -r /opt/app/services/requirements.txt \
    -r /opt/app/tasks/requirements.txt \
    -r /opt/app/api/requirements.txt \
    -r /opt/app/tests/requirements.txt

COPY ./api/entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh
RUN chmod 755 /entrypoint.sh

RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/man/?? /usr/share/man/??_*

ENV PYTHONPATH=/opt/app
ENV PYTHONUNBUFFERED=True
# This is important to run jina flow with playwright inside
# playwright seems not compatible with uvloop
ENV JINA_DISABLE_UVLOOP=True

ENTRYPOINT ["/entrypoint.sh"]
CMD ["pytest", "--show-capture", "no", "-p", "no:logging", "--no-header", "-v", "tests"]
