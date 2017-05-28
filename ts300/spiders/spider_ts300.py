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
        cat_dict = {
            'guwencont2' :"五言绝句",
            'guwencont21':"七言绝句",
            'guwencont22':"五言律诗",
            'guwencont23':"七言律诗",
            'guwencont24':"五言古诗",
            'guwencont25':"七言古诗",
            'guwencont26':"乐府",
        }
        for element in response.xpath("//*[@class='guwencont2']/a")[0:-2]:
            item = Ts300Item()
            poem_url = element.xpath("@href").extract()[0]
            cat = element.xpath("./..").extract()[0].split("\"")[1].split("\"")[0]
            item['cat'] = cat_dict[cat].decode('utf8')
            yield scrapy.Request("http://www.gushiwen.org"+poem_url, meta={'item': item}, callback=self.parse_poem)
            
    def parse_poem(self, response): 
        item = response.meta['item']
        author = response.xpath("//*[@class='titleft']/a/strong/text()").extract()
        if author == []:
            author = response.xpath("//*[@class='titleft']/span/strong/text()").extract()
        item['author'] = author[0]
        item['title'] = response.xpath("//*[@class='authorTile']/h1/text()").extract()[0]
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
        poemstr = response.xpath("//*[@class='authorShow']/p[1]").extract()[0]
        exception_dict = {
            '宣州谢朓楼饯别校书叔云' : 6,
            '行路难·大道如青天' : 8
        }
        title = title.encode("utf8")
        if exception_dict.get(title):
            poemlist = response.xpath("//*[@class='authorShow']/p").extract()
            poemstr = append_poemstr(poemlist, exception_dict.get(title))
    else:
        poemstr = append_poemstr(poemlist, len(poemlist))
    return poemstr
        