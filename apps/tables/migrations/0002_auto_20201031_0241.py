# Generated by Django 3.1.2 on 2020-10-31 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('orders', '0001_initial'),
        ('tables', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='order',
        ),
        migrations.AddField(
            model_name='table',
            name='orders',
            field=models.ManyToManyField(null=True, through='orders.Order', to='products.Product'),
        ),
    ]