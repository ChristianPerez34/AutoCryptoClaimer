import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class CryptoClaimer:
    def __init__(self):
        self.crypto_faucets = {}
        self.driver = None

    def start_collecting_crypto(self):
        self.driver = webdriver.Chrome()
        for url in self.crypto_faucets:
            self.driver.get(url)
            self.login(url=url,)
            self.claim_faucet(url=url)
        self.driver.quit()

    def collect_crypto_faucets(self, crypto_faucets: str):
        with open(crypto_faucets, "r") as file:
            lines = file.readlines()
            for line in lines:
                url, user, password = line.split(";")
                self.crypto_faucets.update({url: {"user": user, "password": password}})

    def claim_faucet(self, url: str):
        if url == "https://free-litecoin.net":
            WebDriverWait(self.driver, 5).until(
                expected_conditions.presence_of_element_located(
                    (By.LINK_TEXT, "LITECOIN FAUCET")
                )
            ).click()
            # faucet_button = self.driver.find_element_by_link_text("LITECOIN FAUCET")
            # faucet_button.click()

            element = self.driver.find_elements_by_class_name("warning")
            if not element or (element and not element[0].is_displayed()):
                claim_cryto = self.driver.find_element_by_xpath(
                    "/html/body/section/div/div/div/div/div/center/input"
                )
                claim_cryto.click()
        elif url in (
            "https://freebinancecoin.com",
            "https://freenem.com",
            "https://freecardano.com",
            "https://coinfaucet.io",
            "https://freebitcoin.io",
            "https://freetether.com",
            "https://freeusdcoin.com",
            "https://freeethereum.com",
            "https://free-tron.com",
        ):
            try:
                WebDriverWait(self.driver, 5).until(
                    expected_conditions.element_to_be_clickable(
                        (By.CLASS_NAME, "roll-button")
                    )
                ).click()
                time.sleep(3)
            except TimeoutException:
                print("Already claimed!")

    def login(self, url: str):
        user = (self.crypto_faucets[url]["user"],)
        password = self.crypto_faucets[url]["password"]

        if url == "https://free-litecoin.net":

            login_button = self.driver.find_element_by_link_text("LOGIN")
            login_button.click()

            user_field = self.driver.find_element_by_name("user")
            user_field.send_keys(user)

            password_field = self.driver.find_element_by_name("pass")
            password_field.send_keys(password)

            # submit_login_button = self.driver.find_element_by_class_name("main-btn")
            # submit_login_button.submit()
        elif url in (
            "https://freebinancecoin.com",
            "https://freenem.com",
            "https://freecardano.com",
            "https://coinfaucet.io",
            "https://freebitcoin.io",
            "https://freetether.com",
            "https://freeusdcoin.com",
            "https://freeethereum.com",
            "https://free-tron.com",
        ):

            user_field = self.driver.find_element_by_name("email")
            user_field.send_keys(user)

            password_field = self.driver.find_element_by_name("password")
            password_field.send_keys(password)

            submit_login_button = self.driver.find_element_by_class_name("login")
            time.sleep(1)
            # self.driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
            submit_login_button.click()

            print(self.driver.current_url)
            WebDriverWait(self.driver, 5).until(
                lambda driver: driver.current_url != f"{url}/"
            )
