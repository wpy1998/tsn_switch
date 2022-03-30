import httpInfo
import networkTopology
import lldp
import json

class NetworkTopologyLauncher:
    def __init__(self, cuc_ip):
        self.urls = {
            'tsn-topology': "http://" + str(cuc_ip) +
                    ":8181/restconf/config/network-topology:network-topology/"
        }

    def registerSwitch(self, lldpImpl):
        url = self.urls.get("tsn-topology") + 'topology/tsn-network'
        topology = networkTopology.Topology('tsn-network', lldpImpl)
        array = []
        array.append(topology.get_json())
        topologies = {}
        topologies['topology'] = array
        httpInfo.put_info(url, json.dumps(topologies))
