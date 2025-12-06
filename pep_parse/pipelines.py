import csv
from collections import Counter
from datetime import datetime
from pathlib import Path

from scrapy.spiders import Spider

from pep_parse.items import PepParseItem

BASE_DIR = Path(__file__).parent.parent
RESULTS_DIR_NAME = 'results'


class PepParsePipeline:
    """Пайплайн для агрегации статусов PEP и записи сводки в CSV-файл."""

    def open_spider(self, spider: Spider) -> None:
        """Инициализирует счётчик статусов PEP при запуске паука.

        Args:
            spider (Spider): Экземпляр запускаемого паука.
        """

        self.status_counter: Counter[str] = Counter()

    def process_item(self, item: PepParseItem, spider: Spider) -> PepParseItem:
        """Увеличивает счётчик для статуса обрабатываемого PEP.

        Args:
            item (PepParseItem): Элемент, представляющий один PEP,
                                 содержащий поля 'number', 'name', 'status'.
            spider (Spider): Паук, который извлёк данный элемент.

        Returns:
            PepParseItem: Тот же элемент без изменений.
        """

        self.status_counter[item.get('status', 'Unknown')] += 1
        return item

    def close_spider(self, spider: Spider) -> None:
        """Записывает сводный CSV-файл с количеством PEP по статусам.

        Файл содержит:
            - строки вида «status,count» для каждого уникального статуса,
            - итоговую строку «Total,<общее_количество>».

        Имя файла: results/status_summary_ГГГГ-ММ-ДД_ЧЧ-ММ-СС.csv

        Args:
            spider (Spider): Экземпляр завершаемого паука.
        """

        results_dir: Path = BASE_DIR / RESULTS_DIR_NAME
        results_dir.mkdir(exist_ok=True)
        timestamp: str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename: Path = results_dir / f'status_summary_{timestamp}.csv'

        total: int = sum(self.status_counter.values())

        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['status', 'count'])
            writer.writerows(sorted(self.status_counter.items()))
            writer.writerow(['Total', total])
