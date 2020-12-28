import scrapy
import re

class LianJiaSpider(scrapy.Spider):
    name = 'ershoufangspider'
    sitemap = 'https://bj.lianjia.com/sitemap/'
    start_urls = [ sitemap ]
    allowed_domains = [ 'lianjia.com' ]

    def parse(self, response):
        if response.url == self.sitemap:
            # extract all ershoufang deep link
            for href in response.xpath("//ul[@class='lis']/li/dl//a[contains(text(), '二手房')]/@href").getall():
                if href.startswith('/ershoufang'):
                    yield response.follow(href, self.parse)
        
        if response.url.startswith('https://bj.lianjia.com/ershoufang'):
            # extact other pages
            for href in response.xpath("//div[@class='page-box house-lst-page-box']//a/@href").getall():
                if href.startswith('/ershoufang'):
                    yield response.follow(href, self.parse)

            # extract house info
            for house in response.xpath("//ul[contains(@class,'sellListContent')]//div[contains(@class,'info')]").getall():
                item = scrapy.Selector(text=house)
                yield {
                    'url': response.urljoin(item.xpath("//*[@class='title']/a/@href").get()),
                    'title': re.sub(r'\s+', ' ', ''.join(item.xpath("//*[@class='title']//text()").getall())),
                    'position': re.sub(r'\s+', ' ', ''.join(item.xpath("//*[@class='positionInfo']//text()").getall())),
                    'info': re.sub(r'\s+', ' ', ''.join(item.xpath("//*[@class='houseInfo']//text()").getall())),
                    'follows': re.sub(r'\s+', ' ', ''.join(item.xpath("//*[@class='followInfo']//text()").getall())),
                    'tags': [re.sub(r'\s+', ' ', tag) for tag in item.xpath("//*[@class='tag']//text()").getall()],
                    'total_price': re.sub(r'\s+', ' ', ''.join(item.xpath("//*[@class='totalPrice']//text()").getall())),
                    'unit_price': re.sub(r'\s+', ' ', ''.join(item.xpath("//*[@class='unitPrice']//text()").getall())),
                }

