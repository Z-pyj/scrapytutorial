from scrapy import Request, Spider
from scrapyitempipelinedemo.scrapyitempipelinedemo.items import MovieItem

class ScrapeSpider(Spider):
    name = 'scrape'
    allowed_domains = ['ssr1.scrape.center']
    base_url = 'https://ssr1.scrape.center'
    max_page = 10

    def start_requests(self):
        for i in range(1, self.max_page + 1):
            url = f'{self.base_url}/page/{i}'
            yield Request(url, callback=self.parse_index)

    def parse_index(self, response):
        node_list = response.css('.el-card')
        for node in node_list:
            href = node.css('.name::attr(href)').get()
            url = response.urljoin(href)
            yield Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        item = MovieItem()
        item['name'] = response.css('.m-b-sm::text').get()
        item['categories'] = response.css('.category span::text').getall()
        item['score'] = response.css('.score::text').get()
        item['drama'] = response.css('.drama p::text').get()
        item['directors'] = response.css('.director .el-card__body .name::text').getall()
        item['actors'] = response.css('.actor .el-card__body .name::text').getall()

