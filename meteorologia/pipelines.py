# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class MeteorologiaPipeline(object):

    def __init__(self, *args, **kwargs):
        self._d = {}

    def open_spider(self, spider):
        self.file = open('resultados.json', 'w')

    def close_spider(self, spider):
        print(json.dumps(self._d, ensure_ascii=False), file=self.file)
        self.file.close()

    def process_item(self, item, spider):
        self._d.update(item)
        return item
