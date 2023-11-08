Remove all container by regex name:
> docker rm $(docker ps -a | grep "localstack-ec2" | awk '{print $1}')
> docker rmi $(docker images | grep -E "ubuntu|alpine" | awk '{print $1 ":" $2}')
