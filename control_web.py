from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import sys

button_name_dict = {1: 'First_Button', 2: 'Second_Button', 3: 'Third_Button'}


def connect_to_page(url='http://192.168.0.110'):
    # Using Chrome to access web
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome('chromedriver', chrome_options=options)
    # driver = webdriver.Chrome('./chromedriver')
    # Open the website
    driver.set_page_load_timeout(5)
    while True:
        try:
            driver.get(url)
            print('connect successful')
            break
        except TimeoutException as e:
            print('try again')
            pass
    return driver


def button_click(driver, button_idx):
    global button_name_dict
    driver.find_element_by_name(button_name_dict[button_idx]).click()
    # time.sleep(1)
    return driver


if __name__ == '__main__':
    driver = connect_to_page(url=sys.argv[1])
    driver = button_click(driver, 1)
    driver = button_click(driver, 1)
