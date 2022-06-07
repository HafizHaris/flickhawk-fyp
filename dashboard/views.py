import os
import io
import base64
import urllib
import sys
import re
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from multiprocessing import context
from notifications.signals import notify
import scrapydo
from django.shortcuts import render,HttpResponse
from amazon.spiders.asin import AsinSpider
from amazon.spiders.top_ten import TopTenSpider
from amazon.spiders.query import AmazonQuery
from amazon.pipelines import AmazonPipeline
from twisted.internet import reactor
from scrapy.crawler import Crawler,CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from amazon import settings as my_settings 
from scrapy.utils.log import configure_logging
from main.items_store import InMemoryItemStore
import time
from scrapy import signals
from django.conf import settings as django_settings
from pydispatch import dispatcher
from pytrends.request import TrendReq
from matplotlib import pyplot as plt
import statistics
# from statsmodels.tsa.seasonal import seasonal_decompose
from .models import Faqs, History, Product, Criteria, Country, Category
from django.db.models import Q
from django.utils.timezone import now
import datetime
from collections import Counter
from datetime import date
from itemadapter import ItemAdapter
from dateutil.relativedelta import relativedelta
from django.template.defaulttags import register
import json





@register.simple_tag
def str_to_json(value):
   return json.loads(value)


# Create your views here.
products = []

@login_required(login_url="login")
def dashboard(request):
    search_products = History.objects.filter(user=request.user, history_type="asin_search").count()
    paid_searches=16
    total_spendings = paid_searches * 2
    predefined_criterias = Criteria.objects.all().count()
    history = History.objects.filter(user=request.user).order_by('-created')[:15]
    recent_products = Product.objects.filter().order_by('-created')[:15]
    context = {'recent_products':recent_products,'history':history,'search_products':search_products,'paid_searches':paid_searches,'total_spendings':total_spendings,'predefined_criterias':predefined_criterias}
    return render(request,'dashboard/home.html',context)

@login_required(login_url="login")
def products(request,slug): 

    keyword=slug
    crawler_settings = Settings()
    scrapydo.setup()
    scrapydo.run_spider(TopTenSpider,keyword=keyword)
    items = InMemoryItemStore.pop_items()    
    myl = []
    for item in items:
        asin = item['asin']
        scrapydo.run_spider(AsinSpider,asin_number=asin)
        product_detail = InMemoryItemStore.pop_items()   
        myl.append(product_detail)
     
    return HttpResponse(myl)

@login_required(login_url="login")
def overview(request):   
    return HttpResponse("hi")

@login_required(login_url="login")
def paypal(request):   
    return render(request,'dashboard/paypal.html')

@login_required(login_url="login")
def profile(request):
    return render(request,'dashboard/profile.html')

@login_required(login_url="login")
def profile_edit(request):    
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        username=request.POST.get('username')
        user=request.user
        user.first_name=name
        user.email=email
        user.username=username
        user.save()        
        messages.success(request,"Profile has been updated.")        
    return render(request,'dashboard/profile_edit.html')

@login_required(login_url="login")
def recent_activities(request):
    history = History.objects.filter(user=request.user).order_by('-created')
    context = {'history':history}
    return render(request,'dashboard/recent_activities.html',context)

@login_required(login_url="login")
def support_tickets(request):
    return render(request,'dashboard/support_tickets.html')

@login_required(login_url="login")
def ticket_edit(request):
    return render(request,'dashboard/ticket_edit.html')

@login_required(login_url="login")
def get_recommendations(request):
    return render(request,'dashboard/recommendations.html')

@login_required(login_url="login")
def faqs(request):
    general_faqs = Faqs.objects.filter(category="general")
    account_faqs = Faqs.objects.filter(category="account")
    privacy_faqs = Faqs.objects.filter(category="privacy")
    context = {'general_faqs':general_faqs,'account_faqs':account_faqs, 'privacy_faqs':privacy_faqs}
    return render(request,'dashboard/faqs.html',context)

@login_required(login_url="login")
def searchproduct(request):
    asin_history = History.objects.filter(Q(user=request.user) & Q(history_type="asin_search")).order_by('-created')[:10]
    context = {'asin_history':asin_history}
    return render(request,'dashboard/search_product.html',context)

