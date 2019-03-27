import re
import sys
from bs4 import BeautifulSoup
from urllib import request
import urllib.request
import requests


def scraping(url):
    print(url)
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    list = soup.find("table")
    if(list != None):
        raw = list.find_all("tr")

        for work_info in raw:
            print(work_info.contents[0], work_info.string)
            print(work_info.contents[1], work_info.string)


if __name__ == "__main__":
    keyword = str('SF創作講座第')
    # keyword = keyword.encode('utf-8')
    base_url = u"https://wonodas.hatenadiary.com/search?num=15&q=" + \
        urllib.parse.quote_plus(keyword, encoding='UTF-8')
    resp = requests.get(base_url)
    resp.raise_for_status()
    # search_result = urllib.request.urlopen(base_url)
    soup = BeautifulSoup(resp.text, "lxml")
    alink = soup.find_all('a', attrs={"class", "entry-title-link"})
    print(alink)
    for result in alink:
        print(result.get("href"))
        scraping(result.get("href"))
