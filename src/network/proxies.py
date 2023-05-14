from __future__ import annotations
import requests
import time
import threading


class Proxy:
    def __init__(self, address, port, code, country, anonymity, google, https, checked):
        self.address    = address
        self.port       = int(port)
        self.code       = code
        self.country    = country
        self.anonymity  = False if anonymity == 'no' else True if anonymity == 'yes' else None
        self.Google     = False if google == 'no' else True
        self.https      = False if https == 'no' else True
        self.checked    = checked

    def url(self):
        return f'{self.address}:{self.port}'

    def __repr__(self):
        return f'''
Proxy details:
----------------------
    address : {self.address}
    port    : {self.port}
    origin  : {self.code} {self.country}
    Anon: {self.anonymity} - Google:{self.Google} - https: {self.https}
'''

def getResponse(proxy, f):
    try:
        response = requests.get(
                'http://ipinfo.io/json',
                proxies={
                    'http':     proxy.url(),
                    'https':    proxy.url()
                    }
                )
        if response.status_code != 200: raise Exception(f'Status code f{response.status_code}')
        print(proxy.url())
        f.write(f'{proxy.url()}\n')
    except Exception:
        print(proxy.url(), 'errored')

if __name__ == '__main__':
    proxies = []

    with open('src/network/proxylist.txt') as f:
        for line in f:
            proxy = line.split("\t")
            try:    proxies.append(Proxy(*proxy))
            except: pass

    print(len(proxies), 'proxies')

    with open('src/network/valid.txt', 'w+') as f:
        for proxy in proxies:
            thread = threading.Thread(target=getResponse, args=(proxy, f))
            thread.start()





proxy_list = [
]
