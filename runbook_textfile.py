#!./norbox/bin/python

from nornir.plugins.tasks import networking
from nornir.plugins.functions.text import print_result, print_title
from nornir.plugins.tasks.networking import netmiko_send_config, netmiko_send_command
from nornir.plugins.tasks.files import write_file
from nornir import InitNornir
from nornir.core.filter import F
import pprint

def baseconfig(task):
#    r = task.run(task=networking.napalm_get, getters=["facts", "interfaces"])
    task.run(task=netmiko_send_config, config_file= "config_textfile")
    task.run(task=netmiko_send_command, command_string = "show lldp neighbors")
    task.run(task=netmiko_send_command, command_string = "write memory")

nr = InitNornir(config_file="../config.yaml")

devices = nr.filter(F(role="switch-L3") & F(site="cochabamba"))

result = devices.run(
   name="Habilitacion de LLDP & SCP server", task=baseconfig
)

#print_result(result, vars=["stdout"])
print_title("DEPLOYING AUTOMATED BASELINE CONFIGURATIONS")
print_result(result)
