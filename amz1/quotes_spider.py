import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/tag/humor/']

    def parse(self, response):
        for quote in response.css('div.quotes'):
            yield {
                'author': quote.xpath('span/small/text()').get(),
                'text': quote.css('span/text()').get,
            }
        next_page = response.css('li.next a::attr("href")').get()
        if next_page is None:
            yield response.follow(next_page,self.parse)
