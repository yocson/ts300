# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
# from os import path
# from scrapy import signals
import re
import mysql.connector
from mysql.connector import errorcode

class Ts300Pipeline(object):
    def __init__(self):
        self.file = codecs.open('raw_data.txt', 'w', "utf-8")

    def process_item(self, item, spider):
        self.file.write(item['author']+'/')
        self.file.write(item['title']+'/')
        temp = item['poem']
        poem = re.sub("[\x00-\xff]", "".decode("utf8"), temp)
        self.file.write(poem)
        #self.file.write(item['link']+'\n')
        return item

    def spider_closed(self, spider):
        self.file.close()

class MySQLScrapyPipeline(object): 
    def __init__(self,cnx,cur):
        self.cnx = cnx
        self.cur = cur
    
    @classmethod
    def from_settings(cls,settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。 
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        config = {
            'user' : settings['MYSQL_USER'],
            'password' : settings['MYSQL_PASSWD'],
            'host' : settings['MYSQL_HOST'], #读取settings中的配置
            #'port' : settings['MYSQL_PORT'],
            'database' : settings['MYSQL_DB'],
            #charset='utf8',#编码要加上，否则可能出现中文乱码问题
        }
        cnx = mysql.connector.connect(**config)
        cur = cnx.cursor()
        return cls(cnx, cur)

    #pipeline默认调用
    def process_item(self, item, spider):
        add_poem =("INSERT INTO ts300_poem "
                   "(author, title, poem)"
                   "VALUES (%s, %s, %s)")
        item['poem'] = re.sub("[\x00-\xff]", "".decode("utf8"), item['poem'])
        data_poem = (item['author'], item['title'], item['poem'])
        self.cur.execute(add_poem, data_poem)
        self.cnx.commit()
        return item
    
    def spider_closed(self, spider):
        self.cnx.close()