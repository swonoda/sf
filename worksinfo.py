import re
import sys
from bs4 import BeautifulSoup
from urllib import request
import urllib.request
import requests
import postgres_controller


class WorksInfo:
    base_url = u"https://school.genron.co.jp/works/sf/2018/subjects/"
    ordinal = 0
    works_list = []
    pg_ctrl = postgres_controller.Postgres_controller()
    work_title = ""
    newline_count = 0
    ruby_count = 0
    scat_count = 0
    body_count = 0
    name = ""
    summary_title = ""
    summary_count = 0
    score = 1

    def work_body_scraping(self, work_body):
        self.work_title = work_body.find("h1", attrs={"class", "work-title"}).get_text()
        print(self.work_title)
        content = work_body.find("div", attrs={"class", "work-content"})
        self.newline_count = len(content.find_all("p")) + len(content.find_all("br"))
        self.ruby_count = len(content.find_all("ruby"))
        self.scat_count = content.get_text().count("「")
        body_count_str = content.find("p", attrs={"class", "count-character"})
        if(body_count_str != None):
            str = body_count_str.get_text().replace('\t', '')
            print(str.find("："))
            self.body_count = int(str[str.find("：")+1:])

    def works_scraping(self, url):
        resp = requests.get(url)
        body = BeautifulSoup(resp.text, "html.parser")
        self.summary_title = body.find("h3", attrs={"class", "summary-title"}).get_text()
        summary_count_str = body.find("p", attrs="count-character").get_text().replace('\t', '')
        pos = summary_count_str.rfind("：") + 1
        self.summary_count = int(summary_count_str[pos:])
        self.body_count = 0
        self.work_title = ""
        self.newline_count = 0
        self.ruby_count = 0
        self.scat_count = 0
        if(body.find("h1", attrs={"class", "work-title"}) != None):
            self.work_body_scraping(body)

    def students_scraping(self, student_list):
        for student in student_list:
            if (student.find("figure", attrs={"class", "written"}) == None):
                continue

            self.score = 1
            if (student.find("span", attrs={"class", "score"}) != None):
                print("has score")
                self.score = self.score + int(student.find("span", attrs={"class", "score"}).get_text())
            self.name = student.find("span", attrs={"class", "name"}).get_text().replace(' ', '')
            if (self.name.find('/') > 0):
                self.name = self.name[:self.name.find('/')]
            link = student.find("a", attrs={"class", "anchor-block"}).get("href")
            print(link)
            self.works_scraping(link)
            self.pg_ctrl.put_worksdata(self.ordinal, self.name, self.summary_title, self.summary_count,
                                       self.work_title, self.newline_count, self.ruby_count, self.scat_count, self.body_count, self.score)
#            self.works_list.append(raw)

    def scraping(self):
        for i in range(9):
            self.ordinal = i
            url = self.base_url + str(i) + "/"
            print(url)
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "lxml")
            list_items = soup.find_all("li", attrs={"class", "student-list-item"})
            self.students_scraping(list_items)

    def get_works_info(self):
        return self.works_list
