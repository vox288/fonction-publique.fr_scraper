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


import argparse
import tablib
import requests
from bs4 import BeautifulSoup
from modules.Link_Scraper import LinkScraper


class JobScraper:
    def __init__(self, start_page = 0, end_page = None):
        """
        This JobScraper gets information about jobs from the website: 
        https://www.pass.fonction-publique.gouv.fr/recherche-offre

        The website's exact url is defined in the sub-module Link_Scraper.
        
        The main method of this class is:  
        
            start_scraping 
            
        --> it will automatically scrape the information for every job
        found on the page,

        switch to the next page of the website and
        print out the progress.
        
        Finally creates a .csv and a .xls file in the data folder containing
        all available information.
            
                    
                    other metods are:

                    get_data --> loops through the urls and bundles data it gets by calling other get_methods.
                    get_job_info --> collects all information from the blue box in the job offer.
                    get_job_location --> collects additional location info if available.
                    get_contact_info --> collects contact information like mail or url.
                    create_csv --> creates a Jobs.csv from data collected in data_set.
                    create_xls --> creates a Jobs.xls from data collected in data_set.
                    
                    Please read the README.txt for more Information.
                    Take a look at requirements.txt for dependencies.
        """


        self.is_scraping = True
        self.current_page = start_page
        self.end_page = end_page
        self.article = 1
        self.scraped_pages = 0
        self.data_list = []

        self.data_set = tablib.Dataset()

        self.data_set.headers = [
            "Numéro d'offre",
            "Type de contrat",
            "Niveau de diplôme préparé",
            "Domaine d'activité",
            "Administration de rattachement",
            "Entité",
            "Service d'affectation",
            "Lieu d'affectation",
            "Localisation du poste",
            "Contact",
            "Additional Contact",
        ]

        self.start_scraping()



    def get_data(self):
        """
        Loops through the urls collected by LinkScraper
        and bundles the scraped data in the data_list.
        The data then gets appended to the tablib data_set.
        """
        self.list = LinkScraper(f"{self.current_page}").get_link_list()
        if self.list is not None:
            for link in self.list:
                response = requests.get(link)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "lxml")
                    info_box = soup.find(class_="bloc-bleu")
                    contact_box = soup.find(class_="contact-offre")
                    if info_box and contact_box is not None:
                        try:
                            self.get_job_info(info_box)
                            self.get_job_location(info_box)
                            self.get_contact_info(contact_box)
                            self.data_set.append(self.data_list)
                            self.data_list.clear()
                            print(f"{self.article} Jobs scraped")
                            self.article += 1
                        except Exception as e:
                            print(e)
                            print(f"Job number {self.article} skipped, failed to load information")
                        continue
            
                else:
                    print(f"Connection Error Code{response.status_code}")
                    break
            else:
                pass


    def get_job_info(self, info_box):
        """
        Collects all information from the blue-info-box in the job offer.
        """
        content = info_box.find_all(class_="field__item")
        if len(content) == 8:
            for element in content:
                self.data_list.append(element.text)
        elif len(content) == 7:
            for element in content:
                self.data_list.append(element.text)
            self.data_list.append("-----")
        elif len(content) > 8:
            for i in range(8):
                self.data_list.append(content[i].text)
        else:
            difference = 8 - len(content)
            for element in content:
                self.data_list.append(element.text)
            for i in range(difference):
                self.data_list.append("-----")


    def get_job_location(self, info_box):
        """
        Collects additional location info, if available.
        """
        location = info_box.find(class_="localisation").find_all(class_="field")
        element_list = []
        for element in location:
            element_list.append(element.text)
        self.data_list.append(" ".join(map(str, element_list)))


    def get_contact_info(self, contact_box):
        """
        Collects contact information like mail or url.
        """
        contact_info = contact_box.find_all("a")
        if len(contact_info) == 2:
            for element in contact_info:
                self.data_list.append(element.text)
        elif len(contact_info) == 1:
            for element in contact_info:
                self.data_list.append(element.text)
            self.data_list.append("-----")
        else:
            self.data_list.append(contact_info[0].text)
            self.data_list.append(contact_info[1].text)


    def create_csv(self):
        """
        Creates a Jobs.csv from data collected in data_set.
        """
        with open("scraped_data/Jobs.csv", "w", encoding="utf-8") as csv_file:
            csv_file.write(self.data_set.export("csv"))


    def create_xls(self):
        """
        Creates a Jobs.xls from data collected in data_set.
        """
        with open("scraped_data/Jobs.xls", "wb") as xls_file:
            xls_file.write(self.data_set.export("xls"))


    def start_scraping(self):
        """
        Starts the whole scraping process and handles the pagination.
        """
        while self.is_scraping:
            self.site_content = LinkScraper(f"{self.current_page}").get_soup()
            self.next_button = self.site_content.find(class_="pager__item pager__item--next")
            self.get_data()
            self.scraped_pages += 1

            if self.next_button:
                print(f"Now scraping page {self.current_page+ 1}")
                self.current_page += 1

                if self.end_page is not None:
                    if self.current_page >= self.end_page+1:
                        self.is_scraping = False

            else:
                self.is_scraping = False

        print(f"{self.scraped_pages} Pages have been scraped")
        self.create_csv()
        self.create_xls()
        print("CSV and XLS data successfully created")


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description="""This script scrapes all job information from https://www.pass.fonction-publique.gouv.fr/recherche-offre
                       and writes them into a csv and a xls file. 
                       It takes two optional arguements:  start_page   and   end_page as integers.
                       If no arguments are passed all information from all pages will be scraped.""")
    
    parser.add_argument("-start_page", required=False, type=int, default=0)
    parser.add_argument("-end_page", required=False, type=int, default=None)

    args = parser.parse_args()

    start_page = args.start_page
    end_page = args.end_page

    run_scraper = JobScraper(start_page, end_page)

        