from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome('chromedriver')
driver.get('https://www.python.org')

search_bar = driver.find_element(By.ID, 'top')
print(search_bar)

driver.close()
