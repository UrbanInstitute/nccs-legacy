from bs4 import BeautifulSoup
import requests
import json
import os

NAMESDIC = {"bmf": "BMF",
            "core": "Core",
            "trend": "Trend",
            "digitizeddata": "DD+",
            "misc": "+",
            "soi": "SOI",
            "home": "."}

BASE_URL = "https://nccs-data.urban.org/"

def archive_dd_scraper(series, folder):
    """
    Function to scrape a data dictionary page from https://nccs-data.urban.org
    Returns a dictionary of data dictionary names and links to data dictionaries
    """
    url_dic = {}

    if series != "home": dd_url = BASE_URL + f"showDD.php?ds={series.lower()}"
    elif series == 'home': 
        if folder == "dictionary": dd_url = BASE_URL + "data-dictionaries.php" 
        elif folder == 'data': dd_url = BASE_URL + "index.php"
    
    req = requests.get(dd_url)
    soup = BeautifulSoup(req.text, "html.parser")

    for link in soup.find_all("a"):
        url = link.get("href")
        if NAMESDIC[series] in url:
            url = BASE_URL + url
            dd_name = link.get_text().strip().replace(" ", "_").replace("/", "_")
            url_dic[dd_name] = url

    with open(f"{folder}/{series.lower()}/{series.lower()}_urls.json", "w+") as f:
        json.dump(url_dic, f)
    
    return("Scraping Complete")
