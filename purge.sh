#!/bin/bash

#purge toutes les images
#docker image prune -a

docker rm -f $(docker ps -aq)
if [ $? != 0 ]; then
	exit 2
fi

#purge  tous les réseaux
#docker network prune -f
# if [ $? != 0 ]; then
# 	exit 2
# fi
# #purge  tous les volumes
#docker volume prune -f
# if [ $? != 0 ]; then
# 	exit 2
# fi

