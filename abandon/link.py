class Link:
    def __init__(self, source_node, source_tp, dest_node, dest_tp, dest_mac):
        self.source_node = source_node
        self.source_tp = source_tp
        self.dest_node = dest_node
        self.dest_tp = dest_tp
        self.dest_mac = dest_mac
        self.speed = None
        self.link_id = str(source_node) + "(" + str(source_tp) + ")--" + str(dest_node) + "(" + \
                       str(dest_tp) + ")"
        try:
            self.link_id.replace('/', '*', self.link_id.length())
        except:
            return

    def set_speed(self, speed):
        self.speed = speed

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
        if self.speed != None:
            link['speed'] = self.speed
        return link