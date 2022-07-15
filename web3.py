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
#getting the browser ready
path = Service('C:\webdrivers\chromedriver')
driver = webdriver.Chrome(service=path)
wait = WebDriverWait(driver, 30)
# connecting to the site
driver.get('https://web3.career/')
driver.maximize_window()
time.sleep(1)
# closing banners and locating elements that has all the jobs

bclose = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Close"]')))
bclose.click()

remotebox = wait.until(EC.presence_of_element_located((By.ID, "remote_checbox")))
time.sleep(1)
remotebox.click()

cs = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'customer support')))
time.sleep(1)
cs.click()
# waits until page title is the present title
wait.until(EC.title_contains('Customer'))
tbd = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody[class="tbody"]'))).get_attribute('outerHTML')
# print(driver.title)

driver.close()

# file = open('page.html', 'w', encoding='utf-8')
# file.write(tbd)
# file.close()

# turning html to soup objects
soup = BeautifulSoup(tbd, 'lxml')
#indented code below turn soup elements to type int
    # soup = soup.prettify()

#element containing all the job information
jobs = soup.find_all('tr', style="cursor: pointer; ")
base_url = 'https://web3.career'
jl = []

for  elem in jobs:
    pub = elem.find('td', class_='align-middle job-time-ago-mobile').text.replace('\n', ' ')
    # order matters if 'd' is first if statement returns nothing
    if ('h') and ('d') in pub:
        title = elem.find('a').h2.text.replace('\n', ' ')
        jl.append(f'job title: {title}\n')
        com = elem.find('div', class_='mt-auto d-block d-md-flex').a.h3.text.replace('\n', ' ')
        jl.append(f'company: {com}\n')
        info =base_url + elem.find('a').get('href')
        jl.append(f'more info: {info} \n')
        loc = elem.find('td', class_='job-location-mobile').text.replace('\n', ' ')
        jl.append(f'job location: {loc}\n')
        jl.append(f'published: {pub} \n\n')

#storing scraped jobs to txt file
file = open('jobs.txt', 'w', encoding='utf-8')
for line in jl:
    file.writelines(line)
file.close()