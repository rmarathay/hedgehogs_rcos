# Generated by Django 2.1.2 on 2018-12-04 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0008_eodcompanyrelation'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='companyfundamentalstable',
            table='fundamentals_sample',
        ),
    ]