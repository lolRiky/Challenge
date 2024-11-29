# Voluntary Homework / Challenge

*This was a voluntary homework during an interview process*

This documentation highlights various ways of deployment, API testing and one way of monitoring on a single VM running Fedora Server

Baseline of VM is:

- Disabled SELinux
- Disabled firewalld
- Removed cockpit service

```bash
# yum remove cockpit --exclude=openssl
```

Tasks: 

[Installation of docker and docker-compose](docker)
    
    
[Deployment of Note Orious in Docker](deployment-docker)
    
    
[Deployment of Note Orious in docker-compose](deployment-docker-compose)
    
    
[Deployment Tests](deployment-tests)

Bonus tasks:

[Deployment in K8s (minikube)](deployment-k8s)

[Postman](postman)
    
[Monitoring - Prometheus and Grafana](monitoring)
