import time
import os
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
		options = webdriver.ChromeOptions()
		prefs = {"download.default_directory" : os.getcwd()+"/downloads"}
		options.add_experimental_option("prefs",prefs)
		# options.add_argument("--no-sandbox")
		# options.add_argument('--headless')
		# options.add_argument("--disable-dev-shm-usage")
		driver = webdriver.Chrome(service=ChromeService( 
			ChromeDriverManager().install()), options=options) 
		
		driver.get(url) 
		driver.implicitly_wait(200)

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

		title = driver.find_element(By.XPATH, '//*[@id="Main_C001_Col00"]/div/div/div/div[2]/div/h1')
		print(title.text)

		driver.implicitly_wait(10)
		# download_button = driver.find_element(By.ID, "buttonId")
		download_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "buttonId")))
		# download_button.click()
		#WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#divmpscreen2 > div.row > div:nth-child(1) > div > div:nth-child(1) > input"))).send_keys('COS')
		#Select(WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//label[text()='By Parliament']//following-sibling::select[1]")))).select_by_value('13: 13')
		driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="buttonId"]'))))

		time.sleep(5)

		driver.quit()
		returnJSON = parser.parse(date=date)
		print(returnJSON)
		return returnJSON

	except Exception as e:
		print(e)
		returnJSON["error"] = "Error in scraping the data"
		returnJSON["success"] = False
		print(returnJSON)
		return returnJSON



if __name__ == "__main__":
	scrape("2023-12-14")