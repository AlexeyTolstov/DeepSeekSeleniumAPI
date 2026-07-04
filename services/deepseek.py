from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from dotenv import load_dotenv

import os
from selenium import webdriver
from pathlib import Path

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

EMAIL = os.getenv('EMAIL_DEEPSEEK', '')
PASSWORD = os.getenv('PASSWORD_DEEPSEEK', '')



class DeepseekParser:
    def __init__(self):
        
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = "/usr/bin/chromium"
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-gpu")
        
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--start-maximized")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)


        self.service = Service("/usr/bin/chromedriver")

        self.driver = webdriver.Chrome(service=self.service, options=self.options)

        self.wait = WebDriverWait(self.driver, 25)

        # self.driver.get("https://google.com")
        self.login()

        # sleep(2)
        

    def login(self):
        self.driver.get("https://chat.deepseek.com/")
        sleep(3)
        sleep(5)
        email_box = self.wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//input[@placeholder='Phone number / email address']"
            ))
        )

        password_box = self.wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//input[@placeholder='Password']"
            ))
        )

        email_box.click()
        email_box.clear()
        email_box.send_keys(EMAIL)

        password_box.click()
        password_box.clear()
        password_box.send_keys(PASSWORD)

        sleep(0.5)

        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[text()='Log in']")
            )
        ).click()
        sleep(1)
    
    def send(self, query: str):
        field_DSeek = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@placeholder='Message DeepSeek']")
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

        sleep(7)

        while True:
            text_answer_blocks = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.ds-markdown.ds-assistant-message-main-content")
                )
            )

            text = text_answer_blocks[-1].text
            
            if (text == last_text):
                break

            last_text = text
            sleep(1)


        text = last_text
        isD = False

        # for line in last_text.split('\n'):
        #     l = line
        #     if line.strip() == '':
        #         text += "\n"
        #     elif not l.isdigit():
        #         if not isD:
        #             text += "\n"
        #         isD = False
        #         text += line
        #     else:
        #         isD = True
            
        
        return text

deepseek = DeepseekParser()


# if __name__ == "__main__":

    # xvfb-run -a python utils/deepseek.py
    # r = deepseek.send("Тебе нужно дать ответ в формате json. ТОЛЬКО JSON. Он должен быть вида {'score': случайное число, можно даже дробное от 0 до 10}")

    # print(r)