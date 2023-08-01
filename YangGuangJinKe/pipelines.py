# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3


class YangGuangJinKePipeline(object):

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
                                    ''',(item['name'], item['bdh'], item['sfzh'],item['br_mobile'],
                           item['pe_name'],item['pe_mobile'],
                           item['xd_name'], item['xd_mobile'],
                           item['fq_name'], item['fq_mobile'],
                           item['mq_name'], item['mq_mobile'],
                           item['ts_name'], item['ts_mobile'],
                           item['qt_name'], item['qt_mobile'])
                            )
        self.connection.commit()



