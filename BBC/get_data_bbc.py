# SELENIUM:
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# UTILS:
import time
import pandas as pd
from tqdm import tqdm
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
import requests
import Utils.config as c
import logging

# BS4:
from bs4 import BeautifulSoup


class get_data_bbc:

    def __init__(self, driver):
        self.df = self.getDf()
        self.driver = driver
        self.list_of_articles = self.get_data()

    def get_data(self):
        """Finds all links current driver website"""
        results = []
        stored_links = []

        logging.info("Getting all links from homepage")
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[class="block-link__overlay-link"]')))
        self.driver.implicitly_wait(c.DELAY)
        links = self.driver.find_elements(By.CSS_SELECTOR, 'a[class="block-link__overlay-link"]')
        for link in tqdm(links):
            stored_links.append(
                {"link.text": link.text, "link.href": link.get_attribute("href")}
            )

        print("Getting title and description from all stored links")
        itr = 0
        for link in tqdm(stored_links):


            print("scraping: ", link["link.href"])
            if link["link.href"] in self.df.values:
                print("link already exists")
                break
            try:
                self.driver.get(link["link.href"])
                # wait for page to load
                time.sleep(c.DELAY)

                description = self.get_article_text(link)




            except (NoSuchElementException, TimeoutException):

                description = "na"
                logging.error(
                    f"Could not find title and description from link={link['link.href']}"
                )

            results.append(
                {
                    "page_url": link["link.href"],
                    "title": link["link.text"],
                    "text": description,
                }
            )

        self.df = self.df.T.append(results, ignore_index=True)
        print(f"Found {len(links)} number of links")

        return results

    def get_article_text(self, link):
        page = requests.get(link["link.href"])
        soup = BeautifulSoup(page.content, "html.parser")
        body = soup.find("article")
        if body:
            text = [p.text for p in body.find_all("p")]
            article = " ".join(text)
        else:
            article = None

        return article

    def getDf(self):
        try:
            df = pd.read_csv("bbc_df.csv", ignore_index=True)

        except:

            df = pd.DataFrame()
        return df
