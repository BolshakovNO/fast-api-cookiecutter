#!/bin/bash

if [ $# -eq 0 ]; then
    printf "Help:\n"
    printf "$0 [[--init|-i] <upload db>] [[--back|-b] <upload back>] [--config|-c] <upload config>]\n"
    exit 1
fi

init=0
back=0
config=0

while [ $# -gt 0 ]; do
  case "$1" in
    --init|-i)
      export init=1
      ;;
    --back|-b)
      export back=1
      ;;
    --config|-c)
      export config=1
      ;;
    *)
      printf "deploy all \n"
      shift
  esac
  shift
done

if [ $init -eq 1 ]; then
  echo 'save mysql'
  docker save mysql:latest > build/mysql.tar
  gzip < build/mysql.tar > build/mysql.tar.gz
  rm build/mysql.tar
  echo 'save adminer'
  docker save adminer:latest > build/adminer.tar
  gzip < build/adminer.tar > build/adminer.tar.gz
  rm build/adminer.tar
  echo 'save nginx'
  docker save nginx:alpine > build/nginx.tar
  gzip < build/nginx.tar > build/nginx.tar.gz
  rm build/nginx.tar
fi

if [ $back -eq 1 ]; then
  echo 'build and save {{cookiecutter.service_name}} app'
  docker-compose build {{cookiecutter.service_name}}
  docker save {{cookiecutter.service_name}}:latest > build/{{cookiecutter.service_name}}.tar
  gzip < build/{{cookiecutter.service_name}}.tar > build/{{cookiecutter.service_name}}.tar.gz
  rm build/{{cookiecutter.service_name}}.tar
fi

if [ $config -eq 1 ]; then
  echo 'save build images'
  cp docker-compose.deploy.yml build/docker-compose.yml
  cp .env_deploy build/.env
  cp -r nginx build/

  tar -czvf deploy/{{cookiecutter.service_name}}.tar.gz build
fi

echo 'upload on stand'
scp deploy/{{cookiecutter.service_name}}.tar.gz scripts/deploy_on_stand.sh cm@{{cookiecutter.deploy_host}}:/home/cm/{{cookiecutter.service_name}}/
rm -rf build/*
