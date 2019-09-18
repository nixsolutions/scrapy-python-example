# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader.processors import MapCompose
from .loaders import CategoryLoader, BookLoader
from .items import CategoryItem, BookItem


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for item in response.xpath('//*[@class="side_categories"]/ul/li/ul/li/a'):
            loader = CategoryLoader(CategoryItem(), item)
            loader.add_xpath('title', 'text()')
            loader.add_xpath('url', '@href', MapCompose(response.urljoin))
            category = loader.load_item()
            yield response.follow(category['url'], meta={'category': category}, callback=self.parse_category)

    def parse_category(self, response):
        category = response.meta['category']

        for url in response.xpath('//article[@class="product_pod"]/h3/a/@href'):
            yield response.follow(url, meta={'category': category}, callback=self.parse_book)

        next_url = response.xpath('//ul[@class="pager"]/li[@class="next"]/a/@href')
        if next_url:
            yield response.follow(next_url, meta={'category': category}, callback=self.parse_category)

    def parse_book(self, response):
        category = response.meta['category']

        loader = BookLoader(BookItem(), response)
        loader.add_xpath('title', '//article[@class="product_page"]//h1/text()')
        loader.add_xpath('price', '//p[@class="price_color"]/text()')
        loader.add_value('url', response.url)
        loader.add_value('category', category)
        book = loader.load_item()

        yield book
