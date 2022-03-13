import os
import json
import computer
import networkTopology

linklist = []
current = networkTopology.Node()

# get_interface->get_neighbor->buildLink
def get_interface():
    fp = os.popen("lldpcli show interface -f json",)
    result = fp.read()
    object = json.loads(result)
    array = object.get('lldp').get('interface')
    try:
        network_card_name = ''
        for var in array:
            network_card_name = var
        network_card = array.get(network_card_name)
        via = network_card.get('via')
        if via != 'LLDP':
            print("there is no LLDP network card")
        neighbor = get_neightbor(network_card_name)
        build_link(network_card_name, neighbor)
    except:
        for object in array:
            network_card_name = ''
            for var in object:
                network_card_name = var
            network_card = object.get(network_card_name)
            via = network_card.get('via')
            if via != 'LLDP':
                continue
            neighbor = get_neightbor(network_card_name)
            build_link(network_card_name, neighbor)

def get_neightbor(network_card_name):
    fp = os.popen('lldpcli show neighbor ports ' + network_card_name + ' summary -f json')
    result = fp.read()
    try:
        object = json.loads(result).get('lldp').get('interface')
    except:
        object = json.loads(result).get('lldp').get('interface').get(0)
    neighbor_key = ''
    for var in object:
        neighbor_key = var
    return object.get(neighbor_key)

def build_link(network_card_name, neighbor):
    n1 = neighbor.get("chassis")
    for var in n1:
        neighbor_name = var
    neighbor_card_name = neighbor.get("port").get("descr")
    link = networkTopology.Link(computer.host_name, network_card_name,
                                neighbor_name, neighbor_card_name)
    linklist.append(link)
    print(link.get_json())



