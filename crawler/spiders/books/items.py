# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class CategoryItem(Item):
    title = Field()
    url = Field()


class BookItem(Item):
    title = Field()
    url = Field()
    price = Field()
    category = Field()
