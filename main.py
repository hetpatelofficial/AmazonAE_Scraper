import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import logging
from bs4 import BeautifulSoup
import requests
import pandas as pd

# ------------- Global Vars -------------
__author__ = "hetpatelofficial@gmail.com (Het Patel)"
CWD = os.path.dirname(os.path.realpath(__file__))
tdt = datetime.now()
td = datetime.now().strftime('%m-%d-%Y--%H%M%S')
categories_file_path = os.path.join(CWD, 'sectors.csv')
logs = os.path.join(CWD, 'logs')
# URL = 'https://www.amazon.ae/gp/bestsellers/'
URL = 'https://www.amazon.ae/gp/bestsellers/appliances'
proxy_file_path = os.path.join(CWD, 'proxy_lists.txt')

if not os.path.exists(logs):
    os.mkdir(logs)
# ------------- Logging Configuration -------------
log_file_path = os.path.join(logs, f"{td}.log")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(filename=log_file_path, mode="a", encoding="UTF-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s-%(levelname)s: Func-%(funcName)s : Line-%(lineno)d : %(message)s"))
logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())
logger.debug(f"\n{'-'*21}  is Started at -> {tdt.strftime('%d-%m-%Y %I:%M:%S %p')} {'-'*21}")
logger.info(f"Current Working Directory: {CWD}")
logger.info(f"Current Date & Time: {tdt.strftime('%d-%m-%Y %I:%M:%S %p')}")
logger.info(f"Log File Path: {log_file_path}")

# ------------- Starter Code -------------

logging.getLogger('WDM').setLevel(logging.NOTSET)
os.environ['WDM_LOG'] = 'false'
DRIVER_PATH = Service(ChromeDriverManager().install())
logger.info(f"Chrome Driver File Path: {log_file_path}")


class AmazonScraper:

    # Create driver and Options
    options = Options()
    options.add_argument("--disable-notifications")  # To disable notifications
    options.add_argument("--suppress-message-center-popups")  # To remove permission pop-ups and other from chrome
    options.add_argument("--disable-translate")  # To disable auto translate & translate pop-up
    options.add_argument('--disable-logging')  # to disable WebDrive Logs
    # options.add_argument('--headless')  # To not show browser
    options.add_argument('--no-sandbox')  # To not show browser
    options.add_argument('--log-level=3')
    links_dict = {}
    leaf_nodes = {}
    options.add_experimental_option("excludeSwitches", ["enable-logging", "test-type"])
    df = pd.DataFrame(
        columns=['id', 'category_name', 'parent_id', 'url', 'all_child_parsed', 'timestamp', 'asin', 'name',
                     'technical_details', 'price', 'stock', 'stars', 'number_of_reviews', 'product_images',
                     'shipping_cost_info'])

    def __init__(self):

        self.get_categories(URL)

    def get_categories(self, url):
        logger.debug(f"URL Scraping is: {url}")
        categories = requests.get(url)
        if categories.status_code == 200:
            soup = BeautifulSoup(categories.content, "html.parser")
            elements = soup.find_all('div', {'role': 'group'})
            for element in elements:
                category = element.find_all('div', {'role': 'treeitem'})
                for link in category:
                    if link.find('a') is not None:
                        title = link.find('a').text
                        if title not in self.links_dict.keys():
                            url = 'https://www.amazon.ae' + link.find('a').get('href')
                            # if not os.path.exists(categories_file_path):
                            #     self.df.loc[self.df.shape[0]] = ['', link.find('a').text, '', url, '', datetime.now().timestamp(),'asin', 'name', 'technical_details', 'price', 'stock', 'stars', 'number_of_reviews', 'product_images', 'shipping_cost_info']
                            #     self.df.to_csv(categories_file_path, index=False, mode='a')
                            # else:
                            #     self.df = pd.read_csv(categories_file_path)
                            #     self.df.loc[self.df.shape[0]] = ['', link.find('a').text, '', url, '', datetime.now().timestamp(), 'asin', 'name', 'technical_details', 'price', 'stock', 'stars', 'number_of_reviews', 'product_images', 'shipping_cost_info']
                            #     self.df.to_csv(categories_file_path, index=False, mode='w')
                            if title not in self.links_dict.keys():
                                self.links_dict[title] = {url: False}

            for title in self.links_dict.keys():
                links_dict = self.links_dict[title]
                url = list(links_dict.keys())[0]
                if not links_dict[url]:
                    self.links_dict[title][url] = True
                    logger.debug(f"{title}: {url} is set to {True}")
                    self.get_categories(url)

        else:
            logger.error(f"Response Code: {categories.status_code}\nFor URL: {url}")


if __name__ == '__main__':
    AmazonScraper()

