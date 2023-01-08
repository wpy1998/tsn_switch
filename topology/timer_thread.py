import threading
import time
import httpInfo
import json
import hardware.computer as hc

class TimerThread(threading.Thread):
    _flag = True
    topology_id = ""
    url_front = ""
    host_name = ""
    time_tap = 1
    def __int__(self):
        super().__init__()
        self.topology_id = hc.topology_id
        self.url_front = hc.urls.get('tsn-topology')
        self.host_name = hc.host_name
        self.time_tap = 0

    def run(self):
        self.registerSwitch()
        while True:
            if not self._flag:
                break
            if self.time_tap == 0:
                hc.refresh()
                self.registerSwitch()
            self.time_tap = (self.time_tap + 1) % 180
            self.block(5)

    def registerSwitch(self):
        url = self.url_front + 'topology/' + self.topology_id
        node = hc.get_node_json()
        httpInfo.put_info(url + '/node/' + node['node-id'], json.dumps(node))
        print('<TSN switch> register node to controller <TSN switch>')
        # nodes = self.topology.get_json().get('node')
        # for node in nodes:
        #     array = []
        #     target = {}
        #     array.append(node)
        #     target['node'] = array
        #     print('<TSN switch> register node to controller <TSN switch>')
        #     httpInfo.put_info(url + '/node/' + node['node-id'], json.dumps(target))
        # links = self.topology.get_json().get('link')
        # for link in links:
        #     array = []
        #     target = {}
        #     array.append(link)
        #     target['link'] = array
        #     print('<TSN switch> register link to controller <TSN switch>')
        #     httpInfo.put_info(url + '/link/' + link['link-id'], json.dumps(target))

    def removeSwitch(self):
        url = self.url_front + 'topology/' + self.topology_id
        node = hc.get_node_json()
        httpInfo.delete_info(url + '/node/' + node['node-id'])
        print('<TSN switch> remove node from controller <TSN switch>')
        # nodes = self.topology.get_json().get('node')
        # for node in nodes:
        #     print('<TSN switch> remove node from controller <TSN switch>')
        #     httpInfo.delete_info(url + '/node/' + node['node-id'])
        # links = self.topology.get_json().get('link')
        # for link in links:
        #     print('<TSN switch> remove link from controller <TSN switch>')
        #     httpInfo.delete_info(url + '/link/' + link['link-id'])

    def stop(self):
        self._flag = False
        self.removeSwitch()

    def block(self, seconds):
        time.sleep(seconds)
