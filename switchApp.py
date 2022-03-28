import time

import lldp
import cucconnect

if __name__ == "__main__":
    cuc_ip = '10.2.25.4'
    print('current cuc_ip： ', cuc_ip)
    print('you can change the cuc_ip in file: switchApp.py')
    lldpImpl = lldp.LLDPImpl()
    cuc_connect = cucconnect.CUCConnect(cuc_ip)
    # cuc_connect.registerSwitch(lldpImpl)
    while 1 == 1:
        # print("next")
        cuc_connect.registerSwitch(lldpImpl)
        time.sleep(15 * 60)
