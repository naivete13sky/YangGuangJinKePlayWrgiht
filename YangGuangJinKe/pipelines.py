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
        self.insert_item(item)
        return item

    def process_item0(self, item, spider):
        print('YangGuangJinKePipeline'.center(30, '❤'))
        print(item)
        return item

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS temp_table (
                                        name TEXT,
                                        bdh TEXT,
                                        sfzh TEXT
            )
        ''')

        self.connection.commit()

    def insert_item(self, item):
        self.cursor.execute('''
        INSERT INTO temp_table (name, bdh, sfzh)
                                    VALUES (?, ?, ?)
                                    ''',
                          (item['name'], item['bdh'], item['sfzh'])
                            )
        self.connection.commit()



