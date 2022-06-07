import scrapy
from ..items import QueryItem
class AmazonQuery(scrapy.Spider):
    name = 'query'
    count=1
    start_urls = [        
        "https://www.amazon.com/s?k=samsung&page=1&qid=1624792241&ref=sr_pg_2"               
        ]

    def parse(self, response):
        product=QueryItem()
        name=response.css(".a-size-medium.a-text-normal::text").extract()
        no_reviews=response.css(".sg-col-12-of-20 .a-link-normal .a-size-base").css("::text").extract()
        price=response.css(".sg-col-12-of-20 .a-price-whole::text").extract()
        image_url=response.css(".s-image-fixed-height .s-image").css("::attr(src)").extract()
        product["p_name"]=name
        product["p_reviews"]=no_reviews
        product["p_price"]=price
        product["url"]=image_url
        yield product    
        AmazonQuery.count+=1
        nxt_page="https://www.amazon.com/s?k=samsung&page="+str(AmazonQuery.count)+"&qid=1624791620&ref=sr_pg_3"
        # nxt_iphone_page="https://www.amazon.com/s?k=iphone&page="+str(AmazonBotSpider.count)+"&qid=1624792241&ref=sr_pg_2"
        if AmazonQuery.count<=1:
            yield response.follow(nxt_page,callback=self.parse)
            # yield response.follow(nxt_iphone_page,callback=self.parse)
