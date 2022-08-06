import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_peps = response.css('section#numerical-index td a::attr(href)')
        for pep_link in all_peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = ''.join(
            response.css('.page-title ::text').getall()).split(' – ')
        data = {
            'number': title[0].split()[1],
            'name': title[1],
            'status': response.xpath(
                "//dt[contains(., 'Status')]/"
                "following-sibling::dd[1]/text()").get()
        }
        yield PepParseItem(data)
