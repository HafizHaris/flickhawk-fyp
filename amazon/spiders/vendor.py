import scrapy
from ..items import AmazonItem
from django.conf import settings as conf_settings
import re



class Vendor(scrapy.Spider):
    name = 'get_vendors'
    count = 1
    products_to_scrape = 5
    keyword = ''
    keyword = keyword.replace(" ", "+")
    start_urls = ['']    

    allowed_domains = ['made-in-china.com']

    def __init__(self, keyword= None):
        self.start_urls = [keyword]    
        Vendor.count=1

    def parse(self, response):        
        product_cards = response.css('.prod-content')   
        prices = []
        attrs = []

        for product in product_cards:
            if Vendor.count>Vendor.products_to_scrape:
                break
            price = product.css('.price::text').extract_first()  
            
            # print(price)
            link = product.css('.product-name a::attr(href)').extract_first()  
            supplier = product.css('.J-compnay-name span::text').extract_first()  
            contact_link = product.css('.btn-main::attr(href)').extract_first()  

            if price is not None:
                Vendor.count += 1   
                if len(price.split()) == 3:
                    price = price.split()[2]
                
                if len(price.split('-')) == 2:
                    price = price.split('-')[1]

                if len(price.split(' ')) == 2:
                    price = price.split(' ')[1]

                
                prices+=[float(price)]
                attrs+=[{"link":link,"supplier":supplier,"contact_link":contact_link}]
                

        if len(prices) != 0:
            ind = prices.index(min(prices))
            min_price = prices[ind]
            attr = attrs[ind]
        else:
            min_price = None
            attr = None

        print("vendor..........")
        print(min_price)
        yield {'min_price':min_price, 'attr':attr}
