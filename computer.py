import socket
import uuid

def get_mac():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0, 11, 2)])

host_ip = socket.gethostbyname(socket.gethostname())
host_name = socket.gethostname()
mac = get_mac()