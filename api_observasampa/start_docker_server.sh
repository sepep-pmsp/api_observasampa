#! /bin/bash

#stop container
sudo docker stop $(docker ps -a -q)
#remove container
sudo docker rm $(docker ps -a -q)


#setar variavel de ambiente
if [ -f ".env" ]; then
    echo "loading .env"
   
else
    echo ".env does not exist. copying example!"
    cp .env.example .env
fi

source ./.env
echo "Building environtment:";
echo $ENV;
if [[ $ENV = "homolog" ]]
then
  echo "checking out homolog"
  git fetch origin homolog
  git pull
  git checkout homolog
else
  echo "checking out main"
  git fetch origin main
  git pull
  git checkout main
fi

#build image
sudo docker build -t api_observa .

#cria arquivo de log se não existis
touch -a api_log.txt

#run container with restart
sudo docker run -d --name api_observa --restart unless-stopped -p 80:80 api_observa
