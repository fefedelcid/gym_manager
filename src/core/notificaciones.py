
# Selenium imports
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Aditional imports
import os, time
from urllib.parse import quote
# from src.database import Database
# from src.config import SESSION_DIR
from datetime import datetime, timedelta

SESSION_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "session")
if not os.path.exists(SESSION_DIR):
    os.mkdir(SESSION_DIR)

class KatzupBot:
    driver: Chrome = None
    options: ChromeOptions = None
    sender: str = ""
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
        # self.options.add_argument("--kiosk")
        self.options.add_argument(f"user-data-dir={SESSION_DIR}")
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
            # wait.until(
            #     EC.visibility_of_element_located(
            #         (By.CSS_SELECTOR, 'span[data-icon="lock-small"]')
            #     )
            # )
            time.sleep(60)
        except TimeoutException as e:
            print(e)
            print("[ERROR] Tiempo de espera excedido.")
        finally:
            self.quit()
        
    def __get_chat_input(self):
        wait = self.__generate_wait(20)
        chat = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div[aria-placeholder="Escribe un mensaje"]')
            )
        )
        return chat

    def __select_my_chat__(self):
        wait = self.__generate_wait(20)
        cuadro_buscar = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div[aria-label="Buscar"]')
            )
        )
        cuadro_buscar.click()
        cuadro_buscar.send_keys(self.sender+"\n")

    
    def run(self):
        print("[INFO] Iniciando WebDriver.")
        self.__init_webdriver()

    def quit(self):
        self.driver.quit()
        

if __name__=="__main__":
    KatzupBot().run()