
# 准备请求的URL
import json

import requests
import scrapy
from jsonpath import jsonpath

from model import DishonestItem

url = 'http://jszx.court.gov.cn/api/front/getPublishInfoPageList'

data = {
    'pageNo': 2, # 当前页号
    'pageSize': 10, # 页面容量
    'orderBy': 1  # 排序方式
}

response = requests.post(url, data=data)
print(response.content.decode())
data =  json.loads(response.content.decode())
result = jsonpath(data, '$..data')
print(len(result[0]))


class CourtSpider(scrapy.Spider):
    name = 'court'
    allowed_domains = ['court.gov.cn']
    # POST请求的URL
    url = 'http://jszx.court.gov.cn/api/front/getPublishInfoPageList'

    def start_requests(self):
        """构建起始请求"""

        data = {
            'pageNo': '1',  # 当前页号
            'pageSize': '10',  # 页面容量
            'orderBy': '1'  # 排序方式
        }
        # 构建起始请求
        yield scrapy.FormRequest(self.url, formdata=data,  callback=self.parse)


    def parse(self, response):
        # 获取总页数
        page_count = json.loads(response.text)['pageCount']
        # 生成所有页面请求
        for i in range(1, page_count):
            data = {
                'pageNo': str(i),  # 当前页号
                'pageSize': '10',  # 页面容量
                'orderBy': '1'  # 排序方式
            }
            yield scrapy.FormRequest(self.url, formdata=data, callback=self.parse_data)


    def parse_data(self, response):
        """解析响应数据"""
        datas = json.loads(response.text)['data']
        for data in datas:
            item = DishonestItem()
            # 把抓取到数据, 交个引擎
            item['name'] = data['name']
            item['card_num'] = data['cardNum']
            item['area_name'] = data['areaName']
            item['content'] = data['duty']
            item['business_entity'] = data['buesinessEntity']
            item['publish_unit'] = data['courtName']
            item['publish_date'] = data['publishDate']

            # 把数据交给引擎
            yield item

