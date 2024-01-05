from asyncio.windows_events import NULL
import undetected_chromedriver as uc
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

location = input("Please Enter Location of Desired Job: ")
title = input("Please Enter Desired Job: ")

path = "C:\Program Files (x86)\chromedriver.exe"
driver = uc.Chrome()
driver.get('https://www.indeed.com/jobs')
print(driver.title)

locationInput = driver.find_element(By.NAME, 'l')
titleInput = driver.find_element(By.NAME, 'q')

titleInput.send_keys(title)
for x in range(3):
    locationInput.send_keys(Keys.CONTROL, Keys.BACKSPACE)
locationInput.send_keys(location,Keys.ENTER)

job_list = []
 
#sidebar = driver.find_element(By.CSS_SELECTOR, '#jobsearch-JapanPage > div > div > div.jobsearch-SerpMainContent > div.jobsearch-LeftPane > nav > div:nth-child('+ str(x) +') > a')
#sidebar.click()

def collectJobs(): 
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jobsearch-ResultsList"))
    )
    
    #print(main.text) 
    #print only text elements of main

    articles = main.find_elements(By.TAG_NAME, "li")
    i = 0
   
    for article in articles:
        try: 
            jobTitle = article.find_element(By.CLASS_NAME, 'jobTitle').text
            link = article.find_element(By.TAG_NAME, 'a').get_attribute('href')
            companyName = article.find_element(By.CLASS_NAME, 'companyName').text
            description = article.find_element(By.TAG_NAME, 'li').text
            jobItem = {
                'Position': jobTitle,
                'Company': companyName,
                'Description': description,
                'Link': link
            }
            job_list.append(jobItem)
        except:
            i = i +1
    data = pd.DataFrame(job_list)
    print(data)
    data.to_excel(r"C:\Users\Mbywn\Documents\indeedBookData.xlsx",index = False)
def nextPage():
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-13p07ha'))
    )
    try:
        main = main[1]
        main.click()
    except:
        driver.quit()


collectJobs()
main = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-13p07ha')))
main.click()
boolean = True
while boolean:
    try:
        collectJobs()
        nextPage() 
    except:
        boolean = False
        driver.quit()
        break

#linksList = pd.read_excel(r"C:\Users\Mbywn\Documents\indeedBookData.xlsx")['Link'].tolist()
#in Selenium the page sometimes cannot load in time for the next instruction
#the try and quit instruction ensures that the next page is pulled up in time


#in Selenium the page sometimes cannot load in time for the next instructio
#the try and quit instruction ensures that the next page is pulled up in time



#print(driver.page_source)
#scrapes and accesses the entire source code from the page 

#ActionChains(driver) is able to perform actions inside of the program and create a bot 
#all actions before .perform()

time.sleep(10)
driver.quit()
