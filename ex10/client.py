import socket
import signal
import sys
import datetime
import struct
import psutil
import time

def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')

##

ip_addr = "127.0.0.1"
tcp_port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((ip_addr, tcp_port))
except socket.error as msg:
    print("Unable to connect!")
    # print(msg)


order=0
while True:
    try: 
        message='CPU: {}%, memory use:{}%'.format(psutil.cpu_percent(interval=1), psutil.virtual_memory()[2]).encode()
        version=1
        order+=1
        size=len(message)
        pkt=struct.pack('!BLL{}s'.format(size),version,size,order,message)
        sock.send(pkt)

        # wait 10 sec. freq = 0.1Hz
        time.sleep(10)
    except (socket.timeout, socket.error):
        print('Server error. Done!')
        sys.exit(0)

