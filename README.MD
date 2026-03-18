
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


# I wrote this scraper some time ago for a friend of mine and as a personal learning
# experience, maybe someone else finds it useful for their project or study.
#
# It is an example on how to scrape complex data from a website, where the desired
# information is embedded in nested articles over several pages. 
# The code doesn't use any threadding or other optimization for performance improve
# on purpose so the target server is not beeing overwhelmed.
# It can scrape about 1000 Jobs in a few minutes though.
# 
#
# # Author: Jens Michalik     E-Mail: vox288@gmail.com
#


Job_Scraper Version 1.0 

Written in python 3.12.3 including the external librarys: requests, BeautifulSoup4, lxml and tablib

_______________________________________________________________________________________________________________________

This scraper collects information about jobs from the website: https://www.pass.fonction-publique.gouv.fr/recherche-offre

Main module is the Job_Scraper class, inside the Job_Scraper.py file.
It takes two optional arguments: -start_page and -end_page
If no arguments are passed the Job_Scraper will cycle through all pages
containing job information and collect the data.

Please take note that the script will only work if the dependencies from the requirements.txt have been installed.

If you want to scrape specific pages the CLI/Terminal input should
look like one of these examples:

python3 Job_Scraper.py -start_page=0 -end_page=8
python3 Job_Scraper.py -start_page=25
python3 Job_Scraper.py -end_page=36

(please take note that the page counter on the website starts at page 0)


If no argument are passed the ClI/Terminal input should
look like this:

python3 Job_Scraper.py


-- The main method of Job_Scraper is: 

start_scraping 

It starts the whole scraping process and is called automatically if you run the python script. 
The script creates/overrides the csv and xls files, after the scraping process is done.
If the process is interrupted, no data will be written!

--- After scraping the xls and csv files can be found in the data directory ---


_______________________________________________________________________________________________________________________

Other metods are:

    get_data         --> loops through the urls and bundles the collected data in the data_list
    get_job_info     --> collects all information from the blue box in the job offer.
    get_job_location --> collects additional location info if available.
    get_contact_info --> collects contact information like mail or url.
    create_csv       --> creates a Jobs.csv from data collected in data_set.
    create_xls       --> creates a Jobs.xls from data collected in data_set


Variables of this class are:

    is_scraping     : bool wich ends the scraping loop if False
    current_page    : refers to the page number of the website wich is beeing scraped,
                      starts at 0 and gets incremented by 1 after every loop.
    article         : refers to the number of jobs that have been scraped from the current page,
                      starts at 0 and gets incremented by 1 after every job (or 12 after every loop)
    scraped_pages   : counts the pages that have been succesfully scraped
    data_list       : This variable holds a list with all information the scraper collects.
    data_set        : Containes a tablib.Dataset wich is used to create the csv and xls files.
                      Gets alls inormation appended from data_list.
    data_set.headers: Defines the headers or collumn titles for the tables.


-----------------------------------------------------------------------------------------------------------------------


Sub-module Link_Scraper is inside modules directory, it takes 1 argument wich is current_page.
The default value is 0. It refers to the page of the website that is beeing scraped.


-- The main method is:

get_link_list

Returns a list of links to all the job-charts found on the page.


Other methods are:

    get_response   --> If response code 200, returns content of the page.
    get_soup       --> Returns a BeautyfulSoup object of the page.
    get_parent     --> Returns the html content of all job-charts of the page


Variables of this class are:

    self.current_page : refers to the websites page that is beeing scraped.
    self.url          : url to be scraped with dynamic page value 
