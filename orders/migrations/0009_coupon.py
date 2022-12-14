# Generated by Django 3.1 on 2022-12-08 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20221203_1947'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_offer', models.IntegerField(max_length=10)),
                ('coupon_name', models.CharField(max_length=50)),
                ('is_use', models.BooleanField(default=False)),
            ],
        ),
    ]
