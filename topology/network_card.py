import time

from hardware import computer as hc


class NetworkCard:
    def __init__(self, name, host_name):
        self.name = name
        self.host_name = host_name
        self.ip = "127.0.0.1"
        self.ipv6 = "::1"
        self.mac = ""

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

    def get_attachment_point_json(self):
        attachment_point = {}
        return attachment_point

    def get_termination_point_json(self):
        termination_point = {}
        termination_point['tp-id'] = self.name
        return termination_point