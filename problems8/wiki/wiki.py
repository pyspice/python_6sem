from requests import get, post
import urllib
import urllib.parse
from bs4 import BeautifulSoup
from IPython.core.display import display, HTML
from time import sleep

def is_phylosophy(soup):
    return soup.title.string == 'Философия — Википедия'

def get_title(soup):
    return (lambda x: x[: x.rindex('—') - 1])(soup.title.string)

def incorrect(tag):
    while tag is not None:
        cls = tag.get('class')
        if tag.name in {'sup', 'i', 'em'} or (cls is not None and ('infobox' in cls or 'ambox' in cls)):
            return True
        tag = tag.parent
        
    return False

def extract_link(tag):
    pscore = [0] * len(tag.text)
    for i in range(len(tag.text)):
        pscore[i] = pscore[i - 1]        
        if tag.text[i] == '(':
            pscore[i] += 1
        elif tag.text[i] == ')':
            pscore[i] -= 1
    
    href = None
    last = 0
    for a in tag.find_all('a'):
        cls = a.get('class')
        last = tag.text.index(a.string, last)        
        if (cls is not None and 'new' in cls) or incorrect(a) or a.string is None \
           or (a.string is not None and pscore[last]):
            continue
        
        href = a.get('href')
        
        if href is not None:
            break
        
    return href

def get_first_link(soup):
    div = soup.find('div', id='bodyContent')
    
    ps = div.find_all('p')    
    for p in ps:
        href = extract_link(p)
        if href is not None:
            return href

def transit(soup):    
    href = get_first_link(soup)
    if href is None:
        return None
    
    url = 'https://ru.wikipedia.org' + href
    req = get(url)
    
    return BeautifulSoup(req.text, 'lxml')

def test():
    url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%A1%D0%BB%D1%83%D1%87%D0%B0%D0%B9%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'
    
    req = get(url)

    soup = BeautifulSoup(req.text, 'lxml')
    
    chain = [get_title(soup)]
    while not is_phylosophy(soup):
        #sleep(1)
        soup = transit(soup)
        if soup is None or get_title(soup) in chain:
            return False, chain
        
        chain.append(get_title(soup))
        
    return True, chain

lens = []
with open('test.txt', 'w', encoding='utf-8') as fout:
    for i in range(137, 200):
        a = test()
        print(i, a[1][0])
        if a[0]:
            print(' ->\n\t'.join(a[1]), file=fout)
            lens.append(len(a[1]))
        else:
            print(a[1][0], '- failed to reach phylosophy', file=fout)
        fout.flush()