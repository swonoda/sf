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
        print(title)
        connection = psycopg2.connect(**self.connection_config)
        count_sql = "select body_title, body_score, body_total_count" + "," + cluster_target + \
            ", author from works where body_total_count > 0 and body_total_count < 40000"
        score_count = pd.read_sql(sql=count_sql, con=connection, index_col='body_title')
        rate = score_count[cluster_target]/score_count.body_total_count * 100
        print(rate)
        label_rate = cluster_target + "_rate"
        score_count[label_rate] = rate

        model1 = KMeans(n_clusters=n_cluster, random_state=0)
        data = score_count[[label_rate]]
        cluster_mean = model1.fit(data)
        cluster = cluster_mean.labels_
        score_count['cluster'] = cluster
        score_count = score_count.sort_values(label_rate, ascending=True)
        print(score_count)
        score_count.to_csv("data/" + cluster_target + ".csv")

        scatter_table = pd.pivot_table(score_count, index='author', columns='cluster',
                                       aggfunc=len, fill_value=0)
        print(scatter_table[label_rate])
        scatter_table[label_rate].to_csv("data/" + cluster_target + "_pivot.csv")

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        sns.set_style('whitegrid')
#        sns.set_palette('winter')

        ax = sns.lmplot(x='body_total_count', y='body_score', hue='cluster',
                        data=score_count, fit_reg=False)
        ax = plt.gca()
        ax.set_title(title)
        plt.savefig("data/" + cluster_target + "_score.png",dpi=300) 
        plt.clf()
        ax2 = fig.add_subplot(1, 2, 1)
        ax2 = sns.lmplot(x = 'body_total_count', y=cluster_target, hue='cluster', data=score_count, fit_reg=False)
        plt.savefig("data/" + cluster_target + ".png",dpi=300) 
        print(mpl.matplotlib_fname())
        plt.show()
        fig.show()

    def clustering_body_score(self, num_cluster):
        print("body_new_line_count")
        self.clustering('body_new_line_count', int(num_cluster), 'total count vs score by cluster new line rate')

    def clustering_scat_score(self, num_cluster):
        self.clustering('body_scat_count', int(num_cluster), 'total count vs score by clustering scat rate')

    def clustering_ruby_score(self, num_cluster):
        self.clustering('body_ruby_count', int(num_cluster), 'total count vs score by clustering ruby rate')

    def clustering_count_score(self, num_cluster):
        self.clustering('summary_total_count', int(num_cluster), 'total count vs score by clustering summary length')
