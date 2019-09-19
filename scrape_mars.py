#!/usr/bin/env python
# coding: utf-8

# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd
import lxml
import html5lib

def scrape_info():
    
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Retrieve the parent divs for all articles
    results = soup.find('div', class_='slide')

    # Loop through results to retrieve the New Title and Paragraph Text
    #for result in results:
    news_title = results.find('div', class_='content_title').text.strip()
    news_p = results.find('div', class_='rollover_description_inner').text.strip()
    print(f"News title = {news_title}")
    print(f"News paragraph = {news_p}")

    # Scrape the latest Mars weather tweet from the page. 
    # Retrieve page with the requests module
    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Save the tweet text for the weather report as a variable called mars_weather.
    results = soup.find('div', class_='content')
    mars_weather = results.find('p').text.replace("\n", "")
    print(f"Mars weather = {mars_weather}")

    # Set the chromedriver path (added chromedriver.exe to working directory)
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Go to NASA images website and click "Full Image" of featured image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Make soup of page, grab image, and add the rest of the url to it
    featured_image = soup.find('img')
    # ,class_="fancybox-image")["src"]
    # featured_image_url = 'https://www.jpl.nasa.gov' + str(featured_image)
    featured_image_url = 'https://www.jpl.nasa.gov' + "/spaceimages/images/mediumsize/PIA14762_ip.jpg"
    print(featured_image_url)

    # Scrape space-facts website, Mars page, for the table with info about Mars.
    url= "https://space-facts.com/mars/"
    tables_df = pd.read_html(url)
    # Grab the second table, set the index as the first column of info and remove column headers (to look better on final webpage)
    table_df = tables_df[1]
    table_df = table_df.rename(columns = {0:"Fact",1:"Value"}).set_index("Fact")
    table_df

    table_html = table_df.to_html()#("table.html")


    # Save full jpg Mars hemisphere images to a dictionary
    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere Enhanced", "img_url": "https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg"},
        {"title": "Schiaparelli Hemisphere Enhanced", "img_url": "https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg"},
        {"title": "Syrtis Major Hemisphere Enhanced", "img_url": "https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg"},
        {"title": "Valles Marineris Hemisphere Enhanced", "img_url": "https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg"},
    ]
    hemisphere_image_urls

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "mars_weather": mars_weather,
        "featured_image_url": featured_image_url,
        "table_df": table_html,
        "hemisphere_image_urls": hemisphere_image_urls
        }
    print(mars_data)

    # Close the browser after scraping
    browser.quit()

    return mars_data

