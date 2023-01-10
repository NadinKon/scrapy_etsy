import scrapy


class ShopSpider(scrapy.Spider):
    name = 'shop'
    start_urls = ['https://www.etsy.com/search/shops?ref=empty_redirect']

    def parse(self, response, **kwargs):
        for link in response.css('div.wt-grid__item-xs-12.wt-grid__item-md-6.wt-grid__item-lg-4.wt-grid__item-xl-3.wt-pr-md-4.wt-mb-xs-6 a::attr(href)'):
            yield response.follow(link, callback=self.parse_book)

        for i in range(1, 3):
            next_page = f'https://www.etsy.com/search/shops?ref=pagination&page={i}/'
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        yield {
            "name": response.css('h1.wt-text-heading-01.wt-text-truncate::text').get(),
            "link": response.css('span.wt-text-caption.wt-no-wrap::text').get()
        }