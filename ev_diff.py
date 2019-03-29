import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
from collections import OrderedDict
import seaborn as sns


class Evdiff:
    plt.style.use('ggplot')
    connection_config = {
        'host': 'localhost',
        'port': '5432',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'postgres'
    }

    def analysis_scatter_ordinal_and_ev(self):
        connection = psycopg2.connect(**self.connection_config)
        summary_sql = "select ordinal, summary_self_ev from works where summary_self_ev <> 'None'"
        ordinal_ev = pd.read_sql(sql=summary_sql, con=connection)
        scatter_table = pd.pivot_table(ordinal_ev, index='ordinal',
                                       columns='summary_self_ev', aggfunc=len, fill_value=0)
#        ordinal_ev = ordinal_ev.reindex(scatter_table['summary_self_ev'].sort_values(by='High', ascending=False).index)
        print(scatter_table)
        # グラフ表示
        high_sql = "select ordinal, count(summary_self_ev) from works where summary_self_ev = 'High' group by ordinal, summary_self_ev order by ordinal"
        middle_sql = "select ordinal, count(summary_self_ev) from works where summary_self_ev = 'Middle' group by ordinal, summary_self_ev order by ordinal"
        low_sql = "select ordinal, count(summary_self_ev) from works where summary_self_ev = 'Low' group by ordinal, summary_self_ev order by ordinal"
        high_ev = pd.read_sql(sql=high_sql, con=connection, index_col='ordinal')
        middle_ev = pd.read_sql(sql=middle_sql, con=connection, index_col='ordinal')
        low_ev = pd.read_sql(sql=low_sql, con=connection, index_col='ordinal')

        plt.plot(high_ev['count'], 'o', label='high', alpha=0.5, markersize=15)
        plt.plot(middle_ev['count'], 'o', label='middle', alpha=0.5, markersize=10)
        plt.plot(low_ev['count'], 'o', label='low', alpha=0.5, markersize=5)
        plt.legend()
        plt.show()

    def analysis_scatter_ordinal_and_author(self):
        connection = psycopg2.connect(**self.connection_config)
        summary_sql = "select author, summary_self_ev from works where summary_self_ev <> 'None'"
        ordinal_ev = pd.read_sql(sql=summary_sql, con=connection, index_col='author')
        scatter_table = pd.pivot_table(ordinal_ev, index='author', columns='summary_self_ev',
                                       aggfunc=len, fill_value=0)
        print(scatter_table)
        # グラフ表示
        high_sql = "select author, count(summary_self_ev) from works where summary_self_ev = 'High' group by author, summary_self_ev order by author"
        middle_sql = "select author, count(summary_self_ev) from works where summary_self_ev = 'Middle' group by author, summary_self_ev order by author"
        low_sql = "select author, count(summary_self_ev) from works where summary_self_ev = 'Low' group by author, summary_self_ev order by author"
        high_ev = pd.read_sql(sql=high_sql, con=connection, index_col='author')
        middle_ev = pd.read_sql(sql=middle_sql, con=connection, index_col='author')
        low_ev = pd.read_sql(sql=low_sql, con=connection, index_col='author')

        plt.plot(high_ev['count'], 'o', label='high', alpha=0.5, markersize=15)
        plt.plot(middle_ev['count'], 'o', label='middle', alpha=0.5, markersize=10)
        plt.plot(low_ev['count'], 'o', label='low', alpha=0.5, markersize=5)
        plt.legend()
        plt.show()

    def analysis_ev_and_score(self):
        connection = psycopg2.connect(**self.connection_config)
        summary_sql = "select author, summary_title, summary_self_ev, body_score from works where body_title <> 'None' order by body_score"
        ordinal_ev = pd.read_sql(sql=summary_sql, con=connection, index_col='summary_title')
        print(ordinal_ev)
        # グラフ表示
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        sns.set()
        sns.set_style('whitegrid')
        sns.set_palette('summer')
        ax = sns.swarmplot(x='summary_self_ev', y='body_score', data=ordinal_ev, alpha=0.5, size=10)
        ax.set_xlabel('講師との評価の差')
        ax.set_ylabel('得点')
        plt.show()
