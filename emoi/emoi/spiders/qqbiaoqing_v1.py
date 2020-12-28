# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from emoi.items import EmoiItem


class QqbiaoqingV1Spider(scrapy.Spider):
    name = "qqbiaoqing_v1"
    allowed_domains = ["http://www.qqbiaoqing.com"]
    start_urls = [
        'http://www.qqbiaoqing.com/qq/1.htm',
        'http://www.qqbiaoqing.com/qq/3000.htm',
        'http://www.qqbiaoqing.com/qq/6000.htm',
        'http://www.qqbiaoqing.com/qq/9000.htm',
        'http://www.qqbiaoqing.com/qq/12002.htm',
        'http://www.qqbiaoqing.com/qq/15000.htm',
        'http://www.qqbiaoqing.com/qq/18000.htm',
        'http://www.qqbiaoqing.com/qq/21001.htm',
        'http://www.qqbiaoqing.com/qq/24000.htm',
        'http://www.qqbiaoqing.com/qq/27001.htm',
        'http://www.qqbiaoqing.com/qq/30001.htm',
        'http://www.qqbiaoqing.com/qq/33001.htm',
        'http://www.qqbiaoqing.com/qq/36001.htm',
        'http://www.qqbiaoqing.com/qq/39001.htm',
        'http://www.qqbiaoqing.com/qq/42001.htm',
        'http://www.qqbiaoqing.com/qq/45001.htm',
        'http://www.qqbiaoqing.com/qq/48001.htm',
        'http://www.qqbiaoqing.com/qq/52001.htm',
        'http://www.qqbiaoqing.com/qq/55001.htm',
        'http://www.qqbiaoqing.com/qq/58001.htm',
        'http://www.qqbiaoqing.com/qq/61001.htm',
        'http://www.qqbiaoqing.com/qq/64001.htm',
        'http://www.qqbiaoqing.com/qq/67001.htm',
        'http://www.qqbiaoqing.com/qq/70001.htm'
    ]

    def parse(self, response):
        content = response.xpath('//div[@class="content"]')
        yield EmoiItem(
            purl = response.url,
            murl = content.xpath('div[@class="cleft"]/span/i/img/@src').extract()[0],
            meta = content.xpath('div[@class="cright"]/h1/text()').extract()[0].encode('utf-8')
        )
        next_url = content.xpath('//a[@class="po-right"]/@href').extract()
        if len(next_url) > 0:
            yield scrapy.Request(
                url = response.urljoin(next_url[0]),
                callback = self.parse
            )
