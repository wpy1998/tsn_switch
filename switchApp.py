# -- coding:UTF-8 --
import hardware.computer as hc
from topology import topology_launcher as tl

if __name__ == "__main__":
    cuc_ip = '192.168.0.119'
    print('*****************************************************************')
    print('current cuc_ip: ', hc.cuc_ip)
    print('you can change the cuc_ip in hardware.computer')
    print('Netconf Server: port, username, password set in hardware.computer')
    print('*****************************************************************')
    launcher = tl.TopologyLauncher()
    launcher.startTimerThread()
    while True:
        next = input()
        if next == 'exit' or next == 'quit' or next == 'stop':
            launcher.stopTimerThread()
            break