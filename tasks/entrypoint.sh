#!/bin/sh

if [ -z "${WAIT_HOSTS}" ]; then
    echo "Environment variable WAIT_HOSTS undefined so skipping check services availability"
else
    /wait
fi

exec "$@"
