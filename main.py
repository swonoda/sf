# -*- coding:utf-8 -*-

import selfevinfo
import worksinfo
import postgres_controller
import ev_diff
import sys
import score_ev
import count_ev
import cluster_author

if __name__ == "__main__":
    evdiff = ev_diff.Evdiff()
    scorev = score_ev.ScoreEv()
    countev = count_ev.CountEv()
    clustauth = cluster_author.ClusterAuthor()

    if (sys.argv[1] == "-c"):
        works = worksinfo.WorksInfo(False)
        works.scraping()
    elif (sys.argv[1] == "-cu"):
        works = worksinfo.WorksInfo(True)
        works.scraping()
    elif(sys.argv[1] == "-self_ev"):
        selfinfo = selfevinfo.Selfevinfo()
        selfinfo.scraping()
    elif (sys.argv[1] == '-ad' and sys.argv[2] == 'ordinal_ev'):
        evdiff.analysis_scatter_ordinal_and_ev()
    elif (sys.argv[1] == '-ad' and sys.argv[2] == 'auth_ev'):
        evdiff.analysis_scatter_ordinal_and_author()
    elif (sys.argv[1] == '-ad' and sys.argv[2] == 'ev_count'):
        evdiff.analysis_ev_and_score()
    elif (sys.argv[1] == '-as' and sys.argv[2] == 'score_bodycount'):
        scorev.analysis_score_bodycount()
    elif (sys.argv[1] == '-as' and sys.argv[2] == 'score_newline_rate'):
        scorev.analysis_score_newline_rate()
    elif (sys.argv[1] == '-as' and sys.argv[2] == 'score_ruby_rate'):
        scorev.analysis_score_ruby_rate()
    elif (sys.argv[1] == '-as' and sys.argv[2] == 'score_scat_rate'):
        scorev.analysis_score_scat_rate()
    elif (sys.argv[1] == '-as' and sys.argv[2] == 'score_count_rate'):
        scorev.analysis_score_count_rate()
    elif (sys.argv[1] == '-as' and sys.argv[2] == 'score_summary_count'):
        scorev.analysis_score_summary_count()
    elif (sys.argv[1] == '-ac' and sys.argv[2] == 'count'):
        countev.analysis_body_summary()
    elif (sys.argv[1] == '-cluster' and sys.argv[2] == 'newline'):
        countev.clustering_body_score(sys.argv[3])
    elif (sys.argv[1] == '-cluster' and sys.argv[2] == 'scat'):
        countev.clustering_scat_score(sys.argv[3])
    elif (sys.argv[1] == '-cluster' and sys.argv[2] == 'ruby'):
        countev.clustering_ruby_score(sys.argv[3])
    elif (sys.argv[1] == '-cluster' and sys.argv[2] == 'count'):
        countev.clustering_count_score(sys.argv[3])
    elif (sys.argv[1] == '-cluster' and sys.argv[2] == 'score_newline'):
        scorev.cluster_newline()
    elif (sys.argv[1] == '-cluster' and sys.argv[2] == 'author') :
        clustauth.clustering()
