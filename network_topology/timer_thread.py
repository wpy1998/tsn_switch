import threading
import time
import httpInfo
import network_topology.topology as nt
import json
import hardware.computer as hc
import network_topology.lldp

class TimerThread(threading.Thread):
    topology_id = hc.topology_id
    url_front = hc.urls.get('tsn-topology')
    host_name = hc.host_name + hc.mac
    lldpImpl = network_topology.lldp.LLDP()
    def __int__(self):
        super().__init__()

    def run(self):
        while True:
            self.registerSwitch()
            time.sleep(15 * 60)

    def registerSwitch(self):
        url = self.url_front + 'topology/' + self.topology_id
        topology = nt.Topology(self.topology_id, self.lldpImpl)

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

