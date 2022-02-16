import ipaddress
import logging
import socket
import threading
from traceback import format_exc
from time import sleep


class Sender:
    def __init__(self, group, port):
        self.group = ipaddress.ip_address(group)
        self.port = int(port)

        self.message = 'Hi there'
        self.sleep_time = 5

    def run(self):
        host = f'{self.group}'  # The server's hostname or IP address
        port = self.port

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((host, port))
            while True:
                try:
                    s.send(self.message.encode('utf-8'))
                except:
                    logging.error(format_exc())

                try:
                    sleep(self.sleep_time)
                except:
                    logging.error(format_exc())
