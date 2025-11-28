import os

c = get_config()  # type: ignore[name-defined]

# --- Spawner: 每個 user 一個 Docker 容器 ---
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

# 使用者 Notebook 所用的 image（從環境變數讀，給 docker-compose 設定）
c.DockerSpawner.image = os.environ.get(
    "DOCKER_NOTEBOOK_IMAGE",
    "quay.io/jupyter/base-notebook:latest",
)

# Hub 跟 user 容器共用的 Docker network
network_name = os.environ.get("DOCKER_NETWORK_NAME", "jupyterhub-network")
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Notebook 在容器裡的路徑
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jupyterhub/work")
c.DockerSpawner.notebook_dir = notebook_dir

# 每個 user 的 Notebook 實體檔案，寫到 D:\jupyterhub\notebooks\{username}
# 注意：這是「Docker host（WSL）」的路徑，所以用 /mnt/d/...
c.DockerSpawner.volumes = {
    "/mnt/d/jupyterhub/notebooks/{username}": notebook_dir,
}

# 使用者停止 server 時，順便把舊 container 清掉
c.DockerSpawner.remove = True
c.DockerSpawner.debug = True

# Hub 在 Docker network 裡對其他容器的位址/port
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8080
c.JupyterHub.bind_url = "http://:8000"
c.JupyterHub.trusted_downstream_ips = ["0.0.0.0/0"]

# Hub 自己的 DB / cookie secrets 存在 /data（會對應到 Docker volume）
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"

# --- Authentication: NativeAuthenticator，讓使用者自行註冊帳號 ---
c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator"

# 所有註冊過的帳號都允許登入
c.Authenticator.allow_all = True

# 開啟自助註冊
c.NativeAuthenticator.open_signup = True
c.NativeAuthenticator.minimum_password_length = 8

# 從環境變數讀 admin 帳號（在 docker-compose 裡設）
admin = os.environ.get("JUPYTERHUB_ADMIN")
if admin:
    c.Authenticator.admin_users = {admin}
