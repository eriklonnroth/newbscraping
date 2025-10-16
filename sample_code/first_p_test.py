import requests
from bs4 import BeautifulSoup as BS

URL='https://www.daynurseries.co.uk/daynursery.cfm/searchazref/65432253422'
h={'User-Agent':'Mozilla/5.0'}; s=BS(requests.get(URL,headers=h,timeout=30).text,'lxml')
p=s.select_one('p')
print('First <p> text:', (p.get_text(strip=True) if p else ''))