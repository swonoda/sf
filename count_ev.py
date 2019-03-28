import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
from collections import OrderedDict
import matplotlib.cm as cm

class CountEv:
    plt.style.use('ggplot')
    connection_config = {
        'host': 'localhost',
        'port': '5432',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'postgres'
    }

    def analysis_body_summary(self) :
        connection = psycopg2.connect(**self.connection_config)
        count_sql = "select body_title, summary_total_count, body_total_count, author from works where body_total_count > 0 and body_total_count < 40000"
        score_count = pd.read_sql(sql=count_sql, con=connection, index_col='body_title')
        print(score_count)
        x = {}
        y = {}
        i = 0
        for user in score_count.author :
            if not (user in x.keys()) :
                x[user] = score_count[score_count.author==user].summary_total_count
                y[user] = score_count[score_count.author==user].body_total_count
                plt.scatter(x[user], y[user], color=cm.summer(i/22.0), alpha=0.5, s=50+10*i)
                i = i + 1

        # グラフ表示
        plt.show()
