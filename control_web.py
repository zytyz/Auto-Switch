from selenium import webdriver
import time

button_name_dict = {1:'First_Button', 2:'Second_Button', 3:'Third_Button'}

def connect_to_page(url='http://172.20.10.2'):
	# Using Chrome to access web
	driver = webdriver.Chrome('./chromedriver')
	# Open the website
	driver.get("chrome://downloads/")
	time.sleep(1)
	current_time = time.time()
	print(current_time)
	driver.get('http://172.20.10.2')
	print(current_time)
	time.sleep(1)
	return driver

def button_click(driver, button_idx):
	global button_name_dict
	driver.find_element_by_name(button_name_dict[button_idx]).click()
	time.sleep(1)
	return driver

if __name__ == '__main__':
	driver = connect_to_page()
	driver = button_click(driver, 1)
	driver = button_click(driver, 1)

print("yeah")