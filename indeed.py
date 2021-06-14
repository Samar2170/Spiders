from time import sleep
import requests
from bs4 import BeautifulSoup as bs
import random
import pandas as pd
import os
headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

sd = {'job':'full-stack-developer', 'city':'gurgaon', 'state':'haryana'}

base_url = 'https://in.indeed.com/'

def search_indeed(job,city,state):    
    res = requests.get(f"{base_url}{job}-jobs-in-{city}-City,-{state}", headers=headers)
    sit= res.content
    soup = bs(sit,'lxml')
    print('request sucessful')
    return soup

#called in scrape_indeed
def get_soup_by_arg(arg):
    res = requests.get(f"{base_url}{arg}", headers=headers)
    sit= res.content
    soup = bs(sit,'lxml')
    return soup

def get_soup_by_url(arg):
    res = requests.get(arg, headers=headers)
    sit= res.content
    soup = bs(sit,'lxml')
    return soup

#called in scrape_indeed
def get_jobs(soup):
    job_card = soup.find_all('div', class_='jobsearch-SerpJobCard')
    job_dict = []
    for j in job_card:
        job_url=j.a['href']
        job_title=j.a.get_text()
        co = j.span.get_text()
        try:
            sal = j.find('div', class_='salarySnippet')
            sal = sal.get_text()
        except:
            sal = 'N.A'
        dic = {'title':job_title,'url':job_url, 'co':co, 'sal':sal}    
        job_dict.append(dic)
    return job_dict

#called in scrape_indeed
def get_data_by_job(url):
    bs_url=(f"https://in.indeed.com{url}")
    soup = get_soup_by_url(bs_url)
    try:
        hd_text = soup.find('div', class_='jobsearch-InlineCompanyRating')
        hd_text = hd_text.get_text()
    except:
        hd_text = 'N.A'
    try:
        descpr = soup.find(id='jobDescriptionText')
        descpr = descpr.get_text()       
    except:
        descpr = 'N.A'   
    return hd_text, descpr    


def scrape_indeed(job,city,soup, epochs):
    tj = soup.find('div',id='searchCountPages')
    jd1 = get_jobs(soup)
    for j in jd1:
        head, descp =get_data_by_job(j['url'])
        j['head'] = head
        j['descp'] = descp
        print(j)
        print('going to sleep')
        sleep(random.randint(15,30))
    for i in range(epochs):
        pages = []
        page_url = soup.find('ul', class_='pagination-list')
        for p in page_url:
            try:
                url = p.a['href']
                indx = p.a.span.get_text()
                dic = {'url':url, 'indx':indx}
            except:
                url = 'N.A'
                indx = 'N.A'
                dic = {'url':url, 'indx':indx}
            pages.append(dic)    
        page = pages[-1]
        soup = get_soup_by_arg(page['url'])
        print('next page request sucessful')
        jd2 = get_jobs(soup)
        for j in jd2:
            head, descp =get_data_by_job(j['url'])
            j['head'] = head
            j['descp'] = descp
        jd1 = jd1 + jd2                

        pages.clear()
        print(jd1)
        jobs_df = pd.DataFrame(jd1)
        jobs_df.to_csv(f"{job}_{city}_ij_{len(jd1)}.csv")
        print('file saved')
        print('going to sleep')
        sleep(random.randint(10,20))
        print('im back')

    print('all entries saved')    


def si_by_jobs(**sd):
    job = sd['job']
    city = sd['city']
    state = sd['state']
    
    soup = search_indeed(job,city,state)
    scrape_indeed(job,city,soup, 20)

si_by_jobs(**sd)






