'''
Defines the base "worker" class that custom classes should inherit from
'''
import datetime

class Worker():
    
    def __init__(
        self,
        **kwargs
    ):
        self.__dict__.update(kwargs)
        self.last_iter_timestamp = datetime.datetime.now()
        self.kill_job = False


    def run(self):
        pass
        
