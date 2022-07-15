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

# setting chromedriver path
path = Service('C:\webdrivers\chromedriver')
#initialising browser
driver = webdriver.Chrome(service=path)
wait = WebDriverWait(driver, 10)
# full screen
driver.maximize_window()
#connecting to website
driver.get('https://justremote.co/')

time.sleep(2)
#closing banner
cl = driver.find_element(By.CSS_SELECTOR, 'div[class="emailForm__CloseForm-sc-107egjk-1 bhyCUo"]')
time.sleep(2)
ActionChains(driver).move_to_element(cl).perform()
time.sleep(2)
cl.click()
# choosing remotejobs
rj = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div/div[1]/div/a')
time.sleep(1)
rj.click()
time.sleep(2)
#choosing customer service
cs = driver.find_element(By.LINK_TEXT, 'Customer Service')
cs.click()
time.sleep(1)
# element containing all the customer service jobs 
aj = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div/div[2]')))
# getting html of the element containing all the jobs 
html_page = aj.get_attribute('outerHTML')

""" store html file to pc, open another py file and scrape from file what ever you want"""
#with open('jrem.html', 'w') as f:
#    f.write(str(html_page))
#f.close
# below opens the file from the local storage
#html_page1 = open('jrem.html','r')
#encoding='utf8'


#ending selenium session
driver.close()

#setting the bs4 
soup = BeautifulSoup(html_page, 'lxml')
# makes html more readable
soup.prettify()
# element containing all the job data
jobs = soup.find_all('div', class_="new-job-item__JobInnerWrapper-sc-1qa4r36-12 doExVb")
# list to store job related data title, company...
jl = []
# loop gets the text and appends to jl list 
for x in jobs:
    company = x.find('div', class_="new-job-item__JobItemCompany-sc-1qa4r36-4 jNtqCf").text
    jl.append(f'company: {company}\n')
    job = x.find('h3', class_="new-job-item__JobTitle-sc-1qa4r36-8 iNuReR").text
    jl.append(f'job title: {job}\n')
    jtype = x.find('div', class_="new-job-item__JobItemDate-sc-1qa4r36-5 dmIPAp").text
    jl.append(f'work type: {jtype}\n')
    pdate = x.find('div', class_="new-job-item__Tag-sc-1qa4r36-10 bYagUV").text
    jl.append(f'published: {pdate}\n')
    base_url = 'https://justremote.co/'
    subdomain  = x.find('a', class_="new-job-item__JobMeta-sc-1qa4r36-7 eFiLvL")['href']
    info = (base_url +subdomain)
    jl.append(f'more info: {info}\n\n')

# stores to file
file = open('justremotejobs.txt', 'w')
for x in jl:
        file.writelines(x)
file.close

#ready