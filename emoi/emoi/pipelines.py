# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

class EmoiPipeline(object):
    def open_spider(self, spider):
        self.file = open(spider.name + '_' + time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.tsv', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.file.write(item['murl'])
        self.file.write("\t")
        self.file.write(item['purl'])
        self.file.write("\t")
        self.file.write(item['title'].replace('\n',' ').replace('\r', ' ').replace('\t', ' '))
        self.file.write("\n")
        self.file.flush()
        return item
