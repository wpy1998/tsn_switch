from netconf import netconf_thread

class NetconfLauncher:
    netconfThread = None

    def __init__(self):
        None

    def startNetconfThread(self):
        if self.netconfThread is None:
            self.netconfThread = netconf_thread.NetconfThread()
        self.netconfThread.run()

    def stopNetconfThread(self):
        print('<TSN switch NetconfThread> NetconfThread interrupted.')
        if self.netconfThread is not None and self.netconfThread.is_alive():
            self.netconfThread.stop()