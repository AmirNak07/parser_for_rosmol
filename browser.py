import time

# Main library
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# WebDrive Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# WebDrive Chrome for Server
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.core.os_manager import ChromeType

from config import BROWSER_TYPE


def choose_browser(browser_type):
    if browser_type == "S":
        browser = webdriver.Safari()
        browser.maximize_window()
    elif browser_type == "C":
        browser = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()))
        browser.maximize_window()
    elif browser_type == "C-Server":
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome(service=ChromiumService(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)
    return browser


def parsing_html(browser):
    browser.get("https://events.myrosmol.ru")
    print("Браузер открыт")

    time.sleep(2)
    browser.execute_script("window.scrollTo(0, 700)")
    time.sleep(2)
    browser.find_element(
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
    print("-" * 50)
    return html


def run_parsing():
    return parsing_html(choose_browser(BROWSER_TYPE))
