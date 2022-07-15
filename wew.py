from turtle import ht
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
# setting path and getting driver ready
path = Service('C:\webdrivers\chromedriver')
driver = webdriver.Chrome(service=path)
# connecting to website
driver.maximize_window()
wait = WebDriverWait(driver, 30)
driver.get('https://workew.com/')
# clicking wanted choices in the browser
remo = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="https://workew.com/remote-jobs/"]')))
ActionChains(driver).move_to_element(remo).perform()

cs = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="https://workew.com/remote-jobs/support/"]')))
cs.click()

#waiting until correct page html is available
wait.until(EC.title_contains('Support'))
#print(driver.title)
jlist = driver.find_element(By.CSS_SELECTOR, 'ul[class="job_listings"]').get_attribute('outerHTML')
driver.close()

# file = open('page.html', 'w', encoding='utf-8')
# file.write(jlist)
# file.close()

# converting html to bs4 object
soup = BeautifulSoup(jlist, 'lxml')
# all the jobs in this element
jobs = soup.find_all('li')
# list to store data from for loop
jlist = []

for elem in jobs:
    # try is necessary as element contain type None among wanted data
    try:
        title = elem.find('div', class_="job_listing-position job_listing__column").h3.text +'\n'
        jlist.append(f'title: {title}')
        com = elem.find('div', class_="job_listing-company").strong.text +'\n'
        jlist.append(f'company: {com}')
        pub = elem.find('li', class_="job_listing-date").text +'\n'
        jlist.append(f'published: {pub}')
        loc = elem.find('a', class_="google_map_link").text +'\n'
        jlist.append(f'location: {loc}')
        info = elem.find('a', class_="job_listing-clickbox").get('href')+'\n\n'
        jlist.append(f'more information: {info}')
        #print( title, com, pub, loc, info)
        
    except:
        continue
# txt file to store all the jobs
file = open('jobs.txt', 'w', encoding='utf-8')

for line in jlist:
    file.writelines(line)
file.close()