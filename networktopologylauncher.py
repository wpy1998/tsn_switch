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
        # array = []
        # array.append(topology.get_json())
        # topologies = {}
        # topologies['topology'] = array
        # httpInfo.put_info(url, json.dumps(topologies))

        nodes = topology.get_json().get('node')
        for node in nodes:
            array = []
            target = {}
            array.append(node)
            target['node'] = array
            print('--register node to controller--')
            httpInfo.put_info(url + '/node/' + node['node-id'], json.dumps(target))
        links = topology.get_json().get('link')
        for link in links:
            array = []
            target = {}
            array.append(link)
            target['link'] = array
            print('--register link to controller--')
            httpInfo.put_info(url + '/link/' + link['link-id'], json.dumps(target))
