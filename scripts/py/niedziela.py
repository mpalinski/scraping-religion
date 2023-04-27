# niedziela.py
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
    '''Get links to articles from niedziela.pl
    query: str, query to search for
    return: list of links and query'''
    site=f'https://www.niedziela.pl/znalezione?q={query}'
    # assuming you have chromedriver in your path
    d = webdriver.Chrome()
    # otherwise you can use:
    # chromedriver = "/path/to/chromedriver/folder"
    # d = webdriver.Chrome(chromedriver)

    # get the page
    d.get(site)
    # get the number of pages
    try:
        pagesMax=d.find_element(By.XPATH, '//li[@class="last"]/a').get_attribute('href')
        pagesMax=int(pagesMax.split('&')[1].split('=')[1])
    except IndexError:
        pagesMax=1

    print(f'Found {pagesMax} pages')

    # get the links
    links=[]
    for page in tqdm(range(pagesMax)):
        site=f'https://www.niedziela.pl/znalezione?q={query}&page={page+1}&per-page=25'
        d.get(site)
        # get the links
        links.extend([x.get_attribute('href') for x in d.find_elements(By.XPATH, '//div[@class="col-9 col-md-9 px-main my-main"]/a')])
        sleep(1)
        # links to df
        df=pd.DataFrame({'links':links})
        df.to_csv(f'data/links/niedziela_{query}.csv', index=False)
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
    edition=[]
    tags=[]

    for link in tqdm(links, desc='Getting articles'):    
        try:
            d.get(link)
        except WebDriverException:
            print('WebDriverException, link: ', link)
            continue
        try:
            titles.append(d.find_element(By.XPATH, '//h1[contains(@class, "title-page")]').text)
        except:
            titles.append(np.nan)
        try:
            leads.append(d.find_element(By.XPATH, '//p[contains(@class, "article-lead")]').text)
        except:
            leads.append(np.nan)
        try:
           els=d.find_element(By.XPATH, '//article[contains(@class, "article ")]').text
           txts.append(els)
        except:
            txts.append(np.nan)
        try:
            auths.append(d.find_element(By.XPATH, '//h3[@class="article-author font-weight-bold pt-half "]').text)
        except:
            auths.append(np.nan)
        try:
            edition.append(d.find_element(By.XPATH, '//p[@class="article-magazine mt-half "]/a').get_attribute('href'))
        except:
            edition.append(np.nan)
        try:
            tags.append(d.find_element(By.XPATH, '//a[@class="color-blue2"]').text)
        except:
            tags.append(np.nan)
        sleep(2)


    # articles to df
    df=pd.DataFrame({'title':titles, 'leads':leads, 'txt':txts, 'auth':auths, 'edition':edition, 'tags':tags, 'links':links})
    df.to_csv(f'data/arts/niedziela_{query}.csv', index=False)
    df.to_excel(f'data/arts/niedziela_{query}.xlsx', index=False)

if __name__ == '__main__':
    create_folders()
    arg1_value = str(sys.argv[1])
    links=get_links(arg1_value)[0] # this is a tuple so we need to get the first element
    get_articles(links, arg1_value)