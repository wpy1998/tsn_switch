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
    if len(inters) > 1:
        for obj in inters:
            network_card_name = ''
            for obj1 in obj:
                network_card_name = obj1
            add_computer_message(obj.get(network_card_name))
    else:
        network_card_name = ''
        for obj in inters:
            network_card_name = obj
        add_computer_message(inters.get(network_card_name))


def add_computer_message(inter):
    via = inter.get('via')
    # if via != 'LLDP':
    #     return
    chassis = inter.get('chassis')
    for name in chassis:
        target = chassis.get(name)
        break
    mac = target.get('id').get('value').replace(':', '-')
    macs.append(mac)
    mgmt_ip = target.get('mgmt-ip')
    # print(mgmt_ip)
    ipv4s.append(mgmt_ip[0])
    ipv6s.append(mgmt_ip[1])

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
print(ipv4s, macs, ipv6s, host_name)
if len(macs) == 0:
    print('--Did not find suitable mac--')
    host_merge = host_name
else:
    host_merge = host_name + macs[0]