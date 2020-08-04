from selenium import webdriver


class CryptoClaimer:
    def __init__(self):
        self.crypto_faucets = {}
        self.driver = None

    def start_browser(self):
        self.driver = webdriver.Chrome()
        for url in self.crypto_faucets.keys():
            self.driver.get(url)
            self.login(
                user=self.crypto_faucets[url]["user"],
                password=self.crypto_faucets[url]["password"],
            )
            self.claim_faucet()

    def collect_crypto_faucets(self, crypto_faucets: str):
        with open(crypto_faucets, "r") as file:
            lines = file.readlines()
            for line in lines:
                url, user, password = line.split(";")
                self.crypto_faucets.update({url: {"user": user, "password": password}})

    def claim_faucet(self):
        pass

    def login(self, user: str, password: str):
        login_button = self.driver.find_element_by_link_text("LOGIN")
        login_button.click()

        user_field = self.driver.find_element_by_name("user")
        user_field.send_keys(user)

        password_field = self.driver.find_element_by_name("pass")
        password_field.send_keys(password)

        submit_login_button = self.driver.find_element_by_class_name("main-btn")
        submit_login_button.submit()
