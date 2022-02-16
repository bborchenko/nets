import ipaddress
import logging
import sys
from traceback import format_exc
from threading import Thread

import receiver as receiver
import sender as sender
import checker as checker

# ip = sys.argv[1]
# port = sys.argv[2]

ip = '127.0.0.1'
port = '1025'

address_dictionary = {}

try:
    group = ipaddress.ip_address(ip)

    send = sender.Sender(group, port)
    sender_thread = Thread(target=send.run)
    sender_thread.start()

    receive = receiver.Receiver(group, port, address_dictionary)
    receiver_thread = Thread(target=receive.run)
    receiver_thread.start()

    checker = checker.Checker(address_dictionary)
    checker_thread = Thread(target=checker.run)
    checker_thread.start()

except:
    logging.error(format_exc())
