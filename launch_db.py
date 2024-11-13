import subprocess


def launch_postgres():
    subprocess.run(["open", "/Applications/Postgres.app"])


if __name__ == "__main__":
    launch_postgres()
