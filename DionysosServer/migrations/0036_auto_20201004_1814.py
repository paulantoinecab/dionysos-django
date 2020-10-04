# Generated by Django 3.1.1 on 2020-10-04 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DionysosServer', '0035_auto_20201004_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='stripe_id',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_foods',
            field=models.ManyToManyField(to='DionysosServer.OrderedFood'),
        ),
    ]