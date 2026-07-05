from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, time
from dotenv import load_dotenv

from webdriver_manager.chrome import ChromeDriverManager

import os, platform
from selenium import webdriver
from pathlib import Path
import html2text


converter = html2text.HTML2Text()
converter.ignore_links = False

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

EMAIL = os.getenv('EMAIL_DEEPSEEK', '')
PASSWORD = os.getenv('PASSWORD_DEEPSEEK', '')


class FieldLocator:
    """ Хранит локализованные ключевые слова для поиска полей ввода на веб-странице. """

    def __init__(self, lang: str, phone_email: str, password: str, log_in: str, msg_deepseek: str):
        self.lang = lang
        self.phone_email = phone_email
        self.password = password
        self.log_in = log_in
        self.msg_deepseek = msg_deepseek


field_locators_RU = FieldLocator(
    lang="ru",
    phone_email="Номер телефона / адрес электронной почты",
    password="Пароль",
    log_in="Войти",
    msg_deepseek="Сообщение для "
)

field_locators_EN = FieldLocator(
    lang="en",
    phone_email="Phone number / email address",
    password="Password",
    log_in="Log in",
    msg_deepseek="Message "
)

CHROME_DRIVER_VERSION = "149.0.7827.0"


class DeepseekParser:
    def __init__(self, field_locator: FieldLocator = field_locators_EN):
        self.field_locator = field_locator
        self.options = webdriver.ChromeOptions()
        
        
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-gpu")
        
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--start-maximized")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)

        if platform.system() != "Windows":
            self.options.binary_location = "/usr/bin/chromium"
            self.driver = webdriver.Chrome(
                service=Service("/usr/bin/chromedriver"),
                options=self.options
            )
        else:
            self.driver = webdriver.Chrome(
                # service=Service(ChromeDriverManager(driver_version=CHROME_DRIVER_VERSION).install()),
                options=self.options
            )

            print("fads")
        self.wait = WebDriverWait(self.driver, 25)

        self.login()
        

    def login(self):
        self.driver.get("https://chat.deepseek.com/")
        sleep(1)

        email_box = self.wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//input[@placeholder='{self.field_locator.phone_email}']"
            ))
        )

        password_box = self.wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//input[@placeholder='{self.field_locator.password}']"
            ))
        )

        email_box.click()
        email_box.clear()
        email_box.send_keys(EMAIL)

        password_box.click()
        password_box.clear()
        password_box.send_keys(PASSWORD)

        sleep(0.3)

        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//span[text()='{self.field_locator.log_in}']")
            )
        ).click()
        sleep(1)
    
    def send(self, query: str):
        field_DSeek = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//textarea[starts-with(@placeholder, '{self.field_locator.msg_deepseek}')]")
            )
        )

        field_DSeek.click()
        field_DSeek.clear()
        field_DSeek.send_keys(query)

        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.ds-button.ds-button--primary.ds-button--filled")
            )
        ).click()

        last_text = "..."

        sleep(3)

        while True:
            text_answer_blocks = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.ds-markdown.ds-assistant-message-main-content")
                )
            )

            text = text_answer_blocks[-1].get_attribute("innerHTML")
            
            if (text == last_text):
                break

            last_text = text
            sleep(1)
        print(self.driver.current_url)
        text = converter.handle(last_text)
        
        return text



deepseek = DeepseekParser(field_locator=field_locators_RU)

if __name__ == "__main__":
    q = "Расскажи анекдот"
    r = deepseek.send(q)

    print(r)