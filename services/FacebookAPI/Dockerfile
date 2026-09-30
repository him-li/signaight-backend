FROM jinaai/jina:3.25-py311-standard

RUN apt-get -y update \
    && apt-get -y install git build-essential python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/man/?? /usr/share/man/??_*

WORKDIR /opt/app

# make sure the files are copied into the image
COPY ./requirements.txt /opt/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /opt/app

ENV PYTHONPATH=/opt/app
ENV PYTHONUNBUFFERED=True

ENTRYPOINT ["jina", "executor", "--uses", "config.yml"]
