import time

from pyvirtualdisplay import Display
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

def parse_html():
    display = Display(visible=0, size=(800, 600))
    display.start()


    options = FirefoxOptions()
    options.add_argument("--headless")
    browser = Firefox(service=FirefoxService(executable_path="/usr/bin/geckodriver"), options=options)

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
    display.stop()
    print("Браузер закрыт")
    print("-" * 50)
    return html

