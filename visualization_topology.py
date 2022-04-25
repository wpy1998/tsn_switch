from mininet.topo import Topo
class MyTopo(Topo):
    def __init__(self):
        "Create custom topo."
        Topo.__init__(self)
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')

        sw1 = self.addSwitch('sw1')
        sw2 = self.addSwitch('sw2')
        sw3 = self.addSwitch('sw3')

        self.addLink(sw1, sw2)
        self.addLink(sw1, sw3)
        self.addLink(sw2, sw3)
        self.addLink(h1, sw1)
        self.addLink(h2, sw1)
        self.addLink(h3, sw2)
        self.addLink(h4, sw2)
        self.addLink(h5, sw3)
        self.addLink(h6, sw3)

topos = {'flow1': (lambda: MyTopo())}