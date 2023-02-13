import os

commands = [
    "ifconfig eno2 up",
    "ifconfig swp0 up",
    "ifconfig swp1 up",
    "ifconfig swp2 up",
    "ifconfig swp3 up",
    "brctl addbr br0",
    "brctl addif br0 swp0",
    "brctl addif br0 swp1",
    "brctl addif br0 swp2",
    "brctl addif br0 swp3",
    "ifconfig br0 up",
    "lldptool -L -i eno2 adminStatus=rxtx",
    "lldptool -L -i swp0 adminStatus=rxtx",
    "lldptool -L -i swp1 adminStatus=rxtx",
    "lldptool -L -i swp2 adminStatus=rxtx",
    "lldptool -L -i swp3 adminStatus=rxtx",
    "lldptool -L -i br0 adminStatus=rxtx"
           ]
def run_command(command):
    os.popen(command)

for command in commands:
    run_command(command)