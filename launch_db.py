import subprocess
from time import sleep


def launch_postgres():
    subprocess.run(["open", "/Applications/Postgres.app"])
    print("Waiting for postgres to launch...")
    sleep(0.5)
