
# Selenium imports
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Aditional imports
from urllib.parse import quote
# from src.database import Database
from datetime import datetime, timedelta


class KatzupBot:
    driver: Chrome = None
    options: ChromeOptions = None
    # _database: Database = None

    def __init__(self):
        self.__options_config()

    def __generate_wait(self, timeout:float=5) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout)

    def __options_config(self):
        self.options = ChromeOptions()
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--mute-audio")
        self.options.add_argument("--kiosk")
        self.options.add_argument("user-data-dir=./session")
        self.options.add_argument("--no-sandbox")


    def __init_webdriver(self):
        self.driver = Chrome(
            service = ChromeService(
                ChromeDriverManager().install()
            ),
            options = self.options
        )

        self.driver.get("https://web.whatsapp.com")
        wait = self.__generate_wait(60)

        try:
            wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'span[data-icon="lock-small"]')
                )
            )
        except TimeoutException as e:
            print(e)
            print("[ERROR] Tiempo de espera excedido.")
            self.quit()

    def run(self):
        print("[INFO] Iniciando WebDriver.")
        self.__init_webdriver()
        

if __name__=="__main__":
    KatzupBot().run()