import hardware.computer as hc
import network_topology.lldp
from network_topology import timer_thread

class NetworkTopologyLauncher:
    timerThread = None
    def __init__(self):
        self.topology_id = hc.topology_id
        self.url_front = hc.urls.get('tsn-topology')
        self.host_name = hc.host_merge
        self.lldpImpl = network_topology.lldp.LLDP()

    def startTimerThread(self):
        if self.timerThread is None:
            self.timerThread = timer_thread.TimerThread()

        self.timerThread.start()

    def stopTimerThread(self):
        print('--Thread: TimerThread interrupted--')
        if self.timerThread is not None and self.timerThread.is_alive():
            self.timerThread.stop()
