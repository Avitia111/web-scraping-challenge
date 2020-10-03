from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars = {}

    ###NASA Mars News###
    # Bring in the website to be scraped
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    

    #Iterate through x number of pages:
    for x in range(4):  #--- Don't need this, just getting first occurence
        
        html=browser.html
    
        soup=bs(html, 'html.parser')
    
        articles = soup.find('div', class_='grid_layout')
        article = articles.find('li', class_='slide')
            
    #Check if it found an article, if not try again???
        if article:
            
            news_title = article.find('div', class_='content_title').text
            news_p = article.find('div', class_='article_teaser_body').text 
            mars["news_title"] = news_title
            mars["news_text"] = news_p
            break

        # Click the 'More' button on each page
        else: 
            try:
                print("next page------------------------------------")
                browser.click.links.find_by_partial_text('More')
            
            except:
                print("Scraping Complete")
            
    

    # ###JPL Mars Space Images - Featured Image###
    # #  Bring in the website to be scraped
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    
     ##Get featured image from url
    html = browser.html
    soup = bs(html, 'html.parser')

    result = soup.find('a', class_='button fancybox')

    mars["featured_image"]= f"https://www.jpl.nasa.gov{result['data-fancybox-href']}"
    

    ###Mars Facts###
    browser = init_browser()
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    

    ##Save Mars information to dataframe and set the index to the info fields
    df = tables[0]
    df.columns = ["Description", "Mars"]

    df.set_index("Description", inplace=True)

    ##create and HTML table string
    html_table = df.to_html()
    mars["table_data"] = html_table
    

    ###Mars Hemispheres###
    #Bring in the website to be scraped
    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    ##Get hemisphere search results
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('div', class_='item')
    title = []
    img_url = []

    ##iterate through the hemisphere pages by visiting each page to get title and image url
    for result in results:
        
        link = "https://astrogeology.usgs.gov" + result.find('a', class_='itemLink product-item')['href']
        browser.visit(link)
        html = browser.html
        soup = bs(html,'html.parser')
        page_result = soup.find('div', class_='container')
        
        title.append(page_result.find('h2', class_='title').text)
        img_url.append("https://astrogeology.usgs.gov" + page_result.find('img', class_="wide-image")['src'])
   
    #Save hemisphere info to a dataframe
    hemisphere_image = pd.DataFrame({
        "title": title,
        "img_url": img_url
    })

    mars["title1"] = hemisphere_image['title'][0]
    mars["url1"] = hemisphere_image['img_url'][0]
    mars["title2"] = hemisphere_image['title'][1]
    mars["url2"] = hemisphere_image['img_url'][1]
    mars["title3"] = hemisphere_image['title'][2]
    mars["url3"] = hemisphere_image['img_url'][2]
    mars["title4"] = hemisphere_image['title'][3]
    mars["url4"] = hemisphere_image['img_url'][3]

    return mars