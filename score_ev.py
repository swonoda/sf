import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
from collections import OrderedDict
import matplotlib.cm as cm
import seaborn as sns
import matplotlib.font_manager
import matplotlib as mpl
from sklearn.cluster import KMeans


class ScoreEv:
    plt.style.use('ggplot')
    connection_config = {
        'host': 'localhost',
        'port': '5432',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'postgres'
    }

    def analysis_score(self, target, title):
        connection = psycopg2.connect(**self.connection_config)
        if target == 'body_total_count':
            count_sql = "select body_title, body_score, body_total_count, author from works where body_score > 0 and body_score < 20 and body_total_count > 0 and body_total_count < 40000 order by body_score"
        else:
            count_sql = "select body_title, body_score, " + target + \
                ", body_total_count, author from works where body_score > 0 and body_total_count > 0 and body_score < 20 and body_total_count < 40000 order by body_score"
        score_count = pd.read_sql(sql=count_sql, con=connection, index_col='body_title')
        if(target != 'body_total_count'):
            rate = score_count[target]/score_count.body_total_count * 100
            score_count['rate'] = rate
            score_count = score_count.sort_values('rate', ascending=False)
        else:
            score_count = score_count.sort_values(target, ascending=False)
        print(score_count)

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        sns.set_style('whitegrid')
        sns.set_palette('summer')

        x_target = ''
        if target == 'body_total_count':
            x_target = target
        else:
            x_target = 'rate'
        score_count = score_count.sort_values('body_score', ascending=False)
        ax = sns.lmplot(x=x_target, y='body_score', hue='author', data=score_count, fit_reg=False)
        ax = plt.gca()
        ax.set_title(title)
        # グラフ表示
        plt.show()

    def analysis_score_bodycount(self):
        self.analysis_score('body_total_count', 'Total count vs score')

    def analysis_score_newline_rate(self):
        self.analysis_score('body_new_line_count', 'new line rate vs score')

    def analysis_score_ruby_rate(self):
        self.analysis_score('body_ruby_count', 'ruby vs score')

    def analysis_score_scat_rate(self):
        self.analysis_score('body_scat_count', 'scat vs score')

    def analysis_score_count_rate(self):
        self.analysis_score('summary_total_count', 'summary/body vs score')

    def analysis_score_summary_count(self):
        connection = psycopg2.connect(**self.connection_config)
        count_sql = "select body_title, body_score, summary_total_count, author from works where body_score > 0 and body_total_count > 0 and summary_total_count > 100 order by body_score"
        score_count = pd.read_sql(sql=count_sql, con=connection, index_col='body_title')
        print(score_count)
        print(len(score_count.author))
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        sns.set(font=['komorebi gothic'])
        sns.set_style('whitegrid')
        sns.set_palette('summer')

        ax = sns.lmplot(x='summary_total_count', y='body_score', hue='author', data=score_count, fit_reg=False)
        ax = plt.gca()
        ax.set_title('Total count vs score')
        # グラフ表示
        plt.show()

    def clustering(self, target, n_cluster, title):
        connection = psycopg2.connect(**self.connection_config)
        count_sql = "select body_title, body_score, summary_total_count, body_total_count" + "," + target + \
            ",author from works where body_total_count > 0 and body_total_count < 40000"
        score_count = pd.read_sql(sql=count_sql, con=connection, index_col='body_title')
        rate = score_count[target]/score_count.body_total_count * 100

        model1 = KMeans(n_clusters=n_cluster, random_state=0)
        data = score_count[['body_score']]
        cluster_mean = model1.fit(data)
        cluster = cluster_mean.labels_
        score_count['cluster'] = cluster
        print(score_count)
        scatter_table = pd.pivot_table(score_count, index='author', columns='cluster',
                                       aggfunc=len, fill_value=0)
        print(scatter_table[target])

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        sns.set_style('whitegrid')
#        sns.set_palette('winter')

        ax = sns.lmplot(x='body_total_count', y=target, hue='cluster',
                        data=score_count, fit_reg=False)
        ax = plt.gca()
        ax.set_title(title)
        print(mpl.matplotlib_fname())
        plt.show()

    def cluster_newline(self):
        self.clustering('body_new_line_count', 3, 'total_count vs new line by clustring score')
