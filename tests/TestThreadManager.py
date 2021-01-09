import unittest
from goatscraper.main.Worker import Worker
from goatscraper.main.ThreadManager import ThreadManager

thread_manager = ThreadManager(Worker, 3, kwargs_test=1)


class TestThreadManager(unittest.TestCase):

    def test_kwargs(self):
        self.assertEqual(thread_manager.kwargs['kwargs_test'], 1, 'Should be 1')




if __name__ == '__main__':
    unittest.main()
        
