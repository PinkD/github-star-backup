import json
from urllib.request import urlopen
import os.path
import subprocess
import sys
import datetime


def run(cmd: str):
    print(f">>> running cmd: {cmd}")
    subprocess.call(["bash", "-c", cmd])


def help():
    print(f"{sys.argv[0]} <username> [<path>]\n\tget")


if __name__ == "__main__":
    if len(sys.argv) == 1 or len(sys.argv) > 3:
        help()
        exit()
    username = sys.argv[1]

    backup_dir = "."
    if len(sys.argv) == 3:
        backup_dir = sys.argv[2]
    star_url = f"https://api.github.com/users/{username}/starred"
    page = 0
    start_time = datetime.datetime.now(datetime.timezone.utc)
    print(f"backup start at {start_time.isoformat()}")
    count = 0
    while True:
        page += 1
        data = urlopen(f"{star_url}?per_page=10&page={page}").read().decode()
        star_list = json.loads(data)
        if len(star_list) == 0:
            break
        for star in star_list:
            name = star["name"]
            full_name = star["full_name"]
            repo_url = star["html_url"]
            if os.path.exists(f"{backup_dir}/{username}/{full_name}"):
                print(f"update {full_name}")
                run(f"pushd {backup_dir}/{username}/{full_name} && git fetch && popd")
            else:
                print(f"clone {full_name}")
                run(f"git clone {repo_url} {backup_dir}/{username}/{full_name}")
            count += 1
    end_time = datetime.datetime.now(datetime.timezone.utc)
    print(f"backup end at {end_time.isoformat()}")
    elapsed = end_time - start_time
    print(f"{str(elapsed)} elapsed, {count} repos backuped")
