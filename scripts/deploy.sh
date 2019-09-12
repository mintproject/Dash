#!/bin/bash
set -xe
DOCKER_COMPOSE=$1 
if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    exit 1
fi

ssh mintui@vm1.mint.isi.edu "docker-compose -f $DOCKER_COMPOSE up -d"
exit $?	