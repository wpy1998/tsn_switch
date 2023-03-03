# -- coding:UTF-8 --
import json
import os

import hardware.computer as hc
from topology import topology_launcher as tl
from netconf import netconf_launcher as nl

if __name__ == "__main__":
    # netconf_launcher = nl.NetconfLauncher()
    # netconf_launcher.startNetconfThread()
    #
    # while True:
    #     next = input()
    #     if next == 'exit' or next == 'quit' or next == 'stop':
    #         netconf_launcher.stopNetconfThread()
    #         break
    fp = os.popen('mtr -r -s 64 192.168.1.11 -j')
    result = fp.read()
    report = json.loads(result).get('report')
    mtr = report.get('mtr')
    hubs = report.get('hubs')
    obj = hubs[0]
    print(json.dumps(obj))