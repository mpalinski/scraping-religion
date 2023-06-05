# jw.py
import numpy as np
import pandas as pd
import glob
from time import sleep
from tqdm import tqdm
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    '''Get links to articles from jw.org/pl
    query: str, query to search for
    return: list of links and query'''
    site=f'https://www.jw.org/pl/szukaj/?q={query}'
    # assuming you have chromedriver in your path
    d = webdriver.Chrome()
    # otherwise you can use:
    # chromedriver = "/path/to/chromedriver/folder"
    # d = webdriver.Chrome(chromedriver)

    # get the page
    d.get(site)
    sleep(4) # asynchronous site

    # get the number of pages
    try:
        pagesMax=d.find_elements(By.XPATH, '//li[@class="cc-buttonGroup-container"]')[-2].text
    except IndexError:
        pagesMax=1

    print(f'Found {pagesMax} pages')

    # get the links
    links=[]

    d.get(site)
    sleep(1)
    els=d.find_elements(By.XPATH, '//div[@class="cc-mediaObject cc-mediaObject--horizontal cc-articleOmniSearchResultItem cc-articleOmniSearchResultItem--js"]//a')
    for el in els:
        links.append(el.get_attribute('href'))
    for page in tqdm(range(int(pagesMax))):
        try:
            d.find_element(By.XPATH, '//button[@class="lnc-button lnc-button--primary lnc-acceptCookiesButton"]').click()
        except:
            pass
        d.find_elements(By.XPATH, '//li[@class="cc-buttonGroup-container"]/button')[-1].click()
        sleep(2)
        els=d.find_elements(By.XPATH, '//div[@class="cc-mediaObject cc-mediaObject--horizontal cc-articleOmniSearchResultItem cc-articleOmniSearchResultItem--js"]//a')
        for el in els:
            links.append(el.get_attribute('href'))

    links=list(set(links))
    # links to df
    df=pd.DataFrame({'links':links})
    df.to_csv(f'data/links/jw_{query}.csv', index=False)
    
    return links, query

def get_articles(links, query):
    '''Get articles from links'''    
    print("Collecting articles...")
    # assuming you have chromedriver in your path (see: get_links function)
    d = webdriver.Chrome()

    titles=[]
    txts=[]
    added=[]
    workingLinks=[]

    for link in tqdm(links, desc='Getting articles'):
        if 'wol.jw' in link:
            try:
                d.get(link)
                workingLinks.append(link)
            except WebDriverException:
                print('WebDriverException, link: ', link)
                continue
            sleep(.5)
            try:
                titles.append(d.find_element(By.XPATH, '//div[@class="scalableui"]/p/strong').text)
            except:
                titles.append(np.nan)
            try:
                txts.append(d.find_element(By.XPATH, '//div[@class="scalableui"]').text)
            except:
                txts.append(np.nan)
            added.append(np.nan)
        else:
            try:
                d.get(link)
                workingLinks.append(link)
            except WebDriverException:
                print('WebDriverException, link: ', link)
                continue
            sleep(.5)
            try:
                titles.append(d.find_element(By.XPATH, '//article//header').text)
            except:
                titles.append(np.nan)
            try:
                txts.append(d.find_element(By.XPATH, '//div[@class="contentBody"]').text)
            except:
                txts.append(np.nan)
            try:
                added.append(d.find_element(By.XPATH, '//p[@class="newsPublishDate"]').text)
            except:
                added.append(np.nan)
                
    # articles to df
    df=pd.DataFrame({'title':titles, 'txt':txts, 'added':added, 'links':workingLinks})
    df.to_csv(f'data/arts/jw_{query}.csv', index=False)
    df.to_excel(f'data/arts/jw_{query}.xlsx', index=False)


if __name__ == '__main__':
    create_folders()
    arg1_value = str(sys.argv[1])
    links=get_links(arg1_value)[0] # this is a tuple so we need to get the first element
    get_articles(links, arg1_value)