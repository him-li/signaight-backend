#!/bin/sh

if [ -z "${WAIT_HOSTS}" ]; then
    echo "Environment variable WAIT_HOSTS undefined so skipping check services availability"
else
    /wait
fi

# Run migrations before start
MONGODB_DB=$(echo $MONGODB_URI | grep -oP "[mongodb|mongodb+srv]://.*@.*[:.*]?/\K(.+?)$" | cut -d "?" -f 1 )
beanie migrate -uri $MONGODB_URI -p core/migrations -db $MONGODB_DB

exec "$@"