@login_required(login_url="login")
def overview(request,slug):
    try:
        asin=slug
        check_database = Product.objects.filter(Q(asin=asin) & Q(created__gt=datetime.datetime.today()-datetime.timedelta(days=30))).order_by('-created')
        if check_database:
            items = check_database.first()
            items.attr =  json.loads(items.attr.replace("\'", "\""))
            detail = {"ASIN":asin,"Title":items.title,"Price":items.price}
            context={"items":items,'data':items.seasonality}
        else:
        
            crawler_settings = Settings()
            scrapydo.setup()
            scrapydo.run_spider(AsinSpider, asin_number=asin)
            items = InMemoryItemStore.pop_items()
            items = items[0]

            # trends for seasonality
            try:
                kw=str(items['title']).split()[:3]
                str1 = "" 
                for ele in kw: 
                   str1 += " "+ele  
                kw = re.sub(r'[^a-zA-Z0-9 ]',r'',str1)
                pytrends = TrendReq(hl='en-US', tz=360) 
                kw_list = [kw]
                pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='US') 
                trends = pytrends.interest_over_time()
                plt.plot(trends)
                fig=plt.gcf()
                plt.close(fig)
                buf=io.BytesIO()
                fig.savefig(buf,format='png')
                buf.seek(0)
                string=base64.b64encode(buf.read())
                uri=urllib.parse.quote(string)

            except Exception as e:
                uri=None
            # end trends

            #product

            Product.objects.filter(asin=asin).delete()
            cat=items["category"].strip()
            cat_url=items["category_url"]
            if Category.objects.filter(name=cat).exists():
                check_cat = Category.objects.get(name=cat)
                p_category = check_cat
            else:
                add_category =  Category(
                    name=cat,
                    url=cat_url
                    )
                add_category.save()
                p_category = add_category


            record = Product(
                asin=asin, 
                category=p_category,
                title=items["title"], 
                image=items["image"], 
                price=items["price"],
                reviews=items["reviews"],
                brand=items["brand"],
                weight=items["weight"],
                listing_date=items["listing_date"],
                rating=items["rating"],
                dimensions=items["dimensions"],
                seasonality=uri,
                attr=items["attr"],
            )
            record.save()
            detail = {"ASIN":asin,"Title":items["title"],"Price":items["price"]}
            context={"items":items,'data':uri,'status':"success"}    

        # history
        detail = json.dumps(detail)
        detail = detail.replace("\'", "\"")
        record = History(user=request.user, history_type='asin_search', detail=detail,url='/overview/'+slug)
        record.save()
        
    except:
        context={'status':"error"}

    return render(request,'dashboard/product_overview.html',context)
    


def trends(request,slug):
    kw=slug
    pytrends = TrendReq(hl='en-US', tz=360) 
    kw_list = [kw] # list of keywords to get data 
    pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='US') 
    trends = pytrends.interest_over_time()
    
    

    res=[]
    for column in trends.columns:
        li = trends[column].tolist()
        res.append(li)
    
    
    # std=statistics.stdev(res[0])
    # print(trends)
    
    # print(result.)
    plt.plot(trends)
    fig=plt.gcf()
    plt.close(fig)
    buf=io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string=base64.b64encode(buf.read())
    uri=urllib.parse.quote(string)

    print(trends)
    return render(request,'dashboard\graph.html',{'data':uri,'kw':kw})    
    # return response
    # print(type(trends))
    
    # return HttpResponse(trends)

def ss(request):        
    return HttpResponse(django_settings.PRODUCTS)
    li = InMemoryItemStore.pop_items() 
    print("im closing........................")    

def spider(request):        
    # InMemoryItemStore.pop_items() 
    # reactor.stop() 
    crawler_settings = Settings()
    # setup()
    scrapydo.setup()
    # configure_logging()
    # crawler_settings.setmodule(my_settings)
    # runner= CrawlerRunner(settings=crawler_settings)
    # d=runner.crawl(AsinSpider)            
    # print("crawl..........")
    scrapydo.run_spider(AsinSpider)
    # d.addBoth(lambda _: reactor.stop())
    # reactor.run() 
    items= InMemoryItemStore.pop_items()
    # d.addBoth(lambda _: reactor.stop())
    context={"items":items}
    # reactor.stop()
    # time.sleep(5)
    # close_spider(self, AsinSpider)    
    # context={'items':items }
    # return HttpResponse(items)
    # return HttpResponse(items)
    return render(request,'main/products.html',context)
