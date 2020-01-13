from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser=init_browser()
    scrape_result={}

    news_url="https://mars.nasa.gov/news/"
    browser.visit(news_url)
    news_html=browser.html    
    soup=bs(news_html,'html.parser')

    t=soup.find_all('div',class_='content_title')
    c=soup.find_all('div', class_="rollover_description_inner")
    title=t[0].text
    content=c[0].text
    scrape_result['news_title']=title
    scrape_result['news_p']=content

    mars_img_url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_img_url)
    mars_img_html=browser.html

    full_image=browser.find_by_xpath('//*[@id="full_image"]').first
    full_image.click()
    save_img=browser.find_by_xpath('//*[@id="fancybox-lock"]/div/div[2]/div/div[1]/a[2]').first
    save_img.click()

    soup=bs(browser.html,'html.parser')
    img=soup.find('figure',class_='lede')
    img_url=img.find('a')['href']
    url_base='https://www.jpl.nasa.gov'
    featured_image_url = url_base+img_url
    scrape_result['featured_image_url']=featured_image_url

    mars_weather_url='https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)
    mars_weather_html=browser.html    
    soup=bs(mars_weather_html,'html.parser')

    temps=soup.find_all('p',class_='TweetTextSize')
    weather=temps[0].text
    mars_weather=weather.strip('InSight').replace('pic.twitter.com/','    ')
    scrape_result['mars_weather']=mars_weather

    mars_fact_url='https://space-facts.com/mars/'
    table=pd.read_html(mars_fact_url)
    table_m=table[0].rename(columns={0:'Description',1:'Data'})
    table_m=table_m.set_index('Description')
    mars_table=table_m.to_html()
    mars_table=mars_table.replace('\n','')
    scrape_result['mars_table']=mars_table

    hemis_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemis_url)
    hemis_html=browser.html
    soup=bs(hemis_html,'html.parser')

    hemisphere_image_urls=[]
    hemispheres=soup.find_all('div', class_='item')
    for hemisphere in hemispheres:
        title=hemisphere.find('h3').text
        title_click=browser.find_by_text(title)
        title_click.click()
        #scrape with beautiful soup
        hemis_soup=bs(browser.html,'html.parser')
        url_div=hemis_soup.find('div',class_='downloads')
        url_img=url_div.find('a')['href']
        hemisphere_image_urls.append({'title': title, 'img_url' : url_img})
        browser.back()
    scrape_result['hemisphere_image_urls']=hemisphere_image_urls
    
    return scrape_result