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
        item['poem'] = get_poem(item['title'], response)
        yield item


def append_poemstr(poemlist, num):
    poemstr = ''
    for sen in poemlist[0:num]:
        poemstr += sen
    return poemstr

def get_poem(title, response):
    poemstr = ''
    poemlist = response.css("p[align='center']").extract()
    if poemlist == []:
        poemstr = response.xpath("/html/body/div[3]/div[3]/div[2]/div[2]/div[2]/p[1]").extract()[0]
        exception_dict = {
            '宣州谢朓楼饯别校书叔云' : 6,
            '行路难·大道如青天' : 8
        }
        title = title.encode("utf8")
        if exception_dict.get(title):
            poemlist = response.xpath("/html/body/div[3]/div[3]/div[2]/div[2]/div[2]/p").extract()
            poemstr = append_poemstr(poemlist, exception_dict.get(title))
    else:
        poemstr = append_poemstr(poemlist, len(poemlist))
    return poemstr
        