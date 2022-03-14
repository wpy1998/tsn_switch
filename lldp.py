import os
import json
import computer
import networkTopology

class LLDPImpl:
    linklist = []
    current = networkTopology.Node()

    def __init__(self):
        self.refresh()
        self.get_interface()

    def refresh(self):
        self.linklist.clear()
        self.current.refresh()

    # get_interface->get_neighbor->buildLink->buildNode
    def get_interface(self):
        fp = os.popen("lldpcli show interface -f json",)
        result = fp.read()
        object = json.loads(result)
        array = object.get('lldp').get('interface')
        if len(array) > 1:
            for object in array:
                network_card_name = ''
                for var in object:
                    network_card_name = var
                network_card = object.get(network_card_name)
                via = network_card.get('via')
                if via != 'LLDP':
                    continue
                neighbor = self.get_neighbor(network_card_name)
                self.build_link(network_card_name, neighbor)
                self.build_node(network_card_name)
        else:
            network_card_name = ''
            for var in array:
                network_card_name = var
            network_card = array.get(network_card_name)
            via = network_card.get('via')
            if via != 'LLDP':
                print("there is no LLDP network card")
            neighbor = self.get_neighbor(network_card_name)
            self.build_link(network_card_name, neighbor)
            self.build_node(network_card_name)

    def get_neighbor(self, network_card_name):
        fp = os.popen('lldpcli show neighbor ports ' + network_card_name + ' summary -f json')
        result = fp.read()
        object = json.loads(result).get('lldp').get('interface')
        if len(object) > 1:
            object = object[0]
        neighbor_key = ''
        for var in object:
            neighbor_key = var
        return object.get(neighbor_key)

    def build_link(self, network_card_name, neighbor):
        n1 = neighbor.get("chassis")
        for var in n1:
            neighbor_name = var
        neighbor_card_name = neighbor.get("port").get("descr")
        link = networkTopology.Link(computer.host_name, network_card_name,
                                    neighbor_name, neighbor_card_name)
        self.linklist.append(link)

    def build_node(self, network_card_name):
        self.current.node_id = computer.host_name
        self.current.set_termination_points(network_card_name)