import json

class Topology:
    topology_id = ''
    def Topology(self, topology_id):
        self.topology_id = topology_id

    def get_json(self):
        return

class Node:
    node_id = ''
    termination_points = []
    def Node(self):
        self.refresh()

    def refresh(self):
        self.termination_points.clear()

    def get_json(self):
        return

class Link:
    link_id = ''
    source_node = ''
    source_tp = ''
    dest_node = ''
    dest_tp = ''
    def Link(self, source_node, source_tp, dest_node, dest_tp):
        self.source_node = source_node
        self.source_tp = source_tp
        self.dest_node = dest_node
        self.dest_tp = dest_tp
        self.link_id = source_node + "(" + source_tp + ")--" + dest_node + "(" + dest_tp + ")"
        self.link_id.replace('/', '*', self.link_id.length())

    def get_json(self):
        link = json.dumps({})
        print(link)