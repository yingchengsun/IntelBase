# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CraigslistItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    price = scrapy.Field()
    
    maplink = scrapy.Field()
    
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    
    url = scrapy.Field()
    attributes = scrapy.Field()
    size = scrapy.Field()
    image_links = scrapy.Field()
    time = scrapy.Field()

    bedrooms = scrapy.Field()
