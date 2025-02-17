# SnipBox API
-----------------------
SnipBox is a short note saving app which lets you save short notes and group them together with tags. The task is
to develop the backend APIs using Django Rest Framework.

# How to run the app

1. Install `docker` and `docker-compose` in the system.(https://docs.docker.com/engine/install/)

2. Change directory to the path where `compose.yml` file is placed.

3. Run `docker compose up -d` in terminal to start the API

4. To run tests `docker exec -it snipbox-api-container python manage.py test` .
   
5. Run `docker compose down` in terminal to stop the API

------------------------------------------------------------
# Note:
1. This repository contains sample `env` file and values to check the application. Change them as requirement.
