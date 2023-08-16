# its time to docker

I build the image using the Dockerfile defined in this repository

## COMMAND FOR CREATE THE IMAGE
`docker build -t chat_immigrant .`
## COMMAND TO START AND INITIALIZE A CONTAINER AND BIND VOLUME TO THE CONTAINER
`docker run -it --mount type=bind,src="$(pwd)",target=/app/data -p 8888:8888 --name chat_immigrant_cont chat_immigrant bash`
## display all container
`docker ps -a`
## start an existing container
`docker start -i [container_id]` 

## EXECUTE
# docker run -p 8501:8501 chat_immigrant --> CON STREAMLIT 

# docker run -it chat_immigrant bash

# ENTRYPOINT ["bash"]

# to run app on app services with docker
[link](https://learn.microsoft.com/en-us/training/modules/deploy-run-container-app-service/1-introduction)


