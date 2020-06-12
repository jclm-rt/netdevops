#!./norbox/bin/python

from nornir.plugins.tasks import networking
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.files import write_file
from nornir import InitNornir
from datetime import date
import pathlib

#BACKUP_PATH = "./data/configs"


def backup_config(task):
    config_dir = "config-archive"
    device_dir = config_dir + "/" + task.host.name
    pathlib.Path(config_dir).mkdir(exist_ok=True)
    pathlib.Path(device_dir).mkdir(exist_ok=True)
    r = task.run(task=networking.napalm_get, getters=["config"])
    task.run(
        task=write_file,
        content=r.result["config"]["running"],
        filename=f"" + str(device_dir) + "/" + str(date.today()) + ".txt",
    )


nr = InitNornir(config_file="../config.yaml")

devices = nr.filter(role="switch")
#device = nr.inventory.hosts

result = devices.run(
    name="Backup Device configurations", task=backup_config
)

print_result(result, vars=["stdout"])
