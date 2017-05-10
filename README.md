### 0.环境搭建
```
sudo pip install scrapy

//可以考虑配置一下python源
详见下面链接
```
[python,pip配置镜像提升安装速度](http://www.liaobaocheng.com/blog/post/python-mirror-speed-installation)

### 1.开始项目
> 生成一个爬虫

```

scrapy  startproject github_most_stars

scrapy genspider -t crawl easy most_stars
```

### 2.编写Item
```
from scrapy.item import Item, Field


class GithubMostStarsItem(Item):
    # 一级信息
    name = Field()
    star = Field()
    url = Field()
    desc = Field()
```

### 3.编写easy逻辑
```
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from github_most_stars.items import GithubMostStarsItem

class EasySpider(CrawlSpider):
    name = 'electron'
    allowed_domains = ['github.com']
    download_delay = 5

    start_urls = ['https://github.com/search?o=desc&p=1&q=electron&ref=opensearch&s=stars&type=Repositories']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//em[@class="current"]'), callback="next_page"),  # 翻页规则
        Rule(LinkExtractor(restrict_xpaths='//*[@class="v-align-middle"]'), callback='parse_item')  # 本页规则
    )

    def start_requests(self):
        reqs = []
        for i in range(1, 101):
            req = scrapy.Request("https://github.com/search?o=desc&p=%s&q=electron&ref=opensearch&s=stars&type=Repositories" % i)
            reqs.append(req)
        return reqs

    def next_page(self, page):
        next_url = int(page) + 1
        url = "https://github.com/search?o=desc&p=%s&q=electron&ref=opensearch&s=stars&type=Repositories" % next_url
        return url


    def parse_item(self, response):
        l = ItemLoader(item=GithubMostStarsItem(), response=response)
        l.add_value('url',response.url)
        l.add_xpath('name','//*[@id="js-repo-pjax-container"]/div[1]/div[1]/h1/strong/a/text()')
        l.add_xpath('star','normalize-space(//*[@id="js-repo-pjax-container"]/div[1]/div[1]/ul/li[2]/a[2])')
        #l.add_xpath('stars','normalize-space(//*[@id="js-repo-pjax-container"]/div[1]/div[1]/ul/li[2]/div/form[1]/a/text())')
        l.add_xpath('desc','normalize-space(//*[@id="js-repo-pjax-container"]/div[2]/div[1]/div[1]/div/div/span)')
        return l.load_item()
```

使用Chrome插件Xpath-Helper可以提升查找效率，[插件地址](https://chrome.google.com/webstore/detail/xpath-helper/hgimnogjllphhhkhlmebbmlgjoejdpjl)

遇到的坑
-  1.使用download_delay解决429(太多请求)的问题
-  2.在chrome是使用xpath可以获取到star，scrapy中却不可以，因为scrapy中的响应和浏览器响应不一样，所以有必要使用scrapy shell再次验证xpath选择器


### 4.编写pipeline
>使用了dataset这个简化了数据库操作的包，很不错，我用的是postgresql
>
>sudo pip install dataset
>
>sudo pip install psycopg2

[Ubuntu上如何安装postgresql教程](http://www.liaobaocheng.com/blog/post/postgresql-tutorial-updating)

```
from scrapy.utils.project import get_project_settings
import dataset,codecs,os,json


SETTINGS = get_project_settings()


class GithubMostStarsPipeline(object):
    def __init__(self):
        db = dataset.connect('postgresql://liaobaocheng:liaobaocheng@localhost:5432/electron')
        self.table = db['github']


    def process_item(self, item, spider):
        self.table.insert(dict(name=item['name'],url=item['url'],desc=item['desc'],star=item['star']))
        return item


class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('scraped_data_utf8.json', 'w', encoding='utf-8')
        self.file.write('[')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.write(']')
        self.file.close()
```

- 1.使用了postgresql存储数据
- 2.使用了json为pipeline保存结果


### 5.settings设置
```
FEED_EXPORT_ENCODING = 'utf-8'

RETRY_TIMES = 10
# RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408, 429]
# PROXY_LIST = '/home/liaobaocheng/Python/github_most_stars/proxy_list.txt'
# PROXY_MODE = 0

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 80,
    # 'github_most_stars.middlewares.ProxyMiddleware': 40,
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 10,
}

# add item pipeline
ITEM_PIPELINES = {'github_most_stars.pipelines.GithubMostStarsPipeline': 400,
                  'github_most_stars.pipelines.JsonWithEncodingPipeline': 401
                  }
```

配置了ITEM_PIPELINES和DOWNLOAD_MIDDLEWARES，还有重试次数，继续实战中学习scrapy吧

[本案例项目地址](https://github.com/liaobaocheng/github_most_stars)
![项目真相](/storage/vendor/Screenshot%20from%202017-05-10%2018-16-50.png)

### 6.bonus加点点
[查看github上点赞数最多的项目,从高到低](https://github.com/search?q=stars%3A%3E1&ref=opensearch)

>如何爬其他数据，将url中的关键字替换成自己感兴趣的次就可以了https://github.com/search?o=desc&p=1&q=electron&ref=opensearch&s=stars&type=Repositories


