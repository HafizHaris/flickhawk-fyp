import scrapy
from ..items import AmazonItem
from django.conf import settings as conf_settings
import re



class TopTenSpider(scrapy.Spider):
    name = 'top_ten'
    asin= ''
    count = 1
    products_to_scrape = 2
    keyword = 'macbook'
    start_urls = ['https://www.amazon.com/s?k='+keyword]    
    allowed_domains = ['amazon.com']
    def __init__(self, keyword= None):
        self.start_urls = [keyword]    
        TopTenSpider.count=1
    def parse(self, response):        
        
        product_cards = response.css('.s-asin')       
        no_of_products = response.css('.s-breadcrumb.sg-col-10-of-16 span:nth-child(1)').css('::text').extract_first()

        results = []
        for product in product_cards:
            if TopTenSpider.count>TopTenSpider.products_to_scrape:
                break
            TopTenSpider.count += 1    
            product_link = product.css('::attr(data-asin)').extract_first()  

            yield {"asin":product_link,"no_of_products":no_of_products}