---
layout:     post
title:      "Quick Guide for Migrating a DigitalOcean Droplet to AWS EC2"
date:       2020-08-09 19:00
keywords:   "cloud migration, cheat sheet, digital ocean to aws, aws to digitalocean, docker, docker-compose, volumes, development"
---

I needed to move a DigitalOcean Droplet to AWS which was running a Docker application using Docker Compose and had its SSL configured using Let's Encrypt. I couldn't find an easy way to convert the DigitalOcean disk snapshots to AWS EBS ones, otherwise, the whole disk could be cloned in AWS with much less effort since Linux configuration is all about the filesystem. I ended up installing needed packages on the target machine and move the configurations. Since I tested everything and it was successful I figured it might be useful to put all the commands and steps in the same place as a quick step-by-step guide. Also, the exact same steps apply to any other cloud as well as the other way around, from AWS to DigitalOcean.

<!--more-->

## Setup the New Machine

Both the Droplet and AWS EC2 instance are running Ubuntu 18.04 but this guide should work for newer versions of Ubuntu.

First of all, it's a good idea to make sure that the swap memory is enabled. There is a nice tutorial from DigitalOcean on [how to enable the swap space on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-ubuntu-16-04).

## Install requirements

First, start by updating the `apt` repository on the new machine:

```bash
sudo apt update
```

### Install Docker

```bash
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# If the user is not root
sudo usermod -aG docker $USER
```

You also need to logout and login again to be able to work with docker without running as root.

### Install Docker Compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Install Nginx and Certbot

```bash
sudo apt install nginx

sudo add-apt-repository universe
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx
```

## Copy the Application

Copy the application folder including docker-compose files by running the following commands on the source machine:

```bash
tar cjvf app.tar.bz2 [APP_DIR]
scp -i [PEM_FILE].pem app.tar.bz2 [DESITNATION_MACHINE_SSH]:~/
```

And on the new machine:

```bash
tar xvf app.tar.bz2
```

## Backup and Restore Docker Volumes

> You can skip this section if you don't have any Docker volumes that needs to be moved or you mount your files to the local disk and that will be copied as part of the source code or similar way

On the source machine, run `docker volume ls` and find the volume names you need to migrate then run the following command to create a backup of the volume:

```bash
docker run --rm \
  --volume [VOLUME_NAME]:/home/volume \
  --volume $(pwd):/home/backup \
  ubuntu \
  tar cvf /home/backup/volume.tar /home/volume
```

The first volume exposes the original volume to this temporary Docker container and the second one allows us to copy the volume back into another path at the host machine. Though instead of copy we create a `tar` file using the last command.

Transfer the file to the new machine using `scp` as before and then:

```bash
docker run --rm \ 
  --volume [VOLUME_NAME]:/home/volume \
  --volume $(pwd):/home/backup \
  ubuntu \
  tar xvf /home/backup/volume.tar -C /home/volume --strip 1
```

This is the same approach just a different command to extract the `tar` file.

## Start the app using Docker Compose

```bash
docker-compose up -d --build
```

## Configuring Let's Encrypt using Certbot

The original server had Let's Encrypt configured [using Certbot and Nginx running on the host machine](https://certbot.eff.org/lets-encrypt/ubuntubionic-nginx).

Since Nginx is installed on the new machine, it should work out of the box by just copying the configs and key files from the original machine.

### Move the files

The easiest way is to use `tar` and `scp` like copying the source code above. First make `tar.bz2` files from `/etc/nginx` and `/etc/letsencrypt` folders on the source machine:

```bash
tar cjvf nginx.tar.bz2 /etc/nginx/
tar cjvf letsencrypt.tar.bz2 /etc/letsencrypt

scp -i [PEM_FILE].pem nginx.tar.bz2 letsencrypt.tar.bz2 [DESITNATION_MACHINE_SSH]:~/
```

Then on the new machine:

```bash
sudo tar xvf nginx.tar.bz2 -C /
sudo tar xvf letsencrypt.tar.bz2 -C /
```

### Update your domain

You need to update your domain to point to this new server IP address before being able to enable automatic renewal.

### Enable automatic renewal

Just to make sure the renewal is working run:

```bash
sudo certbot renew --dry-run
```
