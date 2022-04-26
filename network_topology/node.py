import hardware.computer as hc

class Node:
    termination_points = []
    def __init__(self):
        self.refresh()

    def refresh(self):
        self.node_id = hc.host_name + hc.macs[0]
        self.termination_points.clear()

    def get_json(self):
        node = {}
        node['node-id'] = self.node_id
        node['node-type'] = 'switch'
        tps = []
        for tp_str in self.termination_points:
            tp = {}
            tp['tp-id'] = tp_str
            tps.append(tp)
        node['termination-point'] = tps
        return node

    def set_termination_points(self, tp):
        self.termination_points.append(tp)