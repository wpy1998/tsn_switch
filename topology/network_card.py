import time

from hardware import computer as hc


class NetworkCard:
    def __init__(self, name, host_name):
        self.name = name
        self.host_name = host_name
        self.ip = "127.0.0.1"
        self.ipv6 = "::1"
        self.mac = ""

        self.name2 = ""
        self.host_name2 = ""
        self.ip2 = ""
        self.ipv6s = ""
        self.mac2 = ""

    def load_linux_object(self, origin):
        self.mac = origin.get("ether").replace(":", "-")
        self.ip = origin.get("inet")
        self.ipv6 = origin.get("inet6")
        self.netmask = origin.get("netmask")
        ethtool = origin.get("ethtool")
        mid_string = ethtool.get("Speed")
        speed = ''
        for i in range(len(mid_string)):
            if(mid_string[i] >= '0' and mid_string[i] <= '9'):
                speed = speed + mid_string[i]
            else:
                break
        self.speed = int(speed)
        self.node_id = self.host_name + self.mac

        if(origin.get("neighbor") != None):
            neighbor = origin.get("neighbor")
            self.ip2 = neighbor.get("ip")
            self.host_name2 = neighbor.get("host-name")
            self.mac2 = neighbor.get("mac")
            self.ipv6s = neighbor.get("ipv6")
            self.name2 = neighbor.get("tp")

        self.link_id = self.host_name + "(" + self.name + ")--" + self.host_name2 + "(" + self.name2 + ")"

    def get_attachment_point_json(self):
        attachment_point = {}
        attachment_point['tp-id'] = self.name
        attachment_point['active'] = True
        attachment_point['corresponding-tp'] = self.name2
        return attachment_point

    def get_termination_point_json(self):
        termination_point = {}
        termination_point['tp-id'] = self.name
        return termination_point

    def get_link_json(self):
        link = {}
        link['link-id'] = self.link_id
        source = {}
        link['source'] = source
        source['source-tp'] = self.name
        source['source-node'] = self.host_name
        dest = {}
        link['destination'] = dest
        dest['dest-tp'] = self.name2
        dest['dest-node'] = self.host_name2
        return link
