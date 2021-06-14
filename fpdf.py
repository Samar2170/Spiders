import requests
from bs4 import BeautifulSoup as bs
import re
import time
import pandas as pd 
from ratelimit import limits


TEN_SECONDS = 10

headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }
@limits(calls=5, period=TEN_SECONDS)    
def get_soup(url):
    res = requests.get(url, headers=headers)
    soup = bs(res.content, 'lxml')
    return soup

co_dict = [{'co':'ITC','url':'https://www.itcportal.com'}, {'co':'RIL', 'url':'https://www.ril.com'}, {'co':'TCS', 'url':'https://www.tcs.com'},
           {'co':'ADANIENT','url':'https://www.adanienterprises.com'}, {'co':'BAL', 'url':'https://www.bajajauto.com'}]



def get_downloads2(**co_dict):
    link=co_dict['url']
    soup = get_soup(link)

    iv = soup.find_all('a', string=re.compile('Financial'))
    if len(iv)==0:
        iv = soup.find_all('li', string=re.compile('Financial'))
        if len(iv) == 0:
            iv = soup.find_all('div', string=re.compile('Financial'))
            if len(iv)==0:
                iv = soup.find_all('a', string=re.compile('Investor'))
    iv = iv[0]
    link =(co_dict['url'] +iv['href'])
    soup = get_soup(link)
    pd =soup.find_all('a', href=re.compile("pdf"))

    print(pd)            



def get_sitemap(url):
    res = requests.get(f"{url}/sitemap.xml", headers=headers)
    if res.status_code != 200:
        res= requests.get(f"{url}/sitemap", headers=headers)
        if res.status_code == 404:
            res = (f"soup couldnt be created, Bad site design to blame for {url}")
    try:        
        soup = bs(res.content, 'lxml')
        return soup
    except:
        print(res)
        return(res)    
    

# def get_downloads(url):
#     soup = get_sitemap(url)
#     if soup == (f"soup couldnt be created, Bad site design to blame for {url}"):
#         return ("Poor soup served")
#     else:



# for c in co_dict:
#     get_downloads(**c)