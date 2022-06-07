# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from numpy import tile
import scrapy
from scrapy_djangoitem import DjangoItem
from django.db import models

# Create your models here.

class AmazonItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    rating = scrapy.Field()
    reviews = scrapy.Field()
    brand = scrapy.Field()
    weight = scrapy.Field()
    listing_date = scrapy.Field()
    dimensions = scrapy.Field()
    stars = scrapy.Field()
    category = scrapy.Field()
    category_url = scrapy.Field()
    attr = scrapy.Field()
    


class QueryItem(scrapy.Item):
    # define the fields for your item here like:
    p_name = scrapy.Field()
    p_reviews=scrapy.Field()
    p_price=scrapy.Field()
    url=scrapy.Field()
