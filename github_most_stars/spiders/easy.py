# -*- coding: utf-8 -*-
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
