import random
import time
import os
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import parser
#2023-01-21


def dateParser(date):
	date_list = date.split("-")
	parsed_date = ""
	parsed_date+=date_list[2]
	parsed_date+=date_list[1]
	parsed_date+=date_list[0]
	return parsed_date


def scrape(date):
	parsed_date = dateParser(date)
	url = 'https://www.mcb.mu/en/personal/download-daily-rates' 
	returnJSON = {}

	try:
		#####OLD####
		options = webdriver.ChromeOptions()
		prefs = {"download.default_directory" : os.getcwd()+"/downloads"}
		options.add_experimental_option("prefs",prefs)
		# # options.add_argument('--no-sandbox')
		# #options.add_argument('--headless')
		# # options.add_argument("--disable-setuid-sandbox")
        # # # other options
		# # options.add_argument("--disable-extensions")
		# options.add_argument("--disable-gpu")
		# options.add_argument('--ignore-certificate-errors')
		# driver = webdriver.Chrome(service=ChromeService( 
		# 	ChromeDriverManager().install()), options=options) 
		
		# driver.get(url) 
		# driver.implicitly_wait(2)
		####OLD####


		####NEW###
		# options = webdriver.ChromeOptions()
		# options.add_argument('--no-sandbox')
		# options.add_argument('--headless')
		# options.add_argument('--ignore-certificate-errors')
		# options.add_argument('--disable-dev-shm-usage')
		# options.add_argument('--disable-extensions')
		# options.add_argument('--disable-gpu')
		# options.add_argument('--user-agent={}'.format(random.choice(list(self.user_agents))))

		driver = webdriver.Chrome(options=options)
		driver.set_page_load_timeout(90)

		# Load the URL and get the page source
		driver.implicitly_wait(6)
		driver.get(url)
		###NEW###

		currency_selector = driver.find_element(By.ID, "forexCurrency")
		select = Select(currency_selector)
		select.select_by_value("ALL")

		start_date = driver.find_element(By.ID, "forexDateStart")
		driver.implicitly_wait(10)
		start_date.click()
		start_date.send_keys(Keys.LEFT)
		start_date.send_keys(Keys.LEFT)
		start_date.send_keys(Keys.LEFT)
		start_date.send_keys(Keys.LEFT)
		start_date.send_keys(parsed_date)

		end_date = driver.find_element(By.ID, "forexDateEnd")
		driver.implicitly_wait(10)
		end_date.click()
		end_date.send_keys(Keys.LEFT)
		end_date.send_keys(Keys.LEFT)
		end_date.send_keys(Keys.LEFT)
		end_date.send_keys(Keys.LEFT)
		end_date.send_keys(parsed_date)

		driver.implicitly_wait(10)
		download_button = driver.find_element(By.ID, "buttonId")
		download_button.click()

		time.sleep(5)

		driver.quit()
		returnJSON = parser.parse(date=date)
		print(returnJSON)
		return returnJSON

	except:
		returnJSON["error"] = "Error in scraping the data"
		returnJSON["success"] = False
		print(returnJSON)
		return returnJSON



if __name__ == "__main__":
	scrape("2023-12-14")