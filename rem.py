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

path = Service('C:\webdrivers\chromedriver')
# connecting selenium to chromedriver
driver = webdriver.Chrome(service=path)
# for waiting the elements or element actions
wait = WebDriverWait(driver, 10)
# full screen
driver.maximize_window()

driver.get('https://remoteok.com/')
# selecting job category
sr = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"]')))
time.sleep(2)
sr.click()
time.sleep(1)
sr.send_keys('customer support', Keys.ENTER)

# selecting the location 
loc = wait.until(EC.presence_of_element_located((By.LINK_TEXT, '⬜️ Worldwide')))
ActionChains(driver).move_to_element(loc).perform()
time.sleep(1)
loc.click()
time.sleep(1)

# closing email banner
cb = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="action-close-catch-emails"]')))
ActionChains(driver).move_to_element(cb).perform()
cb.click()

# element has all the job lists
aj = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody'))).get_attribute('outerHTML')
driver.close()


# turn to soup object
soup = BeautifulSoup(aj, 'lxml')
# make html more readable
soup.prettify()
# table containing all the jobs
jobs = soup.find_all('tr')
# for later use 
base_url = 'https://remoteok.com'
# list to store all the results
jl = []
# loop to extract data from job table 
for x in jobs:
    # lots of nonetype objects
    
    try:
        hiring = x.find('span', class_='closed style= tooltip-set').text.replace('\n', ' ')
        jl.append(f'hiring is: {hiring} \n')
    #if hiring != 'closed':
        com = x.find('td', class_='company position company_and_position').h3.text.replace('\n', ' ')
        jl.append(f'company name: {com} \n')
        title = x.find('td', class_='company position company_and_position').h2.text.replace('\n', ' ')
        jl.append(f'position: {title}\n')
        loc = x.find('div', class_='location tooltip').text.replace('\n', ' ')
        jl.append(f'location: {loc} \n')
        info =base_url + x.find('a', class_='preventLink')['href']
        jl.append(f'more info: {info} \n')
        pub = (x.find('td', class_='time').text.replace('\n', ' '))
        jl.append(f'published: {pub} ago\n\n')
    except AttributeError:
        continue
# storing the data to text file
file = open('remjobs.txt', 'w', encoding='utf8')
for x in jl:
    try:
        file.writelines(x)
    except:
        pass
file.close()