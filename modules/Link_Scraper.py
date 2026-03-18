# [!IMPORTANT]
# Disclaimer: For Educational Purposes Only
# This project is developed solely for educational and research purposes.
# It is intended to demonstrate web scraping techniques and data processing workflows.
#
# Usage Responsibility:
# 
#     The author of this script is not responsible for any misuse or potential damage caused by this tool.
#     Users are strictly advised to comply with the Terms of Service (ToS) of the targeted websites and ensure that
#     their scraping activities do not violate any local or international laws.
#     Always check the website's robots.txt file and respect the site's crawling policies.
#     Do not use this script for large-scale data harvesting or any activity that may
#     disrupt the performance of the target server.
# 
# By using this software, you agree to take full responsibility for your actions.


import requests
from bs4 import BeautifulSoup


class LinkScraper:
    def __init__(self, current_page=0):
        """
        LinkScraper extracts the content from the website.
        The parameter current_page refers to the page on the website
        to be scraped

        Methods are:

        get_response: If response code 200, returns content of the page.

        get_soup: Returns a BeautyfulSoup object of the page.

        get_parent: Returns the html content of all job-articles of the page.

        get_link_list: Returns a list of links to all the job-articles found on the page.
        """

        self.current_page = current_page
        self.url = f"https://www.pass.fonction-publique.gouv.fr/recherche-offre?field_type_de_contrat_value%5Bapprentissage%5D=apprentissage&field_type_de_contrat_value%5Bstage%5D=stage&page={self.current_page}"



    def get_response(self):
        self.response = requests.get(self.url)
        if self.response.status_code == 200:
            return self.response.content
        else:
            print(f"Error Status Code = {self.response.status_code}")


    def get_soup(self):
        self.response_text = self.get_response()
        self.soup = BeautifulSoup(self.response_text, "lxml")
        return self.soup


    def get_parent(self):
        self.soup_content = self.get_soup()
        self.find_parent = self.soup_content.find(class_="affichage-mosaique")
        return self.find_parent


    def get_link_list(self):
        self.parent = self.get_parent()
        if self.parent is not None:
            self.number_links = self.parent.find_all(class_="mosaique")
            self.link_list = []
            if self.number_links is not None:
                for i in range(len(self.number_links)):
                    self.find_link = self.parent.find_all(class_="mosaique")[i]["href"]
                    self.parsed_link = self.url[0:42] + self.find_link
                    self.link_list.append(self.parsed_link)
                return self.link_list
            else:
                return None
        else:
            return None
