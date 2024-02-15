#!/usr/bin/bash

USERS=($(echo "select usename from pg_user" | psql))
USER=${USERS[3]}

PGPASS=$(cat ~/.pgpass)
PASS=${PGPASS##*:}

echo -e "[DEFAULT]\nPGUSER=$USER\nPGPASSWORD=$PASS\n" > $1
echo "Parsed credentials into $1"