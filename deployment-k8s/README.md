# Deployment of Note Orious in K8s
    
Kubernetes allows us to orchestrate containers, software updates/rollbacks, scaling and load balance. Will be deployed on minikube, local cluster on a single node for development and testing purposes

Minikube is for dev and testing environment, virtualizes a VM inside of a host and creates a new subnet for the VM

Networking sequence in k8s cluster: nodePort → port → targetPort 

## Prerequisites

- Root privileges
- Git

## Installation and configuration of minikube & kubectl

Download and copy minikube binary

```bash
$ curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
$ sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

Install and verify installation of minikube

```bash
$ minikube start
$ minikube status
```

Install and configure kubectl to interact with k8s

```bash
# Download binary with checksum
$ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"

# Verify binary
$ echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check

# Copy binary to path
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verify
$ kubectl version --client

# Get autocompletion, each user has to do
$ echo 'source <(kubectl completion bash)' >>~/.bashrc && source ~/.bashrc
```

## Deploying MongoDB

Since Orious depends on database, therefore, it needs to be deployed first.

Create following k8s-depl-mongodb.yml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: depl-mongo-orious
  labels:
    app: mongo-orious
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mongo-orious
  template:
    metadata:
      labels:
        app: mongo-orious
    spec:
      containers:
        - name: mongo-orious
          image: mongo
          ports:
            - containerPort: 27017
---
apiVersion: v1
kind: Service
metadata:
  name: srv-mongo
spec:
  selector:
    app: mongo-orious
  ports:
    - protocol: TCP
      port: 27017
      targetPort: 27017
```

Yaml defines two k8s objects:

- Deployment:
    - replicas - number of desired instances
- Service:
    - type - by default ClusterIP
    - port - pod/MongoDB is listening on
    - targetPort - port to forward traffic to service

Run to create deployment and service 

```bash
$ kubectl create -f k8s-depl-mongodb.yaml

# Verify service and pod is healthy
$ kubectl get all
```

Once MongoDB is deployed, Orious can be deployed

Note we are using ClusterIP’s service name in DB connection string

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-orious
  labels:
    app: app-orious
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app-orious
  template:
    metadata:
      labels:
        app: app-orious
    spec:
      containers:
        - name: app-orious
          image: node:21-alpine3.17
          workingDir: /app
          ports:
            - containerPort: 3000
          command: ["/bin/sh", "-c"]
          args: ["echo \"MONGO_URI=mongodb://srv-mongo:27017\" > .env; apk update ; apk add git ; git clone https://github.com/Deepak-png981/Note-Orious ; mv Note-Orious/* . ; rm -rf Note-Orious ; npm install && node index.js"]

---
apiVersion: v1
kind: Service
metadata:
  name: srv-orious
spec:
  selector:
    app: app-orious
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 3000
      targetPort: 3000
      nodePort: 30002
```

- Deployment:
    - replicas - number of desired instances
    - command & args - get a shell, configure DB connection string, pull repo, install all dependencies and start client
- Service:
    - type - exposes Orious to the network
    - nodePort - port to be exposed to network
    - port - service port
    - targetPort - pod’s port

Create and verify Orious has connected to MongoDB

```bash
$ kubectl create -f k8s-depl-orious.yaml
# Expected output; ignore npm messages:
# Server is running fine on port : 3000
# MongoDB Connected....

$ kubectl logs app-orious<rest_of_string>

# Verify we receive html
$ curl $(minikube service srv-orious --url)
```

As mentioned before, minikube creates a VM along with new subnet. Load Balancer only exposes Orious to the world outside of a nested subnet. In other words, not reachable on LAN/WAN

Two options to make Orious available on LAN/WAN

1. kubectl proxy
2. Reverse Proxy in front of k8s

---

1. Kubectl Proxy 

Simple and fastest, however, can not bind to :80 and :443

Service will be available on node’s IP :3000

```bash
$ kubectl port-forward --address 0.0.0.0 service/srv-orious 3000:3000
```

1. Reverse Proxy 

Requires additional software and configuration, but can bind to any port.

Nginx can be used, following procedure will describe steps for Apache

Install and configure Apache

```bash
# yum install -y httpd
# systemctl enable httpd
cat <<'EOF' >> /etc/httpd/conf.d/k8s-proxy.conf
<VirtualHost *:80>
  ProxyPass "/" "http://192.168.49.2:30002/"
  ProxyPassReverse "/" "http://192.168.49.2:30002/"

  ErrorLog /var/log/httpd/revproxy-error.log
  CustomLog /var/log/httpd/revproxy-access.log combined
  LogLevel error
</VirtualHost>
EOF

# systemctl start httpd
```

From this point Orious will be accessible in LAN/WAN
