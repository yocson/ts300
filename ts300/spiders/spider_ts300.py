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
        links = []
        for element in response.xpath("//*[@class='guwencont2']/a"):
            links.append(element.xpath("@href").extract()[0])
            
        for poem_url in links:
            yield scrapy.Request("http://www.gushiwen.org"+poem_url, self.parse_poem)

    def parse_poem(self, response): 
        item = Ts300Item()
        item['author'] = response.xpath("/html/body/div[3]/div[3]/div[2]/div[1]/div[1]/a/strong/text()").extract()[0]
        item['title'] = response.xpath("/html/body/div[3]/div[3]/div[2]/div[2]/div[1]/h1/text()").extract()[0]
        poemstr = ''
        poemlist= response.css("p[align='center']").extract()
        if poemlist == []:
            poemstr = response.xpath("/html/body/div[3]/div[3]/div[2]/div[2]/div[2]/p[1]").extract()[0]
        else:
            for sen in poemlist:
                poemstr += sen
        item['poem'] = poemstr
        yield item