def scrapy_response(request):
    li = InMemoryItemStore.pop_items() 
    print(li) 



def convert_to_pounds(value,unit):
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


def numOfDays(date1, date2):
    return (date2-date1).days
     

def query_products(request):       
    
             
    try:
        keyword=''
        link = ''
        if request.GET.get('keyword') is not None:        
            keyword=request.GET.get('keyword')
        if request.GET.get('criteria'):
            criteria=request.GET.get('criteria')
            criteria=Criteria.objects.get(criteria_name=criteria)        
            min_avg_price=criteria.min_avg_price
            max_avg_price=criteria.max_avg_price
            min_avg_revenue=criteria.min_avg_revenue
            max_avg_revenue=criteria.max_avg_revenue
            min_avg_rating=criteria.min_avg_rating
            max_avg_rating=criteria.max_avg_rating
            min_avg_reviews=criteria.min_avg_reviews
            max_avg_reviews=criteria.max_avg_reviews
            request_avg_weight=criteria.avg_weight
            request_no_of_products=criteria.no_of_products
            request_brand_domination=criteria.brand_domination
            if request_brand_domination:
                request_brand_domination = "Yes"
            else:
                request_brand_domination = "No"

            request_amz_as_seller=criteria.amz_as_seller
            if request_amz_as_seller:
                request_amz_as_seller = "Yes"
            else:
                request_amz_as_seller = "No"

            request_country=criteria.country.name
            if request_country is not None:
                country=Country.objects.get(name=request_country)  
                link = country.url+"s?k="+keyword

            
        else:
            min_avg_price=request.GET.get('min_avg_price')
            max_avg_price=request.GET.get('max_avg_price')
            min_avg_revenue=request.GET.get('min_avg_revenue')
            max_avg_revenue=request.GET.get('max_avg_revenue')
            min_avg_rating=request.GET.get('min_avg_rating')
            max_avg_rating=request.GET.get('max_avg_rating')
            min_avg_reviews=request.GET.get('min_avg_reviews')
            max_avg_reviews=request.GET.get('max_avg_reviews')
            request_avg_weight=request.GET.get('avg_weight')
            request_no_of_products=request.GET.get('no_of_products')
            request_brand_domination=request.GET.get('brand_domination')
            request_amz_as_seller=request.GET.get('amz_as_seller')
            request_country=request.GET.get('country')     
            if request_country is not None:
                country=Country.objects.get(name=request_country)  
                link = country.url+"s?k="+keyword
                 


        brand_domination=False
        amz_as_seller=False    
        seller_reviews=False 
        seller_revenue=False 
        crawler_settings = Settings()
        scrapydo.setup()    
        


        scrapydo.run_spider(TopTenSpider,keyword=""+link)    
        items = InMemoryItemStore.pop_items()    
        myl = []
        avg_price=0.0
        avg_ratings=0.0
        avg_reviews=0.0
        reviews_list=[]
        revenue_list=[]
        avg_weight=0.0
        avg_revenue=0.0
        listing_days=0
        brands_list=[]
        weights_list=[]
        no_of_products=0    
        for item in items:
            asin = item['asin']
            if item['no_of_products'] is not None:
                no_of_products=item['no_of_products']        
            scrapydo.run_spider(AsinSpider,asin_number=asin)         
            product_detail = InMemoryItemStore.pop_items()   
            myl.append(product_detail)
        try:    
            if no_of_products is not None:
                no_of_products=list(no_of_products.split(' '))
                no_of_products=no_of_products[no_of_products.index('results')-1]            
                no_of_products=int(no_of_products.replace(',',''))        
        except:
            no_of_products=0

        for item in myl:
            attr=item[0]['attr']  
            
            listing_date=item[0]['listing_date']
            if listing_date is not None:
                todays_date = date.today()
                date2 = date(todays_date.year, todays_date.month, todays_date.day)
                date1 = date(int(datetime.datetime.strptime(listing_date, '%B %d, %Y').strftime('%Y')), int(datetime.datetime.strptime(listing_date, '%B %d, %Y').strftime('%m')), int(datetime.datetime.strptime(listing_date, '%B %d, %Y').strftime('%d')))
                listing_days += numOfDays(date1, date2)


        #2 3 sellers reviews
            reviews=item[0]['reviews']        
            
            if reviews is not None:        
                reviews=reviews.split(' ')
                reviews=reviews[0]
                reviews=reviews.replace(',','')
                reviews=float(reviews)
            else:
                reviews=0       
            avg_reviews=avg_reviews+reviews  
            reviews_list.append(reviews)
        #4 average price
            price=item[0]['price']        
            if price is not None:
                price=price.replace('$','')
                price=float(price.replace(',',''))
            else:
                price=0
            avg_price=price+avg_price; 
        #3 Revenue
            revenue=price*reviews
            avg_revenue=avg_revenue+revenue
            revenue_list.append(revenue)
        #8 Brand Domination
            brand=item[0]['brand']
            if brand is not None:
                brands_list.append(brand)        
        #11 Avg Weight       
            try:
                if attr['Item Weight'] is not None:   
                    weight=convert_to_pounds(float(list(attr['Item Weight'].split(' '))[0]),list(attr['Item Weight'].split(' '))[1])
                else:
                    weight=0
            except:
                weight=0
            avg_weight=avg_weight+weight
            weights_list.append(weight)
        #12 average star ratings        
            ratings=item[0]['stars']
            if ratings is not None:            
                ratings=list(ratings.split(' '))
                ratings=float(ratings[0])
            else:
                ratings=0
            avg_ratings=avg_ratings+ratings                                  
        counts=Counter(brands_list)    
        avg_revenue=avg_revenue/10
        avg_revenue=round(avg_revenue,2)
        avg_reviews=avg_reviews/10    
        avg_weight=round(avg_weight/10,2)
        avg_ratings=round(avg_ratings/10,2)
        avg_price=round(avg_price/10,2)    
        listing_days=round(listing_days/10,2)
        
        for key, value in counts.items():
            if value>3:
                brand_domination=True
            if key=="AMZ" and value>=3:
                amz_as_seller=True
        review_count=0

        for review in reviews_list:
            if review>400:
                review_count=review_count+1
        if review_count>3:
            seller_reviews=True
        revenue_count=0
        for revenue in revenue_list:
            if revenue>7000:
                revenue_count=revenue_count+1
        if revenue_count>3:
            seller_revenue=True
        print(review_count)
        print(revenue_count)
        
        predefined_criterias=Criteria.objects.all()
        countries=Country.objects.all()
        
        
        context={"myl":myl,'avg_weight':avg_weight,'avg_reviews':avg_reviews,
        'avg_revenue':avg_revenue,'brands_list':brands_list,'brand_domination':brand_domination,
        'amz_as_seller':amz_as_seller,'seller_revenue':seller_revenue,
        'seller_reviews':seller_reviews,'avg_ratings':avg_ratings,'avg_price':avg_price,
        'no_of_products':int(no_of_products),'min_avg_price':float(min_avg_price),'max_avg_price':float(max_avg_price),
        'min_avg_reviews':float(min_avg_reviews),'max_avg_reviews':float(max_avg_reviews),'min_avg_revenue':float(min_avg_revenue),
        'max_avg_revenue':float(max_avg_revenue),'min_avg_ratings':float(min_avg_rating),'max_avg_ratings':float(max_avg_rating),
        'request_avg_weight':float(request_avg_weight),'request_amz_as_seller':request_amz_as_seller,
        'request_no_of_products':request_no_of_products,'request_brand_domination':request_brand_domination,    
        'keyword':keyword,'predefined_criterias':predefined_criterias,'request_country':request_country,'countries':countries,'avg_listing_days':listing_days,'status':"success"
        }    
    # return HttpResponse(myl)
    except:
        context={'status':"error"}

    return render(request,'dashboard/query_products.html',context)



def read_notifications(request):
    if request.user.notifications.unread() is not None:
        response=request.user.notifications.mark_all_as_read()
    return HttpResponse("Ok")
def notifications_count(request):    
    if request.user.notifications.unread() is not None:
        count=request.user.notifications.unread()
        return HttpResponse(count.count())
        return count
    else:
        return 0

        
def notifications(request):
    read=request.user.notifications.mark_all_as_read()
    notifications=request.user.notifications.read()
    context={"notifications":notifications}
    return render(request, 'dashboard/notifications.html',context)

def send_notification(request):
    user=request.user
    notify.send(user, recipient=user, verb='4th Live Notification')
    return HttpResponse("OK")