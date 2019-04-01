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

class ClusterAuthor :
    plt.style.use('ggplot')
    connection_config = {
        'host': 'localhost',
        'port': '5432',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'postgres'
    }

    def clustering(self) :
        connection = psycopg2.connect(**self.connection_config)
        count_sql = "select body_title, body_score, summary_total_count, body_total_count, author, body_new_line_count, body_ruby_count, body_scat_count \
            from works where body_score > 0 and body_total_count > 0"
        score_count = pd.read_sql(sql=count_sql, con=connection, index_col='body_title')
        work_len = score_count.body_total_count
        summary_len = score_count.summary_total_count
        summary_rate = summary_len / work_len * 100
        newline_rate = score_count.body_new_line_count/work_len * 100
        ruby_rate = score_count.body_ruby_count/work_len * 100
        scat_rate = score_count.body_scat_count/work_len * 100

        score_count["summary_rate"] = summary_rate
        score_count["newline_rate"] = newline_rate
        score_count["ruby_rate"] = ruby_rate
        score_count["scat_rate"] = scat_rate
        print(score_count)
        model = KMeans(n_clusters=7, random_state=0)
        # data = score_count[['summary_rate', 'newline_rate', 'ruby_rate', 'scat_rate']]
        data = score_count[['newline_rate', 'ruby_rate', 'scat_rate']]
        # data = score_count[['summary_rate']]
        # data = score_count[['newline_rate']]
        # data = score_count[['ruby_rate', 'scat_rate']]
        # data = score_count[['ruby_rate']]
        # data = score_count[['scat_rate']]
        cluster_mean = model.fit(data)
        cluster = cluster_mean.labels_
        score_count['cluster'] = cluster
        score_count = score_count.sort_values('cluster', ascending=True)
        print(score_count)
        score_count.to_csv("data/cluster_author.csv")
        scatter_table = pd.pivot_table(score_count, index='author', columns='cluster', values='scat_rate', aggfunc=len, fill_value=0)

        print(pd.pivot_table(score_count, index='author', columns='cluster',aggfunc=len, fill_value=0))
        scatter_table.to_csv("data/cluster_author_pivot.csv")

        fig = plt.figure()
        axes = fig.subplots(1,1)
        # fig.set_size_inches((12, 9))
        sns.set_style('whitegrid', rc={'legend.frameon':False})
        sns.set_context(font_scale=1, rc={'legend.fontsize':10})
        ax_score = axes
        # # ax_summary = axes[0,1]
        # # ax_body = axes[0,2]
        # # ax_newline = axes[1,0]
        # # ax_ruby = axes[1,1]        
        # # ax_scat = axes[1,2]        

        ax_score= sns.clustermap(scatter_table, alpha=0.8, cmap='summer', standard_scale=1)

        # # ax_summary= sns.swarmplot(x='cluster', y='summary_total_count', data=score_count, hue='author', alpha=0.8, ax=ax_summary)        
        # # ax_summary.set_title("summary len")

        # # ax_body= sns.swarmplot(x='cluster', y='body_total_count', data=score_count,hue='author',  alpha=0.8, ax=ax_body)        
        # # ax_body.set_title("total len")

        # # ax_newline= sns.swarmplot(x='cluster', y='newline_rate', data=score_count,hue='author',  alpha=0.8, ax=ax_newline)        
        # # ax_newline.set_title("newline rate")

        # # ax_ruby= sns.swarmplot(x='cluster', y='ruby_rate', data=score_count,hue='author',  alpha=0.8, ax=ax_ruby)        
        # # ax_ruby.set_title("ruby rate")

        # # ax_scat= sns.swarmplot(x='cluster', y='scat_rate', data=score_count, hue='author', alpha=0.8, ax=ax_scat)        
        # # ax_scat.set_title("scat rate")

        ax_score = plt.gca()
        fig.tight_layout()        
        plt.show()