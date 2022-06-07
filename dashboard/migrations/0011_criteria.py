# Generated by Django 4.0.3 on 2022-06-05 11:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_alter_product_attr'),
    ]

    operations = [
        migrations.CreateModel(
            name='Criteria',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('criteria_name', models.CharField(blank=True, max_length=500, null=True)),
                ('min_avg_price', models.IntegerField(blank=True, default=0, null=True)),
                ('max_avg_price', models.IntegerField(blank=True, default=0, null=True)),
                ('min_avg_reviews', models.IntegerField(blank=True, default=0, null=True)),
                ('max_avg_reviews', models.IntegerField(blank=True, default=0, null=True)),
                ('min_avg_revenue', models.IntegerField(blank=True, default=0, null=True)),
                ('max_avg_revenue', models.IntegerField(blank=True, default=0, null=True)),
                ('min_avg_rating', models.IntegerField(blank=True, default=0, null=True)),
                ('max_avg_rating', models.IntegerField(blank=True, default=0, null=True)),
                ('avg_weight', models.IntegerField(blank=True, default=0, null=True)),
                ('no_of_products', models.IntegerField(blank=True, default=0, null=True)),
                ('amz_as_seller', models.BooleanField(blank=True, default=False, null=True)),
                ('brand_domination', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
    ]
