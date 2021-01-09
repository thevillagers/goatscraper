'''
Implements base class for proxy managers. Inherit this to quickly create classes using different proxy APIs
'''
from pytimeparse.timeparse import timeparse
import datetime
from collections import deque


class ProxyManager():
    

    def __init__(
        self,
        blacklist_cooldown='8hr',
        reuse_cooldown='10m'
    ):
        self._proxy_list        = deque([])
        self._proxy_hist_dict   = {}
        self.blacklist_cooldown = timeparse(blacklist_cooldown)
        self.reuse_cooldown     = timeparse(reuse_cooldown)
        
        self.grab_proxies_from_api()

        

    def grab_proxies_from_api(self):
        pass
    
    def check_proxy(self, proxy):
        pass

    def grab_proxy(self):
        pass


    def blacklist_proxy(self, proxy):
        self._proxy_hist_dict[proxy]['blacklist_time'] = datetime.datetime.now()

    def log_proxy_request(self, proxy):
        self._proxy_hist_dict[proxy]['last_request_time'] = datetime.datetime.now()
        self._proxy_hist_dict[proxy]['request_count'] += 1



