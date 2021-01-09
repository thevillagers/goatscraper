'''
setup.py
(c) Vinny Meller

distutils setup script for goatscraper
'''

from setuptools import setup, find_packages #setuptools >>
from codecs import open
import os

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, 'goatscraper', 'VERSION'), encoding='utf-8') as f:
    VERSION = f.read().strip()

with open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='goatscraping',
    version=VERSION,
    description='Web Scraping Framework',
    long_description=LONG_DESCRIPTION,
    url='https://www.github.com/thevillagers/goatscraping',
    author='Vinny Meller',
    author_email='vinny@goathousing.com',
    license='License :: OSI Approved :: MIT License',
    keywords='web scrape scraping',
    packages=find_packages(exclude=[]),
    package_data={'goatscraping': ['VERSION'],},
)


