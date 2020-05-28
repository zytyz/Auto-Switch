from selenium import webdriver
import time
# Using Chrome to access web
driver = webdriver.Chrome('./chromedriver')
# Open the website
driver.get("chrome://downloads/")

if __name__ == '__main__':
	time.sleep(1)
	current_time = time.time()
	print(current_time)
	driver.get('http://172.20.10.2')
	print(current_time)
	time.sleep(1)
	driver.find_element_by_name('First_Button').click()

print("yeah")