import requests
from bs4 import BeautifulSoup as bs
import re
import time
import pandas as pd 
from ratelimit import limits
from multiprocessing import Pool
import urllib.robotparser as rp

headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }
def getFilename_fromCd(cd):
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

def get_rt(url, suffix):
    urll = (f"http://{url}.{suffix}/robots.txt")  
    r = requests.get(urll,headers=headers, allow_redirects=True)
    if r.status_code == 200:
        print(f'request for {url} successful')
    else:
        print(f'request for {url} failed')  
    filename = getFilename_fromCd(r.headers.get('content-disposition'))
    open(f'{url}.txt', 'wb').write(r.content)
    print(f'file for {url} saved')
    time.sleep(5)

def df_loader(df):
    df = pd.read_csv(df)
    for i,r in df.iterrows():
        get_rt(r['Url'], r['suffix'])

# df_loader('indian_websites.csv')

def parse_robofile():
    r = rp.RobotFileParser()
    r.set_url(file)
    r.read()
    rrate = r.request_rate("*")

def check_robotfile(name, url):
    fle = open(f"webs_robots_files/{name}.txt")
    r = rp.RobotFileParser()
    r = r.set_url(fle)
    op = r.can_fetch("*", url)
    print(op)
    return op

