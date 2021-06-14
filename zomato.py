from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import random
import time

driver = webdriver.Chrome('../chromedriver_linux64/chromedriver')

def parse_xyz(city):
    driver.get('https://www.xyz.com/')
    try:
        driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[2]/div/div[1]/input').send_keys(city, Keys.ENTER)
    except:
        driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/header/nav/ul[2]/li[1]/div/div/div[1]/input').send_keys(city, Keys.ENTER)    
    driver.implicitly_wait(8)
    time.sleep(random.randint(0,10))
    
    driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[4]/div[2]/div/div[1]/a').click()
    driver.implicitly_wait(8)
    time.sleep(random.randint(0, 10))
    z_dir = []
    for i in range(50):
        driver.find_element_by_xpath('/html/body/div[1]/div/div[8]/div/div[1]/div/div/a[2]/div['+i+']').click()
        driver.implicitly_wait(5)
        time.sleep(random.randint(0, 10))
        name = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/section[3]/section/section[1]/div/h1').text
        driver.find_element_by_xpath('/html/body/div[1]/div/main/div/article/div/section/section/div[1]/h2/a').click()
        address = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/section[4]/section/article/section/p').text
        time.sleep(random.randint(0, 10))
        phone = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/section[4]/section/article/p[1]').text
        try:
            phone2 = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/section[4]/section/article/p[2]').text
        except:
            phone2='N.A'

        try:
            phone3 = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/section[4]/section/article/p[3]').text
        except:
            phone3='N.A'
        try:
            cuisine = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/section[3]/section/section[1]/section[1]/div').text
        except:
            cuisine = 'N.A'
        rating = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/section[3]/section/section[2]/section[1]/div[1]/p').text
        n_revs = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/section[3]/section/section[2]/section[1]/div[2]/p').text
        try:
            time = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/section[3]/section/section[1]/section[2]/section/span[2]').text
        except:
            time='N.A'
        z_dic = {'name':name, 'address':address, 'phone':phone, 'phone2':phone2, 'phone3':phone3, 'ratings':rating, 'reviews':n_revs,'cus':cuisine, 'time':time}
        z_dir.append(z_dic)
        driver.back()
        driver.back()
        time.sleep(random.randint(2,7))
        print(z_dir)

parse_zomato('Delhi NCR')