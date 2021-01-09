'''
Defines the base "worker" class that custom classes should inherit from
'''

class Worker():
    
    def __init__(
        self,
        **kwargs
    ):
        self.__dict__.update(kwargs)
        self.kill_job = False


    def run(self):
        pass
        
