import scrapy
from ..items import AmazonItem
from django.conf import settings as conf_settings
import re



class AsinSpider(scrapy.Spider):

    name = 'asin'
    asin= ''

    def __init__(self, asin_number= None):
        self.start_urls = ['https://www.amazon.com/dp/'+asin_number]

    allowed_domains = ['amazon.com']
        
    # custom_settings = {
    #     'FEED_FORMAT': 'csv',
    #     'FEED_URI': 'test.csv'
    # }    

    
        

    def Convert(self,a):
            a = list(filter(None, a))
            it = iter(a)
            res_dct = dict(zip(it, it))
            return res_dct


    def beautify_string(self, str):
        str = str.encode("ascii", "ignore")
        str = str.decode()
        str = str.strip()
        return str


    def parse(self, response):                
        item=AmazonItem()
        item['title']=response.xpath("//span[@id='productTitle']/text()").get()
        item['price']=response.xpath("//span[@class='a-price a-text-price a-size-medium apexPriceToPay']//span[2]/text()").get()             
        item['image']=response.xpath("//*[@id='landingImage']").css("::attr(src)").get()
        item['reviews'] = response.css('#acrCustomerReviewText').css('::text').extract_first()
        item['brand'] = response.css('.po-brand .a-span9 .a-size-base::text').extract_first()
        item['stars']=response.css('.AverageCustomerReviews     .a-size-medium.a-color-base::text').extract_first()
        item['rating']=response.css('#reviewsMedley .a-size-medium::text').extract_first()
        item['category']=response.css('.a-breadcrumb li:nth-child(1) .a-color-tertiary::text').extract_first()
        item['category_url']=response.css('.a-breadcrumb li:nth-child(1) .a-color-tertiary::attr(href)').extract_first()
        attr = response.css('#prodDetails .a-size-base::text').extract()

        attr = [self.beautify_string(x) for x in attr]
        attr = self.Convert(attr)
        item['attr'] = attr

        item['weight'] = attr.get("Item Weight")
        item['listing_date'] = attr.get("Date First Available")
        item['dimensions'] = attr.get("Product Dimensions")

        yield item