# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class GithubMostStarsItem(Item):
    # 一级信息
    name = Field()
    star = Field()
    url = Field()
    desc = Field()


