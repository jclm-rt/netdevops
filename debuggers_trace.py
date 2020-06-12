#!./norbox/bin/python

from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_config



def get_facts(task):
    r = task.run(netmiko_send_command, command_string="show interface switchport", use_textfsm=True)
    task.host["facts"] = r.result

def main() -> None:
    nr = InitNornir(config_file="../config.yaml")
    #devices = nr.filter(F(role="switch-L3") & F(site="cochabamba"))
    devices = nr.filter(asset_tag = "03-SW02-R1P2")
#    result = nr.run(task=get_facts)
    result = devices.run(task=get_facts)
    print_result(result)
#    print_result(devices_sw_cbba.inventory.hosts.keys())
    import ipdb;
    ipdb.set_trace()

if __name__ == '__main__':
    main()
