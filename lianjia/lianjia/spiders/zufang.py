import scrapy
import re

class ZuFangSpider(scrapy.Spider):
    name = 'zufangspider'
    sitemap = 'https://bj.lianjia.com/sitemap/'
    start_urls = [ sitemap ]
    allowed_domains = [ 'lianjia.com' ]

    def parse(self, response):
        if response.url == self.sitemap:
            # extract all zufang deep link
            for href in response.xpath("//ul[@class='lis']/li/dl//a[contains(text(), '租房') and not(contains(text(), '地铁'))]/@href").getall():
                if href.startswith('/zufang'):
                    yield response.follow(href, self.parse)
        
        if response.url.startswith('https://bj.lianjia.com/zufang'):
            # extact other pages
            for href in response.xpath("//div[@class='content__pg']//a/@href").getall():
                if href.startswith('/zufang'):
                    yield response.follow(href, self.parse)
            # extract house info
            for house in response.xpath("//*[contains(@class, 'content__list--item--main')]").getall():
                item = scrapy.Selector(text=house)
                yield {
                    'url': response.urljoin(item.xpath("//*[contains(@class, 'content__list--item--title')]/a/@href").get()),
                    'title': re.sub(r'\s+', ' ', ''.join(item.xpath("//*[contains(@class, 'content__list--item--title')]//text()").getall())),
                    'desc': re.sub(r'\s+', ' ', ''.join(item.xpath("//*[contains(@class, 'content__list--item--des')]//text()").getall())),
                    'tags': [re.sub(r'\s+', ' ', tag) for tag in item.xpath("//*[contains(@class, 'content__item__tag')]/text()").getall()],
                    'brand': re.sub(r'\s+', ' ', ''.join(item.xpath("//*[contains(@class, 'content__list--item--brand')]//text()").getall())),
                    'price': re.sub(r'\s+', ' ', ''.join(item.xpath("//*[contains(@class, 'content__list--item-price')]//text()").getall())),
                }