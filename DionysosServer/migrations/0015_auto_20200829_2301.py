# Generated by Django 3.1 on 2020-08-29 21:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('DionysosServer', '0014_orderedfood_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderedfood',
            name='food_ptr',
        ),
    ]
