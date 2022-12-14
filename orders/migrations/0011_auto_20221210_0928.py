# Generated by Django 3.1 on 2022-12-10 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20221208_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_option',
            field=models.CharField(choices=[('CASH ON DELIVERY', 'Cash On Delivery'), ('PAYPAL', 'Paypal')], max_length=100, null=True),
        ),
    ]
