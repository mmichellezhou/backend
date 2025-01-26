Name: Michelle Zhou
NetID: msz49

Challenges Attempted (Tier I/II/III):
Working Endpoint: GET /api/courses/
Your Docker Hub Repository Link: hub.docker.com/repository/docker/mmichellezhou/demo/general

Questions:
Explain the concept of containerization in your own words.
Containerization is like packing an app and all its necessary files and settings into a portable box, so it works the same way no matter where you run it (Mac, Windows, etc.).

What is the difference between a Docker image and a Docker container?
A Docker image is the blueprint (static), while a Docker container is the running instance (dynamic) based on that blueprint.

What is the command to list all Docker images?
docker images

What is the command to list all Docker containers?
docker ps -a

What is a Docker tag and what is it used for?
A Docker tag is like a version label for an image, used to identify and manage specific versions.

What is Docker Hub and what is it used for?
Docker Hub is an online repository (like GitHub) where developers store and share Docker images.

What is Docker compose used for?
Docker compose is used to define and run multi-container applications with a single YAML file.

What is the difference between the RUN and CMD commands?
RUN is used to execute commands during image creation, while CMD specifies the default command to run when the container starts.