# Generated by Django 4.2 on 2024-09-02 05:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import hificom.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hificom', '0027_remove_cart_coupon_order_coupon_order_oid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.CharField(db_index=True, default=hificom.models.hexcode_gen, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('products', models.ManyToManyField(related_name='wishlists', to='hificom.product')),
            ],
        ),
    ]
