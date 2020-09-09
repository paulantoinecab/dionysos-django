# Generated by Django 3.1 on 2020-08-29 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DionysosServer', '0016_auto_20200829_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderedfood',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_foods',
            field=models.ManyToManyField(to='DionysosServer.OrderedFood'),
        ),
    ]
