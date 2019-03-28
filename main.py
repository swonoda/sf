# -*- coding:utf-8 -*-

import selfevinfo
import worksinfo
import postgres_controller

if __name__ == "__main__":
    works = worksinfo.WorksInfo()
    works.scraping()
    works_list = works.get_works_info()

    selfinfo = selfevinfo.Selfevinfo()
    selfinfo.scraping()
    self_list = selfinfo.get_self_info()
