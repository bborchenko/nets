import ipaddress
import logging
import sys
import os
from traceback import format_exc
from threading import Thread
import sender as sender


# filename = sys.argv[1]
# ip = sys.argv[2]
# port = sys.argv[3]

filename = 'E:\labs\OOP\labs\Python\lab2\sender\Dzhon.Uik.2014.DUAL.BDRip.XviD.AC3.-HRIME.avi'
ip = '192.168.56.1'
port = '1025'

# ip = '127.0.0.1'
# port = '1025'

try:
    group = ipaddress.ip_address(ip)

    if os.path.exists(filename):
        send = sender.Sender(group, port, filename)
        sender_thread = Thread(target=send.run)
        sender_thread.start()

    else:
        logging.error('file does not exist')

except:
    logging.error(format_exc())
