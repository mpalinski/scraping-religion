# tp.py
import numpy as np
import pandas as pd
import glob
from time import sleep
from tqdm import tqdm
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
import os
import sys
import json

def create_folders():
    '''Create folders for articles run from the main repo folder level if folders already exist do nothing'''
    if not os.path.exists('data/arts/links.csv'):
        os.makedirs('data/links', exist_ok=True)
        print('Created links folder')
    else:
        print('Links folder already exists')
    if not os.path.exists('data/arts/'):
        os.makedirs('data/arts', exist_ok=True)
        print('Created arts folder')        
    else:
        print('Arts folder already exists')

def load_cookie(d, path):
    with open(path, 'r') as cookiesfile:
        cookies = json.load(cookiesfile)
    for cookie in cookies:
        d.add_cookie(cookie)

def get_links(query):
    '''Get links to articles from tygodnikpowszechny.pl
    query: str, query to search for
    return: list of links and query'''
    
    site="https://powszechswiat.pl/user"
    # assuming you have chromedriver in your path
    d = webdriver.Chrome()
    # otherwise you can use:
    # chromedriver = "/path/to/chromedriver/folder"
    # d = webdriver.Chrome(chromedriver)
    
    # get the page    
    # d.get(site)

    # sleep(60)
    # login manually and solve captcha
    # save cookies:
    # def save_cookie(d, path):
    # with open(path, 'wb') as filehandler:
    #     pickle.dump(d.get_cookies(), filehandler)
    
    d.get(f"https://www.tygodnikpowszechny.pl/search/site/{query}")
    load_cookie(d,"scripts/py/cookies.json")

    pagesMax=d.find_element(By.XPATH, '//li[@class="pager-last last"]/a').get_attribute('href')
    pagesMax=int(pagesMax.split('=')[-1])
    print(f'Found {pagesMax} pages')

    links=[]

    els=d.find_elements(By.XPATH, '//li[@class="search-result"]//a')
    for el in els:
        links.append(el.get_attribute('href'))

    for page in tqdm(range(pagesMax)):
        site=f"https://www.tygodnikpowszechny.pl/search/site/{query}?page={page+1}"
        d.get(site)
        els=d.find_elements(By.XPATH, '//li[@class="search-result"]//a')
        for el in els:
            links.append(el.get_attribute('href'))

    return links, query

def get_articles(links, query):
    '''Get articles from links'''    
    print("Collecting articles...")
    # assuming you have chromedriver in your path (see: get_links function)
    d = webdriver.Chrome()

    titles=[]
    leads=[]
    txts=[]
    auths=[]
    added=[]

    for link in tqdm(links, desc='Getting articles'):    
        try:
            d.get(link)
            load_cookie(d,"scripts/py/cookies.json")
        except WebDriverException:
            print('WebDriverException, link: ', link)
            continue
        try:
            titles.append(d.find_element(By.XPATH, '//h1[@class="field-content"]').text)
        except:
            titles.append(np.nan)
        try:
            leads.append(d.find_element(By.XPATH, '//div[@class="views-field views-field-field-summary"]/div[@class="field-content"]').text)
        except:
            leads.append(np.nan)
        try:
            txts.append(d.find_element(By.XPATH, '//div[@class="views-field views-field-body"]/div[@class="field-content"]').text)
        except:
            txts.append(np.nan)
        try:
            auths.append(d.find_element(By.XPATH, '//div[@class="field-content views-field-name"]').text)
        except:
            auths.append(np.nan)
        try:
            added.append(d.find_element(By.XPATH, '//span[@class="field-content"]').text)
        except:
            added.append(np.nan)

        sleep(2)

    # articles to df
    df=pd.DataFrame({'title':titles, 'leads':leads, 'txt':txts, 'auth':auths, 'added':added, 'links':links})
    df.to_csv(f'data/arts/tp_{query}.csv', index=False)
    df.to_excel(f'data/arts/tp_{query}.xlsx', index=False)

if __name__ == '__main__':
    create_folders()
    arg1_value = str(sys.argv[1])
    links=get_links(arg1_value)[0] # this is a tuple so we need to get the first element
    get_articles(links, arg1_value)
