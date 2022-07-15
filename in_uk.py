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
# getting selenium ready for scraping
path = Service("C:\webdrivers\chromedriver")
driver = webdriver.Chrome(service=path)
wait = WebDriverWait(driver, 30)
# connecting to browser and website
driver.get('https://uk.indeed.com/')
driver.maximize_window()

# closing banners
rej = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-reject-all-handler')))
time.sleep(2)
rej.click()

# selecting jobs
stw = wait.until(EC.presence_of_element_located((By.ID, 'text-input-what')))
time.sleep(2)
stw.click()
time.sleep(1)
stw.clear()
stw.send_keys("customer service")
# selectng location
stw1 = wait.until(EC.presence_of_element_located((By.ID, 'text-input-where')))
time.sleep(2)
stw1.click()
time.sleep(1)
stw1.clear()
stw1.send_keys('remote')
se = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
se.click()

# closing banners
cl = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[onclick="closeGoogleOnlyModal()"]')))
cl.click()
time.sleep(1)
# job list by date
sort1 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="resultsCol"]/div[3]/div[4]/div[1]/span[2]/a')))
sort1.click()
time.sleep(2)

# closing banners
banner = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[autofocus]')))
banner.click()


# ensuring we are in correct page
wait.until(EC.title_contains('Customer Service'))
# print(driver.title)
time.sleep(5)
# waiting until job list html is same as in the browser html
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[class="jobsearch-ResultsList css-0"]')))
jobl = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul[class="jobsearch-ResultsList css-0"]'))).get_attribute('outerHTML')
# ending selenium session 
driver.close()


# file = open('page.html', 'w', encoding='utf-8')
# file.write(jobl)
# file.close()

soup = BeautifulSoup(jobl, 'lxml')

jobs = soup.find_all('div', class_='slider_container css-g7s71f eu4oa1w0')

base_url = 'https://uk.indeed.com'
joblist = []
for elem in jobs:
    try:
        # only newjob titles
        title = elem.find('h2', class_='jobTitle jobTitle-newJob css-bdjp2m eu4oa1w0').text + '\n'
        joblist.append(f'position: {title}')
        com = elem.find('span', class_='companyName').text + '\n'
        joblist.append(f'company: {com}')
        loc = elem.find('div', class_='companyLocation').text + '\n'
        joblist.append(f'job location: {loc}')
        pub = elem.find('span', class_='date').find(string=True, recursive=False).text + '\n'
        joblist.append(f'published: {pub}')
        info = base_url + elem.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0').get('href') + '\n\n'
        joblist.append(f'more info: {info}')

    except:
        continue

file = open('jobs.txt', 'w', encoding='utf-8')
for line in joblist:
    file.writelines(line)
file.close()