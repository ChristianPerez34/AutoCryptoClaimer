import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class CryptoClaimer:
    def __init__(self):
        self.crypto_faucets = {}
        self.browser = None

    def start_driver(self, driver):

        if driver.lower() == "firefox":
            browser = webdriver.Firefox
            driver_options = FirefoxOptions()
        else:
            browser = webdriver.Chrome
            driver_options = ChromeOptions()

        driver_options.add_argument("--headless")
        driver_options.add_argument("window-size=1920,1080")
        driver_options.add_argument("--log-level=3")
        self.browser = browser(options=driver_options, service_log_path="NUL")

    def start_collecting_crypto(self):
        self.browser.maximize_window()

        for url in self.crypto_faucets:
            print(f"Visiting {url}")
            self.browser.get(url)
            self.login(url=url)
            self.claim_faucet(url=url)
            self.check_balance(url=url)
        self.browser.quit()

    def collect_crypto_faucets(self, crypto_faucets: str):
        print("Collecting crypto faucets...")
        with open(crypto_faucets, "r") as file:
            lines = file.readlines()
            for line in lines:
                url, user, password = line.split(";")
                self.crypto_faucets.update(
                    {url: {"user": user, "password": password}})

    def claim_faucet(self, url: str):
        success_message = "Already claimed..."
        print(f"Claiming crypto...")
        if url == "https://free-litecoin.net":
            WebDriverWait(self.browser, 5).until(
                expected_conditions.presence_of_element_located(
                    (By.LINK_TEXT, "LITECOIN FAUCET")
                )
            ).click()
            # faucet_button = self.driver.find_element_by_link_text("LITECOIN FAUCET")
            # faucet_button.click()

            element = self.browser.find_elements_by_class_name("warning")
            if not element or (element and not element[0].is_displayed()):
                claim_cryto = self.browser.find_element_by_xpath(
                    "/html/body/section/div/div/div/div/div/center/input"
                )
                claim_cryto.click()

                success_message = self.browser.find_element_by_class_name(
                    "success").text
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
                WebDriverWait(self.browser, 5).until(
                    expected_conditions.element_to_be_clickable(
                        (By.CLASS_NAME, "roll-button")
                    )
                ).click()
                success_message = (
                    WebDriverWait(self.browser, 5)
                    .until(
                        expected_conditions.visibility_of_element_located(
                            (By.CLASS_NAME, "result")
                        )
                    )
                    .text
                )
            except TimeoutException:
                pass
        print(success_message)

    def login(self, url: str):
        user = self.crypto_faucets[url]["user"]
        password = self.crypto_faucets[url]["password"]
        print(f"Logging in...")

        if url == "https://free-litecoin.net":

            login_button = self.browser.find_element_by_link_text("LOGIN")
            login_button.click()

            user_field = self.browser.find_element_by_name("user")
            user_field.send_keys(user)

            password_field = self.browser.find_element_by_name("pass")
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

            user_field = self.browser.find_element_by_name("email")
            user_field.send_keys(user)

            password_field = self.browser.find_element_by_name("password")
            password_field.send_keys(password)

            submit_login_button = self.browser.find_element_by_class_name(
                "login")
            time.sleep(1)
            submit_login_button.click()

            WebDriverWait(self.browser, 5).until(
                lambda driver: driver.current_url != f"{url}/"
            )

    def check_balance(self, url: str):
        balance = ""

        if url == "https://free-litecoin.net":
            account_button = self.browser.find_element_by_link_text("ACCOUNT")
            account_button.click()
            balance = f'{self.browser.find_element_by_xpath("/html/body/section/div/div/div/div/div/div[2]/div[1]/div/div[1]/a").text} LTC'
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
            balance = (
                self.browser.find_element_by_class_name("navbar-coins")
                .find_element_by_tag_name("a")
                .text
            )

        print(f"Current balance: {balance}\n")
