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

from scrapy import Spider, Request
import time
import sqlite3
import pandas as pd
import YangGuangJinKe.gl as gl
from bs4 import BeautifulSoup
import re
from YangGuangJinKe.items import YangGuangJinKeItem


class YangGuangJinKeSpider(Spider):
    name = 'yangGuangJinKe'
    allowed_domains = ['https://osms.sinosig.com/','https://osms-web-prd.hyan-tech.com']
    start_urls=[]
    df_name = pd.read_excel("name.xlsx")
    for each in range(0, len(df_name)):
        gl.search_name = (df_name.iloc[[each], [0]].values[0][0])
        gl.search_bdh = (df_name.iloc[[each], [1]].values[0][0])
        gl.search_sfzh = (df_name.iloc[[each], [1]].values[0][0])
        # print(search_bdh,search_name)
        start_urls.append('https://osms-web-prd.hyan-tech.com/#/caseDetails?policyCode={}&name={}'.format(gl.search_bdh,gl.search_name))

    print("*" * 30, start_urls, "*" * 30)



    def parse(self, response):

        if "苏州应时雨商务信息咨询有限公司" in response.text:
            with open(r'temp\{}.html'.format(int(round(time.time() * 1000))), 'w', encoding='utf8') as f:
                f.write(response.text)

            item = YangGuangJinKeItem()

            soup = BeautifulSoup(response.text, 'lxml')

            item['bdh'] = soup.find_all('span', class_="caseContainerLeft_tile_policyNo")[0].text

            current_name = soup.find_all('span', class_="caseContainerLeft_tile_name")[0].text
            item['name'] = current_name
            item['sfzh'] = soup.select(
                '#app > div > div > section > div.el-tabs.el-tabs--top > div.el-tabs__content > div.containter > div.row-content.el-row.is-justify-space-between.el-row--flex > div.el-col.el-col-18 > div > div.carousel1.el-carousel.el-carousel--horizontal > div > div.el-carousel__item.is-active.is-animating > div > div > div:nth-child(4) > div:nth-child(1) > div > span')[
                0].text


            df = pd.read_html(response.text)
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
            my_df = df[3]
            print('{0}的联系方式纪录数'.format(current_name), len(my_df))
            # 本人手机号
            item['br_mobile'] = my_df[(my_df[2] == "本人") & (my_df[3] == "移动电话")].values[0][0]
            # item['br_mobile'] = my_df[(my_df[1] == "本人") & (my_df[3] == "移动电话")].values[0][0]


            # 配偶姓名
            try:
                item['pe_name'] = my_df[(my_df[2] == "配偶") & (my_df[3] == "移动电话")].values[0][1]
                # item['pe_name']= my_df[(my_df[1] == "配偶") & (my_df[3] == "移动电话")].values[0][1]
            except:
                item['pe_name'] = ""
            # 配偶手机号
            try:
                item['pe_mobile'] = my_df[(my_df[2] == "配偶") & (my_df[3] == "移动电话")].values[0][0]
                # item['pe_mobile'] = my_df[(my_df[1] == "配偶") & (my_df[3] == "移动电话")].values[0][0]
            except:
                item['pe_mobile'] = ""

            # 兄弟姓名
            try:
                item['xd_name'] = my_df[(my_df[2] == "兄弟") & (my_df[3] == "移动电话")].values[0][1]
                # item['xd_name'] = my_df[(my_df[1] == "兄弟") & (my_df[3] == "移动电话")].values[0][1]
            except:
                item['xd_name'] = ""
            # 兄弟手机号
            try:
                item['xd_mobile'] = my_df[(my_df[2] == "兄弟") & (my_df[3] == "移动电话")].values[0][0]
                # xd_mobile = my_df[(my_df[1] == "兄弟") & (my_df[3] == "移动电话")].values[0][0]
            except:
                item['xd_mobile'] = ""

            # 父亲姓名
            try:
                item['fq_name'] = my_df[(my_df[2] == "父亲") & (my_df[3] == "移动电话")].values[0][1]
                # item['fq_name'] = my_df[(my_df[1] == "父亲") & (my_df[3] == "移动电话")].values[0][1]
            except:
                item['fq_name'] = ""
            # 父亲手机号
            try:
                item['fq_mobile'] = my_df[(my_df[2] == "父亲") & (my_df[3] == "移动电话")].values[0][0]
                # item['fq_mobile'] = my_df[(my_df[1] == "父亲") & (my_df[3] == "移动电话")].values[0][0]
            except:
                item['fq_mobile'] = ""

            # 母亲姓名
            try:
                item['mq_name'] = my_df[(my_df[2] == "母亲") & (my_df[3] == "移动电话")].values[0][1]
                # item['mq_name'] = my_df[(my_df[1] == "母亲") & (my_df[3] == "移动电话")].values[0][1]
            except:
                item['mq_name'] = ""
            # 母亲手机号
            try:
                item['mq_mobile'] = my_df[(my_df[2] == "母亲") & (my_df[3] == "移动电话")].values[0][0]
                # item['mq_mobile'] = my_df[(my_df[1] == "母亲") & (my_df[3] == "移动电话")].values[0][0]
            except:
                item['mq_mobile'] = ""

            # 同事姓名
            try:
                item['ts_name'] = my_df[(my_df[2] == "同事") & (my_df[3] == "移动电话")].values[0][1]
                # item['ts_name'] = my_df[(my_df[1] == "同事") & (my_df[3] == "移动电话")].values[0][1]
            except:
                item['ts_name'] = ""
            # 同事手机号
            try:
                item['ts_mobile'] = my_df[(my_df[2] == "同事") & (my_df[3] == "移动电话")].values[0][0]
                # item['ts_mobile'] = my_df[(my_df[1] == "同事") & (my_df[3] == "移动电话")].values[0][0]
            except:
                item['ts_mobile'] = ""

            # 其他姓名
            try:
                item['qt_name'] = my_df[(my_df[2] == "其他") & (my_df[3] == "移动电话")].values[0][1]
                # item['qt_name'] = my_df[(my_df[1] == "其他") & (my_df[3] == "移动电话")].values[0][1]
            except:
                item['qt_name'] = ""
            # 其他手机号
            try:
                item['qt_mobile'] = my_df[(my_df[2] == "其他") & (my_df[3] == "移动电话")].values[0][0]
                # item['qt_mobile'] = my_df[(my_df[1] == "其他") & (my_df[3] == "移动电话")].values[0][0]
            except:
                item['qt_mobile'] = ""

            yield item








