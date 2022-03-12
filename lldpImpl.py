import os
import json

# get_interface->get_neighbor
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
        via = array.get('via')
        if via != 'LLDP':
            print("there is no possible network card")
        neighbor = get_neightbor(network_card_name)
        print(network_card)
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
            print(network_card)

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
