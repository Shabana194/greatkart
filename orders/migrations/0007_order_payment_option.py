# Generated by Django 3.1 on 2022-12-03 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20221203_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_option',
            field=models.CharField(choices=[('CASH ON DELIVERY', 'Cash On Delivery'), ('PAYPAL', 'Paypal'), ('RAZORPAY', 'Razorpay')], max_length=100, null=True),
        ),
    ]
