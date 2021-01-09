import unittest
from goatscraper.main.Worker import Worker

worker = Worker(kwargs_test=1)

class TestWorker(unittest.TestCase):
    

    def test_kwargs(self):
        self.assertEqual(worker.kwargs_test, 1, 'Should be 1')

    def test_kill_job_default(self):
        self.assertEqual(worker.kill_job, False, 'Should be False')


if __name__ == '__main__':
    unittest.main()

