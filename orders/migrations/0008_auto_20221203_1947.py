# Generated by Django 3.1 on 2022-12-03 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_order_payment_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(max_length=100),
        ),
    ]
