# Operation Guide

## System Info
- Ubuntu 24.04.3
- Docker version 29.1.0

## Requirements before running the project
- Dockerfile.jupyterhub
- Dockerfile.singleuser
- jupiterhub_config.py
- docker-compose.yml

## How to run the jupyterhub?
```bash
cd ~/jupyterhub/

// Create the local folder in project directory, and set the read and write permissions for container
sudo mkdir -p notebooks
sudo chown -R 1000:1000 notebooks/

// Build the images and start up the jupyterhub container
sudo docker compose up -d --build
```

## DNS? Nginx? How's their routes?
1. First, setting the firewall for the nginx server connection (just access the ports 8888).

> This is for Windows require steps:
>    Cause we run this hub by docker, we need to create a tunnel for the localhost visitation (not only using docker port forwarding).
>        ```bash=
>        netsh interface portproxy add v4tov4 `
>        listenport=8000 listenaddress=0.0.0.0 `
>        connectport=8000 connectaddress=172.25.165.226
>        ```

2. Then, we can check the connection in our nginx server in sdpmlab.
    If it is okay, we can write the nginx config in `/etc/nginx/sites-available/jupyterhub.sdpmlab.org`
3. Last but not least, we use DNS from cloudflare.

> The last step in cloudflare, cause the frontend page of the jupyterhub is kind of special, I create a specific settings for this hostname. (And it got me crazy :D)

## How to use it?
1. Search https://jupyterhub.sdpmlab.org on website
2. Login / Sign up the system
3. Start your travel on Jupyter Notebook