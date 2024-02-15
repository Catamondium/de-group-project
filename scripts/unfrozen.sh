#!/usr/bin/sh

YELLOW='\033[1;33m'
NC='\033[0m'

pip freeze > /tmp/packages.txt
if [ "$(diff requirements.txt /tmp/packages.txt | grep ">")" ]; then
    STR=$(printf "%sWARNING:%s there are %unfrozen%s packages in VENV" "$YELLOW" "$NC" "$YELLOW" "$NC")
    echo $STR
fi