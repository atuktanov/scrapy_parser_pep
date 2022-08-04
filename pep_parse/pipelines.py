import datetime as dt

from pep_parse.settings import BASE_DIR


class PepParsePipeline:
    statuses = {}
    total = 0

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.total += 1
        self.statuses[item['status']] = (
            self.statuses.get(item['status'], 0) + 1)
        return item

    def close_spider(self, spider):
        filepath = BASE_DIR / 'results'
        filepath.mkdir(exist_ok=True)
        now = dt.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'status_summary_{now}.csv'
        with open(filepath / filename, mode='w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            for stat in self.statuses:
                f.write(f'{stat},{self.statuses[stat]}\n')
            f.write(f'Total,{self.total}\n')
