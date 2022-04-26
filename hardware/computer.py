import socket
import json
import os

def refresh():
    macs.clear()
    ipv6s.clear()
    ipv4s.clear()
    fp = os.popen("lldpcli show interface -f json")
    result = fp.read()
    origin = json.loads(result).get("lldp")
    inters = origin.get('interface')
    for network_card_name in inters:
        inter = inters.get(network_card_name)
        via = inter.get('via')
        if via != 'LLDP':
            continue
        chassis = inter.get('chassis')
        for name in chassis:
            target = chassis.get(name)
            break
        mac = target.get('id').get('value').replace(':', '-')
        macs.append(mac)
        ipv4s.append(target.get('mgmt-ip')[0])
        ipv6s.append(target.get('mgmt-ip')[1])


topology_id = 'tsn-network'
host_name = socket.gethostname()
cuc_ip = "localhost"
urls = {
    'tsn-topology': "http://" + cuc_ip +
                    ":8181/restconf/config/network-topology:network-topology/",
    'tsn-listener': "http://" + cuc_ip +
                    ":8181/restconf/config/tsn-listener-type:stream-listener-config/devices/",
    'tsn-talker': "http://" + cuc_ip +
                  ":8181/restconf/config/tsn-talker-type:stream-talker-config/devices/"
}
macs = []
ipv4s = []
ipv6s = []
refresh()