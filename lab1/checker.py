import threading
from traceback import format_exc
import logging
import address_dict as address_dict
from time import sleep


class Checker:
    def __init__(self, address_):
        self.sleep_time = 3
        self.address_dict_class = address_dict.AddressDict()
        self.dict = address_

    def run(self):
        while True:
            try:
                sleep(self.sleep_time)
                print(self.dict)
                self.address_dict_class.check(self.dict)
            except:
                logging.error(format_exc())
