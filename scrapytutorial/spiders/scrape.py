import scrapy


class ScrapeSpider(scrapy.Spider):
    name = 'scrape'
    allowed_domains = ['ss1.scrape.center']
    start_urls = ['http://ss1.scrape.center/']

    def parse(self, response):
        pass
