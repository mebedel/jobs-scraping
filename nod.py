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

# connecting chromedriver to selenium
path = Service('C:\webdrivers\chromedriver')
driver = webdriver.Chrome(service=path)
# webdriver wait for later use
wait = WebDriverWait(driver, 10)
# connecting to browser
driver.get('https://nodesk.co/')
#full screen
driver.maximize_window()
# locating and clicking remote jobs button in the browser
rmj = driver.find_element(By.CSS_SELECTOR, 'a[href="/remote-jobs/"]')
time.sleep(2)
rmj.click()

time.sleep(2)
# locating and closing banner at the browser
cl = driver.find_element(By.CSS_SELECTOR, 'svg[class="grey-050 dim h4 w4 ml4 newsletter-banner-close pointer"]')
time.sleep(2)
cl.click()
# locating and closing banner at the browser
cl1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'svg[class="cookie-banner-close dim h4 w4 ml2 pointer"]')))
# mouse hover action
ActionChains(driver).move_to_element(cl1).perform()
cl1.click()
# locating and clicking button
cs = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Customer Support')))
time.sleep(2)
#mouse hover action
ActionChains(driver).move_to_element(cs).perform()
time.sleep(1)
cs.click()
rnclick = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchbox"]/div/form/input')))
ActionChains(driver).move_to_element(rnclick).perform()
rnclick.click()
time.sleep(1)
rnclick.send_keys(Keys.ENTER)

# locating search bar element
loc = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Filter by remote location"]')))
#mouse hover action
ActionChains(driver).move_to_element(loc).perform()
loc.click()
time.sleep(1)
# sending word to search bar
loc.send_keys('worldwide')
time.sleep(2)
loc.send_keys(Keys.ENTER)
time.sleep(2)

# all jobs div[id="hits"]
# element containing all the jobs converted to html 
aj = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ol[class="ais-Hits-list"]'))).get_attribute('outerHTML')
# selenium session over
driver.close()

#storing html to file for scraping  
"""with open('page.html', 'w') as f:
    f.write(str(aj))
f.close()
"""
# html to bs4 to scrape data from it 
soup = BeautifulSoup(aj, 'lxml')
# makes the html more readable
soup.prettify()

# for later use
base_url = 'https://nodesk.co'
# list containing the jobs
jobs = soup.find_all('div', class_ = 'dt-s dt-ns w-100 pa3 pv4 pa5-l bt b--indigo-050 bg-white')
# list to store scraped data
jl = []
# looping the listjobs and adding to another list jl
for x in jobs:
    title = x.find('h2').text.strip(' ')
    jl.append(f'searching for: {title} \n')
    company = x.find('h3').text.strip(' ')
    jl.append(f'Company name: {company} \n')
    location = x.find('h4').text.strip(' ') + x.find('h5').text
    jl.append(f'work location {location} \n')
    jobtype = x.find('div', class_ = 'flex inline-flex-s inline-flex-ns items-center mr3-s mr3-m mr6-l mv1 mv0-l nowrap').h4.text.strip(' ')
    jl.append(f'jobtype: {jobtype}\n')
    info = base_url + x.find('a')['href'].strip(' ')
    jl.append(f'more info: {info} \n')
    pub =  x.find('span', class_ = 'f9').text
    jl.append(f'published: {pub} \n\n')

# file to store scraped data
file = open('nodejobs.txt', 'w')

for lines in jl:
    file.writelines(lines)
file.close()