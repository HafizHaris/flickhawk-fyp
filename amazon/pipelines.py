# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from urllib import request
from itemadapter import ItemAdapter
# from main.models import Product
from main.items_store import InMemoryItemStore
from main import views
from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings as conf_settings
from django.http import HttpRequest
class AmazonPipeline:

    def process_item(self, item, spider):        
    #     product =  Product()
    #     product.name=item['title']
    #     product.price=item['price']
    #     product.save()
          return "1"    
class StoreInMemoryPipeline(object):
    """Add items to the in-memory item store."""
    def process_item(self, item, spider):
        # conf_settings.PRODUCTS.append(item)         
        InMemoryItemStore.add_item(item)        
        # print("HERE IS THE LIST........................")
        
    def close_spider(self, spider):
        print('im closing from pipeline...........................')
        # request=HttpRequest()
        # views.ss(request)
class AmazonQueryPipeline:
    def process_item(self, item, spider):
        InMemoryItemStore.add_item(item)        
    def close_spider(self, spider):
        print('im closing from pipeline........................Query Spider')