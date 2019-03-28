import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
from collections import OrderedDict
import matplotlib.cm as cm

class ScoreEv :
    plt.style.use('ggplot')
    connection_config = {
        'host': 'localhost',
        'port': '5432',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'postgres'
    }

    def analysis_score_bodycount(self) :
        connection = psycopg2.connect(**self.connection_config)
        count_sql = "select body_title, body_score, body_total_count, author from works where body_score > 1"
        score_count = pd.read_sql(sql=count_sql, con=connection, index_col='body_title')
        print(score_count)
        x = {}
        y = {}
        i = 0
        for user in score_count.author :
            if not (user in x.keys()) :
                x[user] = score_count[score_count.author==user].body_score
                y[user] = score_count[score_count.author==user].body_total_count
                plt.scatter(x[user], y[user], color=cm.autumn(i/22.0), alpha=0.5, s=50+10*i)
                i = i + 1

        # グラフ表示
        plt.show()

    def analysis_score_newline_rate(self) :
        connection = psycopg2.connect(**self.connection_config)
        count_sql = "select body_title, body_score, body_new_line_count, body_total_count, author from works where body_score > 1 and body_total_count > 0"
        score_count = pd.read_sql(sql=count_sql, con=connection, index_col='body_title')
        print(score_count)
        print(len(score_count.author))
        x = {}
        y = {}
        i = 0
        for user in score_count.author :
            if not (user in x.keys()) :
                x[user] = score_count[score_count.author==user].body_score
                y[user] = score_count[score_count.author==user].body_new_line_count * 100/ score_count[score_count.author==user].body_total_count
                plt.scatter(x[user], y[user], color=cm.autumn(i/22.0), alpha=0.5, s=50+10*i)
                i = i + 1

        print(x)
        print(y)
        # グラフ表示
        plt.show()

    def analysis_score_ruby_rate(self) :
        connection = psycopg2.connect(**self.connection_config)
        count_sql = "select body_title, body_score, body_ruby_count, body_total_count, author from works where body_score > 1 and body_total_count > 0"
        score_count = pd.read_sql(sql=count_sql, con=connection, index_col='body_title')
        print(score_count)
        print(len(score_count.author))
        x = {}
        y = {}
        i = 0
        for user in score_count.author :
            if not (user in x.keys()) :
                x[user] = score_count[score_count.author==user].body_score
                y[user] = score_count[score_count.author==user].body_ruby_count * 100/ score_count[score_count.author==user].body_total_count
                plt.scatter(x[user], y[user], color=cm.autumn(i/22.0), alpha=0.5, s=50+10*i)
                i = i + 1

        print(x)
        print(y)
        # グラフ表示
        plt.show()

    def analysis_score_scat_rate(self) :
        connection = psycopg2.connect(**self.connection_config)
        count_sql = "select body_title, body_score, body_scat_count, body_total_count, author from works where body_score > 1 and body_total_count > 0"
        score_count = pd.read_sql(sql=count_sql, con=connection, index_col='body_title')
        print(score_count)
        print(len(score_count.author))
        x = {}
        y = {}
        i = 0
        for user in score_count.author :
            if not (user in x.keys()) :
                x[user] = score_count[score_count.author==user].body_score
                y[user] = score_count[score_count.author==user].body_scat_count * 100/ score_count[score_count.author==user].body_total_count
                plt.scatter(x[user], y[user], color=cm.autumn(i/22.0), alpha=0.5, s=50+10*i)
                i = i + 1

        print(x)
        print(y)
        # グラフ表示
        plt.show()

    def analysis_score_count_rate(self) :
        connection = psycopg2.connect(**self.connection_config)
        count_sql = "select body_title, body_score, summary_total_count, body_total_count, author from works where body_score > 1 and body_total_count > 0"
        score_count = pd.read_sql(sql=count_sql, con=connection, index_col='body_title')
        print(score_count)
        print(len(score_count.author))
        x = {}
        y = {}
        i = 0
        for user in score_count.author :
            if not (user in x.keys()) :
                x[user] = score_count[score_count.author==user].body_score
                y[user] = score_count[score_count.author==user].summary_total_count/ score_count[score_count.author==user].body_total_count
                plt.scatter(x[user], y[user], color=cm.autumn(i/22.0), alpha=0.5, s=50+10*i)
                i = i + 1

        print(x)
        print(y)
        # グラフ表示
        plt.show()

    def analysis_score_summary_count(self) :
        connection = psycopg2.connect(**self.connection_config)
        count_sql = "select body_title, body_score, summary_total_count, author from works where body_score > 1 and body_total_count > 0"
        score_count = pd.read_sql(sql=count_sql, con=connection, index_col='body_title')
        print(score_count)
        print(len(score_count.author))
        x = {}
        y = {}
        i = 0
        for user in score_count.author :
            if not (user in x.keys()) :
                x[user] = score_count[score_count.author==user].body_score
                y[user] = score_count[score_count.author==user].summary_total_count
                plt.scatter(x[user], y[user], color=cm.autumn(i/22.0), alpha=0.5, s=50+10*i)
                i = i + 1

        print(x)
        print(y)
        # グラフ表示
        plt.show()
