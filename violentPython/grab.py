
# https://samsclass.info/124/proj14/p3-portscan.htm

import socket
s = socket.socket()

s.connect(("attack.samsclass.info", 22))
print (s.recv(1024))
s.close()
