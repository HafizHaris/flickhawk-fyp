from django.db import models
import uuid
# Create your models here.


class Country(models.Model):
	class Meta:
		verbose_name_plural = "Countries"
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key = True, editable=False)
	name = models.CharField(max_length=500)
	url = models.CharField(max_length=5000, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class Category(models.Model):
	class Meta:
		verbose_name_plural = "Categories"
		
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key = True, editable=False)
	name = models.CharField(max_length=500)
	url = models.CharField(max_length=5000, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True,blank=True)

	def __str__(self):
		return self.name


class Faqs(models.Model):
	class Meta:
		verbose_name_plural = "FAQs"

	question_type = (
		('general','General Questions'),
		('account','Manage Account'),
		('privacy','Privacy & Security'),
	)

	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key = True, editable=False)
	category = models.CharField(max_length=500, choices=question_type)
	question = models.CharField(max_length=1000)
	answer = models.TextField(max_length=10000)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.question

class History(models.Model):
	type_choices = (
		('asin_search','ASIN Search'),
		('recommendation','Recommendation'),
	)

	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key = True, editable=False)
	user = models.ForeignKey('auth.User',on_delete=models.CASCADE)
	history_type = models.CharField(max_length=500, choices=type_choices)
	detail = models.TextField(max_length=10000)
	url = models.CharField(max_length=5000, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
	class Meta:
		verbose_name_plural = "Products"
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key = True, editable=False)
	asin = models.CharField(max_length=500)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False,blank=False)
	title = models.CharField(max_length=1000)
	image = models.CharField(max_length=5000, null=True, blank=True)
	price = models.CharField(max_length=500, null=True, blank=True)
	reviews = models.CharField(max_length=500, null=True, blank=True)
	brand = models.CharField(max_length=500, null=True, blank=True)
	weight = models.CharField(max_length=500, null=True, blank=True)
	listing_date = models.CharField(max_length=500, null=True, blank=True)
	rating = models.CharField(max_length=500, null=True, blank=True)
	dimensions = models.CharField(max_length=500, null=True, blank=True)
	seasonality = models.CharField(max_length=500, null=True, blank=True)
	attr = models.TextField(max_length=10000, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)

class Criteria(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key = True, editable=False)
	criteria_name = models.CharField(max_length=500,null=True, blank=True)
	country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True,blank=True)
	min_avg_price = models.IntegerField(default=0, null=True, blank=True)
	max_avg_price = models.IntegerField(default=0, null=True, blank=True)
	min_avg_reviews = models.IntegerField(default=0, null=True, blank=True)
	max_avg_reviews = models.IntegerField(default=0, null=True, blank=True)
	min_avg_revenue = models.IntegerField(default=0, null=True, blank=True)
	max_avg_revenue = models.IntegerField(default=0, null=True, blank=True)
	min_avg_rating = models.IntegerField(default=0, null=True, blank=True)
	max_avg_rating = models.IntegerField(default=0, null=True, blank=True)
	avg_weight = models.IntegerField(default=0, null=True, blank=True)
	no_of_products = models.IntegerField(default=0, null=True, blank=True)
	amz_as_seller = models.BooleanField(default=False, null=True,blank=True)
	brand_domination = models.BooleanField(default=False, null=True,blank=True)
	
	def _str_(self):
		return self.criteria_name