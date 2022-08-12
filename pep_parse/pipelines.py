import datetime as dt

from scrapy.exceptions import DropItem

from pep_parse.settings import BASE_DIR, RESULT_DIR


class PepParsePipeline:

    def open_spider(self, spider):
        self.statuses = {}
        self.total = 0

    def process_item(self, item, spider):
        self.total += 1
        if 'status' not in item:
            raise DropItem('Не найден ключ "status"')
        self.statuses[item['status']] = (
            self.statuses.get(item['status'], 0) + 1)
        return item

    def close_spider(self, spider):
        filepath = BASE_DIR / RESULT_DIR
        filepath.mkdir(exist_ok=True)
        now = dt.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'status_summary_{now}.csv'
        with open(filepath / filename, mode='w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            for status in self.statuses:
                f.write(f'{status},{self.statuses[status]}\n')
            f.write(f'Total,{self.total}\n')
