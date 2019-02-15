# Generated by Django 2.1.2 on 2018-10-23 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_auto_20181022_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.FloatField(default=False)),
                ('ticker', models.CharField(max_length=250)),
                ('company_name', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Company_Info',
            },
        ),
        migrations.CreateModel(
            name='Fundamentals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_id', models.FloatField(default=False)),
                ('company_name', models.CharField(max_length=250)),
                ('common_shares_outstanding', models.FloatField(default=False)),
            ],
            options={
                'verbose_name': 'Fundamentals',
            },
        ),
        migrations.CreateModel(
            name='Time_Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ts_id', models.FloatField(default=False)),
                ('company_id', models.FloatField(default=False)),
                ('ticker', models.CharField(max_length=250)),
                ('price', models.FloatField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('open_data', models.FloatField(default=False)),
                ('high', models.FloatField(default=False)),
                ('low', models.FloatField(default=False)),
                ('close', models.FloatField(default=False)),
            ],
            options={
                'verbose_name': 'Time_Series',
            },
        ),
    ]