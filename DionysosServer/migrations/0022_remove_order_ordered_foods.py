# Generated by Django 3.1 on 2020-08-29 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DionysosServer', '0021_remove_order_ordered_foods'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='ordered_foods',
        ),
    ]
