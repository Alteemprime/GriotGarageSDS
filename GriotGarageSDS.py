from urllib import response
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from urllib.parse import urlparse
import pandas as pd

# check if next label available with valid href
def pagination_detection(soup):
    result = False
    next_page = None
    pagination_symptom = soup.find('a', {'aria-label' : 'Next'})
    #if next label exist save next page on href value
    if len(pagination_symptom) > 0 :
        result = True
        next_page = pagination_symptom['href']
    else :
        result = False
        next_page = None
    #print (next_page)
    return result, next_page
    
    
def scrape_links(soup) :
    #list to contain every specific product links
    product_addresses_url = []   
    address = soup.find('ul',class_ = 'productGrid')
    #finds all links that is found uniquely in span tags under data-bv-redirect-url cat
    all_links = address.find_all('span',{'data-bv-redirect-url' : True})
    #save each link to product link list
    for links in all_links :
        link = links['data-bv-redirect-url']
        #print(link)
        product_addresses_url.append(link)
    return product_addresses_url

#function to download pdf content on located link element freom selenium
def download_pdf(url,destination_folder) :
    response = requests.get(url, stream=True)
    if response.status_code == 200 :
        parsed_url = urlparse(url)
        file_name = os.path.join(destination_folder,os.path.basename(parsed_url.path))
        
        with open(file_name, 'wb') as pdf_file:
            #retrive response chunk content of 1024 bytes
            for chunk in response.iter_content(1024):
                #append every chunk in file writing
                pdf_file.write(chunk)
        print(f'Downloading {file_name} success')                
    else :
        print(f'Failed to download {url}. Status code : {response.status_code}')

def scrape_pdf(url_link, destination_folder) :
    #pdf link are dynamically inserted via java script, need selenium to access    
    driver = webdriver.Edge()
    driver.get(url_link)
        
    try:
        # Wait for the presence of an anchor element with an href ending in '.pdf'
        sds_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="safetydatasheet"]'))
        )

        # Get url in sds link.get_attribute('href')
        pdf_url = sds_link.get_attribute('href')
        
        #download pdf
        download_pdf(pdf_url,destination_folder)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Allow some time for visualization (remove this in production)
        time.sleep(5)
        # Close the browser window
        driver.quit()

#main address
url = 'https://www.griotsgarage.com/'
#list to contain every product department page
sub_url_product_list =['wash-detail/wash-liquids/','wash-detail/detailers-liquids/','wash-detail/wheels-metal-liquids/',
                       'wash-detail/tires-trim-liquids/','wash-detail/glass-plastic-liquids/','wash-detail/leather-interiors-liquids/',
                       'wash-detail/specialty-solutions-liquids/','wash-detail/collections/all-microfiber/','wash-detail/wash-detail-kits/']
 
#for sub_url in sub_url_product_list :
#    full_url = url + sub_url    
#    html_text = requests.get(full_url).text    
#    soup = BeautifulSoup(html_text, 'lxml')         
#    product_links = scrape_links(soup)
#    print(product_links)
    
    #next_button, next_page = pagination_detection(soup)
    #if next_button :
    #    print (f'more page available at {next_page}')
download_folder = r'C:\Users\asus\Downloads\griotsgarage'        
scrape_pdf('https://www.griotsgarage.com/microfiber-foam-pad-cleaner/',download_folder)
#print(product_links)
