from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

chrome_options = Options()
chrome_options.add_argument("--window-size=2252,1341")

LOGIN = '//*[@id="root"]/div[1]/div[1]/div[1]/div/span/button'
EMAIL = '/html/body/div[1]/div[1]/div[1]/div/div/div[2]/div/form/div[1]/div[1]/input'
PASSWORD = '//*[@id="modal-container"]/div/div/div[2]/div/form/div[1]/div[2]/input'
LOGIN_BUTTON = '//*[@id="login"]'
BUY = '//*[@id="buy"]'
BUY_SIZE = '//*[@id="modal-container"]/div/div/div[5]/div[3]/input'
BUY_CLICK = '//*[@id="firstButton"]'
BUY_CONFIRM = '/html/body/div[1]/div[1]/div[1]/div/div/div[7]/button[1]'
SELL = '/html/body/div[1]/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/div/div[2]/div/button[1]'
SELL_SIZE = '//*[@id="modal-container"]/div/div/div[5]/div[3]/input'
SELL_ORDER_CLICK = '//*[@id="secondButton"]'
RESERVE_PRICE_CLICK = '//*[@id="secondButton"]'
REDUCE_PRICE = '/html/body/div[1]/div[1]/div[1]/div/div/div[5]/div[2]/button[1]'
CONFIRM_RESERVE_PRICE = '/html/body/div[1]/div[1]/div[1]/div/div/div[6]/button[1]'

url = 'https://www.footballindex.co.uk'


class Player(object):
    def __init__(self, first, last) -> None:
        self.first = first
        self.last = last

    @property
    def __str__(self):
        return f'{self.first} {self.last}'


class FootballIndexBot:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(f'{url}/top-200')
        self.wait = WebDriverWait(driver=self.driver, timeout=120)

    def login(self, email: str, password: str) -> None:
        attempt = 1
        while True:
            try:
                self.driver.find_element_by_xpath(xpath=LOGIN).click()
                self.driver.find_element_by_xpath(xpath=EMAIL).send_keys(email)
                self.driver.find_element_by_xpath(xpath=PASSWORD).send_keys(password)
                self.driver.find_element_by_xpath(xpath=LOGIN_BUTTON).click()
                break
            except NoSuchElementException as e:
                if attempt > 20:
                    raise e
                attempt += 1

    def search(self, player: Player) -> None:
        self.driver.get(f'{url}/search?q={player.first}+{player.last}')

    def buy(self, player: Player, shares: int = 1) -> None:
        self.search(player=player)
        attempt = 1
        while True:
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, BUY))).click()
                break
            except StaleElementReferenceException as e:
                if attempt > 20:
                    raise e
                attempt += 1
        shares_input = self.driver.find_element_by_xpath(xpath=BUY_SIZE)
        while shares_input.get_attribute('value') != '0':
            shares_input.send_keys(Keys.BACKSPACE)
        shares_input.send_keys(shares)
        self.driver.find_element_by_xpath(xpath=BUY_CLICK).click()
        self.driver.find_element_by_xpath(xpath=BUY_CONFIRM).click()

    def sell(self, player: Player, shares: int = 1) -> None:
        self.search(player=player)
        attempt = 1
        while True:
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, SELL))).click()
                break
            except StaleElementReferenceException as e:
                if attempt > 20:
                    raise e
                attempt += 1
        shares_input = self.driver.find_element_by_xpath(xpath=SELL_SIZE)
        while shares_input.get_attribute('value') != '0':
            shares_input.send_keys(Keys.BACKSPACE)
        shares_input.send_keys(shares)
        self.driver.find_element_by_xpath(xpath=SELL_ORDER_CLICK).click()
        self.driver.find_element_by_xpath(xpath=RESERVE_PRICE_CLICK).click()
        self.driver.find_element_by_xpath(xpath=REDUCE_PRICE).click()
        self.driver.find_element_by_xpath(xpath=CONFIRM_RESERVE_PRICE).click()


if __name__ == '__main__':
    bot = FootballIndexBot()
    bot.login(email='example@gmail.com', password='password') #insert details
    player = Player('Kalidou', 'Koulibaly')
    bot.sell(player=player)
