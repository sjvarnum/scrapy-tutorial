import scrapy


# spider subclasses scrapy.Spider
class QuoteSpider(scrapy.Spider):
    name = 'quotes' # indentifies the spider
    start_urls = [
        'http://quotes.toscrape.com'
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parse)