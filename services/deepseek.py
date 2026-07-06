from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, time
from dotenv import load_dotenv

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import os, platform
from selenium import webdriver
from pathlib import Path
from markdownify import markdownify as md
from models import FieldLocator, field_locators_RU, field_locators_EN


env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

EMAIL = os.getenv('EMAIL_DEEPSEEK', '')
PASSWORD = os.getenv('PASSWORD_DEEPSEEK', '')


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
                options=self.options
            )

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
    
    def create_new_chat(self):
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('j').key_up(Keys.CONTROL).perform()
        sleep(0.3)

    def send(self, query: str):
        field_DSeek = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//textarea[starts-with(@placeholder, '{self.field_locator.msg_deepseek}')]")
            )
        )

        field_DSeek.click()
        field_DSeek.clear()
        self.driver.execute_cdp_cmd(
            "Input.insertText", { "text": query }
        )

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
            
        text = md(last_text)
        return text
    
    def __del__(self):
        self.driver.quit()
        print("Сессия закрыта")

    def close(self):
        self.driver.quit()
        print("Сессия закрыта")


if __name__ == "__main__":
    deepseek = DeepseekParser(field_locator=field_locators_RU)
    q = "Ты чебурашка! Это твоя роль"
    r = deepseek.send(q)
    deepseek.create_new_chat()
    q = "Кто ты?"
    r = deepseek.send(q)