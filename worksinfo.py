import re
import sys
from bs4 import BeautifulSoup
from urllib import request
import urllib.request
import requests
import postgres_controller
import dbData
from statistics import mean


class WorksInfo:
    base_url = u"https://school.genron.co.jp/works/sf/2018/subjects/"
    wd = dbData.WorkData()
    ordinal = 0
    pg_ctrl = postgres_controller.Postgres_controller()
    is_update = False

    def __init__(self, is_update):
        self.is_update = is_update

    def count_paragraph_and_average_len(self, content):
        count_paragraph = 0
        average_sentence_len = 0

        br_len = len(content.find_all("br"))
        if(br_len == 0):
            p_arr = content.find_all("p")
            remove_newline = list(filter(lambda a: len(a.get_text()) < 2, p_arr))
            count_paragraph = len(remove_newline) + 1
        else:
            count_paragraph = len(content.find_all("p"))

        arr = content.get_text().split("。")
        sentence_len = []
        for sentence in arr:
            sentence_len.append(len(sentence))

        average_sentence_len = mean(sentence_len)
        info = [count_paragraph, average_sentence_len]
        return info

    def work_body_scraping(self, work_body):
        self.wd.work_title = work_body.find("h1", attrs={"class", "work-title"}).get_text()
        entry = work_body.find("section", attrs={"id", "work-entry"})
        content = work_body.find("div", attrs={"class", "work-content"})
        body_count_str = work_body.find_all("p", attrs={"class", "count-character"})
        if(len(body_count_str) > 2):
            str = body_count_str[2].get_text().replace('\t', '')
            self.wd.body_total_count = int(str[str.find("：")+1:])

        if len(content.get_text()) < self.wd.body_total_count:
            content = work_body
        self.wd.body_newline = len(content.find_all("p")) + len(content.find_all("br"))
        self.wd.body_ruby = len(content.find_all("ruby"))
        self.wd.body_scat = content.get_text().count("「")
        self.wd.body_sentence_count = content.get_text().count("。")
        print("get body paragraph count and average sentence length")
        info = self.count_paragraph_and_average_len(content)
        print(info)
        self.wd.body_pragraph_count = info[0]
        self.wd.body_ave_sentence_len = info[1]

    def works_scraping(self, url):
        resp = requests.get(url)
        body = BeautifulSoup(resp.text, "html.parser")
        self.wd.summary_title = body.find("h3", attrs={"class", "summary-title"}).get_text()
        summary_count_str = body.find("p", attrs="count-character").get_text().replace('\t', '')
        pos = summary_count_str.rfind("：") + 1
        summary_content = body.find("div", attrs="summary-content")
        print("get summary paragraph count and average sentence length")
        content_info = self.count_paragraph_and_average_len(summary_content)
        print(content_info)
        self.wd.summary_sentence_count = summary_content.get_text().count("。")
        self.wd.summary_count = int(summary_count_str[pos:])
        self.wd.summary_ave_sentence_len = content_info[1]
        self.wd.body_total_count = 0
        self.wd.body_title = ""
        self.wd.body_newline = 0
        self.wd.body_ruby = 0
        self.wd.body_scat = 0
        self.wd.body_ave_sentence_len = 0
        self.wd.body_pragraph_count = 0
        self.wd.body_sentence_count = 0
        if(body.find("h1", attrs={"class", "work-title"}) != None):
            self.work_body_scraping(body)

    def students_scraping(self, student_list):
        for student in student_list:
            if (student.find("figure", attrs={"class", "written"}) == None):
                continue

            self.score = 1
            if (student.find("span", attrs={"class", "score"}) != None):
                print("has score")
                self.wd.score = self.wd.score + int(student.find("span", attrs={"class", "score"}).get_text())
            self.name = student.find("span", attrs={"class", "name"}).get_text().replace(' ', '')
            if (self.wd.author.find('/') > 0):
                self.wd.author = self.wd.author[:self.wd.author.find('/')]

            self.wd.work_url = student.find("a", attrs={"class", "anchor-block"}).get("href")
            print(self.wd.work_url)
            link = self.wd.work_url
            self.works_scraping(link)
            self.pg_ctrl.put_worksdata(self.wd)
#            self.works_list.append(raw)

    def scraping(self):
        if(self.is_update):
            self.update()
        else:
            for i in range(9):
                self.ordinal = i
                self.wd.ordinal = self.ordinal
                url = self.base_url + str(i) + "/"
                print(url)
                resp = requests.get(url)
                soup = BeautifulSoup(resp.text, "lxml")
                list_items = soup.find_all("li", attrs={"class", "student-list-item"})
                self.students_scraping(list_items)

    def update(self):
        sql = "select ordinal, author, summary_title, summary_total_count, body_title, work_url from works where (body_title <> '' and body_total_count < 5000) or (body_score > 1 and body_total_count < 5000) or (summary_ave_sentence_len < 1)"
        result = self.pg_ctrl.select(sql)
        print(result)
        for update_work in result:
            self.wd.ordinal = update_work[0]
            self.wd.author = update_work[1]
            self.wd.summary_title = update_work[2]
            self.wd.summary_count = update_work[3]
            self.wd.work_title = update_work[4]
            self.wd.work_url = update_work[5]
            self.wd.body_total_count = 0
            self.wd.body_newline = 0
            self.wd.body_ruby = 0
            self.wd.body_scat = 0
            self.wd.summary_ave_sentence_len = 0
            self.wd.summary_sentence_count = 0
            self.wd.body_ave_sentence_len = 0
            self.wd.body_paragraph_count = 0
            self.wd.body_sentence_count = 0
            self.works_scraping(self.wd.work_url)
            self.pg_ctrl.put_worksdata(self.wd)

    def get_works_info(self):
        return self.works_list
