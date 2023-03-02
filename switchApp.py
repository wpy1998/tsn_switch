# -- coding:UTF-8 --
import hardware.computer as hc
from topology import topology_launcher as tl
from netconf import netconf_launcher as nl

if __name__ == "__main__":
    print('*****************************************************************')
    print('current cuc_ip: ', hc.cuc_ip)
    print('you can change the cuc_ip in hardware.computer')
    print('Netconf Server: port, username, password set in hardware.computer')
    print('*****************************************************************')
    topology_launcher = tl.TopologyLauncher()
    topology_launcher.startTimerThread()
    netconf_launcher = nl.NetconfLauncher()
    netconf_launcher.startNetconfThread()
    while True:
        next = input()
        if next == 'exit' or next == 'quit' or next == 'stop':
            topology_launcher.stopTimerThread()
            netconf_launcher.stopNetconfThread()
            break