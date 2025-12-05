from typing import Generator

import scrapy
from scrapy import Request
from scrapy.http import Response

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    """Паук для сбора информации о всех PEP с сайта peps.python.org."""

    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/numerical/']

    def parse(self, response: Response) -> Generator[Request, None, None]:
        """Извлекает ссылки на отдельные PEP и запускает их парсинг.

        Args:
            response (Response): Ответ от стартовой страницы со списком PEP.

        Yields:
            Request: Запрос к странице отдельного PEP с callback-функцией.
        """

        pep_links = response.css('a.pep::attr(href)').getall()
        for pep_link in pep_links:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(
            self, response: Response) -> Generator[PepParseItem, None, None]:
        """Парсит страницу отдельного PEP и формирует элемент данных.

        Обрабатывает заголовок, который может содержать вложенные HTML-теги
        (например, <code>), и извлекает номер, название и статус PEP.

        Args:
            response (Response): Ответ со страницы конкретного PEP.

        Yields:
            PepParseItem: Элемент, содержащий номер, название и статус PEP.
        """

        # В заголовке могут быть вложенные теги, например <code> в PEP 499.
        title: str = ''.join(response.css(
            'h1.page-title *::text').getall()).strip()
        # или
        # title: str = response.xpath(
        #     'string(//h1[@class="page-title"])').get().strip()

        # Пример заголовка 'PEP 2 – Procedure for Adding New Modules',
        # между номером и наименованием стандарта символ юникода 8211,
        # наименование тоже может содержать тире, поэтому ограничиваем split
        number_string, name = title.split(' – ', 1)
        yield PepParseItem(
            number=int(number_string.replace('PEP', '').strip()),
            name=name,
            status=response.css(
                'dt:contains("Status") + dd > abbr::text').get()
        )
