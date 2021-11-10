import random

import requests
from proxy_checker import ProxyChecker


class FosyProxyTools:
    def __init__(self, fosy_key):
        fosy_url = "https://fosy.club/api/proxy/backconnect/link?key=" + fosy_key
        all_proxies = requests.get(fosy_url)
        self.proxies = all_proxies.text.strip().split("\n")
        self.MAX_TRIES = 20
        self.PROXY_TIMEOUT = 700

    def get_proxy(self, protocol='http'):
        counter = self.MAX_TRIES
        while counter > 0:
            proxy = random.choice(self.proxies)
            result = self.check_proxy(proxy, protocol)
            if result is not None:
                return proxy
            counter -= 1
        raise Exception("Cannot choice proxy")

    def check_proxy(self, address, protocol='http'):
        checker = ProxyChecker()
        result = checker.check_proxy(f'{address}')
        if result is not False:
            if result['timeout'] < self.PROXY_TIMEOUT:
                print(result)
                if protocol in result['protocols']:
                    print(f"Good proxy - {address}")
                    return address
                else:
                    print(f"{address} is a {result['protocols']} IP. Not " + protocol + ". ")
            else:
                print(f"{address}: Timeout!")
        else:
            print(f"{address} isn't valid. ")

