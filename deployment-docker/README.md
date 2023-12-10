# Deployment of Note Orious

## Prerequisites

- Docker
- Git

Orious depends on MongoDB database, hence needs to be pulled and functional first

Pull MongoDB image first from registry and perform health check

```bash
# If git isn't installed
# yum install -y git

$ docker run --network host --name note-todo-mongo -d mongo:7.0.4

# Test connection with curl
# Expected Output: 
# It looks like you are trying to access MongoDB over HTTP on the native driver port.
$ curl localhost:27017

$ Verify MongoDB is well and healthy
$ docker container ls
```

Clone Note Orious. set MongoDB connection string and create a docker image. Again, make sure to use VM’s network, else npm won’t be able to install app’s dependencies

```bash
$ git clone https://github.com/Deepak-png981/Note-Orious
$ cd Note-Orious
$ cat <<'EOF' >> Dockerfile
FROM node:21-alpine3.17
WORKDIR /app
EXPOSE 3000

COPY package*.json ./
RUN echo "MONGO_URI=mongodb://127.0.0.1:27017" > .env
RUN mkdir node_modules
RUN npm install

COPY . .
CMD ["node", "index.js"]
EOF

$ docker build --network host -t note-orious .
```

Create container from the recently built image and verify container is running and has NOT exited

