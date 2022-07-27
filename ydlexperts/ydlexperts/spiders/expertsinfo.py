import scrapy
from ydlexperts.items import YdlexpertsItem


class ExpertsinfoSpider(scrapy.Spider):
    name = 'expertsinfo'
    allowed_domains = ['testwww.ydl.com']
    base_url = 'https://testwww.ydl.com/experts/p'
    index = 1
    start_urls = [base_url + str(index)]

    def parse(self, response):
        expert_list = response.css('.expertsList_items .item')
        index_num = response.css('.page-tab-tog .totle::text').get()[1:-2]
        print(index_num)

        if self.index > int(index_num):
            return
        for expert in expert_list:
            item = YdlexpertsItem()
            item['expertName'] = expert.css('.info h3 a::text').get().strip()
            print(item['expertName'])
            item['footnotelabel'] = expert.css('.info .txt p::text').get().strip()
            item['numberOfSpaces'] = expert.css('.number1::text').get().strip()

            yield item

        self.index += 1
        url = self.base_url + str(self.index)
        print(url)

        yield scrapy.Request(url, callback=self.parse)
