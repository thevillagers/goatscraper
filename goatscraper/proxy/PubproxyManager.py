'''
Implements a Proxy Manager for Pubproxy's Proxy API
'''
from goatscraper.proxy.ProxyManager import ProxyManager
import requests
from pytimeparse.timeparse import timeparse
import datetime
import json
import time

class PubproxyManager(ProxyManager):

    def __init__(
        self,
        api_url,
        proxy_test_url='https://www.google.com',
        blacklist_cooldown='8hr',
        reuse_cooldown='10m'
    ):
        self.api_url            = api_url
        self.proxy_test_url     = proxy_test_url
        super().__init__(blacklist_cooldown, reuse_cooldown)

    # expect proxy to work with http and https
    def check_proxy(self, proxy):
        proxies = {'http':     f'http://{proxy}'}
        try:
            r = requests.get(self.proxy_test_url, proxies=proxies)
            return r.ok
        except Exception as e:
            return False

    # call the API and add proxies to the proxy queue and deque
    def grab_proxies_from_api(self):
        r = requests.get(self.api_url)
        proxy_data = json.loads(r.text)['data']
        for proxy_dict in proxy_data:
            proxy = proxy_dict['ipPort']
            if proxy not in self._proxy_hist_dict:
                self._proxy_list.append(proxy)
                self._proxy_hist_dict[proxy] = {
                    'blacklist_time': None,
                    'last_request_time': None,
                    'request_count': 0,
                    'failed_checks': 0
                }

    def grab_proxy(self):
        # loop until returns a working proxy
        while(True):
            while(len(self._proxy_list) == 0):
                time.sleep(2)   # to stop API from rate limiting you
                self.grab_proxies_from_api()

            proxy = self._proxy_list.popleft()
            if self._proxy_hist_dict[proxy]['blacklist_time'] is not None and self._proxy_hist_dict[proxy]['blacklist_time'] + datetime.timedelta(seconds=self.blacklist_cooldown) > datetime.datetime.now():
                continue
            if self._proxy_hist_dict[proxy]['last_request_time'] is not None and self._proxy_hist_dict[proxy]['last_request_time'] + datetime.timedelta(seconds=self.reuse_cooldown) > datetime.datetime.now():
                continue

            if not self.check_proxy(proxy):
                self._proxy_hist_dict[proxy]['failed_checks'] += 1
                self._blacklist_proxy(proxy)
                continue

            break
        return proxy
