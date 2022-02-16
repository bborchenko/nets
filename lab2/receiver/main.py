import ipaddress
import logging
import sys
from traceback import format_exc
from threading import Thread

import receiver


#port = sys.argv[1]

# ip = '127.0.0.1'
port = '1025'

try:

    receive = receiver.Receiver(port)
    receiver_thread = Thread(target=receive.run)
    receiver_thread.start()

except:
    logging.error(format_exc())
