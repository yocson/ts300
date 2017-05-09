# -*- coding: utf-8 -*-

import scrapy
from ts300.items import Ts300Item

class Ts300Spider(scrapy.Spider):
    name = 'ts300'
    allowed_domians = ["gushiwen.org"]

    start_urls = [
        "http://www.gushiwen.org/gushi/tangshi.aspx"
    ]

    def parse(self, response):
        for element in response.xpath("//*[@class='guwencont2']/a"):
            item = Ts300Item()
            authortitle = element.xpath("text()").extract()[0]
            try:
                item['author'] = authortitle.split("(")[1].split(")")[0]
            except:
                continue
            item['title'] = authortitle.split("(")[0]
            item['link'] = element.xpath("@href").extract()[0]
            yield item
