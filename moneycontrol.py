import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import re
from base import get_soup, get_content
from time import sleep
import random
import os
import datetime as dt 

dtt = dt.datetime.now()
dtt = dtt.strftime('%Y-%m-%d')

def get_bs(name,symbol, url):
    dir_path = "MC/NSE/BS"
    if not os.path.exists(f"{dir_path}/{symbol}_stnd_BS.csv"):
        try:
            sleep(random.randint(5,10))
            html = get_content(url)
            df = pd.read_html(html)
            df = df[0]
            df.to_csv(f'{dir_path}/{symbol}_stnd_BS.csv')
            print(f"{name} Balance sheet recieved")
        except Exception as e:
            print(str(e))    
    else:
        print('DD AD')        

def get_pl(name,symbol, url):
    dir_path = "MC/NSE/PL"
    if not os.path.exists(f"{dir_path}/{symbol}_stnd_PL.csv"):
        try:
            sleep(random.randint(5,10))
            html = get_content(url)
            df = pd.read_html(html)
            df = df[0]
            df.to_csv(f'{dir_path}/{symbol}_stnd_PL.csv')
            print(f"{name} P&L recieved")
        except Exception as e:
            print(str(e))
    else:
        print('DD AD')        

# function not working, works on fresh reload - inconsitent

# def get_peer_table(name,url):
#     resc = get_content(url)
#     df = pd.read_html(resc)
#     df = df[65]
#     df.to_csv(f"MC/Cos/PT/{name}_peer_table.csv")
#     print(f"{name} Peer table recieved")


def get_brokers(name,symbol, soup):
    dir_path = "MC/NSE/Brokers"
    if not os.path.exists(f"{dir_path}/{symbol}_brokers.csv"):
        try:
            divv =soup.find('div', class_='brrs_stock')
            cards = divv.find_all('div', class_='brrs_bx')
            brokers_dict = []
            for c in cards:
                date = c.find('div', class_='br_date').get_text()
                rec = c.find('button').get_text()
                tds = c.find_all('td')
                recp = tds[0].get_text()
                trgtp = tds[1].get_text()
                dic = {'date':date, 'recm':rec, 'rec_price':recp, 'trgt_price':trgtp}
                brokers_dict.append(dic)
            df = pd.DataFrame(brokers_dict)
            df.to_csv(f"{dir_path}/{symbol}_brokers.csv")
            print(f"{name} brokers sheet recieved")    
        except Exception as e:
            print(str(e))    
    else:
        print('DD AD')    

def get_bds(co_name,symbol, soup):
    dir_path = "MC/NSE/BDs"
    if not os.path.exists(f"{dir_path}/{symbol}_deals.csv"):
        try:
            divv =soup.find('div', class_='dealbx')
            cards = divv.find_all('div', class_='bd_bx')
            bd_dict = []
            for c in cards:
                date = c.find('div', class_='br_date').get_text()
                transc = c.find('button', class_='btndeal').get_text()
                name = c.find('div', class_='brstk_name').get_text()
                tds = c.find_all('td')
                qty = tds[0].get_text()
                price = tds[1].get_text()
                traded_pc = tds[2].get_text()
                dic = {'date':date, 'transc':transc, 'name':name, 'qty':qty, 'price':price, 'traded_pc':traded_pc}
                bd_dict.append(dic)
            df = pd.DataFrame(bd_dict)
            df.to_csv(f"{dir_path}/{symbol}_deals.csv")
            print(f"{co_name} block deals sheet recieved") 
        except:
            print(f"Block Deals not available for {co_name}")    
    else:
        print('DD AD')        

