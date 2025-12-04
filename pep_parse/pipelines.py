import csv
from collections import Counter
from datetime import datetime
from pathlib import Path

from scrapy.item import Item
from scrapy.spiders import Spider

BASE_DIR = Path(__file__).parent


class PepParsePipeline:

    def open_spider(self, spider: Spider) -> None:
        self.status_counter: Counter[str, int] = Counter()

    def process_item(self, item: Item, spider: Spider) -> Item:
        self.status_counter[item['status']] += 1
        return item

    def close_spider(self, spider: Spider) -> None:
        RESULTS_DIR: Path = BASE_DIR / 'results'
        RESULTS_DIR.mkdir(exist_ok=True)
        timestamp: str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename: Path = RESULTS_DIR / f'status_summary_{timestamp}.csv'

        total: int = sum(self.status_counter.values())

        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['status', 'count'])
            for status, count in sorted(self.status_counter.items()):
                writer.writerow([status, count])
            writer.writerow(['Total', total])
