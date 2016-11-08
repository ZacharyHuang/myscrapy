# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from emoi.items import EmoiItem


class Qqtu8V1Spider(CrawlSpider):
    name = "qqtu8_v1"
    allowed_domains = ["www.qqtu8.com"]
    start_urls = ['http://www.qqtu8.com/']

    rules = (
        Rule(LinkExtractor(allow=('(class)|(display)_\d+\.html?'), deny=('(link\.htm)|(about\.htm)|(qqxz\.htm)'))),
        Rule(LinkExtractor(allow=('display_\d+\.html?')), callback='parse_page')
    )

    def parse(self, response):
        img = response.xpath('//td[@id="purl"]//img')
        title = img.xpath('@alt').extract()
        yield EmoiItem(
            murl = response.urljoin(img.xpath('@src').extract()[0]),
            purl = response.url,
            meta = ('', title[0].encode('utf-8'))[len(title) > 0]
        )
