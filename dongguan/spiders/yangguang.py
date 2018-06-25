# -*- coding: utf-8 -*-
import scrapy
from dongguan.items import DongguanItem

class YangguangSpider(scrapy.Spider):
    name = 'yangguang'
    allowed_domains = ['wz.sun0769.com']
    offset = 0
    url = 'http://wz.sun0769.com/index.php/question/report?page='
    start_urls = [url + str(offset)]

    def parse(self, response):
        links = response.xpath('//div[@class="greyframe"]//table//a[@class="news14"]/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_details)

        if self.offset <= 121950:
            self.offset += 30
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)


    def parse_details(self, response):
        item = DongguanItem()
        item['name'] = response.xpath('//div[@class="pagecenter p3"]//strong[@class="tgray14"]/text()').extract()[0]
        print(item['name'])
        item['num'] = item['name'].split(' ')[-1].split(":")[-1]
        item['detail_link'] = response.url
        item['content'] = response.xpath('//div[@class="content text14_2"]/div/text()').extract()[0]
        yield item




