import lldpImpl
import httpInfo
import networkTopology

if __name__ == "__main__":
    # url = 'http://localhost:8181/restconf/operational/network-topology:network-topology'
    # get_info(url)
    cuc_ip = input('please input cuc_ip： ')
    lldpImpl.get_interface()