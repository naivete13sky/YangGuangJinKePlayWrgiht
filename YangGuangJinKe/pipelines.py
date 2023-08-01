# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import pandas as pd

class YangGuangJinKePipeline(object):

    def __init__(self):
        pass

    def open_spider(self, spider):
        pass
        self.conn = sqlite3.connect("my_scrapy3.db")


    def close_spider(self, spider):
        pass
        self.conn.close()

    def process_item(self, item, spider):
        pass
        # 创建一条记录
        name = item['name']
        bdh = item['bdh']
        sfzh = item['sfzh']
        br_mobile = item['br_mobile']
        pe_name = item['pe_name']
        pe_mobile = item['pe_mobile']
        xd_name = item['xd_name']
        xd_mobile = item['xd_mobile']
        fq_name = item['fq_name']
        fq_mobile = item['fq_mobile']
        mq_name = item['mq_name']
        mq_mobile = item['mq_mobile']
        ts_name = item['ts_name']
        ts_mobile = item['ts_mobile']
        qt_name = item['qt_name']
        qt_mobile = item['qt_mobile']
        new = pd.DataFrame({'姓名': name,
                            '保单号': bdh,
                            '身体证号码': sfzh,
                            '本人手机号': br_mobile,
                            '配偶': pe_name,
                            '配偶手机号': pe_mobile,
                            '兄弟': xd_name,
                            '兄弟手机号': xd_mobile,
                            '父亲': fq_name,
                            '父亲手机号': fq_mobile,
                            '母亲': mq_name,
                            '母亲手机号': mq_mobile,
                            '同事': ts_name,
                            '同事手机号': ts_mobile,
                            '其他': qt_name,
                            '其他手机号': qt_mobile,
                            }, index=[1]
                           )  # 自定义索引为：1 ，这里也可以不设置index

        new.to_sql("cc", self.conn, if_exists='append', index=False)

    def create_table(self):
        pass





class YangGuangJinKePipeline_sql(object):

    def __init__(self):
        pass

    def open_spider(self, spider):
        self.connection = sqlite3.connect('my_scrapy3.db')
        self.cursor = self.connection.cursor()
        self.create_table()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        print('YangGuangJinKePipeline_insert_item'.center(30, '❤'))
        self.insert_item(item)
        return item

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS temp_table (
                                        name TEXT,
                                        bdh TEXT,
                                        sfzh TEXT,
                                        br_mobile,
                                        pe_name,
                                        pe_mobile,
                                        xd_name,
                                        xd_mobile,
                                        fq_name,
                                        fq_mobile,
                                        mq_name,
                                        mq_mobile,
                                        ts_name,
                                        ts_mobile,
                                        qt_name,
                                        qt_mobile

            )
        ''')

        self.connection.commit()

    def insert_item(self, item):
        self.cursor.execute('''
        INSERT INTO temp_table (name, bdh, sfzh,br_mobile,
                                        pe_name,pe_mobile,
                                        xd_name,xd_mobile,
                                        fq_name,fq_mobile,
                                        mq_name,mq_mobile,
                                        ts_name,ts_mobile,
                                        qt_name,qt_mobile)
                                    VALUES (?, ?, ?,?,
                                        ?,?,
                                        ?,?,
                                        ?,?,
                                        ?,?,
                                        ?,?,
                                        ?,?
                                    )
                                    ''', (item['name'], item['bdh'], item['sfzh'], item['br_mobile'],
                                          item['pe_name'], item['pe_mobile'],
                                          item['xd_name'], item['xd_mobile'],
                                          item['fq_name'], item['fq_mobile'],
                                          item['mq_name'], item['mq_mobile'],
                                          item['ts_name'], item['ts_mobile'],
                                          item['qt_name'], item['qt_mobile'])
                            )
        self.connection.commit()
