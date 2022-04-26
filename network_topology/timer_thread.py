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
    host_name = hc.host_merge
    lldpImpl = network_topology.lldp.LLDP()
    topology = None
    _flag = True
    time_tap = 0
    def __int__(self):
        super().__init__()

    def run(self):
        while True:
            if not self._flag:
                break
            if self.time_tap == 0:
                self.registerSwitch()
            self.time_tap = (self.time_tap + 1) % 180
            self.block(5)

    def registerSwitch(self):
        url = self.url_front + 'topology/' + self.topology_id
        self.topology = nt.Topology(self.topology_id, self.lldpImpl)

        nodes = self.topology.get_json().get('node')
        for node in nodes:
            array = []
            target = {}
            array.append(node)
            target['node'] = array
            print('--register node to controller--')
            httpInfo.put_info(url + '/node/' + node['node-id'], json.dumps(target))
        links = self.topology.get_json().get('link')
        for link in links:
            array = []
            target = {}
            array.append(link)
            target['link'] = array
            print('--register link to controller--')
            httpInfo.put_info(url + '/link/' + link['link-id'], json.dumps(target))

    def removeSwitch(self):
        url = self.url_front + 'topology/' + self.topology_id
        if self.topology is None:
            self.topology = nt.Topology(self.topology_id, self.lldpImpl)

        nodes = self.topology.get_json().get('node')
        for node in nodes:
            print('--remove node from controller--')
            httpInfo.delete_info(url + '/node/' + node['node-id'])
        links = self.topology.get_json().get('link')
        for link in links:
            print('--remove link from controller--')
            httpInfo.delete_info(url + '/link/' + link['link-id'])


    def stop(self):
        self._flag = False
        self.removeSwitch()

    def block(self, seconds):
        time.sleep(seconds)
