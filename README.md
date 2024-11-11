# Mission Client
A ROS2 package for interacting between an API and an Action Server

## Requirements
- Docker

## Install
This repo contains a Dockerfile for simple installation of this app
- Clone the repo
- Create the docker container
```sh
docker build -t <container-name> .
```
- Verify successful installation

## Deploy
Build your docker container as mentioned in the install section
- The default dds (Fast DDS) implementation in ROS2 utilizes shared memory when both nodes are on the same network. By setting the docker network to host, FastDDS will use shared memory breaking communication between ros nodes in seperate docker containers. To fix this use:
```sh
docker run --network host -v /dev/shm:/dev/shm -it <container-name>
```
- This will mount the shared memory volumes to facilitate communication
- Alternatively if you want to communicate between the host pc and the docker container, adjust the Dockerfile to create a user and ensure the UID of the host pc and the container are the same. To run the container use:
```sh
docker run --network host --ipc=host --pid=host -it <container-name>
```


