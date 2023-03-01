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

        self.loss = 0
        self.best = 0
        self.avg = 0
        self.worst = 0
        self.sending_speed = 0

        self.bridge = ""
        self.mtr = False

    def load_linux_object(self, origin):
        self.mac = origin.get("ether").replace(":", "-")
        self.ip = origin.get("inet")
        self.ipv6 = origin.get("inet6")
        self.netmask = origin.get("netmask")
        self.bridge = origin.get("bridge")
        ethtool = origin.get("ethtool")
        mid_string = ethtool.get("Speed")
        speed = ''
        for i in range(len(mid_string)):
            if(mid_string[i] >= '0' and mid_string[i] <= '9'):
                speed = speed + mid_string[i]
            else:
                break
        self.sending_speed = int(speed)
        self.node_id = self.host_name + self.mac

        if(origin.get("neighbor") != None):
            neighbor = origin.get("neighbor")
            self.ip2 = neighbor.get("ip")
            # self.host_name2 = neighbor.get("host-name")
            # if(self.host_name2 == None):
            #     self.host_name2 = ""
            self.mac2 = neighbor.get("mac")
            self.ipv6s = neighbor.get("ipv6")
            if(self.ipv6s == None):
                self.ipv6s = ""
            self.name2 = neighbor.get("tp")
            if(self.name2 == None):
                self.name2 = ""

        if(origin.get("speed") != None):
            self.speed = origin['speed']
            self.speed['sending-speed'] = self.sending_speed

        self.link_id = self.mac + "(" + self.name + ")--" + \
                       self.mac2 + "(" + self.name2 + ")"

    def get_attachment_point_json(self):
        attachment_point = {}
        attachment_point['tp-id'] = self.name
        attachment_point['active'] = True
        attachment_point['corresponding-tp'] = self.name2
        return attachment_point

    def get_termination_point_json(self):
        termination_point = {}
        termination_point['tp-id'] = self.name
        termination_point['bridge-name'] = self.bridge
        return termination_point

    def get_link_json(self):
        link = {}
        link['link-id'] = self.link_id
        source = {}
        link['source'] = source
        source['source-tp'] = self.name
        source['source-node'] = self.mac.replace("-", ":")
        dest = {}
        link['destination'] = dest
        dest['dest-tp'] = self.name2
        dest['dest-node'] = self.mac2.replace("-", ":")
        if(self.sending_speed != None):
            speed = {}
            link['speed'] = speed
            speed['sending-speed'] = self.sending_speed
            self.mtr = True
        return link
