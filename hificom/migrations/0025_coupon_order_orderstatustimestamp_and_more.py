# Generated by Django 4.2 on 2024-08-12 11:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hificom', '0024_cartproduct_unique_product_in_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=200, unique=True)),
                ('discount_percent', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(100)])),
                ('max_amount', models.FloatField(blank=True, null=True)),
                ('discount_amount', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('min_spend', models.FloatField(default=0)),
                ('max_usage', models.IntegerField(blank=True, null=True)),
                ('expiry', models.DateTimeField()),
                ('added_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=256, null=True)),
                ('location', models.CharField(choices=[('inside', 'Sylhet City'), ('outside', 'Outside Sylhet City')], max_length=20)),
                ('address', models.CharField(max_length=512)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='pending', max_length=20)),
                ('added_at', models.DateField(auto_now_add=True)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hificom.cart')),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatusTimestamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='pending', max_length=20)),
                ('completed_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hificom.order')),
            ],
        ),
        migrations.AddConstraint(
            model_name='orderstatustimestamp',
            constraint=models.UniqueConstraint(fields=('order', 'status'), name='uniqe status in an order'),
        ),
    ]
