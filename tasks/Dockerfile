FROM jinaai/jina:3.34-py311-standard

# install git and slim down image
RUN apt-get -y update \
    && apt-get -y install dos2unix git build-essential python3-dev dirmngr \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/man/?? /usr/share/man/??_*

# Add the wait script to the image
COPY --from=ghcr.io/ufoscout/docker-compose-wait:latest /wait /wait
RUN chmod +x /wait

WORKDIR /opt/app

COPY ./lib /opt/app/lib/
RUN pip install  --no-cache-dir -r  /opt/app/lib/business_rules/requirements.txt \
    && pip install -e /opt/app/lib/business_rules

COPY ./core /opt/app/core/
COPY ./cli /opt/app/cli/
COPY ./tasks /opt/app/tasks/
# should detached from this image as dependency
# flows code refactoring required
COPY ./services /opt/app/services/

#install with override docarray for master jina branch to support DocArrayv2
RUN pip install --upgrade pip && pip install  --no-cache-dir \
    -r /opt/app/cli/requirements.txt \
    -r /opt/app/tasks/requirements.txt \
    -r /opt/app/services/requirements.txt

COPY ./tasks/entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh
RUN chmod 755 /entrypoint.sh

ENV PYTHONPATH=/opt/app
ENV PYTHONUNBUFFERED=True

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["taskiq", "worker", "tasks.app:broker", "--max-async-tasks", "24", "--max-threadpool-threads", "24"]
