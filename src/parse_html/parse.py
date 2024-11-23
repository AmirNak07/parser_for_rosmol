from loguru import logger
from pyvirtualdisplay import Display
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService


@logger.catch
def parse_html():
    display = Display(visible=0, size=(800, 600))
    display.start()

    options = FirefoxOptions()
    options.add_argument("--headless")
    browser = Firefox(service=FirefoxService(executable_path="/usr/bin/geckodriver"), options=options)

    browser.get("https://events.myrosmol.ru")
    logger.debug("Браузер открыт")

    browser.implicitly_wait(2)

    browser.execute_script("window.scrollTo(0, 700)")
    browser.implicitly_wait(2)
    browser.find_element(
        By.XPATH, '//*[@id="i-9-bitrix-catalog-smart-filter-horizontal-1m-KZ7kpsh6etqY"]/div/div/div/div/form/div[3]/div[1]/div/div[3]/div[2]/div/div[1]/div/label').click()
    logger.debug("Фильтр применён")
    browser.implicitly_wait(2)

    try:
        while True:
            browser.implicitly_wait(1.5)
            button = browser.find_element(
                By.XPATH, '//*[@id="i-11-bitrix-catalog-section-catalog-tile-3rm-OQ3k9PHlVICg"]/div[2]/div/div')
            browser.execute_script("arguments[0].scrollIntoView();", button)
            browser.implicitly_wait(1.5)
            button.click()
    except NoSuchElementException:
        pass

    logger.debug("Все старнички открыты")
    html = browser.page_source
    logger.debug("HTML Сохранён")
    browser.close()
    display.stop()
    logger.debug("Браузер закрыт")
    return html
