import requests
from bs4 import BeautifulSoup
import pandas as pd

#main address
url = 'https://www.griotsgarage.com/'
#list to contain every product department page
sub_url_product_list =['wash-detail/wash-liquids/']
#list to contain every specific product links
product_addresses_url = [] 
for sub_url in sub_url_product_list :
    full_url = url + sub_url
    html_text = requests.get(full_url).text
    soup = BeautifulSoup(html_text, 'lxml')
    address = soup.find('ul',class_ = 'productGrid')
    #finds all links that is found uniquely in span tags under data-bv-redirect-url cat
    all_links = address.find_all('span',{'data-bv-redirect-url' : True})
    #save each link to product link list
    for links in all_links :
        link = links['data-bv-redirect-url']
        #print(link)
        product_addresses_url.append(link)

print(product_addresses_url)
