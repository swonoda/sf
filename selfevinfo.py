import re
import sys
from bs4 import BeautifulSoup
from urllib import request
import urllib.request
import requests
import postgres_controller


class Selfevinfo:
    keyword = 'SF創作講座'
    base_url = u"https://wonodas.hatenadiary.com/"
    ordinal = 9
    work_list = []
    pg_ctrl = postgres_controller.Postgres_controller()

    def getInfo(self, list):
        item = list.find_all("tr")
        for raws in item:
            raw = raws.find_all("td")
            if(len(raw) < 4):
                continue
            user = raw[0].get_text()
            if user == '作者':
                continue
            title = raw[1].get_text()
            ev = raw[3].get_text()
            if ev == '高' :
                ev = '大'
            if ev == '低' :
                ev = '小'

            self.pg_ctrl.update_selfdata(ev, self.ordinal, title, user)
            # self.work_list.append(info)

    def scraping(self):
        self.base_url = self.base_url + u"search?num=15&q=" + \
            urllib.parse.quote_plus(self.keyword, encoding='UTF-8')
        resp = requests.get(self.base_url)
        soup = BeautifulSoup(resp.text, "lxml")
        alink = soup.find_all('a', attrs={"class", "entry-title-link"})
        for result in alink:
            url = result.get("href")
            html = request.urlopen(url)
            soup = BeautifulSoup(html, "html.parser")

            list = soup.find("table")
            if(list != None):
                self.getInfo(list)
                self.ordinal = self.ordinal - 1

    def get_self_info(self):
        return self.work_list
