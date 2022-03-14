class Topology:
    def __init__(self, topology_id, lldpImpl):
        self.topology_id = topology_id
        self.current = lldpImpl.current
        self.linklist = lldpImpl.linklist

    def get_json(self):
        topology = {}
        topology['topology-id'] = self.topology_id
        nodes = []
        nodes.append(self.current.get_json())
        topology['node'] = nodes
        links = []
        for link in self.linklist:
            links.append(link.get_json())
        topology['link'] = links
        return topology

class Node:
    termination_points = []
    def __init__(self):
        self.refresh()

    def refresh(self):
        self.termination_points.clear()

    def get_json(self):
        node = {}
        node['node-id'] = self.node_id
        tps = []
        for tp_str in self.termination_points:
            tp = {}
            tp['tp-id'] = tp_str
            tps.append(tp)
        node['termination_point'] = tps
        return node

    def set_termination_points(self, tp):
        self.termination_points.append(tp)

class Link:
    def __init__(self, source_node, source_tp, dest_node, dest_tp):
        self.source_node = source_node
        self.source_tp = source_tp
        self.dest_node = dest_node
        self.dest_tp = dest_tp
        self.link_id = source_node + "(" + source_tp + ")--" + dest_node + "(" + dest_tp + ")"
        try:
            self.link_id.replace('/', '*', self.link_id.length())
        except:
            return

    def get_json(self):
        link = {}
        link['link-id'] = self.link_id
        source = {}
        source['source-tp'] = self.source_tp
        source['source-node'] = self.source_node
        link['source'] = source
        destination = {}
        destination['dest-node'] = self.dest_node
        destination['dest-tp'] = self.dest_tp
        link['destination'] = destination
        return link