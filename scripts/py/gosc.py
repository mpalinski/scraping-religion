# gosc.py
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

# known issues: we don't collect "RELACJA NA ŻYWO" 

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
    
def get_links(query):
    '''Get links to articles from gosc.pl
    query: str, query to search for
    return: list of links and query'''
    site=f'https://www.gosc.pl/wyszukaj/wyrazy?q={query}'
    # assuming you have chromedriver in your path
    d = webdriver.Chrome()
    # otherwise you can use:
    # chromedriver = "/path/to/chromedriver/folder"
    # d = webdriver.Chrome(chromedriver)
    
    # get the page
    d.get(site)
    # get the number of pages
    try:
        pagesMax=d.find_elements(By.XPATH, '//a[@class="pgr_arrow"]')[-1].get_attribute('href')
        pagesMax=int(pagesMax.split('/')[-1].split('?')[0])
    except IndexError:
        pagesMax=1

    print(f'Found {pagesMax} pages')

    # get the links
    links=[]
    for page in tqdm(range(pagesMax)):
        site=f'https://www.gosc.pl/wyszukaj/wyrazy/{page+1}?q={query}'
        d.get(site)
        # get the links
        links.extend([x.get_attribute('href') for x in d.find_elements(By.XPATH, '//h1[@class="src_auth_h"]/a')])
        sleep(1)
        # links to df
        df=pd.DataFrame({'links':links})
        df.to_csv(f'data/links/gosc_{query}.csv', index=False)
    return links, query

def get_articles(links, query):
    '''Get articles from links'''    
    print("Collecting articles...")
    # assuming you have chromedriver in your path (see: get_links function)
    d = webdriver.Chrome()

    titles=[]
    txts=[]
    auths=[]
    added=[]
    edition=[]
    tags=[]
    workingLinks=[]

    for link in tqdm(links, desc='Getting articles'):    
        try:
            d.get(link)
            workingLinks.append(link)
        except WebDriverException:
            print('WebDriverException, link: ', link)
            continue
        try:
            titles.append(d.find_element(By.XPATH, '//div[@class="cf txt "]/h1').text)
        except:
            titles.append(np.nan)
        try:
            txts.append(d.find_element(By.XPATH, '//div[@class="txt__content"]').text)
        except:
            txts.append(np.nan)
        try:
            auths.append(d.find_element(By.XPATH, '//p[@class="l doc-author"]').text)
        except:
            auths.append(np.nan)
        try:
            added.append(d.find_element(By.XPATH, '//span[@class="txt__doc-date"]').text)
        except:
            added.append(np.nan)
        try:
            edition.append(d.find_element(By.XPATH, '//span[@class="s"]').text)
        except:
            edition.append(np.nan)
        try:
            tags.append(d.find_element(By.XPATH, '//div[@class="tags"]').text)
        except:
            tags.append(np.nan)
        sleep(2)

    # articles to df
    df=pd.DataFrame({'title':titles, 'txt':txts, 'auth':auths, 'added':added, 'edition':edition, 'tags':tags, 'links':workingLinks})
    df.to_csv(f'data/arts/gosc_{query}.csv', index=False)
    df.to_excel(f'data/arts/gosc_{query}.xlsx', index=False)


if __name__ == '__main__':
    create_folders()
    arg1_value = str(sys.argv[1])
    links=get_links(arg1_value)[0] # this is a tuple so we need to get the first element
    get_articles(links, arg1_value)