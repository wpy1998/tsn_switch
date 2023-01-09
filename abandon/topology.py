import topology.lldp

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