import time
import logging

class AddressDict:
    def __init__(self):
        self.timeout = 7

    def check(self, address_dict):
        if address_dict:
            for k in address_dict.copy():
                if int(round(time.time())) - address_dict[k] > self.timeout:
                    address_dict.pop(k)
                    print(f'someone disconnected {address_dict}')

