import os


def run_command(command):
    os.popen(command)

run_command("ifconfig eno2 up")
run_command("ifconfig swp0 up")
run_command("ifconfig swp1 up")
run_command("ifconfig swp2 up")
run_command("ifconfig swp3 up")
run_command("brctl addbr br0")
run_command("brctl addif br0 swp0")
run_command("brctl addif br0 swp1")
run_command("brctl addif br0 swp2")
run_command("brctl addif br0 swp3")
run_command("ifconfig br0 up")