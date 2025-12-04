import csv
from datetime import datetime
import os
from collections import Counter


class PepParsePipeline:

    def open_spider(self, spider):
        self.status_counter = Counter()

    def process_item(self, item, spider):
        self.status_counter[item['status']] += 1
        return item

    def close_spider(self, spider):
        os.makedirs('results', exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'results/status_summary_{timestamp}.csv'

        total = sum(self.status_counter.values())

        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['status', 'count'])
            for status, count in sorted(self.status_counter.items()):
                writer.writerow([status, count])
            writer.writerow(['Total', total])
