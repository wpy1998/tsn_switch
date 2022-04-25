# -- coding:UTF-8 --
import hardware.computer as hc
from network_topology import lldp
import network_topology_launcher

if __name__ == "__main__":
    cuc_ip = 'localhost'
    print('current cuc_ip: ', hc.cuc_ip)
    print('you can change the cuc_ip in hardware.computer')
    lldpImpl = lldp.LLDP()
    launcher = network_topology_launcher.NetworkTopologyLauncher()
    launcher.startTimerThread()
