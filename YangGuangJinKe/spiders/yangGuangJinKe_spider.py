# -*- coding: utf-8 -*-
# __author__="maple"
"""
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

from scrapy import Spider
import pandas as pd
import YangGuangJinKe.gl as gl
from bs4 import BeautifulSoup
from YangGuangJinKe.items import YangGuangJinKeItem


class YangGuangJinKeSpider(Spider):
    name = 'yangGuangJinKe'
    allowed_domains = ['https://osms.sinosig.com/','https://osms-web-prd.hyan-tech.com']
    start_urls=[]
    df_name = pd.read_excel("name.xlsx")
    for each in range(0, len(df_name)):
        gl.search_name = (df_name.iloc[[each], [0]].values[0][0])
        gl.search_bdh = (df_name.iloc[[each], [1]].values[0][0])
        start_urls.append('https://osms-web-prd.hyan-tech.com/#/caseDetails?policyCode={}&name={}'.format(gl.search_bdh,gl.search_name))


    def parse(self, response):
        if "苏州应时雨商务信息咨询有限公司" in response.text:
            item = YangGuangJinKeItem()#获取字段，字段在items.py中定义了

            soup = BeautifulSoup(response.text, 'lxml')
            item['name'] = soup.find_all('span', class_="caseContainerLeft_tile_name")[0].text
            item['bdh'] = soup.find_all('span', class_="caseContainerLeft_tile_policyNo")[0].text
            item['sfzh'] = soup.select(
                '#app > div > div > section > div.el-tabs.el-tabs--top > div.el-tabs__content > div.containter > div.row-content.el-row.is-justify-space-between.el-row--flex > div.el-col.el-col-18 > div > div.carousel1.el-carousel.el-carousel--horizontal > div > div.el-carousel__item.is-active.is-animating > div > div > div:nth-child(4) > div:nth-child(1) > div > span')[
                0].text

            df_all = pd.read_html(response.text)
            # print("df:",df)
            # my_df = df[4]
            # print("df[1]:", df[1])
            # print("df[2]:", df[2])
            # print("df[3]:", df[3])
            # print("df[4]:", df[4])
            # print("df[5]:", df[5])
            # print("df[6]:", df[6])
            # print("df[7]:", df[7])
            # print("df[8]:", df[8])
            # print("my_df:",my_df)
            my_df = df_all[3]
            print('{0}的联系方式纪录数'.format(item['name']), len(my_df))
            # 本人手机号
            item['br_mobile'] = my_df[(my_df[2] == "本人") & (my_df[3] == "移动电话")].values[0][0]

            person_relationShip_list = ["配偶","兄弟","父亲","母亲","同事","其他"]
            person_name_list = ['pe_name','xd_name','fq_name','mq_name','ts_name','qt_name']
            person_mobile_list = ['pe_mobile', 'xd_mobile', 'fq_mobile', 'mq_mobile', 'ts_mobile', 'qt_mobile']
            # 使用zip将这三个列表打包成元组的列表
            # zip会将对应位置的元素打包成元组，结果是一个可迭代对象
            # [("配偶", 'pe_name', 'pe_mobile'), ("兄弟", 'xd_name', 'xd_mobile')...]
            zipped_data = zip(person_relationShip_list, person_name_list, person_mobile_list)
            for data in zipped_data:
                person_relationShip, person_name, person_mobile = data# data是一个元组，分别表示人员关系、姓名、手机号

                # 姓名
                try:
                    item[person_name] = my_df[(my_df[2] == person_relationShip) & (my_df[3] == "移动电话")].values[0][1]
                except:
                    item[person_name] = ""
                # 手机号
                try:
                    item[person_mobile] = my_df[(my_df[2] == person_relationShip) & (my_df[3] == "移动电话")].values[0][0]
                except:
                    item[person_mobile] = ""


            item['responseText'] = response.text#网页内容也作为一个字段传给pipelines。

            yield item


