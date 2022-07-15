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

# path to chromedrive
path = Service('C:\webdrivers\chromedriver')
#setting the driver up
driver = webdriver.Chrome(service=path)
# connecting to website
driver.get('https://remotive.com/')
# setting random waits so i don't get detected
time.sleep(1)
# browser full screen
driver.maximize_window()
# random wait
time.sleep(1)
# timer for waiting until element is located
wait = WebDriverWait(driver, 10)
#closing banner that is blocking screen
#cban = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Dismiss Message"]')
cban = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Dismiss Message"]')))
cban.click()
time.sleep(1)
# finding and clicking category in the search bar
cate = driver.find_element(By.XPATH, '//*[@id="categories"]/div/select')
ActionChains(driver).move_to_element(cate).perform()
cate.click()
time.sleep(1)
#choosing customer support from the category
cate1 = driver.find_element(By.XPATH, '//*[@id="categories"]/div/select/option[5]/span')
cate.send_keys('c', Keys.ENTER)
time.sleep(1)

# element for location box
loc2 = driver.find_element(By.XPATH, '//*[@id="location-filter"]/div/ul/li[1]/div/label/span/img')
# clicking location box
ActionChains(driver).move_to_element(loc2).click().perform()
time.sleep(1)

# clicks element that sort jobs by relevance/date
sort = driver.find_element(By.CSS_SELECTOR, "div[class='ais-SortBy tw-py-4 tw-px-3']")
ActionChains(driver).move_to_element(sort).click().perform()
time.sleep(1)
#choosing sort by date
sort1 = driver.find_element(By.CSS_SELECTOR, 'select.ais-SortBy-select')
sort1.send_keys(Keys.ARROW_DOWN, Keys.ENTER)

time.sleep(1)

# selecting unordered list containing jobs and setting waiting until its present
# when searching list element use find_elements by xpath
ulist = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="hits"]/ul')))

# getting html for bs4
page = ulist.get_attribute('outerHTML')
#ending selenium session
driver.close()


# setting bs4 for scraping the data from html
soup = BeautifulSoup(page, "lxml")



# variable for the element containing the jobs, all customer service jobs are in this element 
jobs = soup.find_all('div', class_="job-tile remotive-bg-light")
# list for storing the jobs
jl = []
# for loop to locate data from the jobs element
for x in jobs:
    # job title as string
    title = x.find('div', class_="job-tile-title").span.text
    # adding to list also '\n' is necessary so the file won't have just one line of text
    jl.append(title + '\n')
    # company names as string
    company = x.find('div', class_="job-tile-title").find('span', class_="tw-block md:tw-hidden").text
    # adding to list also '\n' is necessary so the file won't have just one line of text
    jl.append(company + '\n')
    # links to jobs dont need .text at the end as it's already string
    info = x.find('div', class_="job-tile-title").a['href']
    # adding to list also '\n' is necessary so the file won't have just one line of text
    jl.append(info + '\n')
    # date published as string
    publ = x.find('div', class_="tw-hidden sm:tw-flex tw-items-center tw-justify-between tw-w-auto").span.span.text
    # adding to list also '\n' is necessary so the file won't have just one line of text
    jl.append(publ + '\n\n')    
#storing to file
file = open('jobs.txt','w')
for items in jl:
    file.writelines(items)
file.close()