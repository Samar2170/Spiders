import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from base import get_soup
import re
from time import sleep
import os

def save_listings(soup,indx, loc):
    cards = soup.find_all('div', class_="pageComponent srpTuple__srpTupleBox srp")
    re_dict = []
    print(f" found {str(len(cards))} listings")
    for c in cards:
        title = c.find('a', id='srp_tuple_property_title')
        title = title.get_text()
        price = c.find('td', id='srp_tuple_price').get_text()
        area = c.find('td', id='srp_tuple_primary_area').get_text()
        bhk = c.find('td', id='srp_tuple_bedroom').get_text()
        des = c.find('div', id='srp_tuple_description').get_text()
        dic = {'title':title,'price':price,'area':area,'bhk':bhk,'descrp':des}
        re_dict.append(dic)
    df = pd.DataFrame(re_dict)
    if not os.path.isdir(f'RE_listings/{loc}'):
        os.mkdir(f'RE_listings/{loc}')

    df.to_csv(f'RE_listings/{loc}/99acres_listings_{indx}.csv')


# def get_n_listings(soup,locality):
    


def parse_99acres(locality,n):
    url=(f"https://www.99acres.com/search/property/buy/residential-all/{locality}?search_type=QS&refSection=GNB&search_location=HP&lstAcn=HP_R&lstAcnId=0&src=CLUSTER&preference=S&selected_tab=1&city=5&res_com=R&property_type=R&isvoicesearch=N&keyword_suggest=Delhi%20West%3B&fullSelectedSuggestions=Delhi%20West&strEntityMap=W3sidHlwZSI6ImNpdHkifSx7IjEiOlsiRGVsaGkgV2VzdCIsIkNJVFlfNSwgUFJFRkVSRU5DRV9TLCBSRVNDT01fUiJdfV0%3D&texttypedtillsuggestion=De&refine_results=Y&Refine_Localities=Refine%20Localities&action=%2Fdo%2Fquicksearch%2Fsearch&suggestion=CITY_5%2C%20PREFERENCE_S%2C%20RESCOM_R&searchform=1&price_min=null&price_max=null")
    soup = get_soup(url)
    save_listings(soup,281, locality)
    sleep(2)
    for i in range(n):
        loc = locality
        npl = soup.find('a',string=re.compile('Next Page'))
        npl = npl['href']
        np_soup = get_soup(npl)
        save_listings(np_soup,i, loc)
        sleep(5)
        print(f"saved page {str(n)} ")

parse_99acres('model-town',25)
