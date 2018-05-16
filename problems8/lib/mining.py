from requests import get, post
import urllib
import urllib.parse
from bs4 import BeautifulSoup
from random import randint
import numpy as np
import os

TOTAL = 57126

def fix_name(name):
    name.replace('<', '')
    name.replace('>', '')
    name.replace('\\', '')
    name.replace('|', '')
    name.replace('/', '')
    name.replace('"', '')
    name.replace('?', '')
    name.replace(':', '')
    name.replace('*', '')
    return name

def get_book_name(soup):
    h = soup.find('h1')
    if h is not None:
        return h.text.split(' by ')

def get_book_content(soup):  
    a = soup.find('a', title='Download', type='text/plain')
    if a is not None:
        return BeautifulSoup(get('https:' + a.get('href')).text, 'lxml')
    
    a = soup.find('a', title='Download', type='text/plain; charset=utf-8')
    if a is not None:
        return BeautifulSoup(get('https:' + a.get('href')).text, 'lxml')

url = 'https://www.gutenberg.org/ebooks/{}'

nums = np.random.choice(TOTAL, 200, replace=False) + 1
for n in nums:
    soup = BeautifulSoup(get(url.format(n)).text, 'lxml')

    name = get_book_name(soup)
    if name is None or len(name) != 2:
        continue 
    name, author = name
    name = fix_name(name)
    author = fix_name(author)
        
    book = get_book_content(soup)
    if book is None:
        continue
    
    if not os.path.exists('books/' + author):
        os.mkdir('books/' + author)
    
    fout = open('books/' + author + '/' + name + '.txt', 'w', encoding='utf-8')
    fout.write(book.text)
    fout.close()
    