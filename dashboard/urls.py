from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    
    path('dashboard/',views.dashboard,name='dashboard'),    
    path('trends/<str:slug>/',views.trends,name='trends'), 
    path('trends/',views.trends,name='trends'), 
    path('paypal/',views.paypal,name='paypal'),    
    path('searchproduct/',views.searchproduct,name='searchproduct'), 
    path('products/',views.query_products,name='query_products'),   
    # path('products/<str:slug>/',views.products,name='products'),         
    path('overview/<str:slug>/',views.overview,name='overview'),    
    path('overview/',views.overview,name='overview'),    
    path('profile/',views.profile,name='profile'),    
    path('profile_edit/',views.profile_edit,name='profile_edit'),    
    path('recent_activities/',views.recent_activities,name='recent_activities'),    
    path('support_tickets/',views.support_tickets,name='support_tickets'),    
    path('faqs/',views.faqs,name='faqs'),    
    path('ticket_edit/',views.ticket_edit,name='ticket_edit'),        
    # path('scrapy/',views.spider,name='scrapy'),    
    path('scrapy_response/',views.scrapy_response,name='scrapy_response'),    
    path('get_recommendations/',views.get_recommendations,name='get_recommendations'),
    path('notifications/',views.notifications,name='notifications'),
    path('send_notification/',views.send_notification,name='send_notification'),
    path('read_notifications/',views.read_notifications,name='read_notifications'),
    path('notifications_count/',views.notifications_count,name='notifications_count'),
]

