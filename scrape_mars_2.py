#!/usr/bin/env python
# coding: utf-8

# In[4]:


from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint


# In[5]:


def init_browser():
    # executable_path = {"executable_path": "chromedriver.exe"}
    executable_path = {"executable_path": "chromedriver.exe"}
    driver = webdriver.Chrome(executable_path)
    # return Browser("chrome", **executable_path, headless=False)
    return Browser("chrome", **driver, headless=False)


# In[6]:

    # mars news
def mars_news(browser):     
    # browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    ul = soup.find("ul", class_="item_list")
    print(ul)    
    news_title = ul.find_all('li',class_='slide')[0].find("div", class_="image_and_description_container").find("div",class_="list_text").find("div",class_="content_title").get_text()
    news_p = ul.find_all('li',class_='slide')[0].find("div", class_="image_and_description_container").find("div",class_="list_text").find("div", class_="article_teaser_body").get_text()
    print (news_title)
    print(news_p)
    return news_title, news_p


 # image url
def featured_image(browser):    
    # browser = init_browser()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
        
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")
        
     # find the relative image url
    img_url_rel = image_soup.select_one("img.main_image").get("src")
    img_url_rel
    featured_image_url = f"https://www.jpl.nasa.gov{img_url_rel}"
    print (featured_image_url)
    return featured_image_url


    ### Mars Weather
def mars_weather(browser):
    # browser = init_browser()
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html = browser.html
    weather_soup = BeautifulSoup(html, "html.parser")
    mars_weather = weather_soup.find("div",class_="js-tweet-text-container").find("p", class_="tweet-text").get_text()        
    print(mars_weather)
    return mars_weather
    # ("div", class_="content")


    ### Mars Facts
def mars_facts(browser):
    # browser = init_browser()
    url_facts = "https://space-facts.com/mars/"
    browser.visit(url_facts)

    html = browser.html
    table_soup = BeautifulSoup(html, "html.parser")
    table = table_soup.find("table", id="tablepress-p-mars")
        
    print(table)
    table_df = pd.read_html(url_facts)[1]
    table_df.columns = ["Description", "Facts"]
    table_df.set_index("Description", inplace = True)
    return table_df.to_html()
    

    # In[104]:


    ### Mars Hemispheres
def mars_hemisphere(browser):
    # browser = init_browser()
    reso_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    base_url= " https://astrogeology.usgs.gov"
        
    browser.visit(reso_url)

    html1 = browser.html
    reso_soup = BeautifulSoup(html1, "html.parser")
    results = reso_soup.find_all("div", class_="description")
    #     results
    hemisphere_image_urls = []
    for section in results:
        item_link = section.find("a",class_="itemLink product-item").get("href")
        title =  section.find("h3").get_text()
    #         print(item_link)
        print(title)
        final_link = base_url+item_link
        browser.visit(final_link)
        html2 = browser.html
        img_soup = BeautifulSoup(html2, "html.parser")
        img_link = img_soup.find("div", class_="downloads").find("a").get("href")
        print(img_link)
        print("-------------")
        hemisphere_image_urls.append({"title":title,"img_url":img_link})   
    return hemisphere_image_urls

    # df= pd.DataFrame(hemisphere_image_urls)
    # df
    # df.to_dict(orient='records')

def scrape():

    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_p = mars_news(browser)

    # Run all scraping functions and store in dictionary.
    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image(browser),
        "weather": mars_weather(browser),
        "facts": mars_facts(browser),
        "hemispheres": mars_hemisphere(browser),
    }

    # Stop webdriver and return data
    browser.quit()
    return data
     





