how to connect to the database with a docker container
- in your .env file add your informations
- docker pull mysql
- sudo docker run --add-host=host.docker.internal:<gateway> --net=host -e MYSQL_ROOT_PASSWORD=<pass> mysql
- if you have any issues with the connection when using wsl read this article: https://superuser.com/questions/1677878/how-can-i-connect-my-wsl-docker-container-to-a-local-instance-of-mariadb-mysql-o

how to run the api
- cd main
- uvicorn api:app --reload