import scrapy


class PepParseItem(scrapy.Item):
    """Элемент данных, представляющий один PEP (Python Enhancement Proposal).

    Используется пауком для передачи извлечённой информации о PEP
    в пайплайны и экспортёры.

    Ключи:
        number (int): Номер PEP (например, 8 для PEP 8).
        name (str): Название PEP.
        status (str): Текущий статус PEP (например, "Active", "Final").
    """

    number: int = scrapy.Field()
    name: str = scrapy.Field()
    status: str = scrapy.Field()
