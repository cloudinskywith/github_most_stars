from scrapy.utils.project import get_project_settings
import dataset


SETTINGS = get_project_settings()


class GithubMostStarsPipeline(object):
    def __init__(self):
        db = dataset.connect('mysql://root:root@localhost/electron')
        self.table = db['github']

    def process_item(self, item, spider):
        self.table.insert(dict(name=item['name'],url=item['url'],desc=item['desc'],star=item['star']))
        return item


