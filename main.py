# -*- coding:utf-8 -*-

import selfevinfo
import worksinfo
import postgres_controller
import ev_diff
import sys
import score_ev
import count_ev

if __name__ == "__main__":
    if (sys.argv[1] == "-c") :
        works = worksinfo.WorksInfo(False)
        works.scraping()
    elif (sys.argv[1] == "-cu") :
        works = worksinfo.WorksInfo(True)
        works.scraping()
    elif(sys.argv[1] == "-self_ev"):
        selfinfo = selfevinfo.Selfevinfo()
        selfinfo.scraping()
    elif (sys.argv[1] == '-a' and sys.argv[2] == 'ordinal_ev') :
        evdiff = ev_diff.Evdiff()
        evdiff.analysis_scatter_ordinal_and_ev()
        evdiff.analysis_scatter_ordinal_and_author()
        evdiff.show_plt()
    elif (sys.argv[1] == '-a' and sys.argv[2] == 'auth_ev') :
        evdiff = ev_diff.Evdiff()
        evdiff.analysis_scatter_ordinal_and_author()
        evdiff.show_plt()
    elif (sys.argv[1] == '-a' and sys.argv[2] == 'score_bodycount'):
        scorev = score_ev.ScoreEv()
        scorev.analysis_score_bodycount()
    elif (sys.argv[1] == '-a' and sys.argv[2] == 'score_newline_rate'):
        scorev = score_ev.ScoreEv()
        scorev.analysis_score_newline_rate()
    elif (sys.argv[1] == '-a' and sys.argv[2] == 'score_ruby_rate'):
        scorev = score_ev.ScoreEv()
        scorev.analysis_score_ruby_rate()
    elif (sys.argv[1] == '-a' and sys.argv[2] == 'score_scat_rate'):
        scorev = score_ev.ScoreEv()
        scorev.analysis_score_scat_rate()
    elif (sys.argv[1] == '-a' and sys.argv[2] == 'score_count_rate'):
        scorev = score_ev.ScoreEv()
        scorev.analysis_score_count_rate()
    elif (sys.argv[1] == '-a' and sys.argv[2] == 'score_summary_count'):
        scorev = score_ev.ScoreEv()
        scorev.analysis_score_summary_count()
    elif (sys.argv[1] == '-a' and sys.argv[2] == 'count') :
        countev = count_ev.CountEv()
        countev.analysis_body_summary()