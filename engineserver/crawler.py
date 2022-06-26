from threading import Thread

import re
import requests
import validators

from engineserver import indexdata, cleanup

from bs4 import BeautifulSoup
from urllib import robotparser
from urllib.parse import urlparse
from collections import defaultdict

class WebCrawler:
    def __init__(self) -> None:
        self.seeds_file = "./database/seeds.sdb"
        self.sites_file = "./database/sites.sdb"
        self.headers = {"User-Agent": "Chromium 86.0.4238.0"}
        self.url_database = indexdata.SearchDatabase()
        self.desc_database = indexdata.DescriptionDatabase()


        self.sites = open(self.seeds_file, "r").readlines()
        self.sites = [line.rstrip() for line in self.sites]

        self.url_database.load_db()
        self.desc_database.load_db()

    def save_sites(self):
        with open(self.seeds_file, "w") as file:
            for current_site in self.sites:
                file.write(current_site + "\n")



    def scan_site(self, site_url: str) -> None:
        


        site_url = site_url.split("#")[0]
        site_url = site_url.split("?")[0]

        site_contents = requests.get(site_url, headers={}).text        
        soup = BeautifulSoup(site_contents, 'html.parser')

        
        for link in soup.findAll("a"):
            href = link.get("href")
            if href is None: continue


            if not validators.url(str(href)): href = site_url + href #href will sometimes do /amo instead of google.com/amo 
            if not validators.url(str(href)): continue #If its not /amo, continue as its not valids


            if href not in self.sites: self.sites.append(href)

        desc_data = soup.find("meta", property="og:description")
        desc_data = desc_data.text if desc_data is not None else "No description provided"
        descr = desc_data if desc_data else "No description provided"

        title = soup.find("title").text if soup.find("title").text else site_url
        
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])] #Extract text from sites
        text  = soup.getText().split() #Get the text in the site


        for current_word in text:
            self.url_database.add_value(current_word, site_url)
            self.desc_database.add_value(site_url, title, descr)

        self.desc_database.save_db()
        self.url_database.save_db()
        self.save_sites()
        cleanup.cleanup_database()

    def scan_all(self):
        i = 0

        while True:
            current_site = self.sites[i]
            self.scan_site(current_site)


            i += 1
            print(f"Scanned Site ({i}) {current_site}")