from scrapy import Request, Spider
from scrapyitempipelinedemo.items import MovieItem


class ScrapeSpider(Spider):
    name = 'scrape'
    allowed_domains = ['ssr1.scrape.center']
    base_url = 'https://ssr1.scrape.center'
    max_page = 1

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
        # 导演
        item['directors'] = []
        directors = response.css('.director .el-card__body')
        for director in directors:
            director_image = director.css('img').attrib['src']
            director_name = director.css('.name::text').get()
            item['directors'].append({
                'name': director_name,
                'image': director_image
            })
        # 演员
        item['actors'] = []
        actors = response.css('.actor .el-card__body')
        for actor in actors:
            actor_name = actor.css('.name::text').get()
            actor_image = actor.css('img').attrib['src']
            item['actors'].append({
                'name': actor_name,
                'image': actor_image
            })

        yield item
