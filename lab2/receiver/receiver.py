import socket
from threading import Thread
import time
from sender_thread import SenderThread


class Receiver:
    def __init__(self, port):
        self.port = int(port)

    def run(self):
        port = self.port  # Port to listen on (non-privileged ports are > 1023)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", port))
            s.listen(10)
            while True:
                conn, addr = s.accept()
                conn.setblocking(True)
                print(f'connected by {conn}')
                sender_ = SenderThread(s, conn)
                sender_th = Thread(target=sender_.run)
                sender_th.start()
