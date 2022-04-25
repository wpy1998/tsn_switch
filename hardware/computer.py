import socket
import uuid

def get_mac():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0, 11, 2)])


cuc_ip = "localhost"
urls = {
    'tsn-topology': "http://" + cuc_ip +
                    ":8181/restconf/config/network-topology:network-topology/",
    'tsn-listener': "http://" + cuc_ip +
                ":8181/restconf/config/tsn-listener-type:stream-listener-config/devices/",
    'tsn-talker': "http://" + cuc_ip +
                ":8181/restconf/config/tsn-talker-type:stream-talker-config/devices/"
}
topology_id = 'tsn-network'
host_ip = socket.gethostbyname(socket.gethostname())
host_name = socket.gethostname()
mac = get_mac()