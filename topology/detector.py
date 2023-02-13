import json
import os

class Detector:
    def __init__(self):
        self.first_command = "ifconfig -a"
        self.second_command = "ethtool "
        self.third_command_front = "tcpdump -i "
        self.third_command_last = " -nev ether proto 0x88cc -c 1"
        self.forth_command = "mtr -r -s 64 "

    def get_local_interface(self):
        terminals = self.run_command(self.first_command)
        result = self.build_ifconfig(terminals)
        result = self.build_network_card(result)
        print(json.dumps(result))
        result = self.build_tcpdump(result)
        print(json.dumps(result))
        return result

    def build_ifconfig(self, terminals):
        origin = self.extract_ifconfig(terminals)
        return origin

    def build_network_card(self, origin):
        keyMap = {}
        for key in origin.keys():
            obj = origin.get(key)
            mac = obj.get("ether")
            ip = obj.get("inet")
            if(ip is None or mac is None):
                continue
            flag = True
            for key2 in keyMap:
                if(key2 == mac):
                    flag = False
                    break
            if(flag and ip != ""):
                keyMap[mac] = ip
        result = self.extract_network_card(origin, keyMap)
        return result

    def build_tcpdump(self, origin):
        mid_object = {}
        for key in origin.keys():
            object = origin.get(key)
            for epoch in range(1):
                third_terminals = self.run_command(self.third_command_front + key + self.third_command_last)
                neighbor = self.extract_tcpdump(third_terminals)
                object["neighbor"] = neighbor
                if (neighbor['mac'] != "" and neighbor['mac'] != object.get("ether")):
                    break
            mid_object[key] = object

            # if (neighbor['ip'] is not ""):
            #     forth_terminals = self.run_command(self.forth_command + neighbor['ip'] + " -j")
            #     result = ""
            #     for line in forth_terminals:
            #         result = result + line
            #     delay = self.extract_mtr(result)
            #     object['delay'] = delay
        return mid_object

    def build_mtr(self, origin):
        result = {}
        for key in origin.keys():
            object = origin.get(key)
            neighbor = object['neighbor']
            if (neighbor['ip'] is not ""):
                forth_terminals = self.run_command(self.forth_command + neighbor['ip'] + " -j")
                result = ""
                for line in forth_terminals:
                    result = result + line
                delay = self.extract_mtr(result)
                object['delay'] = delay
        return result

    def extract_ifconfig(self, terminals):
        origin = {}
        for i in range(len(terminals)):
            mid_str = self.clear_brackets(terminals[i])
            temp = mid_str.split(" ")
            elements = []
            for j in range(len(temp)):
                if(len(temp[j]) != 0):
                    elements.append(temp[j])
            if(terminals[i][0] != ' '):
                object = {}
                name = elements[0].replace(":", "")
                origin[name] = object
                mid_list = elements[1].split('=')
                object[mid_list[0]] = mid_list[1]
                j = 2
                while(j < len(elements)):
                    object[elements[j]] = elements[j + 1]
                    j = j + 2
                mid_object = object
            elif(len(elements) % 2 == 0):
                j = 0
                while(j < len(elements)):
                    mid_object[elements[j]] = elements[j + 1]
                    j = j + 2
            else:
                x_object = {}
                if mid_object.get(elements[0] != None):
                    x_object = mid_object.get(elements[0])
                else:
                    mid_object[elements[0]] = x_object
                j = 1
                while(j < len(elements)):
                    x_object[elements[j]] = elements[j + 1]
                    j = j + 2
        return origin

    def extract_network_card(self, origin, keyMap):
        for key in origin.keys():
            temp_object = origin.get(key)
            temp_mac = temp_object.get("ether")
            if(temp_object.get("inet") == None and keyMap[temp_mac] != None):
                temp_object["inet"] = keyMap[temp_mac]

        mid_object = {}
        for key in origin.keys():
            if(key != "lo" and origin.get(key).get("scopeid") != None):
                object = origin.get(key)
                second_terminals = self.run_command(self.second_command + key)
                ethtool = self.extract_ethtool(second_terminals)
                if(ethtool.get("Speed") == None):
                    continue
                object["ethtool"] = ethtool

                # for epoch in range(1):
                #     third_terminals = self.run_command(self.third_command_front + key + self.third_command_last)
                #     neighbor = self.extract_tcpdump(third_terminals)
                #     object["neighbor"] = neighbor
                #     if(neighbor['mac'] != "" and neighbor['mac'] != object.get("ether")):
                #         break
                #
                # if(neighbor['ip'] is not ""):
                #     forth_terminals = self.run_command(self.forth_command + neighbor['ip'] + " -j")
                #     result = ""
                #     for line in forth_terminals:
                #         result = result + line
                #     delay = self.extract_mtr(result)
                #     object['delay'] = delay

                mid_object[key] = object
        origin = mid_object
        return origin

    def extract_ethtool(self, terminals):
        origin = {}
        i = 1
        while(i < len(terminals)):
            mid_str = terminals[i].replace("\t", "")
            mid_str = mid_str.replace(" ", "")
            temp = mid_str.split(":")
            if(len(temp) % 2 == 0):
                j = 0
                while(j < len(temp)):
                    origin[temp[j]] = temp[j + 1]
                    j = j + 2
            i = i + 1
        return origin

    # 17:29:26.786821 86:bb:ca:6f:9d:8e > 01:80:c2:00:00:0e, ethertype LLDP (0x88cc), length 207: LLDP, length 193
    # 	Chassis ID TLV (1), length 7
    # 	  Subtype MAC address (4): 86:bb:ca:6f:9d:8e
    # 	Port ID TLV (2), length 7
    # 	  Subtype MAC address (3): 86:bb:ca:6f:9d:8e
    # 	Time to Live TLV (3), length 2: TTL 120s
    # 	System Name TLV (5), length 9: localhost
    # 	System Description TLV (6), length 82
    # 	  NXP LSDK 2004 main Linux 5.4.3 #5 SMP PREEMPT Sun Aug 14 20:07:02 PDT 2022 aarch64
    # 	System Capabilities TLV (7), length 4
    # 	  System  Capabilities [Bridge, WLAN AP, Router, Station Only] (0x009c)
    # 	  Enabled Capabilities [Bridge, Router] (0x0014)
    # 	Management Address TLV (8), length 12
    # 	  Management Address length 5, AFI IPv4 (1): 192.168.1.131
    # 	  Interface Index Interface Numbering (2): 3
    # 	Management Address TLV (8), length 24
    # 	  Management Address length 17, AFI IPv6 (2): fe80::2058:d2ff:fe0a:3e4a
    # 	  Interface Index Interface Numbering (2): 3
    # 	Port Description TLV (4), length 4: eno0
    # 	Organization specific TLV (127), length 9: OUI IEEE 802.3 Private (0x00120f)
    # 	  Link aggregation Subtype (3)
    # 	    aggregation status [supported], aggregation port ID 0
    # 	Organization specific TLV (127), length 9: OUI IEEE 802.3 Private (0x00120f)
    # 	  MAC/PHY configuration/status Subtype (1)
    # 	    autonegotiation [supported, enabled] (0x03)
    # 	    PMD autoneg capability [10BASE-T hdx, 10BASE-T fdx, 100BASE-TX hdx, 100BASE-TX fdx, 1000BASE-T fdx] (0xec01)
    # 	    MAU type 1000BASET fdx (0x001e)
    # 	End TLV (0), length 0

    #
    def extract_tcpdump(self, terminals):
        origin = {}
        if(len(terminals) is 7):
            mid_list = []
            temp = terminals[0].split(" ")
            for i in range(len(temp)):
                if (len(temp[i]) != 0):
                    mid_list.append(temp[i])
            origin['mac'] = temp[1]
            origin['ip'] = ""
        elif(len(terminals) is 28):
            mid_list = []
            temp = terminals[0].split(" ")
            for i in range(len(temp)):
                if(len(temp[i]) != 0):
                    mid_list.append(temp[i])
            origin['mac'] = temp[1]
            temp = terminals[6].split(": ")
            origin['host-name'] = temp[1]
            temp = terminals[13].split(": ")
            origin['ip'] = temp[1]
            temp = terminals[16].split(": ")
            origin['ipv6'] = temp[1]
            temp = terminals[18].split(": ")
            origin['tp'] = temp[1]
            print(origin['mac'])
        else:
            origin['mac'] = ""
            origin['ip'] = ""
        return origin

    def extract_mtr(self, result):
        report = json.loads(result).get('report')
        mtr = report.get('mtr')
        hubs = report.get('hubs')
        obj = hubs[0]
        speed = {}
        speed['loss'] = obj.get('Loss%')
        speed['best-transmission-delay'] = obj.get('Best')
        speed['worst-transmission-delay'] = obj.get('Wrst')
        speed['avg-transmission-delay'] = obj.get('Avg')
        return speed

    def run_command(self, command):
        fp = os.popen(command)
        line = fp.read()
        line = line.split("\n")
        terminals = []
        for i in range(len(line)):
            if(len(line[i]) == 0):
                continue
            terminals.append(line[i])
            # print(line[i])
        return terminals

    def clear_brackets(self, content):
        result = ''
        flag = 0
        for i in range(len(content)):
            if(content[i] == '(' or content[i] == '<'):
                flag = flag + 1
            elif(content[i] == ')' or content[i] == '>'):
                flag = flag - 1
            elif(flag == 0):
                result = result + content[i]
        return result