'''
Implements the URL Manager class. Default object to handle URL management for scraper threads
'''
from collections import deque
import pandas as pd

class URL():
    
    def __init__(
        self,
        url
    ):
        self.url                = url
        self.last_returned      = None
        self.in_use             = None
        self.num_times_given    = None
        self.


    def __lt__(self, other):
        if self.


class URLManager():

    def __init__(
        self
    ):
       self._url_df = pd.DataFrame(
                        {
                            'url': pd.Series([], dtype='str'),
                            'last_returned': pd.Series([], dtype='datetime64'),
                            'in_use': pd.Series([], dtype='bool'),
                            'times_given': pd.Series([], dtype='int'),
                            'iteration': pd.Series([], dtype='int'),
                            'times_successful': pd.Series([], dtype='int'),
                            'times_failed': pd.Series([], dtype='int')
                        }
                    )




    def add_url(
        self,
        new_url
    ):
