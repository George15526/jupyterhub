# Operation Guide

## System Info
- Windows Server 2022
- WSL2 Ubuntu 24.04 LTS
- Docker Engine version 29.0.2, build 8108357

## Requirements before running the project
- Dockerfile.jupyterhub
- jupiterhub_config.py
- docker-compose.yml

## How to run the jupyterhub?
- `docker compose up -d --build`

## DNS? Nginx? How's their routes?
1. First, setting the firewall for the nginx server connection (just access the ports 8000).
2. Cause we run this hub by docker, we need to create a tunnel for the localhost visitation (not only using docker port forwarding).
    ```bash=
    netsh interface portproxy add v4tov4 `
    listenport=8000 listenaddress=0.0.0.0 `
    connectport=8000 connectaddress=172.25.165.226
    ```
3. Then, we can check the connection in our nginx server in sdpmlab.
    If it is okay, we can write the nginx config in `/etc/nginx/sites-available/jupyterhub.sdpmlab.org`
4. Last but not least, we use DNS from cloudflare.

> The last step in cloudflare, cause the frontend page of the jupyterhub is kind of special, I create a specific settings for this hostname. (And it got me crazy :D)

## How to use it?
1. Search `https://jupyterhub.sdpmlab.org` on website
2. Login / Sign up the system
3. Start your travel on Jupyter Notebook