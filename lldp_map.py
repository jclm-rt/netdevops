#!./norbox/bin/python

from nornir.plugins.tasks import networking
from nornir.plugins.functions.text import print_result, print_title
from nornir.plugins.tasks.networking import netmiko_send_config, netmiko_send_command
from nornir.plugins.tasks.files import write_file
from nornir import InitNornir
from nornir.core.filter import F
from datetime import date
from pprint import pprint 
import pathlib

def lldp_map(task):
    #r = task.run(task=networking.napalm_get, getters=["lldp_neighbors"])
    #r = task.run(netmiko_send_command, command_string="show lldp neighbors", use_genie=True)
    #r = task.run(netmiko_send_command, command_string="show cdp neighbors detail", use_genie=True)
    r = task.run(netmiko_send_command, command_string="show lldp neighbors", use_textfsm=True)
    task.host["facts"]=r.result
    cant_d_vecinos = len(r.result)
    
    for num in range(0,cant_d_vecinos):
        interface_local = task.host["facts"][num]["local_interface"]
        interfaz_d_vecino = task.host["facts"][num]["neighbor_interface"]
        vecino = task.host["facts"][num]["neighbor"] 
        #plataforma_d_vecino = task.host["facts"][num]["platform"]
        descripcion = task.host["facts"][num]["local_interface"]
        cdp_config = task.run(netmiko_send_config,name="Automatizando las descripciones LLDP de redes",config_commands=[
            "interface " + str(interface_local),
            "description Conetado a " + str(vecino) + " a travez de su interfaz " + str(interfaz_d_vecino)]
        )
            
    

def main():
    nr = InitNornir(config_file="../config.yaml")
    #devices = nr.filter(F(role="switch") & F(site="oruro"))
    devices = nr.filter(asset_tag = "01-SW01-R1P3")
    #result = devices.run(name="Generando CDP MAP", task=lldp_map)
    result = devices.run(name="Recopilando y generando datos de LLDP", task=lldp_map)
    #print_result(result, vars=["stdout"])
    print_title("Desplegando mapa automatizado de LLDP")
    print_result(result)
    #breakpoint()
# Python good practices
if __name__ == '__main__':
    main()
