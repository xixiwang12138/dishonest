import scrapy
import json
from jsonpath import jsonpath
import re




class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    # 1. 准备起始URL
    start_urls = [
        'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信人名单&pn=3150&rn=10&ie=utf-8&oe=utf-8&format=json']
    url_pattern = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信人名单&pn={}&rn=10&ie=utf-8&oe=utf-8&format=json'

    def parse(self, response):
        # 1. json数据转换为字典
        data = json.loads(response.text)
        # 2. 获取总数据条数
        total_num = jsonpath(data, '$..dispNum')[0]
        # 3. 构建所有页面的请求的URL, 交给引擎
        for num in range(0, total_num, 50):
            # 根据URL模板, 生成URL
            url = self.url_pattern.format(num)
            yield scrapy.Request(url, callback=self.parse_data)

    def parse_data(self, response):
        """解析数据"""
        # 把json字符串转换为python的字典
        data = json.loads(response.text)
        # 获取失信人信息
        results = jsonpath(data, '$..result')[0]
        for result in results:
            print(result)
            item = DishonestItem()
            # 把抓取到数据, 交个引擎
            item['name'] = result['iname']
            item['card_num'] = result['cardNum']
            item['content'] = re.sub('%s+', '', result['duty'])
            item['business_entity'] = result['businessEntity']

            item['publish_unit'] = result['courtName']
            item['publish_date'] = result['publishDate']

            # 把数据交给引擎
            yield item
