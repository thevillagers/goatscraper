'''
Implements a Proxy Manager for Pubproxy's Proxy API
'''
from goatscraper.proxy.ProxyManager import ProxyManager
import requests
from pytimeparse.timeparse import timeparse
import datetime
import json

class PubproxyManager(ProxyManager):

    def __init__(
        self,
        api_url,
        proxy_test_url='https://www.google.com',
        blacklist_cooldown='8hr',
        reuse_cooldown='20m'
    ):
        self.api_url            = api_url
        self.proxy_test_url     = proxy_test_url

        self.blacklist_cooldown = timeparse(blacklist_cooldown)
        self.reuse_cooldown     = timeparse(reuse_cooldown)

        self.grab_proxies_from_api()

    # expect proxy to work with http and https
    def check_proxy(self, proxy):
        proxies = {'http':     f'http://{proxy}'}
        try:
            r = requests.get(self.proxy_test_url, proxies=proxies)
            print(f'checked proxy {proxy} and got status {r.ok}')
            return r.ok
        except Exception as e:
            return False

    # call the API and add proxies to the proxy queue and deque
    def grab_proxies_from_api(self):
        r = requests.get(self.api_url)
        proxy_data = json.loads(r.text)['data']
        for proxy_dict in proxy_data:
            proxy = proxy_dict['ipPort']
            if proxy not in self.proxy_hist_dict:
                print(f'adding proxy {proxy}')
                self.proxy_list.append(proxy)
                self.proxy_hist_dict[proxy] = {
                    'blacklist_time': None,
                    'last_request_time': None,
                    'request_count': 0,
                    'failed_checks': 0
                }

    def grab_proxy(self):
        # loop until returns a working proxy
        while(True):
            while(len(self.proxy_list) == 0):
                time.sleep(2)   # to stop API from rate limiting you
                print('proxy list has 0 in it, grabbing more')
                self.grab_proxies_from_api()

            proxy = self.proxy_list.popleft()
            print(f'grabbed proxy {proxy}')
            if self.proxy_hist_dict[proxy]['blacklist_time'] is not None and self.proxy_hist_dict[proxy]['blacklist_time'] + datetime.timedelta(seconds=self.blacklist_cooldown) > datetime.datetime.now():
                print('proxy is blacklisted')
                continue
            if self.proxy_hist_dict[proxy]['last_request_time'] is not None and self.proxy_hist_dict[proxy]['last_request_time'] + datetime.timedelta(seconds=self.reuse_cooldown) > datetime.datetime.now():
                print('cant reuse proxy so soon')
                continue

            if not self.check_proxy(proxy):
                self.proxy_hist_dict[proxy]['failed_checks'] += 1
                self.blacklist_proxy(proxy)
                continue

            break
        return proxy
