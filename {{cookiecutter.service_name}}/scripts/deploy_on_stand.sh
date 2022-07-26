docker-compose -f build/docker-compose.yml down

tar xvf {{cookiecutter.service_name}}.tar.gz

#docker load < build/mysql.tar.gz
#docker load < build/adminer.tar.gz
#docker load < build/nginx.tar.gz
docker load < build/{{cookiecutter.service_name}}.tar.gz

docker-compose -f build/docker-compose.yml up -d

sleep 10

docker-compose -f build/docker-compose.yml run --rm {{cookiecutter.service_name}} sh -c "/app/scripts/migrate_db.sh"
