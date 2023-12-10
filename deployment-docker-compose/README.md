# Deployment of Note Orious in docker-compose

Deployment in docker-compose is similar to Dockerfile. However, docker-compose is more feasible for multi-container setup

## Prerequisites

- Docker
- Docker privileges
- Docker-compose
- Git

Similarly, clone Note Orious repo and set DB connection string

```bash
# Ignore these 3 steps, if you have cloned repo and configured connection string before
$ git clone https://github.com/Deepak-png981/Note-Orious
$ cd Note-Orious

# Create compose file
$ cat <<'EOF' >> docker-compose.yaml
services:
  note-orious:
    network_mode: host
    image: node:21-alpine3.17
    working_dir: /app
    expose:
      - "3000"
    volumes:
      - .:/app
    command:
      - /bin/sh
      - -c
      - |
        echo "MONGO_URI=mongodb://127.0.0.1:27017" > .env
        npm install
        node index.js

    depends_on:
      - note-orious-db

  note-orious-db:
    network_mode: host
    image: mongo:7.0.4
    healthcheck:
      test: curl http://localhost:27017 || exit 1
      interval: 30s
      timeout: 10s
      retries: 5
EOF
```
    
services - first child items are names of the future containers 
network_mode - ensures we are using VM’s network instead of docker’s bridge  
volumes - equivalent of `COPY` in Dockerfile, i.e. copies source code to container  
command -  ensures app’s dependencies are installed, then we can start the Orious  
depends_on - MongoDB is prerequisite to run Orious, hence needs to be deployed first. In other words, ensures MongoDB is started before attempting to deploy Orious container  
healthcheck - required since Orious container is depending on MongoDB  
test - determines whether mongoDB started properly  

Once docker-compose.yaml is constructed, we can start both containers at the same time in proper order

```bash
$ docker-compose up -d 

# Verify containers are running fine
# Additionaly, can be checked via curl/browser
$ docker container ls
$ curl localhost:{3000,27017}
```
