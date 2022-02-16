import ipaddress
import socket
import os


class Sender:
    def __init__(self, group, port, filename):
        self.group = ipaddress.ip_address(group)
        self.port = int(port)
        self.filename = filename.encode('utf-8')
        self.buf_size = 4096
        self.size = os.path.getsize(self.filename)

    def run(self):
        host = f'{self.group}'  # The server's hostname or IP address
        port = self.port

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))

            s.sendto(self.filename, (host, port))
            print(f'Header sent {self.filename}')
            s.sendto(b'\n', (host, port))
            size = f'{self.size}'
            s.sendto(size.encode('utf-8'), (host, port))
            print(f'Size sent {size}')
            s.sendto(b'\n', (host, port))

            with open(self.filename, 'rb') as ff:
                buf = ff.read()
                s.sendall(buf)

            print('File sent')
