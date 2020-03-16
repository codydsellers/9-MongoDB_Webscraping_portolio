from bs4 import BeautifulSoup
from splinter import Browser
import requests
import os
import pandas as pd

def scrape_1():
    
    page = requests.get("https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest")
    soup = BeautifulSoup(page.content, 'html.parser')
    news_title = soup.find('div', class_="content_title").text.strip()
    news_p = soup.find('div', class_="rollover_description_inner").text.strip()
    
    return news_title, news_p

#THIS IS FOR STEP #2

def scrape_2():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    browser.find_by_id('full_image').click()
    browser.find_link_by_partial_text('more info').click()

    new_html = browser.html
    img_soup = BeautifulSoup(new_html, 'html.parser')
    img_link = img_soup.find("figure", class_='lede').a['href']
    recent_image = 'https://www.jpl.nasa.gov' + str(img_link)
    
    return recent_image

#THIS IS FOR STEP #3

def scrape_3():
    page = requests.get("https://twitter.com/marswxreport?lang=en")
    soup = BeautifulSoup(page.content, 'html.parser')
    latest_weather = soup.find("div",class_="js-tweet-text-container").text.strip()
    
    return latest_weather

#THIS IS FOR STEP #4
def scrape_4():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_table = tables[0]
    mars_table.columns = ["Mars Information", "Values"]
    mars_table.set_index("Mars Information", inplace=True)
    table = mars_table.to_html()
    return table


#THIS IS FOR STEP #5
def scrape_5():
    page = requests.get('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find_all('div', class_='item')
    hemisphere_list = []

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    for result in results:
        
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        
        try:
            h3 = result.h3.text
            browser.find_link_by_partial_text(h3).click()
            
            new_html = browser.html
            img_soup = BeautifulSoup(new_html, 'html.parser')
            img_link = img_soup.find("img", class_='wide-image')['src']
            full_url = 'https://astrogeology.usgs.gov/' + img_link
        
            entry = {
                "text": h3,
                "url": full_url
            }
        
            hemisphere_list.append(dict(entry))
        
        except:
            pass

    return hemisphere_list

def scrape():
    news_title, news_p = scrape_1()
    recent_image = scrape_2()
    latest_weather = scrape_3()
    table = scrape_4()
    hemisphere_list = scrape_5()
    
    data = {
        "news title": news_title,
        "news paragraph": news_p,
        "featured image": recent_image,
        "latest weather": latest_weather,
        "mars_facts": table,
        "hemispheres": hemisphere_list
    }

    return data