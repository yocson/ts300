# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from os import path
from scrapy import signals

class Ts300Pipeline(object):
    def __init__(self):
        self.file = codecs.open('raw_data.txt', 'w', "utf-8")

    def process_item(self, item, spider):
        self.file.write(item['author']+'/')
        self.file.write(item['title'])
        self.file.write(item['link']+'\n')
        return item