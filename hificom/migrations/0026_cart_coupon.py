# Generated by Django 4.2 on 2024-08-14 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hificom', '0025_coupon_order_orderstatustimestamp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hificom.coupon'),
        ),
    ]
