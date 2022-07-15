from types import NoneType
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import lxml
# setting path
path = Service('C:\webdrivers\chromedriver')
driver = webdriver.Chrome(service=path)
# connecting to browser
driver.get('https://remote.co/')
driver.maximize_window()

# searching elements for scraping and closing unwanted banners
cs = driver.find_element(By.LINK_TEXT, 'Remote Customer Service Jobs')
wait = WebDriverWait(driver, 30)
time.sleep(1)
cs.click()
#closing banner
cb = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="CloseButton__ButtonElement-sc-79mh24-0 hfWEPH portstlucie-CloseButton portstlucie-close portstlucie-ClosePosition--top-right"]'))) 
time.sleep(2)
cb.click()
#getting html
jl = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/div/div[1]/div[4]/div/div[2]'))).get_attribute('outerHTML')
#ending selenium session
driver.close()

# storing html to file
"""file = open('page.html', 'w', encoding='utf-8')
file.write(jl)
file.close()"""

# turning html to bs4 object
soup = BeautifulSoup(jl, 'lxml')

soup.prettify()
#print(soup)
jobs = soup.find_all('a')
base_url = 'https://remote.co'
jl = []
for x in jobs:

    try:        
            #locating publishing date
            publ = x.find('span', class_='float-right d-none d-md-inline text-secondary').text
            # storing max week old jobs to list
            if 'hours' and 'hour' and 'days' and 'day' in publ:
                
                com = x.find('p', class_='m-0 text-secondary').find_next(string=True).string.replace('|', ' '). replace(' ', '').replace('\n', ' ')
                jl.append(f'company:{com}\n')
                title = x.find('span', class_='font-weight-bold larger').text
                jl.append(f'position: {title}\n')
                jl.append(f'published: {publ}\n')
                info = base_url + (x.get('href'))
                jl.append(f'info: {info}\n\n')  
                jt = x.find('span', class_='badge badge-success')
                jl.append(f'employment type: {jt.string} \n\n')
                
            else:
                pass
    except AttributeError as a:
        print('no info available')

# file containing wanted 
file = open('remotejobs.txt', 'w')
for i in jl:
    file.writelines(i)
file.close()