def get_insiderT(co_name,symbol, soup):
    dir_path = "MC/NSE/IT" 
    if not os.path.exists(f"{dir_path}/{symbol}_ITs.csv"):
        try:
            sleep(random.randint(5,10))
            divv =soup.find('div', id='insider')
            cards = divv.find_all('div', class_='bd_bx')
            it_dict = []
            for c in cards:
                date = c.find('div', class_='br_date').get_text()
                transc = c.find('button', class_='btndeal').get_text()
                name = c.find('div', class_='brstk_name').get_text()
                dsgn = c.find('div', class_='desinper').get_text()
                tds = c.find_all('td')
                qty = tds[0].get_text()
                price = tds[1].get_text()
                traded_pc = tds[2].get_text()
                post_t_hldng = tds[3].get_text()
                dic = {'date':date, 'transc':transc, 'name':name,'dsgn':dsgn, 'qty':qty, 'price':price, 'traded_pc':traded_pc, 'pth':post_t_hldng}
                it_dict.append(dic)
            df = pd.DataFrame(it_dict)
            df.to_csv(f"{dir_path}/{symbol}_ITs.csv")
            print(f"{co_name} insider deals sheet recieved") 
        except:
            print(f"Insider transactions not available for {co_name}") 
    else:
        print('data already available')        

def scrape_indx_table(name, url,co):
    # save index movement table
    dir_path = "MC/NSE"
    html = get_content(url)
    df = pd.read_html(html)
    df = df[0]
    df.to_csv(f'{dir_path}/{name}_{dtt}_movement.csv')
    print(f"{name}_movement saved")

    # get each index table and for each element call get co detail
    soup = get_soup(url)
    table = soup.find_all('table')
    table = table[1]
    table_links = table.find_all('a')
    table_dict = []
    for s in table_links:
        link = s['href']
        name = s.get_text()
        dic = {'name':name, 'link':link}
        table_dict.append(dic)
    for t in table_dict:
        if co == "all":
            name = t['name']
            print(f"calling co detail for {name}")
            get_co_detail(t['name'], t['link'])
        else:
            if t['name'] == co:
                name = t['name']
                name = name
                print(f"calling co detail for {name}")
                get_co_detail(t['name'], t['link'])
            else:
                print('Not what you are looking for')    
        # sleep(random.randint(15,40))


def get_co_detail(name,url):
    soup = get_soup(url)
    bs_link = soup.find_all('a',href=re.compile('balance-sheet'))
    pl_link = soup.find_all('a',href=re.compile('profit-loss'))
    l = bs_link[1]
    pl = pl_link[0]
    pl_url = pl['href']
    bs_url = l['href']

    try:
        uls = soup.find_all('ul', class_='comdetl')
        ul = uls[-1]
        li = ul.find_all('li')
        symbol = li[1].p.get_text()

        get_bds(name,symbol, soup)
        get_insiderT(name,symbol,soup)
        get_brokers(name,symbol,soup)
        get_bs(name,symbol, bs_url)
        get_pl(name,symbol, pl_url)
        
    except:
        print(f'symbol not located for {name}')   




def scrape_mc(url, to_find="all", co="all"):
    # get homepage & navigate to index page
    soup = get_soup(url)
    indices_link = soup.find('a', string=re.compile('Indices'))
    soup = get_soup(indices_link['href'])

    # get all indices and for each call scrape index table
    li = soup.find_all('ul', class_='accordion_list')
    li = li[1]
    indices = li.find_all('li')
    indx_array = []
    for i in indices:
        indx = i.a
        name, link = indx.get_text(), indx['href']
        dic = {'name':name, 'link':link}
        indx_array.append(dic)
    for i in indx_array:
        if to_find != "all":
            if i['name'] == to_find:
                scrape_indx_table(i['name'], i['link'],co)
                sleep(random.randint(5,10))
            else:
                print('Index not found')    
        else:
            scrape_indx_table(i['name'], i['link'],co)
            sleep(random.randint(5,10))        

scrape_mc('https://www.moneycontrol.com',  co="Reliance")





# index dict - contains links for indices
# table dict - contains links for companies
# corp bs -  contains links for balance sheet
# table - contains table of price movement for index
    

