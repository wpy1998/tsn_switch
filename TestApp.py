# -- coding:UTF-8 --
import hardware.computer as hc
from topology import topology_launcher as tl
from netconf import netconf_launcher as nl

if __name__ == "__main__":
    netconf_launcher = nl.NetconfLauncher()
    netconf_launcher.startNetconfThread()

    while True:
        next = input()
        if next == 'exit' or next == 'quit' or next == 'stop':
            netconf_launcher.stopNetconfThread()
            break