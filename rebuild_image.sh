#!/bin/bash -e

#reasign permissions
sudo chown -R ${USER}:${USER} .



# construyo la imagen inicial
rm -Rf .docker/tmp/base/
mkdir -p .docker/tmp/base/.docker;
cp Dockerfile .docker/tmp/base/Dockerfile;
cp requirements.txt .docker/tmp/base/requirements.txt;
#cp deploy.sh .docker/tmp/base/deploy.sh;
#cp -R .docker/id_rsa* .docker/tmp/base/.docker/ ;

cd .docker/tmp/base/ && docker build --tag buho/scraper .;
rm -Rf .docker/tmp
cd ../../../