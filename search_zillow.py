from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import lxml


class ZillowData:
    """
    Obtain the data of rental home in CA under range of $3k with 1 bedroom atleast.

    Libraries used:
    BeautifulSoup: To obtain the data from webfile.
    Selenium: To save the data from zillow in a webfile.

    Methods:
    get_webpage: To get the data from zillow and store in webfile.
    get_data: To get the data from webfile of zillow.
    get_links: To get a list of rental home links from webfile of zillow.
    get_home_address: To get a list of rental home addresses on zillow using webfile.
    get_price: To get a list of rental homes prices on zillow using webfile.
    """
    def __init__(self):
        self.url = 'https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%' \
                   '3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-123.16117323828125%2C%22east%22%3' \
                   'A-121.70548476171875%2C%22south%22%3A37.31689580365897%2C%22north%22%3A38.230862' \
                   '43706723%7D%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A' \
                   '%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%2' \
                   '2value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value' \
                   '%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22' \
                   '%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22' \
                   '%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3' \
                   'Atrue%2C%22mapZoom%22%3A9%7D'

        self.drive_path = "YOUR DRIVE PATH"
        self.file = 'web_file_zillow.txt'

    def get_webpage(self,file,url):
        """
        Requesting the data from webpage using selenium\n
        Storing the data n a web file\n

        :param file: file where the webpage is stored\n
        :param url: url of the webpage\n
        :return: nothing
        """

        option = webdriver.ChromeOptions()
        option.add_experimental_option('detach',True)

        driver = webdriver.Chrome(executable_path=self.drive_path)
        driver.get(url)

        ask_to_save = input("Allow the webpage to completely render. Enter 'y' to save the webpage in a file.\n").lower()
        if ask_to_save == 'y':
            html_source = driver.page_source

            # save the html source in a file
            with open(file,encoding="utf-8",mode='w') as webfile:
                webfile.write(html_source)

        self.get_data()

    def get_data(self):
        """
        open a file and retrieve the data using BeautifulSoup\n
        if the file doesn't exit then call 'get webpage' function to create a file.

        :return: data obtained from the file
        """
        try:
            open(self.file)
        except FileNotFoundError:
            self.get_webpage(self.file,self.url)
        else:
            pass
        finally:
            with open(self.file,mode='r',encoding='utf-8') as webfile:
                content = webfile.read()
            return BeautifulSoup(content,"lxml")


    def get_links(self):
        """
        Get the links of home from zillow using web file.
        :return: links obtained from zillow web file
        """
        links = []
        soup = self.get_data()
        link_path = soup.select('.property-card-data a')
        for link in link_path:
            link_url = link['href']
            if 'http' in link_url:
                links.append(link_url)
            else:
                links.append(f"https://www.zillow.com{link_url}")
        return links

    def get_home_address(self):
        """
        Get the address of available home on zillow using webfile.
        :return: list of addresses of home available on zillow
        """
        home_address_list = []
        soup = self.get_data()
        address_path = soup.select(".property-card-data address")
        for address in address_path:
            home_address = address.get_text()
            home_address_list.append(home_address)
        return home_address_list

    def get_price(self):
        """
        Get the price list of homes available on zillow using webfile.
        :return: list of prices available on zillow
        """

        price_list = []
        soup = self.get_data()
        price_path = soup.select('.property-card-data span')
        for price in price_path:
            price_value = price.get_text()[:6]
            price_list.append(price_value)
        return price_list