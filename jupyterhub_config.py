import os

c = get_config()  # type: ignore[name-defined]

# --- Spawner: 每個 user 一個 Docker 容器 ---
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

# single-user 容器使用的 image
c.DockerSpawner.image = os.environ.get(
    "DOCKER_NOTEBOOK_IMAGE",
    "jupyter-gpu-notebook",
)

# 啟動指令（避免再去讀 image Config.Cmd）
c.DockerSpawner.cmd = ["start-singleuser.sh"]

# Notebook 目錄（容器內）
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan")
c.DockerSpawner.notebook_dir = notebook_dir

# 1. 把使用者資料掛到實體主機
#    host:  /home/nknul40s/jupyterhub/notebooks/<username>
#    container: /home/jovyan (notebook_dir)
c.DockerSpawner.volumes = {
    "/home/nknul40s/jupyterhub/notebooks/{username}": notebook_dir,
}

# 2. 讓 single-user 容器加到 jupyterhub-network
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = os.environ.get(
    "DOCKER_NETWORK_NAME", "jupyterhub-network"
)

# 3. 啟用 GPU (--gpus all 等價設定)
c.DockerSpawner.extra_host_config = {
    "network_mode": os.environ.get("DOCKER_NETWORK_NAME", "jupyterhub-network"),
    "device_requests": [
        {
            "Driver": "nvidia",
            "Count": -1,            # -1 = all GPUs
            "Capabilities": [["gpu"]],
        }
    ],
}

# 使用者停止 server 時，順便把舊 container 清掉
c.DockerSpawner.remove = True
c.DockerSpawner.debug = True

# Hub 在 Docker network 裡對其他容器的位址/port
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8080
c.JupyterHub.bind_url = "http://:8888"
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
