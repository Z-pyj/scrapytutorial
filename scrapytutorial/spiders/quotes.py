import scrapy

from scrapytutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    # 爬虫名，启动爬虫时需要的参数必须
    name = 'quotes'
    # 爬取域范围，允许爬虫在这个域名下进行爬取（可选）
    allowed_domains = ['quotes.toscrape.com']
    # 起始url列表，爬虫执行后第一批请求，将从这个列表中获取
    start_urls = ['https://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            # text = quote.css('.text::text').extract_first()
            # author = quote.css('.author::text').extract_first()
            # tags = quote.css('.tags .tag::text').extract()
            item = QuoteItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            # 字段赋值给item并返回item
            yield item
        # 获取下一页的地址
        next = response.css('.pager .next a::attr("href")').extract_first()
        # 拼接下一页的地址
        url = response.urljoin(next)
        # 执行的命令
        '''
        1. 控制台输出：scrapy crawl quotes
        2. 每个item以后json：scrapy crawl quotes -o quotes.jl
        3. 输入到json文件中：scrapy crawl quotes -o quotes.json

        '''
        # 构造一个全新的Request，回调方法使用parse方法，这个Requst方法执行完成后，Response会重新经过
        # parsse方法处理，得到第二页的解析结果，直到最后一页
        yield scrapy.Request(url=url, callback=self.parse)