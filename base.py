import bs4 as bs
import random
import requests
import pandas as pd
headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

def get_soup(url):
    try:
        resp = requests.get(url, headers=headers)
        soup = bs.BeautifulSoup(resp.content, 'lxml')
        return soup
    except Exception as e:
        print(str(e))
        return []    

def get_content(url):
    try:
        resp = requests.get(url, headers=headers)
        resp = resp.content
        return resp
    except Exception as e:
        print(str(e))
        return []




