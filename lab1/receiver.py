import ipaddress
import logging
import socket
import threading
from traceback import format_exc
import struct
import time


class Receiver:
    def __init__(self, group, port, dict):
        self.group = ipaddress.ip_address(group)
        self.port = int(port)
        self.timeout = 7
        self.address_dict = dict

    def run(self):
        host = f'{self.group}'  # Standard loopback interface address (localhost)
        port = self.port  # Port to listen on (non-privileged ports are > 1023)

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
            # s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
            # s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
            # s.bind((host, port))

            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', port))
            mreq = struct.pack('4sl', socket.inet_aton(host), socket.INADDR_ANY)

            s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            # addrinfo = socket.getaddrinfo(host, None)[0]
            # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
            # s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
            # s.bind((host, port))
            # group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
            # mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
            # s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            print('Listening at {}'.format(s.getsockname()))

            while True:
                try:
                    message, conn = s.recvfrom(8)

                except:
                    logging.error(format_exc())

                self.address_dict[conn] = int(round(time.time()))
