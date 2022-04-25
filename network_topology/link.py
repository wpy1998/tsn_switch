class Link:
    def __init__(self, source_node, source_tp, dest_node, dest_tp):
        self.source_node = source_node
        self.source_tp = source_tp
        self.dest_node = dest_node
        self.dest_tp = dest_tp
        self.link_id = str(source_node) + "(" + str(source_tp) + ")--" + str(dest_node) + "(" + \
                       str(dest_tp) + ")"
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