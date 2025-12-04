import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/numerical/']

    def parse(self, response):
        pep_links = response.css('a.pep::attr(href)').getall()
        for pep_link in pep_links:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        title: str = response.css('h1.page-title::text').get().strip()
        # Пример заголовка 'PEP 2 – Procedure for Adding New Modules'
        # между номером и наименованием стандарта символ юникода 8211
        # наименование тоже может содержать тире, поэтому ограничиваем split
        number_string, name = title.split(' – ', 1)
        yield PepParseItem(
            number=int(number_string.replace('PEP', '').strip()),
            name=name,
            status=response.css(
                'dt:contains("Status") + dd > abbr::text').get()
        )
