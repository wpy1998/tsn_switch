import time

import lldp
import networktopologylauncher

if __name__ == "__main__":
    cuc_ip = '10.2.25.4'
    print('current cuc_ip： ', cuc_ip)
    print('you can change the cuc_ip in file: switchApp.py')
    lldpImpl = lldp.LLDPImpl()
    launcher = networktopologylauncher.NetworkTopologyLauncher(cuc_ip)
    # cuc_connect.registerSwitch(lldpImpl)
    while 1 == 1:
        # print("next")
        launcher.registerSwitch(lldpImpl)
        time.sleep(15 * 60)
