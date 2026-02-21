from __future__ import annotations
import socket
def is_port_open(host,port):
    s=socket.socket(); s.settimeout(0.2)
    try: return s.connect_ex((host,port))==0
    finally: s.close()
