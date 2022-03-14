import lldp
import computer
import httpInfo
import networkTopology
import cucconnect

if __name__ == "__main__":
    # url = 'http://localhost:8181/restconf/operational/network-topology:network-topology'
    # get_info(url)
    cuc_ip = '10.2.25.85'
    print('current cuc_ip： ', cuc_ip)
    print('you can change the cuc_ip in file: switchApp.py')
    lldpImpl = lldp.LLDPImpl()
    cuc_connect = cucconnect.CUCConnect(cuc_ip)
    cuc_connect.registerSwitch(lldpImpl)