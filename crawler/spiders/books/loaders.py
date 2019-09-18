from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


class CategoryLoader(ItemLoader):
    default_output_processor = TakeFirst()

    title_in = MapCompose(''.strip)


class BookLoader(ItemLoader):
    default_output_processor = TakeFirst()

    title_in = MapCompose(''.strip)
