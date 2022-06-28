import scrapy
from ..items import AmazonItem
from django.conf import settings as conf_settings
import re
from datetime import date
import datetime


class ProductStats(scrapy.Spider):

    name = 'product_stats'
    asin= ''


    def __init__(self, asin_number= None):
        self.start_urls = ['https://www.amazon.com/dp/'+asin_number]

    allowed_domains = ['amazon.com']


    def parse(self, response):                
        brand_domination=0
        amz_as_seller = 0
        price = response.xpath("//span[@class='a-price a-text-price a-size-medium apexPriceToPay']//span[2]/text()").get()
        reviews = response.css('#acrCustomerReviewText').css('::text').extract_first()
        rating = response.css('#reviewsMedley .a-size-medium::text').extract_first()
        seller = response.css('#sellerProfileTriggerId::text').extract_first()
        brand = response.css('.po-brand .a-span9 .a-size-base::text').extract_first()
        attr = response.css('#prodDetails .a-size-base::text').extract()

        attr = [self.beautify_string(x) for x in attr]
        attr = self.Convert(attr)
        

        weight = attr.get("Item Weight")
        try:
            if attr['Item Weight'] is not None:   
                weight=self.convert_to_pounds(float(list(weight.split(' '))[0]),list(weight.split(' '))[1])            
            else:
                weight=None
        except:
            weight=0


        
        listing_date = attr.get("Date First Available")
        listing_days=0
        if listing_date is not None:
            todays_date = date.today()
            date2 = date(todays_date.year, todays_date.month, todays_date.day)
            date1 = date(int(datetime.datetime.strptime(listing_date, '%B %d, %Y').strftime('%Y')), int(datetime.datetime.strptime(listing_date, '%B %d, %Y').strftime('%m')), int(datetime.datetime.strptime(listing_date, '%B %d, %Y').strftime('%d')))
            listing_days += self.numOfDays(date1, date2)

        if rating is not None:            
            rating=list(rating.split(' '))
            rating=float(rating[0])
        else:
            rating=0

        if reviews is not None:        
            reviews=reviews.split(' ')
            reviews=reviews[0]
            reviews=reviews.replace(',','')
            reviews=int(reviews)
        else:
            reviews=0


                
        if price is not None:
            price=price.replace('$','')
            price=float(price.replace(',',''))
        else:
            price=0

        if price is not None and reviews is not None:
            revenue=round(reviews*price,2)
        else:
            revenue = 0

        
        
        if brand is not None and seller is not None and brand==seller:
            brand_domination=1

        if seller is not None and seller=="Amazon.com":
            amz_as_seller = 1


        yield {'price': price, 'reviews':reviews, 'rating':rating,'weight':weight,'listing_time':listing_days,'revenue':revenue,'brand_domination':brand_domination,'amz_as_seller':amz_as_seller}
        # parse method from Your OneSpider class




    def beautify_string(self, str):
        str = str.encode("ascii", "ignore")
        str = str.decode()
        str = str.strip()
        return str

    def Convert(self,a):
        a = list(filter(None, a))
        it = iter(a)
        res_dct = dict(zip(it, it))
        return res_dct

    def convert_to_pounds(self,value,unit):
        weight=0.0
        if unit=="kg" or unit=="Kilograms":
            weight=value*2.205
            return weight
        if unit=="Grams" or unit=="gm":
            weight=value/454
            return weight
        if unit=="ounce" or unit=="ounces" or unit=="oz":
            weight=value/16
            return weight
        if unit=="pound" or unit=="pounds" or unit=="lbs":
            return value
        return value

    def numOfDays(self,date1, date2):
        return (date2-date1).days