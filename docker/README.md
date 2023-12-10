# Installation of docker and docker-compose

Section describes installation of Docker Engine and Docker Compose

## Prerequisites:

- Root privileges

Make sure `dnf-plugins-core` is installed and docker repo is added

```bash
# dnf -y install dnf-plugins-core
# dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
```

Lastly, install, start docker unit and verify functionality

```bash
# dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-compose
# systemctl start docker && systemctl enable docker

# Verify by running docker
$ docker -v
```


To note, users on host can be added to a docker group, allows use `docker` command without root privileges. Reboot host after installation to enable this feature
