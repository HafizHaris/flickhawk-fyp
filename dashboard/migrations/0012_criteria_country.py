# Generated by Django 4.0.3 on 2022-06-06 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_criteria'),
    ]

    operations = [
        migrations.AddField(
            model_name='criteria',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.country'),
        ),
    ]
