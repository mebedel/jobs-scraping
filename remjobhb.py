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

#getting browser ready
path = Service('C:\webdrivers\chromedriver')
driver = webdriver.Chrome(service=path)
# connecting to the site
driver.get('https://remotejobhuntbuddy.com/')
time.sleep(1)
driver.maximize_window()
wait = WebDriverWait(driver, 10)
#locating and clicking button on the browser
cate = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Categories'))) 
time.sleep(1)
cate.click()
time.sleep(1)

cs = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/remote-jobs/customer-support"]'))) 
cs.click()

# this stores the tabs in to array?
handels = driver.window_handles
# this shows number of tabs open
print(len(handels))
# this switches the tabs
driver.switch_to.window(handels[1])
# this show what is the current tab
print(driver.title)

#storing  element containing all the jobs as html 
panel = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="panel"]'))).get_attribute('outerHTML')

time.sleep(2)
driver.close()
driver.quit()

# file = open('page.html', 'w', encoding='utf-8')
# file.write(panel)
# file.close()


# getting bs4 ready for scraping 
soup = BeautifulSoup(panel, 'lxml')
# makes html more readable
soup.prettify()
print(soup)
jobs = soup.find('div', class_= 'panel')

jl = []
base_url =  'https://remotejobhuntbuddy.com'
for x in jobs:
    try:
        title = x.find('div', class_= 'job-title').a.text.replace('\n', ' ').replace('     ', ' ')
        jl.append(f'job title: {title} \n')
        com = x.find('span', class_="tag is-light is-hidden").previous_sibling.text +'\n'
        jl.append(f'company: {com} ')
        publ = x.find('span', class_="tag is-light is-hidden").next_sibling.text + '\n'
        jl.append(f'published: {publ} ')
        info = base_url + x.find('div', class_= 'job-title').a.get('href')
        jl.append(f'more information: {info} \n\n')
        
        

    except:
        continue

file = open('joblist.txt', 'w', encoding='utf-8')

for c in jl:
    file.writelines(c)
file.close()