import time
import os

# .env
from dotenv import load_dotenv

# Main library
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# WebDrive Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

browser_type = os.getenv("BROWSER")

if browser_type == "S":
    browser = webdriver.Safari()
elif browser_type == "C":
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

browser.maximize_window()
browser.get("https://events.myrosmol.ru")
print("Браузер открыт")

time.sleep(2)
browser.execute_script("window.scrollTo(0, 700)")
time.sleep(2)
open_registration = browser.find_element(
    By.XPATH, '//*[@id="i-9-bitrix-catalog-smart-filter-horizontal-1m-KZ7kpsh6etqY"]/div/div/div/div/form/div[3]/div[1]/div/div[3]/div[2]/div/div[1]/div/label').click()
print("Фильтр применён")
time.sleep(2)

try:
    while True:
        time.sleep(1.5)
        button = browser.find_element(
            By.XPATH, '//*[@id="i-11-bitrix-catalog-section-catalog-tile-3rm-OQ3k9PHlVICg"]/div[2]/div/div')
        browser.execute_script("arguments[0].scrollIntoView();", button)
        time.sleep(1.5)
        button.click()
except NoSuchElementException:
    pass

print("Все старнички открыты")
html = browser.page_source
print("HTML Сохранён")
time.sleep(5)
browser.close()
print("Браузер закрыт")
print("-" * 100)
