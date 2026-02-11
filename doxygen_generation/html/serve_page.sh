#!/bin/bash
DOCKER_NAME=tt
sudo docker stop $DOCKER_NAME
sudo docker rm $DOCKER_NAME
sudo docker run -p 8080:80 -v $(pwd)/html:/usr/local/apache2/htdocs --name $DOCKER_NAME httpd
