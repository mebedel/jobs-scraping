from types import NoneType
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import lxml
# setting path for chromedriver
path = Service('C:\webdrivers\chromedriver')
# gettin the browser ready for use
driver = webdriver.Chrome(service=path)
wait = WebDriverWait(driver, 10)
# connecting to website
driver.get('https://careers.achievetestprep.com/recruit/Portal.na')
time.sleep(1)
# search publishing date from this element
dt = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="zr-joblist-container"]/tbody')))

# element containing jobs list
aj = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="zr-joblist-container"]/tbody'))).get_attribute('outerHTML')
time.sleep(5)

#closing browser
driver.close()

# getting html to bs4
soup = BeautifulSoup(aj, 'lxml')
# makes html more readable
soup.prettify()
# element containing all the jobs
jobs = soup.find_all('td')
# list to store job data title, company...
jl = []
#loop to get job data companyname...
for x in jobs:
    base_url = 'https://careers.achievetestprep.com'
    print(' ')

    jl.append(x.text + '\n')
    subdomain = x.find(class_='jobdetail', href=True)

    # try method solves typeError as element contains None type too
    try:
        #print(subdomain['href'])
        if subdomain['href'] != None:
            print(type(subdomain['href']))
        else:
            print('none')
        url = (base_url + subdomain['href'])
        
        jl.append(url + '\n')
    except:
        continue

file = open('jobs.txt','w')
for items in jl:
    file.writelines(items)
file.close()
"""project is only missing publishing date i will return on later to solve how"""