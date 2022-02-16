import logging
from threading import Timer
from traceback import format_exc
import time
import os


class SenderThread:
    def __init__(self, sock, conn):
        self.conn = conn
        self.buf_size = 4096
        self.s = sock
        self.bytes_saved = 0
        self.bytes_to_save = 0
        self.size = 0
        self.old_bytes = 0
        self.filename = ''

    def run(self):
        with self.conn:
            try:
                self.filename = b''
                while len(self.filename) < self.buf_size:
                    data = self.conn.recv(1)
                    print(data)
                    if data == b'\n':
                        break
                    self.filename += data
                filepath_list = self.filename.decode('utf-8').split('\\')
                self.filename = filepath_list[-1]
                print(f'Header received {self.filename}')
                path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads', f'{self.filename}')

                self.size = b''
                while len(self.size) < self.buf_size:
                    data = self.conn.recv(1)
                    print(data)
                    if data == b'\n':
                        break
                    self.size += data

                self.size = int(self.size.decode('utf-8')) # !
                print(f'Size received {self.size}')
                print(f'File will be saved as {path}')
                self.bytes_saved = 0
                self.bytes_to_save = self.size

                speed_thread = Timer(1.0, self.count)
                speed_thread.start()

                start_time = time.time()
                with open(path, 'wb') as ff:
                    while True:
                        bytes_received = self.conn.recv(self.buf_size)
                        if len(bytes_received) == 0:
                            break
                        self.bytes_saved += len(bytes_received)
                        ff.write(bytes_received)

                end_time = time.time()
                print(f'File {self.filename} received. Average speed is'
                      f' {self.size / (end_time - start_time) / 8 / 1024 / 1024} MB/s')
            except:
                logging.error(format_exc())
                pass

            finally:
                if speed_thread:
                    speed_thread.cancel()

    def count(self):
        speed = (self.bytes_saved - self.old_bytes) / 8 / 1024 / 1024
        print(f'Current downloading speed of {self.filename} is: {speed} MB/s')
        print(f'Received {self.bytes_saved / self.size * 100} %')
        self.old_bytes = self.bytes_saved
        if self.bytes_saved != self.size:
            Timer(1.0, self.count).start()
