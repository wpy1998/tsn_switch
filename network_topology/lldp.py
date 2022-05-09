import os
import json
from hardware import computer
import network_topology.node as nn
import network_topology.link as nl

class LLDP:
    linklist = []
    current = nn.Node()

    def __init__(self):
        self.refresh()
        self.get_interface()

    def refresh(self):
        self.linklist.clear()
        self.current.refresh()

    # get_interface->get_neighbor->buildLink->buildNode
    def get_interface(self):
        fp = os.popen("lldpcli show interface -f json")
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
                if neighbor != None:
                    self.build_target_link(network_card_name, neighbor)
                self.build_node(network_card_name)
        else:
            network_card_name = ''
            for var in array:
                network_card_name = var
            network_card = array.get(network_card_name)
            via = network_card.get('via')
            if via != 'LLDP':
                return
            neighbor = self.get_neighbor(network_card_name)
            if neighbor != None:
                self.build_target_link(network_card_name, neighbor)
            self.build_node(network_card_name)

    def get_neighbor(self, network_card_name):
        fp = os.popen('lldpcli show neighbor ports ' + network_card_name + ' -f json')
        result = fp.read()
        interfaces = json.loads(result).get('lldp').get('interface')
        # print(len(interfaces))
        if(len(interfaces) > 1):
            for i in range(len(interfaces)):
                object = interfaces[i]
                ttl = int(object.get(network_card_name).get("port").get("ttl"))
                # print(ttl)
                chassis = object.get(network_card_name).get('chassis')
                for var in chassis:
                    neighbor_name = var
                    break
                if chassis.get('id') == None and chassis.get(neighbor_name).get('id') != None:
                    break
        else:
            object = interfaces
            ttl = int(object.get(network_card_name).get("port").get("ttl"))
            # print(ttl)
            if ttl > 10000:
                object = None
        if object == None:
            print("NetworkCard: ", network_card_name, " has no neighbor through LLDP")
            return None
        for var in object:
            neighbor_key = var
        return object.get(neighbor_key)

    def build_target_link(self, network_card_name, neighbor):
        chassis = neighbor.get("chassis")
        for var in chassis:
            neighbor_name = var
        neighbor_card_name = neighbor.get("port").get("descr")
        if(neighbor_name == None or neighbor_card_name == None):
            self.build_empty_link(network_card_name, neighbor)
            return
        link = nl.Link(computer.host_merge, network_card_name,
                                    neighbor_name, neighbor_card_name)
        obj = neighbor.get('chassis').get(neighbor_name).get('mgmt-ip')
        if len(obj) > 1:
            dest_ip = obj[0]
        else:
            dest_ip = obj
        speed = self.get_speed(dest_ip)
        link.set_speed(speed)
        self.linklist.append(link)

    def build_empty_link(self, network_card_name, neighbor):
        # print(json.dumps(neighbor))
        mac = neighbor.get("chassis").get("id").get("value")
        link = nl.Link(computer.host_merge, network_card_name,
                                    mac, mac)
        self.linklist.append(link)

    def build_node(self, network_card_name):
        self.current.node_id = computer.host_merge
        self.current.set_termination_points(network_card_name)

    def get_speed(self, destination_ip):
        fp = os.popen('mtr -r ' + destination_ip + ' -j')
        result = fp.read()
        if len(result) == 0:
            return None
        report = json.loads(result).get('report')
        mtr = report.get('mtr')
        hubs = report.get('hubs')
        obj = hubs[0]
        speed = {}
        speed['packet-size'] = mtr.get('psize')
        speed['loss'] = obj.get('Loss%')
        speed['best'] = obj.get('Best')
        speed['worst'] = obj.get('Wrst')
        speed['avg'] = obj.get('Avg')
        return speed