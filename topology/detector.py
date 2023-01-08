import os

class Detector:
    def __init__(self):
        self.first_command = "ifconfig -a"
        self.second_command = "ethtool "
        self.third_command_front = "tcpdump -i "
        self.third_command_last = " -nev ether proto 0x88cc -c 1"

    def get_local_interface(self):
        terminals = self.run_command(self.first_command)
        result = self.extract_network_card(terminals)
        return result

    def extract_network_card(self, terminals):
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

        mid_object = {}
        for key in origin.keys():
            if(key != "lo" and origin.get(key).get("scopeid") != None):
                object = origin.get(key)
                second_terminals = self.run_command(self.second_command + key)
                ethtool = self.extract_ethtool(second_terminals)
                if(ethtool.get("Speed") == None):
                    continue
                object["ethtool"] = ethtool

                third_terminals = self.run_command(self.third_command_front + key + self.third_command_last)
                tcpdump = self.extract_tcpdump(third_terminals)

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

    def extract_tcpdump(self, terminals):
        origin = {}
        for terminal in terminals:
            print(terminal)
        return origin

    def extract_lldp(self):
        origin = {}
        return origin

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