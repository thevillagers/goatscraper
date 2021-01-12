import time
import logging
import datetime
import threading

class ThreadManager():


    def __init__(
        self,
        worker_class,
        target_workers,
        worker_iter_timeout=None,
        **kwargs
    ):
        self.worker_class       = worker_class
        self.target_workers     = target_workers
        self.worker_iter_timeout = worker_iter_timeout
        self.kwargs             = kwargs

        self.__worker_list      = []

        self.job_start_time     = None
        self.job_end_time       = None

    # create new thread of the passed worker's main function
    def __instantiate_new_worker_thread(self, worker):
        return threading.Thread(target=worker.run)

    
    # create the instance/thread dict for a new worker
    def __instantiate_new_worker(self):
        worker_instance = self.worker_class(**self.kwargs)
        worker_thread   = self.__instantiate_new_worker_thread(worker_instance)
        worker_dict     = {'instance': worker_instance, 'thread': worker_thread}
        return worker_dict


    # check worker instances for the kill_job flag
    def check_kill_job_flags(self):
        for worker_dict in self.__worker_list:
            if worker_dict['instance'].kill_job == True:
                return True
        return False

    # dereference the workers who are no longer with us
    def dereference_dead_workers(self):
        worker_idx_to_deref = []
        for i, worker_dict in enumerate(self.__worker_list):
            if not worker_dict['thread'].is_alive():
                worker_idx_to_deref.append(i)

            # if the worker has timed out then also deref it
            if self.worker_iter_timeout is not None and worker_dict['instance'].last_iter_timestamp + datetime.timedelta(seconds=self.worker_iter_timeout) < datetime.datetime.now():
                worker_idx_to_deref.append(i)
        
        for i in sorted(worker_idx_to_deref, reverse=True): # delete references to dicts from the worker list
            del self.__worker_list[i]

    # create new workers to ensure there are as many threads running as the specified target threads
    def make_new_workers(self):
        num_workers_to_create = self.target_workers - len(self.__worker_list) 
        for _ in range(num_workers_to_create):
            self.__worker_list.append(self.__instantiate_new_worker())
            self.__worker_list[-1]['thread'].start()    # start the thread after adding to the list of workers
    
    # dereference all workers
    def kill_all_workers(self):
        for i in sorted(range(len(self.__worker_list)), reverse=True):
            del self.__worker_list[i]
        
    # run the scraper
    def run(
        self,
        run_time=None,
        worker_check_cooldown=5,
    ):
        '''
        run_time: number of seconds to run the job
        worker_check_cooldown: number of seconds to wait in between checking for dead workers
        '''
        self.job_start_time = datetime.datetime.now()
        if run_time is not None:
            try:
                self.job_end_time = self.job_start_time + datetime.timedelta(seconds=run_time)
            except Exception as e:
                logging.error(f'Failed to add {run_time} seconds to {self.job_start}. Check that var run_time is an integer')


        while(True):
            # check that the job has not timed out
            if run_time is not None:
                if datetime.datetime.now() > self.job_end_time:
                    self.kill_all_workers()
                    return

            # if worker signals for job to be killed, kill all workers and return
            if self.check_kill_job_flags():
                self.kill_all_workers()
                return

            self.dereference_dead_workers() # deref workers whose threads are no longer alive
            self.make_new_workers() # spin up new instances + threads to replace workers that died
            
            time.sleep(worker_check_cooldown)   # sleep for specified time

                        

        
