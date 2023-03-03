import os
import threading

class NetconfThread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        self.run_command("netopeer2-server -d -v3")

    def run_command(self, command):
        os.popen(command)