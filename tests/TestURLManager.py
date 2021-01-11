import unittest
from goatscraper.url.URLManager import URLManager


url_mgr = URLManager()

class TestURLManager(unittest.TestCase):
    
    def test_add_urls_grab_url(self):
       url_mgr.add_url('https://www.google.com')
       url_mgr.add_urls(['https://www.google.com', 'https://www.google.com', 'https://www.honda.com', 'https://www.facebook.com'])

       urls_returned = []
       urls_returned.append(url_mgr.grab_url())
       urls_returned.append(url_mgr.grab_url())
       urls_returned.append(url_mgr.grab_url())
       self.assertEqual(urls_returned, ['https://www.google.com', 'https://www.honda.com', 'https://www.facebook.com'], 'Did not return correct URLS in correct order')



if __name__ == '__main__':
    unittest.main()
       
