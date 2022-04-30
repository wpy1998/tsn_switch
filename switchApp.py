# -- coding:UTF-8 --
import hardware.computer as hc
from network_topology import lldp
import network_topology_launcher

if __name__ == "__main__":
    cuc_ip = 'localhost'
    print('*****************************************************************')
    print('current cuc_ip: ', hc.cuc_ip)
    print('you can change the cuc_ip in hardware.computer')
    print('Netconf Server: port, username, password set in hardware.computer')
    print('*****************************************************************')
    lldpImpl = lldp.LLDP()
    launcher = network_topology_launcher.NetworkTopologyLauncher()
    launcher.startTimerThread()
    while True:
        next = input()
        if next == 'exit' or next == 'quit' or next == 'stop':
            launcher.stopTimerThread()
            break