import json
import os

class Detector:
    def __init__(self):
        self.first_command = "brctl show"
        self.second_command = "ifconfig -a"
        self.third_command = "ethtool "
        self.forth_command_front = "tcpdump -i "
        self.forth_command_last = " -nev ether proto 0x88cc -c 2"
        self.fifth_command = "mtr -r -s 64 "
        self.bridge_map = {}

    def get_local_interface(self):
        terminals = self.run_command(self.first_command)
        self.build_bridges(terminals)
        terminals = self.run_command(self.second_command)
        result = self.build_ifconfig(terminals)
        result = self.build_network_card(result)
        result = self.build_tcpdump(result)
        result = self.build_mtr(result)
        return result

    def build_bridges(self, terminals):
        current_bridge = ""
        for i in range(len(terminals)):
            if (i == 0):
                continue
            lines = str(terminals[i]).split('\t')
            content = []
            for j in range(len(lines)):
                if (len(lines[j]) == 0):
                    continue
                content.append(lines[j])
            if (len(content) == 4):
                current_bridge = content[0]
                self.bridge_map[content[3]] = current_bridge
            elif(len(content) == 1):
                self.bridge_map[content[0]] = current_bridge
        return

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
        result = {}
        for key in origin.keys():
            obj = origin.get(key)
            third_terminals = self.run_command(self.forth_command_front + key +
                                               self.forth_command_last)
            neighbor = self.extract_tcpdump(third_terminals, obj.get("ether"))
            obj["neighbor"] = neighbor
            print('target = ' + neighbor['mac'] + ', current.mac = ' + obj['ether'])
            if (neighbor['mac'] != "" and neighbor['mac'] != obj.get("ether")):
                result[key] = obj
                continue
        return result

    def build_mtr(self, origin):
        result = {}
        for key in origin.keys():
            object = origin.get(key)
            neighbor = object['neighbor']
            if (neighbor['ip'] is not ""):
                forth_terminals = self.run_command(self.fifth_command + neighbor['ip'] + " -j")
                mid = ""
                for line in forth_terminals:
                    mid = mid + line
                delay = self.extract_mtr(mid)
                object['delay'] = delay
            result[key] = object
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
            flag1 = self.search_key(keyMap, temp_mac)
            flag2 = self.search_key(temp_object, "inet")
            if(flag1 and flag2 == False):
                temp_object["inet"] = keyMap[temp_mac]

        mid_object = {}
        for key in origin.keys():
            if(key != "lo" and origin.get(key).get("scopeid") != None):
                object = origin.get(key)
                second_terminals = self.run_command(self.third_command + key)
                ethtool = self.extract_ethtool(second_terminals)
                if(ethtool.get("Speed") == None):
                    continue
                object["ethtool"] = ethtool

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

    def extract_tcpdump(self, terminals, target_mac):
        packet = []
        for i in range(len(terminals)):
            if(terminals[i][0] >= '0' and terminals[i][0] <= '9'):
                if(len(packet) != 0):
                    origin = self.extract_single_tcpdump(packet)
                    if(origin['mac'] != target_mac and origin['mac'] != ""):
                        return origin
                    packet.clear()
            packet.append(terminals[i])
        origin = self.extract_single_tcpdump(packet)
        return origin

    def extract_single_tcpdump(self, terminals):
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

    def search_key(self, key_map, target):
        for key in key_map.keys():
            if(target == key):
                return True
        return False

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