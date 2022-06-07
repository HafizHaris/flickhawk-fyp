from sre_constants import CATEGORY
from django.contrib import admin
from .models import Category, Country, Faqs, History, Product, Criteria
# Register your models here.

admin.site.site_header = "Flick Hawk Admin"
admin.site.site_title = "Flick Hawk Admin Portal"
admin.site.index_title = "Welcome to Flick Hawk Admin Portal"

class CountryAdmin(admin.ModelAdmin):
        list_display=['name','created']
admin.site.register(Country,CountryAdmin)

class CategoryAdmin(admin.ModelAdmin):
        list_display=['name','parent','created']
admin.site.register(Category,CategoryAdmin)


class FaqsAdmin(admin.ModelAdmin):
        list_display=['question','category','created']
admin.site.register(Faqs,FaqsAdmin)

class HistoryAdmin(admin.ModelAdmin):
        list_display=['user','detail','created']
admin.site.register(History,HistoryAdmin)


class ProductAdmin(admin.ModelAdmin):
        list_display=['title','asin','created']
admin.site.register(Product,ProductAdmin)


class CriteriaAdmin(admin.ModelAdmin):
        list_display=['criteria_name']
admin.site.register(Criteria,CriteriaAdmin)