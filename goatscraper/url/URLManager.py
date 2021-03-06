'''
Implements the URL Manager class. Default object to handle URL management for scraper threads
'''
from collections import deque
import heapq 
import datetime 
import threading

class URL():
    
    def __init__(
        self,
        url,
        failures_before_iter=5
    ):
        self.url                    = url   # the URL string 
        self.failures_before_iter   = failures_before_iter # number of times in a row to allow a URL to fail before incrementing iteration

        self.num_times_given        = 0     # number of times the URL was given by the URL manager
        self.last_returned          = datetime.datetime.now()   # the timestamp of the time the URL was last given by the URL manager
        self.in_use                 = False # whether or not this URL is supposed to be currently in use
        
        self.successes              = 0     # the number of times the URL was sent and the result was a success
        self.last_success           = None  # the timestamp of the last success

        self.failures               = 0     # the number of times the URL was sent and the result was a failure
        self.last_failure           = None  # the timestamp of the last failure
        self.failures_in_a_row      = 0     # number of times URL failed in a row

        self.timeouts               = 0
        self.last_timeout           = None

        self.iteration              = 0     # the iteration #


    def __lt__(self, other):
        if self.iteration == other.iteration:
            return self.last_returned < other.last_returned
        return self.iteration < other.iteration

    def _iterate(self):
        self.iteration += 1
        self.failures_in_a_row = 0

    def log_failure(self):
        self.in_use = False
        self.failures += 1
        self.failures_in_a_row += 1
        self.last_failure = datetime.datetime.now()
        if self.failures_in_a_row % self.failures_before_iter == 0:
            self._iterate()

    def log_success(self):
        self.in_use = False 
        self.successes += 1
        self.last_success = datetime.datetime.now()
        self._iterate()

    def log_timeout(self):
        self.log_failure()
        self.timeouts += 1
        self.last_timeout = datetime.datetime.now()

    def grab_url(self):
        self.in_use = True
        self.last_returned = datetime.datetime.now()
        return self.url


class URLManager():

    __url_lock = threading.Lock()

    def __init__(
        self,
        urls=[],
        timeout_secs=120,
        max_url_fails=5,
        velocity_calc_interval=600
    ):
        self.timeout_secs           = timeout_secs
        self.max_url_fails          = max_url_fails
        
        self.__url_dict             = {}
        self.__url_priority_queue   = []
        
        self._initialized_time = datetime.datetime.now()
        self._successes              = 0
        self._failures               = 0


    def add_url(
        self,
        url_str
    ):
        with self.__url_lock:
            if url_str not in self.__url_dict:
                new_url = URL(url=url_str, failures_before_iter=self.max_url_fails)
                self.__url_dict[url_str] = new_url
                heapq.heappush(self.__url_priority_queue, new_url)

    def add_urls(
        self,
        url_str_list
    ):
        with self.__url_lock:
            for url_str in url_str_list:
                self.add_url(url_str)

    def check_url_timeouts(self):
        with self.__url_lock:
            for url_str, url_inst in self.__url_dict.items():
                if url_inst.in_use and url_inst.last_returned + datetime.timedelta(seconds=self.timeout_secs) < datetime.datetime.now():
                    self.failures += 1
                    url_inst.log_timeout()
                    heapq.heappush(self.__url_priority_queue, url_inst)

    def grab_url(self):
        with self.__url_lock:
            if len(self.__url_priority_queue) == 0:
                self.check_url_timeouts()
                if len(self.__url_priority_queue) == 0:
                    return None
            return heapq.heappop(self.__url_priority_queue).grab_url()        

    def log_success(self, url_str):
        with self.__url_lock:
            self._successes += 1
            self.__url_dict[url_str].log_success()
            heapq.heappush(self.__url_priority_queue, self.__url_dict[url_str])

    def log_failure(self, url_str):
        with self.__url_lock:
            self.failures += 1
            self.__url_dict[url_str].log_failure()
            heapq.heappush(self.__url_priority_queue, self.__url_dict[url_str])

    def get_velocity(self):
        print(f'Success velocity: {self._successes / ((datetime.datetime.now() - self._initialized_time).total_seconds / 60.0)} successes per minute')
        print(f'Failure velocity: {self._failures / ((datetime.datetime.now() - self._initialized_time).total_seconds / 60.0)} failures per minute')

        
