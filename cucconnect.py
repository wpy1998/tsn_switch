import httpInfo
import networkTopology
import lldp

class CUCConnect:
    def __init__(self, cuc_ip):
        self.urls = {
            'tsn-topology': "http://" + str(cuc_ip) +
                    ":8181/restconf/config/network-topology:network-topology/",
            'school': "ucas"
        }

    def registerSwitch(self, lldpImpl):
        url = self.urls.get("tsn-topology")
        topology = networkTopology.Topology('tsn-network', lldpImpl)
        print(topology.get_json())
        httpInfo.put_info(url, topology.get_json())
