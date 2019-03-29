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


class CountEv:
    plt.style.use('ggplot')
    connection_config = {
        'host': 'localhost',
        'port': '5432',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'postgres'
    }

    def analysis_body_summary(self):
        connection = psycopg2.connect(**self.connection_config)
        count_sql = "select body_title, summary_total_count, body_total_count, author from works where body_total_count > 0 and body_total_count < 40000"
        score_count = pd.read_sql(sql=count_sql, con=connection, index_col='body_title')
        print(score_count)

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        sns.set_style('whitegrid')
        sns.set_palette('summer')

        ax = sns.lmplot(x='summary_total_count', y='body_total_count', hue='author', data=score_count, fit_reg=False)
        ax = plt.gca()
        ax.set_title('Summary count vs Total count')
        # ax.set_xlabel('summary_count')
        # ax.set_ylabel('work_count')
        # グラフ表示
        print(mpl.matplotlib_fname())
        plt.show()

    def clustering(self, cluster_target, n_cluster, title):
        connection = psycopg2.connect(**self.connection_config)
        count_sql = "select body_title, body_score, summary_total_count, body_total_count" + "," + cluster_target + \
            ", author from works where body_total_count > 0 and body_total_count < 40000"
        score_count = pd.read_sql(sql=count_sql, con=connection, index_col='body_title')
        rate = score_count[cluster_target]/score_count.body_total_count * 100

        label_rate = cluster_target + "_rate"
        score_count[label_rate] = rate
        print(score_count)

        model1 = KMeans(n_clusters=n_cluster, random_state=0)
        data = score_count[[label_rate]]
        cluster_mean = model1.fit(data)
        cluster = cluster_mean.labels_
        score_count['cluster'] = cluster
        print(cluster_mean)
        scatter_table = pd.pivot_table(score_count, index='author', columns='cluster',
                                       aggfunc=len, fill_value=0)
        print(scatter_table[label_rate])

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        sns.set_style('whitegrid')
#        sns.set_palette('winter')

        ax = sns.lmplot(x='body_total_count', y='body_score', hue='cluster',
                        data=score_count, fit_reg=False)
        ax = plt.gca()
        ax.set_title(title)
        print(mpl.matplotlib_fname())
        plt.show()

    def clustering_body_score(self):
        self.clustering('body_new_line_count', 2, 'total count vs score by cluster new line rate')

    def clustering_scat_score(self):
        self.clustering('body_scat_count', 2, 'total count vs score by clustering scat rate')

    def clustering_ruby_score(self):
        self.clustering('body_ruby_count', 2, 'total count vs score by clustering ruby rate')
