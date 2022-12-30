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

    def __int__(self, test):
        print(test)

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
                # network_card = object.get(network_card_name)
                # via = network_card.get('via')
                # if via != 'LLDP':
                #     continue
                neighbor = self.get_neighbor(network_card_name)
                if neighbor != None:
                    self.build_target_link(network_card_name, neighbor)
                self.build_node(network_card_name)
        else:
            network_card_name = ''
            for var in array:
                network_card_name = var
            # network_card = array.get(network_card_name)
            # via = network_card.get('via')
            # if via != 'LLDP':
            #     return
            neighbor = self.get_neighbor(network_card_name)
            if neighbor != None:
                self.build_target_link(network_card_name, neighbor)
            self.build_node(network_card_name)

    def get_neighbor(self, network_card_name):
        fp = os.popen('lldpcli show neighbor ports ' + network_card_name + ' -f json')
        result = fp.read()
        interfaces = json.loads(result).get('lldp').get('interface')
        # print(len(interfaces))
        if(interfaces == None):
            return
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
            dest_node = var
        dest_tp = neighbor.get("port").get("descr")
        dest_mac = neighbor.get('port').get('id').get('value')

        if(dest_node == None or dest_tp == None):
            self.build_empty_link(network_card_name, neighbor)
            return

        link = nl.Link(computer.host_merge, network_card_name,dest_node + dest_mac,
                       dest_tp, dest_mac)
        obj = neighbor.get('chassis').get(dest_node).get('mgmt-ip')
        if len(obj) > 1:
            dest_ip = obj[0]
        else:
            dest_ip = obj
        speed = self.get_delay_speed(dest_ip, network_card_name)
        link.set_speed(speed)
        self.linklist.append(link)

    def build_empty_link(self, network_card_name, neighbor):
        # print(json.dumps(neighbor))
        dest_node = neighbor.get("chassis").get("id").get("value")
        dest_mac = neighbor.get('port').get('id').get('value')
        link = nl.Link(computer.host_merge, network_card_name,
                                    dest_node + dest_mac, dest_mac, dest_mac)
        self.linklist.append(link)

    def build_node(self, network_card_name):
        self.current.node_id = computer.host_merge
        self.current.set_termination_points(network_card_name)

    def get_delay_speed(self, destination_ip, network_card_name):
        fp = os.popen('mtr -r -s 64 ' + destination_ip + ' -j')
        result = fp.read()
        if len(result) == 0:
            return None
        report = json.loads(result).get('report')
        mtr = report.get('mtr')
        hubs = report.get('hubs')
        obj = hubs[0]
        speed = {}
        speed['sending-speed'] = self.get_sending_speed(network_card_name=network_card_name)
        speed['loss'] = obj.get('Loss%')
        speed['best-transmission-delay'] = obj.get('Best')
        speed['worst-transmission-delay'] = obj.get('Wrst')
        speed['avg-transmission-delay'] = obj.get('Avg')
        return speed

    def get_sending_speed(self, network_card_name):
        sendingSpeed = 0
        fp = os.popen('ip -4 -j address')
        result = fp.read()
        if len(result) == 0:
            return None
        if result[0] != '[':
            result = '[' + result + ']'
        report = json.loads(result)
        for network_card in report:
            # print(network_card)
            ifname = network_card.get("ifname")
            if ifname == network_card_name:
                sendingSpeed = network_card.get("txqlen")
                break
        return sendingSpeed