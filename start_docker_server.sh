#stop container
sudo docker stop $(docker ps -a -q)
#remove container
sudo docker rm $(docker ps -a -q)

#pull new commits
sudo git pull

#build image
sudo docker build -t api_observa .

#run container with restart
sudo docker run -d --name api_observa --restart unless-stopped -p 80:80 api_observa