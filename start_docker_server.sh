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
echo $ENV;
if [[ $ENV = "homolog" ]]
then
  echo "checking out homolog"
  git fetch origin homolog
else
  echo "checking out main"
  git fetch origin homolog
fi

#build image
sudo docker build -t api_observa .

#run container with restart
sudo docker run -d --name api_observa --restart unless-stopped -p 80:80 api_observa
