
# SELENIUM:
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

# fake-Agent:
from fake_useragent import UserAgent

#UTILS
import Utils.config as c

class MyWebdriver:

    def __init__(self, url):
        self.driver = None
        self.url=url

    def initialize_driver(url):
        """Initializes chromedriver to the given website needed for further scraping.
        :param website: website to get links from
        :return: ready to scrape driver
        """
        # open driver
        chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
        # and if it doesn't exist, download it automatically,
        # then add chromedriver to path
        #options.headless = True
        options = webdriver.ChromeOptions()
        ua = UserAgent()
        user_agent = ua.random
        print(user_agent)
        options.add_argument(f'user-agent={user_agent}')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
        driver.get(url)
        # wait for page to load
        driver.implicitly_wait(c.DELAY)
        print(f"Successfully loaded {url}")
        return driver

    def close_driver(self):
        self.driver.quit()
        print("Driver quit")